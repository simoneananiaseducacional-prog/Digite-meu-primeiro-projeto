"""Frase da marca por cima de um vídeo dela: as linhas entram uma a uma, a última em dourado
itálico, e a assinatura MENTE MULHER ESTOICA aparece no fim. Mantém o áudio original.

    python3 frase_sobre_video.py video.mov [saida.mp4] \
        --frase "Dirigir à noite ensina:|você não precisa ver o caminho inteiro.|*Só o próximo trecho.*" \
        --altura 620

"|" quebra a linha; *asteriscos* deixam a linha dourada; --altura é o centro do bloco
(em pixels de 1920), para pôr o texto numa área lisa do vídeo (céu, parede...).
"""

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import estilo
import midia

W, H, FPS = estilo.LARGURA, estilo.ALTURA, estilo.FPS
CX = W // 2


def aparece(t, t0, dur=0.8):
    return estilo.suavizar((t - t0) / dur) if t > t0 else 0.0


def main():
    p = argparse.ArgumentParser(description="Frase da marca sobre um vídeo")
    p.add_argument("video")
    p.add_argument("saida", nargs="?")
    p.add_argument("--frase", required=True)
    p.add_argument("--altura", type=int, default=700)
    p.add_argument("--inicio", type=float, default=1.0, help="segundo em que entra a primeira linha")
    p.add_argument("--intervalo", type=float, default=1.6, help="segundos entre uma linha e outra")
    a = p.parse_args()
    saida = Path(a.saida) if a.saida else estilo.PASTA / "saida" / "frase-sobre-video.mp4"
    saida.parent.mkdir(parents=True, exist_ok=True)

    linhas = a.frase.split("|")
    blocos = []
    for l in linhas:
        dourada = l.startswith("*") and l.endswith("*")
        f = estilo.serifa_italica(88, 600) if dourada else estilo.serifa(70, 500)
        while f.getlength(l.strip("*")) > W - 140:
            f = f.font_variant(size=f.size - 2)
        blocos.append((l.strip("*"), f, estilo.DOURADO if dourada else estilo.BRANCO, 112 if dourada else 92))
    altura_bloco = sum(b[3] for b in blocos)
    y0 = a.altura - altura_bloco / 2

    # Cada linha pré-desenhada numa camada própria, com sombra suave para ler sobre o vídeo
    camadas = []
    y = y0
    for s, f, cor, passo in blocos:
        c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sombra = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sombra).text((CX, y + passo / 2), s, font=f, fill=(0, 0, 0, 200), anchor="mm")
        c.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(6)))
        ImageDraw.Draw(c).text((CX, y + passo / 2), s, font=f, fill=cor + (255,), anchor="mm")
        camadas.append(np.asarray(c, np.float32))
        y += passo
    assin = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    estilo.texto_espacado(ImageDraw.Draw(assin), (CX, y + 70), estilo.ASSINATURA, estilo.sem_serifa(26, 500),
                          estilo.BRANCO + (220,), 8)
    camadas.append(np.asarray(assin, np.float32))

    duracao = midia.duracao(a.video)
    entradas = [a.inicio + i * a.intervalo for i in range(len(linhas))] + [a.inicio + len(linhas) * a.intervalo + 0.6]
    leitor = midia.leitor(a.video)
    mudo = saida.with_suffix(".mudo.mp4")
    ff = midia.gravador(mudo, estatico=False)
    tam = W * H * 3
    for k in range(int(duracao * FPS)):
        bruto = leitor.stdout.read(tam)
        if len(bruto) < tam:
            break
        t = k / FPS
        q = np.frombuffer(bruto, np.uint8).reshape(H, W, 3).astype(np.float32)
        some = 1 - aparece(t, duracao - 0.9, 0.8)
        for camada, t0 in zip(camadas, entradas):
            al = aparece(t, t0) * some
            if al > 0:
                m = camada[..., 3:4] / 255 * al
                q = q * (1 - m) + camada[..., :3] * m
        ff.stdin.write(q.astype(np.uint8).tobytes())
    ff.stdin.close()
    ff.wait()
    leitor.stdout.close()
    leitor.wait()
    midia.juntar_audio(mudo, saida, voz=a.video if midia.tem_audio(a.video) else None)
    print(f"Pronto: {saida} ({midia.duracao(saida):.1f} s)")


if __name__ == "__main__":
    sys.exit(main())
