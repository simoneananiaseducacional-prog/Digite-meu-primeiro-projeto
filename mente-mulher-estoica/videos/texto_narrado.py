"""Vídeo de frases narradas: tela preta, serifa branca em caixa alta, uma frase por vez.

    python3 texto_narrado.py saida.mp4            # versão final (sem contagem)
    python3 texto_narrado.py saida.mp4 --guia     # versão para ler em voz alta, com contagem 3, 2, 1
"""
import sys
import numpy as np
from PIL import Image, ImageDraw
import estilo, midia

W, H, FPS = 1080, 1920, 30
FRASES = [
    "Talvez as pessoas nunca entendam",
    "por que você ficou mais reservada.",
    "Não foi frieza.",
    "Foi aprendizado.",
    "Você entregou os bastidores da sua alma",
    "para quem só queria plateia.",
    "E aprendeu que nem todo mundo",
    "merece acesso a tudo o que você é.",
    "Marco Aurélio dizia que não existe refúgio",
    "mais tranquilo do que a própria mente.",
    "Hoje você fala menos, escolhe mais",
    "e protege a sua paz.",
    "Isso não é distância.",
    "É maturidade.",
]
CONTAGEM = 3.0


def tempos():
    t, out = 0.0, []
    for f in FRASES:
        d = 1.1 + 0.42 * len(f.split())
        out.append((t, t + d, f)); t += d
    return out, t + 1.5


def main():
    saida, guia = sys.argv[1], '--guia' in sys.argv
    seq, total = tempos()
    ini = CONTAGEM if guia else 0.0
    ft = estilo.serifa(64, 500)
    ff = midia.gravador(saida.replace('.mp4', '.mudo.mp4'), estatico=False)
    for k in range(int((total + ini) * FPS)):
        t = k / FPS - ini
        img = Image.new('RGB', (W, H), (0, 0, 0)); d = ImageDraw.Draw(img)
        if t < 0:
            d.text((W/2, H/2), str(int(-t) + 1), font=estilo.serifa(200, 600), fill=estilo.DOURADO, anchor='mm')
            d.text((W/2, H/2 + 200), 'LEIA EM VOZ ALTA', font=estilo.sem_serifa(34, 600), fill=estilo.CINZA, anchor='mm')
        for a, b, f in seq:
            if a <= t < b:
                al = min(1, (t - a) / 0.25, (b - t) / 0.2)
                linhas = estilo.quebrar_linhas(f.upper(), ft, W - 240)
                y = H/2 - 150 - (len(linhas) - 1) * 40
                cor = tuple(int(c * al) for c in (240, 240, 240))
                for i, l in enumerate(linhas):
                    d.text((W/2, y + i * 80), l, font=ft, fill=cor, anchor='mm')
        if not guia:
            estilo.texto_espacado(d, (W/2, 1500), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(24, 500), (110, 110, 110), 6)
        ff.stdin.write(np.asarray(img).tobytes())
    ff.stdin.close(); ff.wait()
    midia.juntar_audio(saida.replace('.mp4', '.mudo.mp4'), saida)
    print(total)


if __name__ == '__main__':
    main()
