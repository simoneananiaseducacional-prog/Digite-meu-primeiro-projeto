"""Diagrama animado "três caminhos": Você → Mudar / Aceitar / Sair, e o quarto caminho.

Linhas douradas que se desenham sobre o fundo da marca, rótulos em serifa, um laço
vermelho em volta do "Você" (andar em círculos) e uma frase final.

    python3 caminhos.py
"""

import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

import estilo
import midia

DURACAO = 17.0
VERMELHO = (178, 78, 70)
ORIGEM = (190, 960)
DESTINOS = [  # (rótulo, nota, ponta da seta, início do desenho)
    ("Mudar.", "o que depende de você", (800, 700), 2.0),
    ("Aceitar.", "o que não depende", (800, 960), 3.6),
    ("Sair.", "o que não te cabe mais", (800, 1220), 5.2),
]


def aparece(t, t0, dur=0.6):
    return estilo.suavizar((t - t0) / dur) if t > t0 else 0.0


def seta(d, a, b, p, cor, largura=4):
    """Desenha a fração p da linha a→b; a ponta da seta aparece quando a linha completa."""
    if p <= 0:
        return
    x = a[0] + (b[0] - a[0]) * p
    y = a[1] + (b[1] - a[1]) * p
    d.line((a[0], a[1], x, y), fill=cor, width=largura)
    if p >= 1:
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        for s in (-1, 1):
            d.line((b[0], b[1], b[0] - 26 * math.cos(ang + s * 0.45), b[1] - 26 * math.sin(ang + s * 0.45)),
                   fill=cor, width=largura)


def texto(img, xy, s, f, cor, alfa, ancora="lm"):
    if alfa <= 0:
        return
    camada = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(camada).text(xy, s, font=f, fill=cor + (int(255 * alfa),), anchor=ancora)
    img.alpha_composite(camada)


def quadro(t, fundo):
    img = Image.fromarray(fundo).convert("RGBA")
    d = ImageDraw.Draw(img)
    # Nos 4 segundos finais, o diagrama apaga e fica só a frase final
    apaga = 1 - aparece(t, DURACAO - 4.6, 0.8)

    titulo = estilo.serifa(60, 500)
    for i, l in enumerate(["Quando uma situação não está bem,", "considere três caminhos:"]):
        texto(img, (estilo.LARGURA / 2, estilo.TOPO_SEGURO + 80 + i * 72), l, titulo,
              estilo.BRANCO, aparece(t, 0.2) * apaga, "mm")

    a = aparece(t, 1.2) * apaga
    if a > 0:
        cor = tuple(int(c * a) for c in estilo.BRANCO)
        d = ImageDraw.Draw(img)
        d.ellipse((ORIGEM[0] - 10, ORIGEM[1] - 10, ORIGEM[0] + 10, ORIGEM[1] + 10), fill=cor)
        texto(img, (ORIGEM[0], ORIGEM[1] - 50), "Você", estilo.sem_serifa(34, 600), estilo.BRANCO, a, "mm")

    rotulo, nota = estilo.serifa(64, 600), estilo.serifa_italica(42, 500)
    for nome, obs, ponta, t0 in DESTINOS:
        p = min(1.0, max(0.0, (t - t0) / 1.0))
        linhas = Image.new("RGBA", img.size, (0, 0, 0, 0))
        seta(ImageDraw.Draw(linhas), (ORIGEM[0] + 18, ORIGEM[1]), ponta, estilo.suavizar(p),
             estilo.DOURADO + (int(255 * apaga),))
        img.alpha_composite(linhas)
        texto(img, (ponta[0] + 24, ponta[1]), nome, rotulo, estilo.BRANCO, aparece(t, t0 + 0.9) * apaga)
        texto(img, (ponta[0] - 20, ponta[1] + 60), obs, nota, (205, 196, 182), aparece(t, 9.0 + 0.4 * DESTINOS.index((nome, obs, ponta, t0))) * apaga, "mm")

    # O quarto caminho: um laço vermelho em volta do "Você"
    pl = min(1.0, max(0.0, (t - 7.0) / 1.4))
    if pl > 0:
        laco = Image.new("RGBA", img.size, (0, 0, 0, 0))
        caixa = (ORIGEM[0] - 70, ORIGEM[1] + 30, ORIGEM[0] + 70, ORIGEM[1] + 170)
        ImageDraw.Draw(laco).arc(caixa, 270, 270 + 340 * estilo.suavizar(pl),
                                 fill=VERMELHO + (int(255 * apaga),), width=5)
        img.alpha_composite(laco)
        texto(img, (ORIGEM[0], ORIGEM[1] + 220), "Ficar reclamando.", estilo.serifa_italica(40, 600),
              VERMELHO, aparece(t, 8.0) * apaga, "mm")

    # Frase final
    f1, f2 = estilo.serifa(70, 500), estilo.serifa_italica(80, 600)
    af = aparece(t, DURACAO - 4.0, 0.9)
    texto(img, (estilo.LARGURA / 2, 860), "Só não vale o quarto caminho:", f1, estilo.BRANCO, af, "mm")
    texto(img, (estilo.LARGURA / 2, 970), "andar em círculos.", f2, estilo.DOURADO, aparece(t, DURACAO - 3.4, 0.9), "mm")
    return np.asarray(img.convert("RGB"), np.float32)


def main():
    saida = Path(sys.argv[1]) if len(sys.argv) > 1 else estilo.PASTA / "saida" / "tres-caminhos.mp4"
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
