"""Coloca legendas elegantes num vídeo gravado e fecha com a frase final da marca.

O vídeo é ajustado para o formato vertical 1080x1920. O tempo das legendas vem de:
  --srt     um arquivo de legendas com tempos exatos (o mais preciso), ou
  --roteiro o roteiro em Markdown: o texto é distribuído ao longo do vídeo,
            proporcionalmente ao tamanho de cada trecho (bom quando você lê o roteiro).

Exemplos:
    python3 legendar.py gravacao.mp4 --roteiro ../roteiros/video-sonhos-grandes.md
    python3 legendar.py gravacao.mp4 --srt gravacao.srt --frase-final "Sonhar grande é o começo."
    python3 legendar.py gravacao.mp4 --roteiro ../roteiros/x.md --musica musica/piano.mp3
"""

import argparse
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import estilo
import midia
import roteiro

PALAVRAS_POR_LEGENDA = 7
Y_LEGENDA = 1330  # centro da legenda, acima da área coberta pela interface do Reels
TEMPO_FINAL, ESCURECER = 4.0, 0.8


def trechos_curtos(texto):
    """Quebra o texto em legendas de até ~7 palavras, cortando de preferência na pontuação."""
    trechos = []
    for frase in re.split(r"(?<=[.!?…:;])\s+", texto):
        palavras = frase.split()
        while len(palavras) > PALAVRAS_POR_LEGENDA:
            # Divide em partes de tamanho parecido, cortando numa vírgula se houver perto
            partes = -(-len(palavras) // PALAVRAS_POR_LEGENDA)
            alvo = round(len(palavras) / partes)
            corte = alvo
            for i in sorted(range(3, PALAVRAS_POR_LEGENDA + 2), key=lambda i: abs(i - alvo)):
                if palavras[i - 1].endswith(","):
                    corte = i
                    break
            trechos.append(" ".join(palavras[:corte]))
            palavras = palavras[corte:]
        if palavras:
            trechos.append(" ".join(palavras))
    # Trecho de uma ou duas palavras sozinho na tela pisca rápido demais: junta ao próximo
    unidos = []
    for trecho in trechos:
        if unidos and len(unidos[-1].split()) <= 2:
            unidos[-1] += " " + trecho
        else:
            unidos.append(trecho)
    return unidos


def legendas_do_roteiro(r, duracao):
    texto = " ".join(t.texto for t in r.telas)
    trechos = trechos_curtos(texto)
    pesos = [len(t) + 8 for t in trechos]
    legendas, t = [], 0.0
    for trecho, p in zip(trechos, pesos):
        d = duracao * p / sum(pesos)
        legendas.append((t, t + d, trecho))
        t += d
    return legendas


def _tempo_srt(s):
    h, m, resto = s.strip().replace(",", ".").split(":")
    return int(h) * 3600 + int(m) * 60 + float(resto)


def legendas_do_srt(caminho):
    blocos = re.split(r"\n\s*\n", Path(caminho).read_text(encoding="utf-8-sig").strip())
    legendas = []
    for bloco in blocos:
        linhas = [l for l in bloco.splitlines() if l.strip()]
        tempo = next((l for l in linhas if "-->" in l), None)
        if not tempo:
            continue
        inicio, fim = (_tempo_srt(x) for x in tempo.split("-->"))
        texto = " ".join(linhas[linhas.index(tempo) + 1:])
        legendas.append((inicio, fim, re.sub(r"<[^>]+>", "", texto)))
    return legendas


def camada_legenda(texto):
    """Texto claro em sem serifa, com sombra difusa para ler sobre qualquer imagem."""
    f = estilo.sem_serifa(52, 600)
    linhas = estilo.quebrar_linhas(texto, f, estilo.LARGURA - 2 * estilo.MARGEM_X - 40)
    entre = 70
    y0 = Y_LEGENDA - len(linhas) * entre / 2

    sombra = Image.new("L", (estilo.LARGURA, estilo.ALTURA), 0)
    ds = ImageDraw.Draw(sombra)
    img = Image.new("RGBA", (estilo.LARGURA, estilo.ALTURA), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for i, linha in enumerate(linhas):
        xy = (estilo.LARGURA / 2, y0 + entre * (i + 0.5))
        ds.text(xy, linha, font=f, fill=255, anchor="mm", stroke_width=6)
        d.text(xy, linha, font=f, fill=(255, 255, 255, 255), anchor="mm")
    sombra = sombra.filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.75))
    base = Image.new("RGBA", img.size, (0, 0, 0, 0))
    base.putalpha(sombra)
    return estilo.Camada(Image.alpha_composite(base, img))


