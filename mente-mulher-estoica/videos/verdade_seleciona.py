"""Reel animado "A verdade seleciona": um círculo de pessoas em volta da sua verdade.

A verdade aparece no centro, uma onda dourada se espalha e a maioria das pessoas se
afasta. Ficam poucas, ligadas a você por fios dourados. Fecha com a frase autoral.
Mesmo padrão visual de depende_de_mim.py. Com --musica, a batida da Cidadela entra
junto com a frase final.

    python3 verdade_seleciona.py [saida.mp4] [--musica cidadela.mp4]
"""

import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

import estilo
import midia

DURACAO = 18.0  # duração da animação na velocidade base
LENTO = 1.4  # >1 deixa tudo mais calmo; o vídeo final dura DURACAO * LENTO
CINZA_CLARO = (160, 154, 146)
NOTA = (205, 196, 182)
CX = estilo.LARGURA // 2
CY = 900
RAIO = 300
N = 24
FICAM = {0, 5, 10, 14, 19}  # quem permanece depois da verdade
QUEDA_BATIDA = 23.25  # segundo da Cidadela em que a batida entra


def aparece(t, t0, dur=0.6):
    return estilo.suavizar((t - t0) / dur) if t > t0 else 0.0


def texto(img, xy, s, f, cor, alfa, ancora="mm"):
    if alfa <= 0:
        return
    camada = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(camada).text(xy, s, font=f, fill=cor + (int(255 * alfa),), anchor=ancora)
    img.alpha_composite(camada)


def quadro(t, fundo):
    img = Image.fromarray(fundo).convert("RGBA")
    some = 1 - aparece(t, DURACAO - 5.0, 0.8)  # a cena apaga antes da frase final

    for i, l in enumerate(["A verdade vai afastar", "algumas pessoas."]):
        texto(img, (CX, estilo.TOPO_SEGURO + 90 + i * 74), l, estilo.serifa(62, 500), estilo.BRANCO,
              aparece(t, 0.2 + 0.3 * i) * some)

    camada = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)

    # A onda dourada que sai da verdade
    po = (t - 3.6) / 1.4
    if 0 < po < 1 and some > 0:
        r = 90 + 420 * estilo.suavizar(po)
        d.ellipse((CX - r, CY - r, CX + r, CY + r), outline=estilo.DOURADO + (int(200 * (1 - po) * some),), width=3)

    fio = aparece(t, 6.2, 0.9)
    for k in range(N):
        ang = -math.pi / 2 + 2 * math.pi * k / N
        a = aparece(t, 1.0 + 0.04 * k, 0.5) * some
        if a <= 0:
            continue
        r = RAIO
        cor = CINZA_CLARO
        if k in FICAM:
            mistura = aparece(t, 6.0, 0.8)
            cor = tuple(int(c0 + (c1 - c0) * mistura) for c0, c1 in zip(CINZA_CLARO, estilo.DOURADO))
            if fio > 0:  # fio dourado ligando quem fica à verdade
                fx, fy = CX + math.cos(ang) * 120, CY + math.sin(ang) * 120
                px, py = CX + math.cos(ang) * (r - 20), CY + math.sin(ang) * (r - 20)
                d.line((fx, fy, fx + (px - fx) * fio, fy + (py - fy) * fio),
                       fill=estilo.DOURADO + (int(170 * some),), width=2)
            tam = 13
        else:
            sai = estilo.suavizar((t - 4.2 - 0.03 * k) / 1.6) if t > 4.2 else 0.0
            r += 260 * sai
            a *= 1 - sai
            tam = 11
        x, y = CX + math.cos(ang) * r, CY + math.sin(ang) * r
        if a > 0:
            d.ellipse((x - tam, y - tam, x + tam, y + tam), fill=cor + (int(255 * a),))
    img.alpha_composite(camada)

    texto(img, (CX, CY), "a sua verdade", estilo.serifa_italica(58, 600), estilo.DOURADO, aparece(t, 2.2) * some)

    # O que se afasta e o que fica
    texto(img, (CX, CY + RAIO + 130), "quem só ficava pelo seu silêncio",
          estilo.serifa_italica(40, 500), NOTA, aparece(t, 4.4) * (1 - aparece(t, 6.0)) * some)
    texto(img, (CX, CY + RAIO + 130), "Quem fica.", estilo.serifa(66, 600), estilo.BRANCO, aparece(t, 6.6) * some)
    texto(img, (CX, CY + RAIO + 260), "Deixe.", estilo.serifa_italica(110, 600), estilo.DOURADO,
          aparece(t, 8.6, 0.9) * some)

    # Frase final, junto com a batida
    texto(img, (CX, 820), "Ela está fazendo a seleção", estilo.serifa(62, 500), estilo.BRANCO,
          aparece(t, DURACAO - 4.2, 0.9))
    texto(img, (CX, 900), "que você não teve", estilo.serifa(62, 500), estilo.BRANCO,
          aparece(t, DURACAO - 4.0, 0.9))
    texto(img, (CX, 1000), "coragem de fazer.", estilo.serifa_italica(74, 600), estilo.DOURADO,
          aparece(t, DURACAO - 3.6, 0.9))
    ac = aparece(t, DURACAO - 2.8, 0.9)
    if ac > 0:
        cred = Image.new("RGBA", img.size, (0, 0, 0, 0))
        estilo.texto_espacado(ImageDraw.Draw(cred), (CX, 1110), estilo.ASSINATURA, estilo.sem_serifa(24, 500),
                              estilo.CINZA + (int(255 * ac),), 8)
        img.alpha_composite(cred)
    return np.asarray(img.convert("RGB"), np.float32)


def main():
    args = sys.argv[1:]
    musica = None
    if "--musica" in args:
        i = args.index("--musica")
        musica = args[i + 1]
        del args[i:i + 2]
    saida = Path(args[0]) if args else estilo.PASTA / "saida" / "verdade-seleciona.mp4"
    saida.parent.mkdir(parents=True, exist_ok=True)
    fundo = np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)
    mudo = saida.with_suffix(".mudo.mp4")
    ff = midia.gravador(mudo, estatico=False)
    for k in range(int(DURACAO * LENTO * estilo.FPS)):
        ff.stdin.write(estilo.para_bytes(quadro(k / estilo.FPS / LENTO, fundo)))
    ff.stdin.close()
    ff.wait()
    if musica:
        inicio = QUEDA_BATIDA - (DURACAO - 4.2) * LENTO  # a batida cai quando a frase final entra
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mudo), "-ss", f"{inicio:.2f}",
                        "-t", str(DURACAO * LENTO), "-i", musica, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                        "-af", f"afade=t=in:d=1,afade=t=out:st={DURACAO * LENTO - 2:.2f}:d=2", "-c:a", "aac",
                        "-b:a", "192k", "-movflags", "+faststart", str(saida)], check=True)
        mudo.unlink()
    else:
        midia.juntar_audio(mudo, saida)
    print(f"Pronto: {saida} ({midia.duracao(saida):.1f} s)")


if __name__ == "__main__":
    sys.exit(main())
