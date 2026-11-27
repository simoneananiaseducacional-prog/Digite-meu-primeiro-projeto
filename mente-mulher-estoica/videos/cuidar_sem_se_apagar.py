"""Reel animado "Cuidar sem se apagar": dois círculos, você e quem você ama.

Os dois aparecem ligados por um fio dourado. Quando o cuidado vira tudo, o círculo de
quem você ama cresce e o seu vai sumindo; depois os dois voltam ao mesmo tamanho.
Fecha com a frase autoral. Mesmo padrão visual de depende_de_mim.py e
verdade_seleciona.py. Sai sem som, para a música ser escolhida no Instagram.

    python3 cuidar_sem_se_apagar.py [saida.mp4]
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

import estilo
import midia

DURACAO = 18.0  # duração da animação na velocidade base
LENTO = 1.4  # >1 deixa tudo mais calmo; o vídeo final dura DURACAO * LENTO
NOTA = (205, 196, 182)
CX = estilo.LARGURA // 2
CY = 900
DX = 210  # distância de cada círculo ao centro
R0 = 95  # raio dos dois círculos em equilíbrio


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

    for i, l in enumerate(["Cuidar de quem você ama", "é amor."]):
        texto(img, (CX, estilo.TOPO_SEGURO + 90 + i * 74), l, estilo.serifa(62, 500), estilo.BRANCO,
              aparece(t, 0.2 + 0.3 * i) * some)

    # Desequilíbrio (4 a 7,5 s) e volta ao equilíbrio (9,5 a 11 s)
    desequilibrio = aparece(t, 4.0, 3.5) * (1 - aparece(t, 9.5, 1.5))
    r_voce = R0 * (1 - 0.85 * desequilibrio)
    r_outro = R0 * (1 + 0.6 * desequilibrio)
    luz_voce = 1 - 0.75 * desequilibrio
    entra = aparece(t, 1.4, 0.8) * some

    camada = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    if entra > 0:
        xv, xo = CX - DX, CX + DX
        fio = aparece(t, 2.2, 0.8)
        d.line((xv + r_voce, CY, xv + r_voce + (xo - r_outro - xv - r_voce) * fio, CY),
               fill=estilo.DOURADO + (int(200 * entra),), width=3)
        d.ellipse((xv - r_voce, CY - r_voce, xv + r_voce, CY + r_voce),
                  outline=estilo.DOURADO + (int(255 * entra * luz_voce),), width=4)
        d.ellipse((xo - r_outro, CY - r_outro, xo + r_outro, CY + r_outro),
                  outline=estilo.BRANCO + (int(230 * entra),), width=4)
    img.alpha_composite(camada)

    rot = estilo.serifa_italica(50, 600)
    texto(img, (CX - DX, CY + R0 + 90), "você", rot, estilo.DOURADO, entra * luz_voce)
    texto(img, (CX + DX, CY + R0 + 90), "quem você ama", rot, estilo.BRANCO, entra)

    # Legendas de cada momento
    base = CY + R0 + 260
    texto(img, (CX, base), "Mas quando o cuidado vira tudo,", estilo.serifa_italica(58, 600), estilo.BRANCO,
          aparece(t, 4.2) * (1 - aparece(t, 9.2)) * some)
    texto(img, (CX, base + 80), "você vai desaparecendo.", estilo.serifa_italica(58, 600), NOTA,
          aparece(t, 6.4) * (1 - aparece(t, 9.2)) * some)
    texto(img, (CX, base + 40), "Presença não é se apagar.", estilo.serifa_italica(66, 600), estilo.DOURADO,
          aparece(t, 10.4, 0.9) * some)

    # Frase final
    texto(img, (CX, 800), "Cuidar de quem você ama", estilo.serifa(62, 500), estilo.BRANCO,
          aparece(t, DURACAO - 4.2, 0.9))
    texto(img, (CX, 880), "não pode custar", estilo.serifa(62, 500), estilo.BRANCO,
          aparece(t, DURACAO - 4.0, 0.9))
    texto(img, (CX, 980), "a sua vida.", estilo.serifa_italica(80, 600), estilo.DOURADO,
          aparece(t, DURACAO - 3.6, 0.9))
    texto(img, (CX, 1090), "Amor não pede que você desapareça.", estilo.serifa_italica(54, 600), estilo.BRANCO,
          aparece(t, DURACAO - 3.0, 0.9))
    ac = aparece(t, DURACAO - 2.4, 0.9)
    if ac > 0:
        cred = Image.new("RGBA", img.size, (0, 0, 0, 0))
        estilo.texto_espacado(ImageDraw.Draw(cred), (CX, 1190), estilo.ASSINATURA, estilo.sem_serifa(24, 500),
                              estilo.CINZA + (int(255 * ac),), 8)
        img.alpha_composite(cred)
    return np.asarray(img.convert("RGB"), np.float32)


def main():
    saida = Path(sys.argv[1]) if len(sys.argv) > 1 else estilo.PASTA / "saida" / "cuidar-sem-se-apagar.mp4"
    saida.parent.mkdir(parents=True, exist_ok=True)
    fundo = np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)
    mudo = saida.with_suffix(".mudo.mp4")
    ff = midia.gravador(mudo, estatico=False)
    for k in range(int(DURACAO * LENTO * estilo.FPS)):
        ff.stdin.write(estilo.para_bytes(quadro(k / estilo.FPS / LENTO, fundo)))
    ff.stdin.close()
    ff.wait()
    midia.juntar_audio(mudo, saida)
    print(f"Pronto: {saida} ({midia.duracao(saida):.1f} s)")


if __name__ == "__main__":
    sys.exit(main())
