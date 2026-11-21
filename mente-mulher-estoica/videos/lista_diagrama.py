"""Lista em vídeo no visual dos diagramas: título fixo, cada item surge numa cápsula dourada
e uma seta leva a "Deixe para trás."; no fim, pedido de salvar.

    python3 lista_diagrama.py saida.mp4
"""
import sys
import numpy as np
from PIL import Image, ImageDraw
import estilo, midia

W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
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
INICIO, PASSO, FIM = 1.2, 2.6, 3.0
T = INICIO + PASSO * len(ITENS) + FIM


def ap(t, t0, d=0.4):
    return estilo.suavizar((t - t0) / d) if t > t0 else 0.0


def cor(c, a):
    return c + (int(255 * max(0, min(1, a))),)


def main():
    saida = sys.argv[1]
    fundo = np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)
    fi, fn, fs = estilo.serifa_italica(54, 600), estilo.sem_serifa(34, 600), estilo.serifa(60, 500)
    ff = midia.gravador(saida.replace('.mp4', '.mudo.mp4'), estatico=False)
    for k in range(int(T * FPS)):
        t = k / FPS
        img = Image.fromarray(fundo).convert('RGBA'); cam = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
        d.text((W/2, 520), TITULO[0], font=estilo.serifa(66, 500), fill=cor(B, 1), anchor='mm')
        d.text((W/2, 600), TITULO[1], font=estilo.serifa(66, 500), fill=cor(G, 1), anchor='mm')
        i = int((t - INICIO) // PASSO)
        if 0 <= i < len(ITENS):
            t0 = INICIO + i * PASSO
            a = min(ap(t, t0, 0.35), 1 - ap(t, t0 + PASSO - 0.3, 0.3))
            d.text((W/2, 790), f"{i+1:02d}", font=fn, fill=cor(G, a), anchor='mm')
            linhas = estilo.quebrar_linhas(ITENS[i], fi, 760)
            h = 70 * len(linhas) + 60
            y0 = 900 - h / 2 + 30
            d.rounded_rectangle((130, y0, W - 130, y0 + h), radius=h / 2 if len(linhas) == 1 else 60, outline=cor(G, a), width=3)
            for j, l in enumerate(linhas):
                d.text((W/2, y0 + 30 + 35 + j * 70), l, font=fi, fill=cor(B, a), anchor='mm')
            p = min(1, max(0, (t - t0 - 0.7) / 0.5))
            if p > 0:
                ax, ay = W/2 - 90, y0 + h + 10
                bx, by = W/2 - 200, y0 + h + 230
                ex, ey = ax + (bx - ax) * p, ay + (by - ay) * p
                d.line((ax, ay, ex, ey), fill=cor(G, a), width=3)
                if p > 0.98:
                    d.line((bx, by, bx - 4, by - 30), fill=cor(G, a), width=3)
                    d.line((bx, by, bx + 26, by - 16), fill=cor(G, a), width=3)
            d.text((W/2 - 260, y0 + h + 300), "Deixe para trás.", font=fs, fill=cor(B, a * ap(t, t0 + 1.1)), anchor='lm')
        else:
            tf = INICIO + PASSO * len(ITENS)
            if t >= tf:
                a = ap(t, tf, 0.5)
                d.text((W/2, 960), "Salva e volta nele", font=estilo.serifa_italica(62, 600), fill=cor(G, a), anchor='mm')
                d.text((W/2, 1040), "quando precisar.", font=estilo.serifa_italica(62, 600), fill=cor(G, a), anchor='mm')
                estilo.texto_espacado(d, (W/2, 1200), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(26, 500), cor(C, a), 6)
        img = Image.alpha_composite(img, cam)
        q = np.asarray(img.convert('RGB'), np.float32) * (1 - ap(t, T - 0.5, 0.5))
        ff.stdin.write(estilo.para_bytes(q))
    ff.stdin.close(); ff.wait()
    midia.juntar_audio(saida.replace('.mp4', '.mudo.mp4'), saida)


if __name__ == '__main__':
    main()
