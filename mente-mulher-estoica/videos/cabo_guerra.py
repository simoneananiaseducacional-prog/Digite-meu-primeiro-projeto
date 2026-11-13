"""Cabo de guerra: numa briga cada um puxa a corda. Ela pausa sem largar, ele solta a razão,
a corda vira ponte sobre a rachadura e ela atravessa para dizer o que sente.
Inspiração das frases: @linguagemcorporaldominante. Base: John Gottman (pausa e aceitar influência);
Sêneca, Sobre a ira 3.12.4. Personagens fixos. Uso: python3 cabo_guerra.py saida.mp4
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from personagens import ela, ele
from PIL import Image, ImageDraw
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
saida = Path(sys.argv[1])
fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1): return ap(t, t0) * (1 - ap(t, t1 - 0.5, 0.5))
def rgba(c, a): return c + (int(255 * cl(a)),)
def lerp(a, b, p): return a + (b - a) * p
T = 29.0
CHAO = 1250
def balao(d, alvo, centro, linhas, cor, a, coracao=False):
    if a <= 0.01: return
    f = estilo.sem_serifa(40, 600)
    larg = max(d.textlength(l, font=f) for l in linhas) + 70
    alt = 56 * len(linhas) + 44 + (60 if coracao else 0)
    x0, y0 = centro[0] - larg / 2, centro[1] - alt / 2
    d.rounded_rectangle((x0, y0, x0 + larg, y0 + alt), radius=30, fill=(14, 14, 14, int(235 * a)), outline=rgba(cor, a), width=3)
    bx = max(x0 + 40, min(x0 + larg - 40, alvo[0])); base = y0 + alt
    d.polygon([(bx - 16, base - 2), (bx + 16, base - 2), alvo], fill=(14, 14, 14, int(235 * a)))
    d.line([(bx - 16, base), alvo, (bx + 16, base)], fill=rgba(cor, a), width=3)
    for i, l in enumerate(linhas):
        d.text((centro[0], y0 + 50 + i * 56), l, font=f, fill=rgba(B, a), anchor='mm')
    if coracao:   # coração dourado desenhado
        cx, cy, r = centro[0], y0 + alt - 52, 14
        d.ellipse((cx - 2 * r, cy - r, cx, cy + r), fill=rgba(G, a)); d.ellipse((cx, cy - r, cx + 2 * r, cy + r), fill=rgba(G, a))
        d.polygon([(cx - 2 * r + 1, cy + 3), (cx + 2 * r - 1, cy + 3), (cx, cy + 2.6 * r)], fill=rgba(G, a))

# linha do tempo
PAUSA_DELA, SOLTA_ELE, PONTE, ATRAVESSA, FECHO = 4.0, 9.5, 13.0, 15.0, 21.5
def puxando(t, quem):
    fim = PAUSA_DELA if quem == 'ela' else SOLTA_ELE
    return 1 - ap(t, fim, 0.8)
def x_ela(t):
    base = 300 - 10 * abs(math.sin(t * 7)) * puxando(t, 'ela')
    return lerp(base, 490, estilo.suavizar(cl((t - ATRAVESSA) / 3.5)))
def x_ele(t):
    base = 780 + 10 * abs(math.sin(t * 7 + 1)) * puxando(t, 'ele')
    return lerp(base, 610, estilo.suavizar(cl((t - ATRAVESSA - 0.6) / 3.2)))
def rachadura(d, t, a):
    abre = 70 * ap(t, 1.2, 2.5) * (1 - 0.0 * t)
    if abre < 1: return
    pts_e = [(540 - abre / 2 + dx, CHAO + y) for dx, y in [(0, 0), (-10, 60), (8, 120), (-6, 190), (0, 260)]]
    pts_d = [(540 + abre / 2 + dx, CHAO + y) for dx, y in [(0, 0), (12, 60), (-4, 120), (10, 190), (0, 260)]]
    d.polygon(pts_e + pts_d[::-1], fill=(6, 6, 6, int(255 * a)))
    d.line(pts_e, fill=rgba(C, a), width=3); d.line(pts_d, fill=rgba(C, a), width=3)
def corda(d, t, a):
    xe, xd = x_ela(t), x_ele(t)
    mao_e = (xe + 150, CHAO - 6 - 240 + 50); mao_d = (xd - 150, CHAO - 6 - 240 + 50)
    vira = ap(t, PONTE, 1.6)                      # 0 = corda nas mãos, 1 = ponte no chão
    p0 = (lerp(mao_e[0], 470, vira), lerp(mao_e[1], CHAO, vira))
    p1 = (lerp(mao_d[0], 610, vira), lerp(mao_d[1], CHAO, vira))
    tensa = max(puxando(t, 'ela'), puxando(t, 'ele'))
    sag = lerp(lerp(70, 8, tensa), 18, vira)
    cor = tuple(int(lerp(B[i], G[i], vira)) for i in range(3))
    pts = []
    for i in range(41):
        u = i / 40
        x = lerp(p0[0], p1[0], u); y = lerp(p0[1], p1[1], u) + sag * 4 * u * (1 - u)
        if tensa > 0.5 and vira < 0.01: y += 2 * math.sin(t * 40 + u * 9) * tensa   # vibra esticada
        pts.append((x, y))
    d.line(pts, fill=rgba(cor, a), width=6, joint='curve')
    if vira > 0.6:   # tábuas da ponte
        for i in range(1, 8):
            x, y = pts[i * 5]
            d.line([(x, y - 9), (x, y + 9)], fill=rgba(G, a * (vira - 0.6) / 0.4), width=4)
    return (xe, xd)

P = estilo.playfair
class Desenho(ImageDraw.ImageDraw):
    """Não desenha nada com alfa zero (no RGBA, isso apagaria o que já está embaixo)."""
    def __init__(self, im): super().__init__(im, 'RGBA')
    def text(self, xy, s, fill=None, **kw):
        if fill is not None and len(fill) == 4 and fill[3] < 3: return
        super().text(xy, s, fill=fill, **kw)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = Desenho(cam)
    cena = ap(t, 0.1, 0.6) * (1 - 0.75 * ap(t, FECHO, 0.8))
    d.line([(40, CHAO), (1040, CHAO)], fill=rgba(C, cena), width=4)
    rachadura(d, t, cena)
    corda(d, t, cena)
    br_e = 1.0 - 0.6 * ap(t, PONTE, 1.0)
    br_d = 1.0 - 0.6 * ap(t, PONTE, 1.0)
    ela(d, x_ela(t), CHAO - 6, cena, braco=br_e, lado=1, t=t)
    ele(d, x_ele(t), CHAO - 6, cena, braco=br_d, lado=-1, t=t)
    # gancho
    g = jan(t, 0, 3.6)
    for i, l in enumerate(['Numa briga, quem puxa', 'mais forte ganha?']):
        d.text((W/2, 430 + i * 86), l, font=P(66), fill=rgba(B, g), anchor='mm')
    # falas
    balao(d, (x_ela(t), CHAO - 300), (360, 760), ['Me dá um momento.', 'Mas não vou fugir.'], G, jan(t, 4.6, 8.8))
    balao(d, (x_ele(t), CHAO - 300), (720, 760), ['Não preciso', 'ter razão.'], C, jan(t, 9.8, 13.4))
    balao(d, (x_ela(t) + 10, CHAO - 300), (430, 740), ['Vou te dizer', 'o que eu sinto.'], G, jan(t, 18.4, 21.4) * (1 - 0.75 * ap(t, FECHO, 0.8)), coracao=True)
    # fecho
    d.text((W/2, 330), 'No cabo de guerra,', font=P(64), fill=rgba(B, ap(t, FECHO + 0.4, 0.7)), anchor='mm')
    d.text((W/2, 430), 'se um ganha,', font=P(64), fill=rgba(B, ap(t, FECHO + 1.0, 0.7)), anchor='mm')
    d.text((W/2, 540), 'o relacionamento perde.', font=P(70, True), fill=rgba(G, ap(t, FECHO + 1.8, 0.7)), anchor='mm')
    fs = ap(t, FECHO + 3.2, 0.7)
    for i, l in enumerate(['“O maior remédio', 'para a raiva é a demora.”']):
        d.text((W/2, 1560 + i * 56), l, font=P(44, True), fill=rgba(B, fs), anchor='mm')
    d.text((W/2, 1690), 'Sêneca, Sobre a ira, 3.12.4', font=P(30, True), fill=rgba(C, fs), anchor='mm')
    im = Image.alpha_composite(fundo, cam).convert('RGB')
    ff.stdin.write(estilo.para_bytes(np.asarray(im, np.float32) * (1 - ap(t, T - 0.8, 0.8))))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida)
print('ok', saida)
