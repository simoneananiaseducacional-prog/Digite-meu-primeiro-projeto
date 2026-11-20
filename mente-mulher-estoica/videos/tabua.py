"""Tirar o pé da tábua: ela, na beira do penhasco, segura com o pé a tábua onde ele está gritando com ela.
Ela respira, não grita de volta, tira o pé; a tábua vira e ele cai. Marco Aurélio, Meditações, 6.6.
Ideia inspirada em @hellendalla (cena própria em traço). Uso: python3 tabua.py saida.mp4
"""
import sys, math, random, numpy as np
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

CHAO, K = 1250, 1.35
CENTRO = (560, 1100)
PIV = (520, CHAO)                 # beira do penhasco
L_ESQ, L_DIR = 120, 360           # tábua: até 120 px para dentro, 360 px para o vazio
OFF_ELE = 210                     # onde ele está na tábua
XELA0 = 430
T_RESP, T_PE, T_CAI = 6.2, 8.4, 9.0
random.seed(3)
RAB = [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(9)]

def penhasco(d, a):
    pts = [(0, CHAO), (PIV[0], CHAO), (PIV[0] - 12, CHAO + 90), (PIV[0] + 8, CHAO + 210), (PIV[0] - 30, CHAO + 420), (PIV[0] - 10, H), (0, H)]
    d.polygon(pts, fill=(24, 23, 22, int(255 * a)))
    d.line(pts[:-1], fill=rgba(C, a), width=4, joint='curve')
    for k in range(3):   # mar lá embaixo
        y = 1640 + k * 34
        d.line([(PIV[0] + 40 + 30 * k, y), (W, y)], fill=rgba((90, 100, 118), a * (0.6 - 0.15 * k)), width=3)

fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
saida = Path(sys.argv[1]); ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    cena = 1 - 0.85 * ap(t, 11.4, 0.8)
    resp = ap(t, T_RESP, 1.2)                     # ela respira (brilho)
    pe = ap(t, T_PE, 0.5)                         # ela tira o pé
    ang = math.radians(75) * cl((t - T_PE - 0.2) / 0.9) ** 2 if t > T_PE + 0.2 else 0.0
    cen = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(cen, 'RGBA')
    penhasco(d, cena)
    ca, sa = math.cos(ang), math.sin(ang)
    def tab(s): return (PIV[0] + s * ca, PIV[1] - 6 + s * sa)
    queda = 1100 * max(0.0, t - T_PE - 1.1) ** 2       # a tábua também cai
    pl, pr = tab(-L_ESQ), tab(L_DIR)
    pl, pr = (pl[0] + 0.15 * queda, pl[1] + queda), (pr[0] + 0.15 * queda, pr[1] + queda)
    if pl[1] < H + 400: d.line([pl, pr], fill=rgba((150, 120, 80), cena), width=12)
    # ele: grita na tábua; quando ela inclina, escorrega e cai
    if t < T_PE + 0.2:
        tremor = 4 * math.sin(t * 40) * ap(t, 0.3, 0.3)
        hx, hy = PIV[0] + OFF_ELE + tremor, CHAO - 12
        grito = jan(t, 0.3, T_PE, 0.3)
        ele(d, hx, hy, cena, braco=0.6 + 0.3 * math.sin(t * 9), lado=-1, t=t, emo=dict(raiva=1.0, aberta=0.8))
        if grito > 0.02:   # rabiscos de grito saindo da boca em direção a ela
            bx, by = hx - 70, hy - 210
            for i, (u, v) in enumerate(RAB):
                f = (t * 1.3 + i / len(RAB)) % 1
                x0, y0 = bx - 160 * f, by + 50 * v * f
                d.line([(x0, y0), (x0 - 26, y0 + 10 * u)], fill=rgba((200, 90, 90), grito * cena * (1 - f)), width=4)
    else:
        tc = t - (T_PE + 0.2)
        s = OFF_ELE + 260 * tc ** 2
        px, py = tab(s)
        py += 900 * max(0.0, tc - 0.5) ** 2
        if py < H + 300:
            ele(d, px, py - 6, cena, braco=1.0, lado=-1, t=t, emo=dict(aberta=1.0))
    # ela: calma, pé na tábua; depois dá um passo para trás
    xe = XELA0 - 60 * pe
    personagens.MAO_PEITO = resp * (1 - ap(t, T_PE - 0.4, 0.4))
    ela(d, xe, CHAO - 6, cena, braco=0.0, lado=1, cabeca_baixa=0.2 * (1 - pe), t=t,
        emo=dict(sorriso=0.3 + 0.5 * ap(t, T_CAI + 0.6, 0.8)))
    personagens.MAO_PEITO = 0.0
    big = cen.resize((int(W * K), int(H * K)), Image.BICUBIC)
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.paste(big, (int(W / 2 - CENTRO[0] * K), int(1060 - CENTRO[1] * K)))
    im = fundo.copy()
    br = resp * cena
    if br > 0.02:
        px = W / 2 + (xe - CENTRO[0]) * K
        gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl)
        gd.ellipse((px - 260, 1000 - 320, px + 260, 1000 + 320), fill=G + (int(65 * br),))
        im = Image.alpha_composite(im, gl.filter(ImageFilter.GaussianBlur(80)))
    im = Image.alpha_composite(im, cam)
    q = 1 - ap(t, 10.8, 0.6)   # pergunta inteira desde o quadro zero
    im = texto(im, (W / 2, 290), 'Você ainda sustenta', estilo.playfair(66), B, q)
    im = texto(im, (W / 2, 385), 'quem só grita com você?', estilo.playfair(66, True), G, q)
    f1 = jan(t, 11.8, 15.0); f2 = jan(t, 12.6, 15.0)
    im = texto(im, (W / 2, 800), 'Às vezes, a paz', estilo.playfair(74), B, f1)
    im = texto(im, (W / 2, 900), 'é só tirar o pé da tábua.', estilo.playfair(70, True), G, f2)
    f3 = jan(t, 15.3, 18.6)
    im = texto(im, (W / 2, 790), '“A melhor forma de se defender', estilo.playfair(56, True), B, f3)
    im = texto(im, (W / 2, 870), 'é não se tornar igual.”', estilo.playfair(56, True), G, f3)
    im = texto(im, (W / 2, 980), 'Marco Aurélio, Meditações, 6.6', estilo.playfair(32, True), C, f3)
    d2 = ImageDraw.Draw(im, 'RGBA')
    estilo.texto_espacado(d2, (W / 2, 1720), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(24, 500), rgba((170, 165, 158), 0.8), 6)
    ff.stdin.write(estilo.para_bytes(np.asarray(im.convert('RGB'), np.float32) * (1 - ap(t, T - 0.4, 0.4))))
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); print('ok', saida)
