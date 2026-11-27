"""O copo: ela despeja o seu copo dourado no copo dele, que só olha o celular. O copo dela esvazia, o dele
transborda. Ela para, leva o copo ao peito e ele volta a se encher. Sêneca, Cartas a Lucílio, 1.1.
Uso: python3 copo.py saida.mp4
"""
import sys, math, numpy as np
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
    if a < 0.02: return im
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).text(xy, s, font=font, fill=cor + (255,), anchor='mm')
    lay.putalpha(lay.getchannel('A').point(lambda v: int(v * cl(a))))
    return Image.alpha_composite(im, lay)

CHAO, K = 1250, 1.6
CENTRO = (540, 1080)
XE, XH = 400, 690
DESP = [(1.4, 3.0), (3.6, 5.2), (5.8, 7.4)]   # despejos (início, fim)
T_TRISTE, T_PEITO, T_ENCHE = 8.0, 9.4, 10.0

def copo(d, cx, cy, nivel, a, ang=0.0, cor_liq=G, brilho=0.0):
    """Copo (trapézio) com líquido; ang inclina para a direita."""
    w0, w1, h = 30, 22, 56
    pts = [(-w0, -h), (w0, -h), (w1, 0), (-w1, 0)]
    ca, sa = math.cos(ang), math.sin(ang)
    rot = lambda p: (cx + p[0] * ca - p[1] * sa, cy + p[0] * sa + p[1] * ca)
    if nivel > 0.01:
        hl = h * min(nivel, 1.0)
        wl = w1 + (w0 - w1) * min(nivel, 1.0)
        liq = [(-wl, -hl), (wl, -hl), (w1, 0), (-w1, 0)]
        d.polygon([rot(p) for p in liq], fill=rgba(cor_liq, a * (0.85 + 0.15 * brilho)))
    d.line([rot(p) for p in pts] + [rot(pts[0])], fill=rgba(B, a), width=4)
    return rot((w0, -h))   # borda de onde o líquido sai

fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
saida = Path(sys.argv[1]); ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    cena = 1 - 0.85 * ap(t, 11.4, 0.8)
    despejado = sum(cl((t - a0) / (a1 - a0)) for a0, a1 in DESP) / len(DESP)
    despejando = max((jan(t, a0, a1, 0.3) for a0, a1 in DESP), default=0.0)
    nivel_ela = 1.0 - 0.95 * despejado
    enche = ap(t, T_ENCHE, 1.4)
    nivel_ela = lerp(nivel_ela, 1.0, enche)
    nivel_ele = 0.25 + 1.0 * despejado
    peito = ap(t, T_PEITO, 0.8)
    triste = ap(t, T_TRISTE, 0.8) * (1 - enche)
    cen = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(cen, 'RGBA')
    d.line([(CENTRO[0] - 360, CHAO), (CENTRO[0] + 360, CHAO)], fill=rgba(C, cena * 0.8), width=4)
    # ele: olhando o celular, ignora
    personagens.CINZA = (150, 150, 158)
    ele(d, XH, CHAO - 6, cena, braco=0.35, lado=1, cabeca_baixa=0.7, t=t)
    personagens.CINZA = (175, 175, 175)
    hy = CHAO - 6 - 240 + 11
    d.rounded_rectangle((XH + 38, hy + 60, XH + 56, hy + 92), radius=3, fill=(30, 30, 32, int(255 * cena)), outline=rgba((190, 190, 196), cena), width=2)
    d.rectangle((XH + 41, hy + 64, XH + 53, hy + 84), fill=(120, 150, 200, int(200 * cena)))
    # copo dele, largado na mão de trás, quase sem olhar
    cxh, cyh = XH - 40, CHAO - 88
    copo(d, cxh, cyh, nivel_ele, cena, cor_liq=G)
    if nivel_ele > 1.0:   # transborda
        for i in range(4):
            f = (t * 1.4 + i / 4) % 1
            gx = cxh + (-30 if i % 2 else 30) + (-6 if i % 2 else 6) * f
            d.ellipse((gx - 5, cyh - 50 + 200 * f - 5, gx + 5, cyh - 50 + 200 * f + 5), fill=rgba(G, cena * (1 - f) * min(1, nivel_ele - 1.0) * 3))
    # ela e o copo dela
    personagens.MAO_PEITO = peito
    ela(d, XE, CHAO - 6, cena, braco=0.55 * (1 - peito), lado=1, cabeca_baixa=0.6 * triste, t=t,
        emo=dict(triste=0.8 * triste, sorriso=0.2 * (1 - triste) + 0.6 * enche))
    personagens.MAO_PEITO = 0.0
    cxe = lerp(XE + 120, XE + 34, peito); cye = lerp(CHAO - 165, CHAO - 120, peito)
    ang = math.radians(70) * despejando
    borda = copo(d, cxe, cye, nivel_ela, cena, ang=ang, cor_liq=G, brilho=enche)
    if despejando > 0.2 and nivel_ela > 0.06:   # fio de líquido até o copo dele
        alvo = (cxh, cyh - 50)
        pts = [(lerp(borda[0], alvo[0], u), lerp(borda[1], alvo[1], u) - 70 * math.sin(math.pi * u) * 0.4) for u in np.linspace(0, 1, 20)]
        d.line(pts, fill=rgba(G, cena * despejando), width=5, joint='curve')
    big = cen.resize((int(W * K), int(H * K)), Image.BICUBIC)
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.paste(big, (int(W / 2 - CENTRO[0] * K), int(1060 - CENTRO[1] * K)))
    im = fundo.copy()
    if enche > 0.02:
        px = W / 2 + (XE - CENTRO[0]) * K
        gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl)
        gd.ellipse((px - 280, 1000 - 320, px + 280, 1000 + 320), fill=G + (int(70 * enche * cena),))
        im = Image.alpha_composite(im, gl.filter(ImageFilter.GaussianBlur(85)))
    im = Image.alpha_composite(im, cam)
    q = 1 - ap(t, 10.8, 0.6)   # pergunta inteira desde o quadro zero
    im = texto(im, (W / 2, 290), 'Até quando você vai encher', estilo.playfair(62), B, q)
    im = texto(im, (W / 2, 380), 'quem nem olha para você?', estilo.playfair(64, True), G, q)
    f1 = jan(t, 11.8, 15.0); f2 = jan(t, 12.6, 15.0)
    im = texto(im, (W / 2, 800), 'Ninguém serve', estilo.playfair(76), B, f1)
    im = texto(im, (W / 2, 900), 'de um copo vazio.', estilo.playfair(76, True), G, f2)
    f3 = jan(t, 15.3, 18.6)
    im = texto(im, (W / 2, 820), '“Reivindique-se para si mesma.”', estilo.playfair(58, True), G, f3)
    im = texto(im, (W / 2, 930), 'Sêneca, Cartas a Lucílio, 1.1', estilo.playfair(32, True), C, f3)
    d2 = ImageDraw.Draw(im, 'RGBA')
    estilo.texto_espacado(d2, (W / 2, 1640), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(24, 500), rgba((170, 165, 158), 0.8), 6)
    ff.stdin.write(estilo.para_bytes(np.asarray(im.convert('RGB'), np.float32) * (1 - ap(t, T - 0.4, 0.4))))
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); print('ok', saida)
