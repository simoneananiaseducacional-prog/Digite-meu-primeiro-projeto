"""A versão que aceitava pouco: ela, apagada (cinza), de mãos dadas com ele. Uma versão dourada dela se solta
e segue; a cinza some junto com ele. Fecho: Sêneca, Cartas a Lucílio, 6.1.
Uso: python3 versao.py saida.mp4
"""
import sys, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia, personagens
from personagens import ela, ele
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
W, H, FPS, T = 1080, 1920, 30, 19.0
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.5): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
def rgba(c, a): return c + (int(255 * cl(a)),)
def lerp(a, b, p): return a + (b - a) * p
def texto(im, xy, s, font, cor, a):
    """Texto em camada própria (o Pillow ignora alfa baixo no ImageDraw RGBA)."""
    if a < 0.02: return im
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).text(xy, s, font=font, fill=cor + (255,), anchor='mm')
    lay.putalpha(lay.getchannel('A').point(lambda v: int(v * cl(a))))
    return Image.alpha_composite(im, lay)

CHAO, K = 1250, 1.6
CENTRO = (520, 1090)
XC, XH = 500, 670            # ela cinza, ele
OURO0 = personagens.DOURADO
fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
F1 = estilo.playfair(66); F2 = estilo.playfair(60, True)
saida = Path(sys.argv[1]); ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    cena = 1 - 0.85 * ap(t, 11.2, 0.8)
    solta = ap(t, 2.4, 2.6)            # a dourada se solta e anda
    some = ap(t, 6.0, 2.4)             # a cinza e ele somem
    brilho = ap(t, 7.6, 1.4)
    cen = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(cen, 'RGBA')
    d.line([(CENTRO[0] - 360, CHAO), (CENTRO[0] + 360, CHAO)], fill=rgba(C, cena * 0.8), width=4)
    ag = cena * (1 - some)
    if ag > 0.02:
        ele(d, XH, CHAO - 6, ag, braco=0.45, lado=-1, t=t)
        personagens.DOURADO = (140, 140, 148)
        ela(d, XC, CHAO - 6, ag, braco=0.45, lado=1, cabeca_baixa=0.35, t=t, emo=dict(triste=0.3))
        personagens.DOURADO = OURO0
    if solta > 0.02:
        xd = lerp(XC, 270, solta)
        ela(d, xd, CHAO - 6, cena * solta, braco=0.0, lado=-1, cabeca_baixa=0.0, t=t + 0.7,
            emo=dict(sorriso=0.4 + 0.5 * brilho))
    big = cen.resize((int(W * K), int(H * K)), Image.BICUBIC)
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.paste(big, (int(W / 2 - CENTRO[0] * K), int(1060 - CENTRO[1] * K)))
    im = fundo.copy()
    if brilho > 0.02:
        px = W / 2 + (270 - CENTRO[0]) * K
        gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl)
        gd.ellipse((px - 300, 1000 - 340, px + 300, 1000 + 340), fill=G + (int(70 * brilho * cena),))
        im = Image.alpha_composite(im, gl.filter(ImageFilter.GaussianBlur(90)))
    im = Image.alpha_composite(im, cam); d2 = ImageDraw.Draw(im, 'RGBA')
    a1 = 1 - ap(t, 10.8, 0.6)          # primeira linha inteira desde o quadro zero
    a2 = ap(t, 3.6, 0.8) * a1
    im = texto(im, (W / 2, 300), 'Você não perdeu alguém.', F1, B, a1)
    im = texto(im, (W / 2, 400), 'Perdeu a versão de você', F2, G, a2)
    im = texto(im, (W / 2, 480), 'que aceitava pouco.', F2, G, a2)
    f3 = jan(t, 11.6, 18.6)
    for i, l in enumerate(['“Percebo que não estou', 'apenas melhorando:', 'estou me transformando.”']):
        im = texto(im, (W / 2, 780 + i * 80), l, estilo.playfair(58, True), G if i == 2 else B, f3)
    im = texto(im, (W / 2, 1060), 'Sêneca, Cartas a Lucílio, 6.1', estilo.playfair(32, True), C, f3)
    d2 = ImageDraw.Draw(im, 'RGBA')
    estilo.texto_espacado(d2, (W / 2, 1640), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(24, 500), rgba((170, 165, 158), 0.8), 6)
    ff.stdin.write(estilo.para_bytes(np.asarray(im.convert('RGB'), np.float32) * (1 - ap(t, T - 0.4, 0.4))))
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); print('ok', saida)
