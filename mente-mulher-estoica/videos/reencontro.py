"""Reencontro: amor improvável, intenso, desencontro, vida que segue, reencontro mais maduro.
Roteiro da Simone (9 cenas), anonimizado, com os personagens fixos. Frases curtas no alto, uma por cena.
Uso: python3 reencontro.py saida.mp4
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia, personagens
from personagens import ela, ele
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
saida = Path(sys.argv[1])
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.4): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.4): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
def rgba(c, a): return c + (int(255 * cl(a)),)
def lerp(a, b, p): return a + (b - a) * p
def seg(t, t0, t1): return estilo.suavizar(cl((t - t0) / (t1 - t0)))

CENAS = [0.0, 3.2, 6.4, 9.6, 13.4, 16.6, 19.8, 23.0, 26.2, 30.0]
FRASES = [['Não era pra ser nada…'], ['Mas aconteceu.'], ['E foi intenso.'],
          ['Mas muita gente', 'ficou no meio.'], ['Ela seguiu a vida.', 'E se casou.'],
          ['Mas algumas histórias', 'não terminam dentro da gente.'], ['Anos depois, os dois sozinhos,', 'se encontraram de novo.'],
          ['Dessa vez,', 'com mais consciência.'], ['Alguns sentimentos merecem', 'mais do que impulso.', 'Merecem cuidado.']]
T = CENAS[-1]
CHAO = 1250
HY = CHAO - 6 - 240
K, CX, CY = 1.55, 540, 1090
OURO_ELE = personagens.CINZA

def x_ela(t):
    x = lerp(200, 320, seg(t, 0.2, 2.6))             # cena 1: entram e se cruzam
    x = lerp(x, 430, seg(t, 3.4, 5.6))                # cena 2: se aproximam
    x = lerp(x, 280, seg(t, 9.8, 11.6))              # cena 4: se afastam
    x = lerp(x, 380, seg(t, 20.4, 22.6))  # reencontro              # cena 7: reencontro
    x = lerp(x, 440, seg(t, 23.2, 24.8))
    return x
def x_ele(t):
    x = lerp(940, 780, seg(t, 0.2, 2.6))
    x = lerp(x, 650, seg(t, 3.4, 5.6))
    x = lerp(x, 800, seg(t, 9.8, 11.6))
    x = lerp(x, 1250, seg(t, 12.9, 14.0))             # sai de cena
    x = lerp(x, 700, seg(t, 19.8, 22.4))              # volta
    x = lerp(x, 640, seg(t, 23.2, 24.8))
    return x
def x_outro(t):
    return lerp(1250, 500, seg(t, 13.6, 15.2)) if t < 16.8 else lerp(500, 1250, seg(t, 16.8, 18.6))

def coracao(d, cx, cy, s, a, partido=0.0, metade=None):
    if a < 0.02 or s < 0.02: return
    r = 18 * s
    for lado in (-1, 1):
        if metade is not None and lado != metade: continue
        off = lado * 16 * partido * s
        d.ellipse((cx + off + lado * r - r, cy - r, cx + off + lado * r + r, cy + r), fill=rgba(G, a))
        tri = [(cx + off, cy + 4), (cx + off + lado * (2 * r - 1), cy + 4), (cx + off, cy + 2.6 * r)]
        d.polygon(tri, fill=rgba(G, a))

def rachadura(d, t, a):
    ab = 26 * seg(t, 10.0, 11.0) * (1 - seg(t, 13.2, 14.0))
    if ab < 1: return
    pe = [(540 - ab / 2 + dx, CHAO + y) for dx, y in [(0, 0), (-10, 50), (8, 110), (-6, 180)]]
    pd = [(540 + ab / 2 + dx, CHAO + y) for dx, y in [(0, 0), (10, 50), (-6, 110), (8, 180)]]
    d.polygon(pe + pd[::-1], fill=(4, 4, 4, int(255 * a)))
    d.line(pe, fill=rgba(C, a), width=3); d.line(pd, fill=rgba(C, a), width=3)

def figura_cinza(d, x, a, aponta, t):
    cor = (125, 125, 132); hy = HY + 6
    d.ellipse((x - 32, hy - 32, x + 32, hy + 32), fill=(45, 45, 50, int(235 * a)), outline=rgba(cor, a), width=4)
    d.line([(x, hy + 32), (x, CHAO - 96)], fill=rgba(cor, a), width=5)
    for s_ in (-1, 1): d.line([(x, CHAO - 96), (x + s_ * 26, CHAO - 6)], fill=rgba(cor, a), width=5)
    d.line([(x, hy + 58), (x + aponta * 70, hy + 44 + 5 * math.sin(t * 9 + x))], fill=rgba(cor, a), width=5)
    for s_ in (-1, 1): d.line([(x + s_ * 11 - 5, hy - 4 + 3), (x + s_ * 11 + 5, hy - 4 - 3 * s_)], fill=rgba(cor, a), width=4)
def multidao(d, t, a):
    """Várias pessoas entram entre os dois, apontando, e empurram cada um para um lado."""
    for i, (xa, ti, ap_) in enumerate([(540, 10.0, 1), (460, 10.3, -1), (620, 10.6, 1), (380, 10.9, -1), (700, 11.2, 1)]):
        chega = seg(t, ti, ti + 0.6); sai = seg(t, 12.8, 13.4)
        fa = chega * (1 - sai)
        if fa < 0.02: continue
        xs = xa + (1 if ap_ > 0 else -1) * 300 * (1 - chega)
        figura_cinza(d, xs, a * fa, ap_, t)
def aliancas(d, cx, cy, a, quebra=0.0):
    if a < 0.02: return
    for k, cor in ((-1, G), (1, (170, 170, 176))):
        off = k * (14 + 30 * quebra)
        d.ellipse((cx + off - 18, cy - 18 + 20 * quebra, cx + off + 18, cy + 18 + 20 * quebra), outline=rgba(cor, a), width=5)

fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
FT = estilo.sem_serifa(54, 500); TXT = (205, 200, 194)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    a = ap(t, 0.1, 0.5)
    cena = a * (1 - 0.92 * ap(t, 26.4, 0.8))
    cen = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(cen, 'RGBA')
    d.line([(0, CHAO), (W, CHAO)], fill=rgba(C, cena), width=4)
    multidao(d, t, cena)
    xe, xh = x_ela(t), x_ele(t)
    # emoções por cena
    feliz = seg(t, 3.6, 4.6) * (1 - seg(t, 9.8, 10.4))
    triste_ela = seg(t, 10.0, 10.6) * (1 - seg(t, 13.6, 14.4)) + 0.5 * seg(t, 17.0, 17.6) * (1 - seg(t, 20.6, 21.2))
    calma = seg(t, 21.0, 22.0)
    emo_ela = dict(sorriso=0.3 * (t < 3.4) + 0.9 * feliz + 0.25 * seg(t, 14.0, 14.6) * (1 - seg(t, 16.8, 17.2)) + 0.7 * calma,
                   triste=0.8 * triste_ela)
    emo_ele = dict(sorriso=0.3 * (t < 3.4) + 0.9 * feliz + 0.7 * calma, triste=0.8 * seg(t, 10.0, 10.6) * (1 - seg(t, 12.6, 13.0)))
    ela(d, xe, CHAO - 6, cena, braco=0.15, lado=1, cabeca_baixa=0.4 * triste_ela, t=t, emo=emo_ela)
    if -100 < xh < 1180:
        ele(d, xh, CHAO - 6, cena, braco=0.15, lado=-1, cabeca_baixa=0.3 * seg(t, 10.0, 10.6) * (1 - seg(t, 12.6, 13.0)), t=t, emo=emo_ele)
    xo = x_outro(t)
    if 13.4 < t < 18.8 and xo < 1180:          # o outro relacionamento: figura em cinza escuro, neutra
        personagens.CINZA = (105, 105, 112)
        ele(d, xo, CHAO - 6, cena, braco=0.1, lado=-1, t=t, emo=dict(sorriso=0.1))
        personagens.CINZA = OURO_ELE
        ali = seg(t, 15.0, 15.6) * (1 - seg(t, 17.6, 18.2))
        aliancas(d, (xe + xo) / 2, HY - 40, cena * ali, quebra=seg(t, 16.8, 17.6))
    # o coração: nasce entre eles, cresce, se parte, fica uma metade em cada um, volta a se unir
    meio = ((xe + xh) / 2, HY + 30)
    nasce = seg(t, 4.2, 5.4); cresce = seg(t, 6.6, 8.2)
    s = 0.6 * nasce + 0.9 * cresce
    partido = seg(t, 9.6, 10.2)
    some = seg(t, 10.2, 10.8)                   # metades viram brilhos guardados no peito
    peito = seg(t, 17.0, 18.0) * (1 - seg(t, 23.2, 24.2))
    une = seg(t, 23.4, 24.8)
    glow_s = 0.0
    if t < 13.2:
        coracao(d, meio[0], meio[1] - 30 * cresce, s, cena * (1 - some), partido=partido)
        glow_s = s * (1 - 0.6 * partido) * (1 - some)
    if peito > 0.02:
        coracao(d, xe, HY + 82, 0.5, cena * peito, metade=1)
        if xh < 1100: coracao(d, xh, HY + 82, 0.5, cena * peito, metade=-1)
    if une > 0.02:
        mm = ((xe + xh) / 2, HY + 30)
        coracao(d, mm[0], mm[1], 0.9 * une, cena * une)
        glow_s = 0.7 * une
    # brilho suave
    if glow_s > 0.02:
        gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl)
        gx, gy = (meio[0], meio[1] - 30 * cresce) if t < 13.2 else ((xe + xh) / 2, HY + 30)
        gr = 140 * glow_s
        gd.ellipse((gx - gr, gy - gr, gx + gr, gy + gr), fill=G + (int(60 * cena * glow_s),))
        cen = Image.alpha_composite(gl.filter(ImageFilter.GaussianBlur(30)), cen)
    big = cen.resize((int(W * K), int(H * K)), Image.BICUBIC)
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.paste(big, (int(CX - CX * K), int(CY - CY * K)))
    im = Image.alpha_composite(fundo, cam); d2 = ImageDraw.Draw(im, 'RGBA')
    for i, linhas in enumerate(FRASES):
        t0, t1 = CENAS[i] + 0.2, CENAS[i + 1] - 0.1
        if i == 8: t1 = 28.6
        fa = jan(t, t0, t1, 0.35)
        if fa < 0.02: continue
        y0 = 470 if i < 8 else 760
        for j, l in enumerate(linhas):
            cor = G if (i == 8 and j == 2) else TXT
            fnt = estilo.playfair(56, True) if (i == 8 and j == 2) else FT
            d2.text((W/2, y0 + j * 78), l, font=fnt, fill=rgba(cor, fa), anchor='mm')
    ia = ap(t, 28.6, 0.4)
    if ia > 0.02:
        s_ = 70; yy = 860
        d2.rounded_rectangle((W/2 - s_, yy - s_, W/2 + s_, yy + s_), radius=40, outline=rgba(B, ia), width=10)
        d2.ellipse((W/2 - 34, yy - 34, W/2 + 34, yy + 34), outline=rgba(B, ia), width=10)
        d2.ellipse((W/2 + 36, yy - 50, W/2 + 50, yy - 36), fill=rgba(B, ia))
        d2.text((W/2, yy + 140), '@mente_mulher_estoica', font=estilo.sem_serifa(46, 600), fill=rgba(B, ia), anchor='mm')
    ff.stdin.write(estilo.para_bytes(np.asarray(im.convert('RGB'), np.float32) * (1 - ap(t, T - 0.3, 0.3))))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida)
print('ok', saida)
