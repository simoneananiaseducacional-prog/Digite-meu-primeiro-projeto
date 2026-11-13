"""Cabo de guerra (v2, mais concreto): a briga real ("Você nunca me escuta!"), os dois inclinados puxando,
o chão racha. Ela pausa sem largar, ele solta a razão, a corda vira ponte e ela diz o que sente.
Cena com zoom (bonecos grandes). Inspiração das frases: @linguagemcorporaldominante.
Base: John Gottman (pausa, aceitar influência); Sêneca, Sobre a ira 3.12.4.
Uso: python3 cabo_guerra.py saida.mp4
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
P = estilo.playfair

class Desenho(ImageDraw.ImageDraw):
    """RGBA que mistura; texto com alfa zero não é desenhado (apagaria o que está embaixo)."""
    def __init__(self, im): super().__init__(im, 'RGBA')
    def text(self, xy, s, fill=None, **kw):
        if fill is not None and len(fill) == 4 and fill[3] < 3: return
        super().text(xy, s, fill=fill, **kw)

T = 29.5
CHAO = 1250
K, CX, CY = 1.55, 540, 1150            # zoom da cena
def tela(x, y): return ((x - CX) * K + CX, (y - CY) * K + CY)

# linha do tempo
BRIGA_E, BRIGA_D = 2.9, 4.7
PAUSA_DELA, SOLTA_ELE, PONTE, ATRAVESSA, FECHO = 7.2, 11.4, 14.6, 16.4, 22.2
def puxando(t, quem):
    return 1 - ap(t, PAUSA_DELA if quem == 'ela' else SOLTA_ELE, 0.8)
def x_ela(t):
    base = 330 - 8 * abs(math.sin(t * 6)) * puxando(t, 'ela')
    return lerp(base, 495, estilo.suavizar(cl((t - ATRAVESSA) / 3.2)))
def x_ele(t):
    base = 750 + 8 * abs(math.sin(t * 6 + 1)) * puxando(t, 'ele')
    return lerp(base, 600, estilo.suavizar(cl((t - ATRAVESSA - 0.5) / 3.0)))
def inclina(t, quem): return 13 * puxando(t, quem) * ap(t, 0.3, 0.8)   # graus, para trás
def gira(px, py, ox, oy, graus):
    th = math.radians(graus); dx, dy = px - ox, py - oy
    return ox + dx * math.cos(th) + dy * math.sin(th), oy - dx * math.sin(th) + dy * math.cos(th)

def abertura(t): return 30 + 110 * ap(t, 0.8, 5.0)
def rachadura(d, t, a):
    ab = abertura(t)
    pe = [(540 - ab / 2 + dx, CHAO + y) for dx, y in [(0, 0), (-14, 70), (10, 140), (-8, 220), (0, 320)]]
    pd = [(540 + ab / 2 + dx, CHAO + y) for dx, y in [(0, 0), (14, 70), (-6, 140), (12, 220), (0, 320)]]
    d.polygon(pe + pd[::-1], fill=(4, 4, 4, int(255 * a)))
    d.line(pe, fill=rgba(C, a), width=4); d.line(pd, fill=rgba(C, a), width=4)

def maos(t):
    xe, xd = x_ela(t), x_ele(t)
    be, bd = braco(t)
    me = (xe + (40 + 110 * be), CHAO - 6 - 240 + 72 - 22 * be)
    md = (xd - (40 + 110 * bd), CHAO - 6 - 240 + 72 - 22 * bd)
    return gira(*me, xe, CHAO - 6, inclina(t, 'ela')), gira(*md, xd, CHAO - 6, -inclina(t, 'ele'))
def braco(t):
    v = 1.0 - 0.7 * ap(t, PONTE, 1.0)
    return v, v
def corda(d, t, a):
    me, md = maos(t)
    vira = ap(t, PONTE, 1.6)
    ab = abertura(t)
    p0 = (lerp(me[0], 540 - ab / 2 - 40, vira), lerp(me[1], CHAO, vira))
    p1 = (lerp(md[0], 540 + ab / 2 + 40, vira), lerp(md[1], CHAO, vira))
    tensa = max(puxando(t, 'ela'), puxando(t, 'ele'))
    sag = lerp(lerp(60, 4, tensa), 14, vira)
    cor = tuple(int(lerp(B[i], G[i], vira)) for i in range(3))
    pts = []
    for i in range(41):
        u = i / 40
        y = lerp(p0[1], p1[1], u) + sag * 4 * u * (1 - u)
        if vira < 0.01: y += 3 * math.sin(t * 38 + u * 10) * tensa
        pts.append((lerp(p0[0], p1[0], u), y))
    d.line(pts, fill=rgba(cor, a), width=9, joint='curve')
    if vira < 0.5:   # trançado da corda
        for i in range(2, 39, 3):
            x, y = pts[i]
            d.line([(x - 4, y - 4), (x + 4, y + 4)], fill=rgba((40, 38, 36), a), width=2)
    if vira > 0.6:   # tábuas da ponte
        for i in range(2, 40, 4):
            x, y = pts[i]
            d.line([(x, y - 12), (x, y + 12)], fill=rgba(G, a * (vira - 0.6) / 0.4), width=5)

def figura(t, quem, a):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(lay, 'RGBA')
    x = x_ela(t) if quem == 'ela' else x_ele(t)
    br = braco(t)[0]
    if quem == 'ela': ela(dd, x, CHAO - 6, a, braco=br, lado=1, t=t)
    else: ele(dd, x, CHAO - 6, a, braco=br, lado=-1, t=t)
    g = inclina(t, quem) * (1 if quem == 'ela' else -1)
    return lay.rotate(g, resample=Image.BICUBIC, center=(x, CHAO - 6)) if abs(g) > 0.2 else lay

def balao(d, alvo, centro, linhas, cor, a, coracao=False):
    if a <= 0.01: return
    f = estilo.sem_serifa(46, 700)
    larg = max(d.textlength(l, font=f) for l in linhas) + 80
    alt = 62 * len(linhas) + 50 + (66 if coracao else 0)
    x0, y0 = centro[0] - larg / 2, centro[1] - alt / 2
    d.rounded_rectangle((x0, y0, x0 + larg, y0 + alt), radius=34, fill=(14, 14, 14, int(240 * a)), outline=rgba(cor, a), width=4)
    bx = max(x0 + 44, min(x0 + larg - 44, alvo[0])); base = y0 + alt
    d.polygon([(bx - 18, base - 2), (bx + 18, base - 2), alvo], fill=(14, 14, 14, int(240 * a)))
    d.line([(bx - 18, base), alvo, (bx + 18, base)], fill=rgba(cor, a), width=4)
    for i, l in enumerate(linhas):
        d.text((centro[0], y0 + 56 + i * 62), l, font=f, fill=rgba(B, a), anchor='mm')
    if coracao:
        cx, cy, r = centro[0], y0 + alt - 58, 16
        d.ellipse((cx - 2 * r, cy - r, cx, cy + r), fill=rgba(G, a)); d.ellipse((cx, cy - r, cx + 2 * r, cy + r), fill=rgba(G, a))
        d.polygon([(cx - 2 * r + 1, cy + 3), (cx + 2 * r - 1, cy + 3), (cx, cy + 2.6 * r)], fill=rgba(G, a))

ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    cena_a = ap(t, 0.1, 0.6) * (1 - 0.8 * ap(t, FECHO, 0.8))
    # cena em coordenadas próprias, depois ampliada
    cen = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = Desenho(cen)
    d.line([(0, CHAO), (W, CHAO)], fill=rgba(C, cena_a), width=4)
    rachadura(d, t, cena_a)
    corda(d, t, cena_a)
    cen = Image.alpha_composite(cen, figura(t, 'ela', cena_a))
    cen = Image.alpha_composite(cen, figura(t, 'ele', cena_a))
    big = cen.resize((int(W * K), int(H * K)), Image.BICUBIC)
    ox, oy = int(CX - CX * K), int(CY - CY * K)
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.paste(big, (ox, oy))
    d = Desenho(cam)
    # gancho
    g = jan(t, 0, 2.9)
    for i, l in enumerate(['Numa briga, quem puxa', 'mais forte ganha?']):
        d.text((W/2, 380 + i * 86), l, font=P(68), fill=rgba(B, g), anchor='mm')
    cab_e = tela(x_ela(t) - 30, CHAO - 300); cab_d = tela(x_ele(t) + 30, CHAO - 300)
    # a briga
    balao(d, cab_e, (330, 560), ['Você nunca', 'me escuta!'], B, jan(t, BRIGA_E, BRIGA_E + 2.2))
    balao(d, cab_d, (750, 560), ['Você que', 'exagera!'], C, jan(t, BRIGA_D, BRIGA_D + 2.2))
    # os gestos
    balao(d, cab_e, (380, 520), ['Me dá um momento.', 'Mas não vou fugir.'], G, jan(t, PAUSA_DELA + 0.4, SOLTA_ELE - 0.2))
    balao(d, cab_d, (720, 540), ['Não preciso', 'ter razão.'], C, jan(t, SOLTA_ELE + 0.4, PONTE + 0.2))
    balao(d, tela(x_ela(t), CHAO - 300), (470, 520), ['Vou te dizer', 'o que eu sinto.'], G,
          jan(t, ATRAVESSA + 2.8, FECHO + 0.3) * (1 - 0.8 * ap(t, FECHO, 0.8)), coracao=True)
    # fecho
    d.text((W/2, 300), 'No cabo de guerra,', font=P(66), fill=rgba(B, ap(t, FECHO + 0.4, 0.7)), anchor='mm')
    d.text((W/2, 400), 'se um ganha,', font=P(66), fill=rgba(B, ap(t, FECHO + 1.0, 0.7)), anchor='mm')
    d.text((W/2, 515), 'o relacionamento perde.', font=P(72, True), fill=rgba(G, ap(t, FECHO + 1.8, 0.7)), anchor='mm')
    fs = ap(t, FECHO + 3.4, 0.7)
    for i, l in enumerate(['“O maior remédio', 'para a raiva é a demora.”']):
        d.text((W/2, 1640 + i * 56), l, font=P(44, True), fill=rgba(B, fs), anchor='mm')
    d.text((W/2, 1770), 'Sêneca, Sobre a ira, 3.12.4', font=P(30, True), fill=rgba(C, fs), anchor='mm')
    im = Image.alpha_composite(fundo, cam).convert('RGB')
    ff.stdin.write(estilo.para_bytes(np.asarray(im, np.float32) * (1 - ap(t, T - 0.8, 0.8))))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida)
print('ok', saida)
