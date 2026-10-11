"""Fluxograma animado da dicotomia do controle: "Isso depende de mim?".

Uma pergunta no centro, duas setas douradas (Sim → aja; Não → solte), um laço vermelho
em volta da pergunta (ficar remoendo) e uma frase final de Epicteto.

    python3 depende_de_mim.py [saida.mp4]
"""

import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

import estilo
import midia

DURACAO = 18.0
VERMELHO = (178, 78, 70)
NOTA = (205, 196, 182)
CX = estilo.LARGURA // 2
PERGUNTA_Y = 760
RAMOS = [  # (resposta, conclusão, nota, ponta da seta, início)
    ("Sim.", "Então aja.", "com o que estiver ao seu alcance", (290, 1130), 2.6),
    ("Não.", "Então solte.", "e guarde a sua energia", (790, 1130), 4.4),
]


def aparece(t, t0, dur=0.6):
    return estilo.suavizar((t - t0) / dur) if t > t0 else 0.0


def texto(img, xy, s, f, cor, alfa, ancora="mm"):
    if alfa <= 0:
        return
    camada = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(camada).text(xy, s, font=f, fill=cor + (int(255 * alfa),), anchor=ancora)
    img.alpha_composite(camada)


def seta(img, a, b, p, cor, alfa):
    if p <= 0 or alfa <= 0:
        return
    camada = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    c = cor + (int(255 * alfa),)
    x, y = a[0] + (b[0] - a[0]) * p, a[1] + (b[1] - a[1]) * p
    d.line((a[0], a[1], x, y), fill=c, width=4)
    if p >= 1:
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        for s in (-1, 1):
            d.line((b[0], b[1], b[0] - 26 * math.cos(ang + s * 0.45), b[1] - 26 * math.sin(ang + s * 0.45)),
                   fill=c, width=4)
    img.alpha_composite(camada)


def quadro(t, fundo):
    img = Image.fromarray(fundo).convert("RGBA")
    some = 1 - aparece(t, DURACAO - 5.0, 0.8)  # o fluxograma apaga antes da frase final

    for i, l in enumerate(["Antes de sofrer por algo,", "faça uma pergunta:"]):
        texto(img, (CX, estilo.TOPO_SEGURO + 90 + i * 74), l, estilo.serifa(62, 500), estilo.BRANCO,
              aparece(t, 0.2) * some)

    # A pergunta, dentro de um contorno dourado
    a = aparece(t, 1.3) * some
    if a > 0:
        caixa = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(caixa).rounded_rectangle((CX - 330, PERGUNTA_Y - 70, CX + 330, PERGUNTA_Y + 70),
                                                radius=70, outline=estilo.DOURADO + (int(255 * a),), width=3)
        img.alpha_composite(caixa)
        texto(img, (CX, PERGUNTA_Y), "Isso depende de mim?", estilo.serifa_italica(62, 600), estilo.BRANCO, a)

    for i, (resp, concl, nota, ponta, t0) in enumerate(RAMOS):
        inicio = (CX + (-120 if i == 0 else 120), PERGUNTA_Y + 75)
        seta(img, inicio, ponta, estilo.suavizar(min(1.0, max(0.0, (t - t0) / 0.9))), estilo.DOURADO, some)
        meio = ((inicio[0] + ponta[0]) / 2 + (-60 if i == 0 else 60), (inicio[1] + ponta[1]) / 2)
        texto(img, meio, resp, estilo.sem_serifa(34, 600), estilo.DOURADO, aparece(t, t0 + 0.4) * some)
        texto(img, (ponta[0], ponta[1] + 70), concl, estilo.serifa(66, 600), estilo.BRANCO, aparece(t, t0 + 0.9) * some)
        texto(img, (ponta[0], ponta[1] + 135), nota, estilo.serifa_italica(38, 500), NOTA,
              aparece(t, 8.6 + 0.5 * i) * some)

    # A armadilha: um laço vermelho que gira em volta da pergunta
    pl = min(1.0, max(0.0, (t - 6.4) / 1.4))
    if pl > 0 and some > 0:
        laco = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(laco).arc((CX - 380, PERGUNTA_Y - 120, CX + 380, PERGUNTA_Y + 120), 200,
                                 200 + 330 * estilo.suavizar(pl), fill=VERMELHO + (int(255 * some),), width=5)
        img.alpha_composite(laco)
        texto(img, (CX, PERGUNTA_Y - 170), "Ficar remoendo.", estilo.serifa_italica(44, 600), VERMELHO,
              aparece(t, 7.4) * some)

    # Frase final
    texto(img, (CX, 820), "Remoer não é uma das opções.", estilo.serifa(62, 500), estilo.BRANCO,
          aparece(t, DURACAO - 4.2, 0.9))
    texto(img, (CX, 930), "Algumas coisas dependem de nós.", estilo.serifa_italica(58, 600), estilo.DOURADO,
          aparece(t, DURACAO - 3.4, 0.9))
    texto(img, (CX, 1005), "Outras, não.", estilo.serifa_italica(58, 600), estilo.DOURADO,
          aparece(t, DURACAO - 3.0, 0.9))
    ac = aparece(t, DURACAO - 2.6, 0.9)
    if ac > 0:
        cred = Image.new("RGBA", img.size, (0, 0, 0, 0))
        estilo.texto_espacado(ImageDraw.Draw(cred), (CX, 1100), "EPICTETO · MANUAL, 1", estilo.sem_serifa(24, 500),
                              estilo.CINZA + (int(255 * ac),), 8)
        img.alpha_composite(cred)
    return np.asarray(img.convert("RGB"), np.float32)


def main():
    saida = Path(sys.argv[1]) if len(sys.argv) > 1 else estilo.PASTA / "saida" / "depende-de-mim.mp4"
    saida.parent.mkdir(parents=True, exist_ok=True)
    fundo = np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)
    mudo = saida.with_suffix(".mudo.mp4")
    ff = midia.gravador(mudo, estatico=False)
    for k in range(int(DURACAO * estilo.FPS)):
        ff.stdin.write(estilo.para_bytes(quadro(k / estilo.FPS, fundo)))
    ff.stdin.close()
    ff.wait()
    midia.juntar_audio(mudo, saida)
    print(f"Pronto: {saida} ({midia.duracao(saida):.1f} s)")


if __name__ == "__main__":
    sys.exit(main())
