"""Lista em vídeo como caminho: "Você" segue por uma trilha pontilhada e vai deixando
"bagagens" para trás. Cada item surge grande embaixo; a bagagem fica na trilha, esmaece e
ganha um risco vinho. Variação visual dos diagramas (mesma identidade, outro desenho).

    python3 lista_caminho.py saida.mp4
"""
import math
import sys
import numpy as np
from PIL import Image, ImageDraw
import estilo, midia

W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
VINHO = (150, 45, 60)
TITULO = ("O que você ainda carrega", "que já devia ter deixado?")
ITENS = [
    "Explicar demais o seu \"não\".",
    "Se forçar a superar antes da hora.",
    "O medo de tentar e falhar.",
    "Comparar a sua vida com a dos outros.",
    "Sofrer pelo que você não pode mudar.",
    "Forçar relacionamentos.",
    "Depender da aprovação dos outros.",
    "Esquecer o quanto você já avançou.",
]
INICIO, PASSO, FIM = 0.8, 3.2, 2.5
T = INICIO + PASSO * len(ITENS) + FIM
VX, VY, ESP = 800, 930, 230  # posição do "Você" e espaço entre bagagens


def ap(t, t0, d=0.4):
    return estilo.suavizar((t - t0) / d) if t > t0 else 0.0


def ca(c, a):
    return c + (int(255 * max(0, min(1, a))),)


def trilha_y(x):
    return VY + 38 * math.sin(x / 210)


def bagagem(d, x, y, cor, a):
    d.rounded_rectangle((x - 30, y - 34, x + 30, y + 10), radius=8, outline=ca(cor, a), width=3)
    d.arc((x - 14, y - 50, x + 14, y - 26), 180, 360, fill=ca(cor, a), width=3)


def main():
    saida = sys.argv[1]
    fundo = np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)
    fi, fn = estilo.serifa_italica(58, 600), estilo.sem_serifa(28, 600)
    mudo = saida.replace('.mp4', '.mudo.mp4')
    ff = midia.gravador(mudo, estatico=False)
    for k in range(int(T * FPS)):
        t = k / FPS
        img = Image.fromarray(fundo).convert('RGBA'); cam = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
        d.text((W/2, 470), TITULO[0], font=estilo.serifa(66, 500), fill=ca(B, 1), anchor='mm')
        d.text((W/2, 550), TITULO[1], font=estilo.serifa_italica(70, 600), fill=ca(G, 1), anchor='mm')
        prog = max(0.0, (t - INICIO) / PASSO)
        andar = ESP * min(prog, len(ITENS))  # o mundo desliza para a esquerda
        a0 = ap(t, 0.3, 0.5)
        for x in range(-40, W + 40, 26):  # trilha pontilhada
            wx = x + andar
            d.ellipse((x - 3, trilha_y(wx) - 3, x + 3, trilha_y(wx) + 3), fill=ca(C, a0 * (0.35 if x < VX else 0.8)))
        n = min(int(prog), len(ITENS) - 1) if prog > 0 else -1
        for i in range(0, n + 1):
            x = VX + i * ESP - andar + ESP * 0.15
            if x < -60 or x > W + 60:
                continue
            y = trilha_y(x + andar)
            atual = (i == int(prog)) and prog < len(ITENS)
            surge = ap(t, INICIO + i * PASSO, 0.4)
            alfa = surge * (1.0 if atual else 0.45)
            bagagem(d, x, y - 26, G if atual else C, alfa)
            d.text((x, y - 98), f"{i+1:02d}", font=fn, fill=ca(G if atual else C, alfa), anchor='mm')
            if not atual:
                d.line((x - 34, y - 64, x + 34, y + 8), fill=ca(VINHO, 0.8 * surge), width=4)
        d.ellipse((VX - 13, trilha_y(VX + andar) - 13, VX + 13, trilha_y(VX + andar) + 13), fill=ca(B, a0))
        d.text((VX, trilha_y(VX + andar) + 52), "Você", font=estilo.sem_serifa(34, 600), fill=ca(B, a0), anchor='mm')
        i = int(prog)
        if t >= INICIO and i < len(ITENS):
            t0 = INICIO + i * PASSO
            a = min(ap(t, t0, 0.2), 1 - ap(t, t0 + PASSO - 0.15, 0.15))
            for j, l in enumerate(estilo.quebrar_linhas(ITENS[i], fi, 860)):
                d.text((W/2, 1200 + j * 76), l, font=fi, fill=ca(B, a), anchor='mm')
            d.text((W/2, 1380), "Deixe para trás.", font=estilo.sem_serifa(34, 600), fill=ca(G, a * ap(t, t0 + 0.6)), anchor='mm')
        tf = INICIO + PASSO * len(ITENS)
        if t >= tf:
            a = ap(t, tf, 0.5)
            d.text((W/2, 1220), "Mais leve, você vai mais longe.", font=estilo.serifa_italica(58, 600), fill=ca(G, a), anchor='mm')
            estilo.texto_espacado(d, (W/2, 1330), 'SALVA E VOLTA NELE QUANDO PRECISAR', estilo.sem_serifa(28, 600), ca(B, a), 5)
            estilo.texto_espacado(d, (W/2, 1400), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(24, 500), ca(C, a), 6)
        img = Image.alpha_composite(img, cam)
        q = np.asarray(img.convert('RGB'), np.float32) * (1 - ap(t, T - 0.5, 0.5))
        ff.stdin.write(estilo.para_bytes(q))
    ff.stdin.close(); ff.wait()
    midia.juntar_audio(mudo, saida)


if __name__ == '__main__':
    main()