def opacidade(t, inicio, fim, fade=0.12):
    if t < inicio or t >= fim:
        return 0.0
    return min(1.0, (t - inicio) / fade, (fim - t) / fade)


def gerar(video, legendas, saida, frase_final="", musica=None, volume_musica=0.15):
    dur = midia.duracao(video)
    camadas = [(camada_legenda(txt), ini, fim) for ini, fim, txt in legendas]
    tamanho = estilo.LARGURA * estilo.ALTURA * 3

    mudo = saida.with_suffix(".mudo.mp4")
    ff = midia.gravador(mudo, estatico=False)
    entrada = midia.leitor(video)
    i, ultimo = 0, None
    while True:
        bruto = entrada.stdout.read(tamanho)
        if len(bruto) < tamanho:
            break
        t = i / estilo.FPS
        quadro = np.frombuffer(bruto, np.uint8).reshape(estilo.ALTURA, estilo.LARGURA, 3)
        quadro = quadro.astype(np.float32)
        for camada, ini, fim in camadas:
            camada.compor(quadro, opacidade(t, ini, fim))
        ff.stdin.write(estilo.para_bytes(quadro))
        ultimo = quadro
        i += 1
        if i % estilo.FPS == 0:
            print(f"\r  {t:.0f}/{dur:.0f} s", end="", flush=True)
    entrada.wait()

    if frase_final and ultimo is not None:
        # Depois da fala: o vídeo escurece até o fundo da marca e entra a frase final
        fundo = estilo.granulado(estilo.Camada(estilo.moldura()).compor(estilo.fundo()))
        final = estilo.Camada(estilo.tela_final(frase_final))
        for k in range(int(TEMPO_FINAL * estilo.FPS)):
            t = k / estilo.FPS
            mistura = estilo.suavizar(t / ESCURECER)
            quadro = ultimo * (1 - mistura) + fundo * mistura
            p = estilo.suavizar((t - ESCURECER) / 0.8) if t > ESCURECER else 0.0
            final.compor(quadro, p, int(round((1 - p) * 26)))
            ff.stdin.write(estilo.para_bytes(quadro))
    ff.stdin.close()
    ff.wait()
    print()

    voz = video if midia.tem_audio(video) else None
    midia.juntar_audio(mudo, saida, voz=voz, musica=musica, volume_musica=volume_musica)
    return midia.duracao(saida)


def main():
    p = argparse.ArgumentParser(description="Legendas no estilo @mente.mulher.estoica")
    p.add_argument("video", help="vídeo gravado (qualquer formato; vira 1080x1920)")
    fonte = p.add_mutually_exclusive_group(required=True)
    fonte.add_argument("--roteiro", help="roteiro .md que você leu na gravação")
    fonte.add_argument("--srt", help="arquivo de legendas .srt com os tempos exatos")
    p.add_argument("--frase-final", help="frase da tela de fechamento (padrão: a do roteiro)")
    p.add_argument("--sem-final", action="store_true", help="não acrescenta a tela de fechamento")
    p.add_argument("--musica", help="música de fundo, bem baixinha sob a sua voz")
    p.add_argument("--volume-musica", type=float, default=0.15)
    p.add_argument("--saida", help="arquivo .mp4 de saída (padrão: saida/<video>-legendado.mp4)")
    a = p.parse_args()

    dur = midia.duracao(a.video)
    frase_final = a.frase_final or ""
    if a.roteiro:
        r = roteiro.ler(a.roteiro)
        legendas = legendas_do_roteiro(r, dur)
        frase_final = frase_final or r.frase_final
    else:
        legendas = legendas_do_srt(a.srt)
    if a.sem_final:
        frase_final = ""

    saida = Path(a.saida) if a.saida else estilo.PASTA / "saida" / f"{Path(a.video).stem}-legendado.mp4"
    saida.parent.mkdir(parents=True, exist_ok=True)
    print(f"Legendando {a.video} ({len(legendas)} legendas)...")
    total = gerar(a.video, legendas, saida, frase_final, a.musica, a.volume_musica)
    print(f"Pronto: {saida} ({total:.1f} s)")


if __name__ == "__main__":
    sys.exit(main())
