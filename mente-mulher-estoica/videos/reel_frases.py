"""Gera um reel vertical de frases animadas a partir de um roteiro em Markdown.

Exemplos:
    python3 reel_frases.py ../roteiros/video-sonhos-grandes.md
    python3 reel_frases.py ../roteiros/video-sonhos-grandes.md --musica musica/piano.mp3
    python3 reel_frases.py ../roteiros/video-sonhos-grandes.md --narracao voz.mp3 --musica musica/piano.mp3
    python3 reel_frases.py ../roteiros/video-sonhos-grandes.md --previa
"""

import argparse
import re
import sys
from pathlib import Path

import estilo
import midia
import roteiro

ENTRADA, SAIDA_FADE, SUBIDA = 0.7, 0.5, 26  # segundos, segundos, pixels
TEMPO_FINAL = 4.5
INICIO_NARRACAO = 0.4


def tempo_de_leitura(tela):
    """Tempo confortável para ler a tela em silêncio (~2,5 palavras por segundo)."""
    return max(2.8, 1.3 + tela.palavras / 2.5)


def montar_cronograma(r, narracao=None):
    """Devolve [(camada, inicio, fim)] e a duração total do vídeo."""
    if narracao:
        # As telas acompanham a narração, proporcionalmente ao tamanho de cada texto
        falado = midia.duracao(narracao)
        pesos = [len(t.texto) + 25 for t in r.telas]
        tempos = [falado * p / sum(pesos) for p in pesos]
        tempos[0] += INICIO_NARRACAO
    else:
        tempos = [tempo_de_leitura(t) for t in r.telas]

    cronograma, t = [], 0.0
    for tela, d in zip(r.telas, tempos):
        cronograma.append((estilo.Camada(estilo.tela_de_texto(tela.linhas)), t, t + d))
        t += d
    if r.frase_final:
        cronograma.append((estilo.Camada(estilo.tela_final(r.frase_final)), t, t + TEMPO_FINAL))
        t += TEMPO_FINAL
    return cronograma, t


def opacidade_e_subida(t, inicio, fim, primeira):
    entrada = 0.35 if primeira else ENTRADA
    if t < inicio or t >= fim:
        return 0.0, 0
    p = estilo.suavizar((t - inicio) / entrada)
    q = min(1.0, (fim - t) / SAIDA_FADE)
    return p * q, int(round((1 - p) * SUBIDA))


def gerar(r, saida, narracao=None, musica=None, volume_musica=None):
    cronograma, total = montar_cronograma(r, narracao)
    base = estilo.fundo()
    base = estilo.granulado(estilo.Camada(estilo.moldura()).compor(base))

    mudo = saida.with_suffix(".mudo.mp4")
    ff = midia.gravador(mudo)
    quadros = int(total * estilo.FPS)
    for i in range(quadros):
        t = i / estilo.FPS
        quadro = base.copy()
        for n, (camada, inicio, fim) in enumerate(cronograma):
            op, dy = opacidade_e_subida(t, inicio, fim, n == 0)
            camada.compor(quadro, op, dy)
        ff.stdin.write(estilo.para_bytes(quadro))
        if i % estilo.FPS == 0:
            print(f"\r  quadro {i}/{quadros}", end="", flush=True)
    ff.stdin.close()
    ff.wait()
    print()

    if volume_musica is None:
        volume_musica = 0.18 if narracao else 0.8
    midia.juntar_audio(mudo, saida, voz=narracao, musica=musica,
                       volume_musica=volume_musica, atraso_voz=INICIO_NARRACAO)
    return total


def previa(r, pasta):
    """Salva um PNG de cada tela, para revisar o texto sem renderizar o vídeo."""
    pasta.mkdir(parents=True, exist_ok=True)
    from PIL import Image

    base = estilo.fundo()
    base = estilo.granulado(estilo.Camada(estilo.moldura()).compor(base))
    telas = [estilo.tela_de_texto(t.linhas) for t in r.telas]
    if r.frase_final:
        telas.append(estilo.tela_final(r.frase_final))
    for i, tela in enumerate(telas, 1):
        quadro = estilo.Camada(tela).compor(base.copy())
        Image.frombytes("RGB", (estilo.LARGURA, estilo.ALTURA),
                        estilo.para_bytes(quadro)).save(pasta / f"tela-{i:02d}.png")
    return len(telas)


def nome_do_arquivo(caminho):
    nome = Path(caminho).stem
    return re.sub(r"^video-", "", nome)


def main():
    p = argparse.ArgumentParser(description="Reel de frases animadas da @mente.mulher.estoica")
    p.add_argument("roteiro", help="arquivo .md do roteiro")
    p.add_argument("--narracao", help="áudio da narração (sua voz gravada ou voz gerada)")
    p.add_argument("--musica", help="música de fundo (mp3, m4a, wav)")
    p.add_argument("--volume-musica", type=float,
                   help="volume da música, de 0 a 1 (padrão: 0.8 sozinha, 0.18 sob narração)")
    p.add_argument("--saida", help="arquivo .mp4 de saída (padrão: saida/<roteiro>.mp4)")
    p.add_argument("--previa", action="store_true", help="só gera os PNGs das telas")
    a = p.parse_args()

    r = roteiro.ler(a.roteiro)
    pasta_saida = estilo.PASTA / "saida"
    nome = nome_do_arquivo(a.roteiro)

    if a.previa:
        n = previa(r, pasta_saida / f"previa-{nome}")
        print(f"{n} telas salvas em {pasta_saida / f'previa-{nome}'}")
        return

    saida = Path(a.saida) if a.saida else pasta_saida / f"{nome}.mp4"
    saida.parent.mkdir(parents=True, exist_ok=True)
    print(f"Gerando “{r.titulo}” ({len(r.telas)} telas)...")
    total = gerar(r, saida, a.narracao, a.musica, a.volume_musica)
    print(f"Pronto: {saida} ({total:.1f} s)")


if __name__ == "__main__":
    sys.exit(main())
