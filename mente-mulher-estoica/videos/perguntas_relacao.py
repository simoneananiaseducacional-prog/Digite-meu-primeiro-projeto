"""4 perguntas estoicas para a sua relação. Gancho: estoicismo não é aguentar em silêncio.
Lista que cresce na tela (a pergunta atual em destaque, as anteriores apagadas). Fontes conferidas:
Sêneca, Cartas a Lucílio, 20.2; gaslighting (Sweet, 2019); controle coercitivo (Stark, 2007); Epicteto, Encheirídion, 1.
Uso: python3 perguntas_relacao.py saida.mp4
"""
import sys, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw
from pathlib import Path
W, H, FPS, T = 1080, 1920, 30, 30.0
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
P, S = estilo.playfair, estilo.sem_serifa
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.25): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.25): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
def texto(im, xy, s, font, cor, a, anchor='mm'):
    if a < 0.02: return im
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).text(xy, s, font=font, fill=cor + (255,), anchor=anchor)
    lay.putalpha(lay.getchannel('A').point(lambda v: int(v * cl(a))))
    return Image.alpha_composite(im, lay)

PERG = [  # (início, linhas, fonte)
    (6.6, ['O que a pessoa faz', 'combina com o que ela diz?'], 'Sêneca, Cartas a Lucílio, 20.2'),
    (10.6, ['Você tem duvidado', 'da própria memória?'], 'Gaslighting (Paige Sweet, 2019)'),
    (14.6, ['Você está se afastando', 'de quem te faz bem?'], 'Controle coercitivo (Evan Stark, 2007)'),
    (18.6, ['Você está tentando mudar', 'quem não quer mudar?'], 'Epicteto, Encheirídion, 1'),
]
FIM_LISTA = 22.8
Y0, PASSO = 560, 250
fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
saida = Path(sys.argv[1]); ff = midia.gravador(saida.with_suffix('.mudo.mp4'))
for k in range(int(T * FPS)):
    t = k / FPS
    im = fundo.copy()
    # gancho (desde o primeiro quadro)
    g = 1 - ap(t, 5.8, 0.3)
    im = texto(im, (W / 2, 820), 'Estoicismo não é', P(84), B, g)
    im = texto(im, (W / 2, 925), 'aguentar em silêncio.', P(84), B, g)
    im = texto(im, (W / 2, 1060), 'É enxergar com clareza.', P(76, True), G, g * ap(t, 1.6, 0.4))
    # lista
    lista = ap(t, 6.0, 0.3) * (1 - ap(t, FIM_LISTA, 0.3))
    if lista > 0.02:
        d = ImageDraw.Draw(im)
        im = texto(im, (W / 2, 300), '4 PERGUNTAS ESTOICAS', S(40, 600), G, lista)
        im = texto(im, (W / 2, 362), 'para a sua relação', P(48, True), B, lista)
        for i, (t0, linhas, fonte) in enumerate(PERG):
            if t < t0: continue
            atual = i == len(PERG) - 1 or t < PERG[i + 1][0]
            a = lista * ap(t, t0) * (1.0 if atual else 0.42)
            y = Y0 + i * PASSO
            im = texto(im, (110, y + 38), f'0{i + 1}', P(64, True), G, a, 'lm')
            for j, l in enumerate(linhas):
                im = texto(im, (225, y + j * 64), l, P(54), B, a, 'lm')
            if atual: im = texto(im, (225, y + 140), fonte, P(32, True), C, lista * ap(t, t0 + 0.4), 'lm')
    # fecho
    f1 = jan(t, 23.0, 27.0)
    im = texto(im, (W / 2, 880), 'Lucidez não é frieza.', P(84), B, f1)
    im = texto(im, (W / 2, 990), 'É amor-próprio.', P(84, True), G, f1 * ap(t, 23.6, 0.3))
    f2 = ap(t, 27.2)
    im = texto(im, (W / 2, 880), 'Manda para quem', P(80), B, f2)
    im = texto(im, (W / 2, 985), 'precisa dessas perguntas.', P(76, True), G, f2)
    d2 = ImageDraw.Draw(im, 'RGBA')
    estilo.texto_espacado(d2, (W / 2, 1720), '@MENTE_MULHER_ESTOICA', S(26, 500), (170, 165, 158, 210), 6)
    ff.stdin.write(estilo.para_bytes(np.asarray(im.convert('RGB'), np.float32) * cl((T - t) / 0.4)))
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida)
saida.with_suffix('.mudo.mp4').unlink(missing_ok=True); print('ok', saida)
