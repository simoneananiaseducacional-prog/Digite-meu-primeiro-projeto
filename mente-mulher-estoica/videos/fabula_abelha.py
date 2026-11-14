"""Fábula: a borboleta, o besouro e a abelha estoica. Identidade dos Mapas da mente.
Uso: python3 fabula_abelha.py saida.mp4  (vídeo mudo; a música entra no Instagram)
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
VERM = (190, 60, 60)
saida = Path(sys.argv[1])
fundo = np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)
CHAO = 1150
def ap(t, t0, d=0.4): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1): return ap(t, t0) * (1 - ap(t, t1 - 0.3, 0.3))
def lerp(a, b, p): return a + (b - a) * p
def cl(p): return max(0.0, min(1.0, p))
def el(cx, cy, rx, ry, ang=0, n=40):
    ca, sa = math.cos(ang), math.sin(ang)
    return [(cx + rx * math.cos(k * 2 * math.pi / n) * ca - ry * math.sin(k * 2 * math.pi / n) * sa,
             cy + rx * math.cos(k * 2 * math.pi / n) * sa + ry * math.sin(k * 2 * math.pi / n) * ca) for k in range(n)]
def rgba(c, a): return c + (int(255 * cl(a)),)

def borboleta(d, x, y, abre, a, rot=0, cor=B):
    """abre: 1 asas abertas, 0.2 fechadas."""
    ca, sa = math.cos(rot), math.sin(rot)
    def R(px, py): return (x + px * ca - py * sa, y + px * sa + py * ca)
    for s in (-1, 1):
        sup = [R(px, py) for px, py in el(s * 34 * abre, -18, 34 * abre, 26, s * -0.5)]
        inf = [R(px, py) for px, py in el(s * 24 * abre, 18, 22 * abre, 17, s * 0.5)]
        d.line(sup + [sup[0]], fill=rgba(cor, a), width=3)
        d.line(inf + [inf[0]], fill=rgba(cor, a), width=3)
        d.line([R(0, -26), R(s * 14, -46)], fill=rgba(cor, a), width=2)
    d.line([R(0, -26), R(0, 30)], fill=rgba(cor, a), width=5)

def abelha(d, x, y, a, bate, dirx=1):
    """dirx=1 cabeça à direita; dirx=-1 cabeça à esquerda (ferrão para a direita)."""
    for sd in (-1, 1):
        w = el(x + sd * 4, y - 30, 14, 22 * (0.6 + 0.4 * abs(math.sin(bate))), sd * 0.4)
        d.line(w + [w[0]], fill=rgba(B, a * 0.7), width=2)
    corpo = el(x, y, 38, 24)
    d.polygon(corpo, fill=rgba(G, a * 0.18)); d.line(corpo + [corpo[0]], fill=rgba(G, a), width=4)
    for dx in (-8, 10):
        dx *= dirx
        hh = 24 * math.sqrt(max(0, 1 - (dx / 38) ** 2))
        d.line([(x + dx, y - hh + 2), (x + dx, y + hh - 2)], fill=rgba(G, a), width=5)
    hx = x + dirx * 47
    d.ellipse((hx - 13, y - 13, hx + 13, y + 13), outline=rgba(G, a), width=4)
    d.polygon([(x - dirx * 38, y - 7), (x - dirx * 38, y + 7), (x - dirx * 60, y)], fill=rgba(G, a))

def besouro(d, x, y, a, passo, s=1.0, virado=0.0, dirx=-1):
    """virado: 0 de pé, 1 de patas para cima."""
    cor = VERM
    fy = 1 - 2 * virado
    for i, dx in enumerate((-18, 0, 18)):
        mexe = math.sin(passo + i * 2.1) * 8
        for sd in (-1, 1):
            d.line([(x + dx * s, y), (x + (dx + mexe * sd) * s, y + 34 * s * fy)], fill=rgba(cor, a), width=3)
    corpo = el(x, y - 6 * fy * s, 40 * s, 26 * s)
    d.polygon(corpo, fill=rgba((60, 22, 22), a)); d.line(corpo + [corpo[0]], fill=rgba(cor, a), width=4)
    d.line([(x, y - 30 * fy * s), (x, y + 18 * fy * s)], fill=rgba(cor, a), width=2)
    hx = x + dirx * 46 * s
    d.ellipse((hx - 13 * s, y - 13 * s, hx + 13 * s, y + 13 * s), outline=rgba(cor, a), width=4)

def flor(d, x, a):
    d.line([(x, CHAO), (x, 930)], fill=rgba(C, a), width=3)
    d.line([(x, 1040), (x + 26, 1010)], fill=rgba(C, a), width=3)
    for k in range(6):
        ang = k * math.pi / 3
        p = el(x + 24 * math.cos(ang), 910 + 24 * math.sin(ang), 18, 11, ang)
        d.line(p + [p[0]], fill=rgba(G, a), width=3)
    d.ellipse((x - 9, 901, x + 9, 919), fill=rgba(G, a))

rng = np.random.default_rng(7)
EMBOLO = [(720 + 40 * math.sin(k * 0.9) * math.cos(k * 0.37), CHAO - 14 + 10 * math.sin(k * 1.7)) for k in range(26)]
PEDRAS = [260, 420, 760]

T = 30.0
T_CHOQUE = 5.2
def voo1(t):  # caminho da borboleta antes do choque
    x = lerp(-80, 560, cl(t / T_CHOQUE)); return x, 1000 + 34 * math.sin(t * 2.0)
K, CX, CY = 1.35, 540, 1100
def tela(x, y): return ((x - CX) * K + CX, (y - CY) * K + CY)
def txt(d, y, s, f, cor, a):
    if a > 0.01: d.text((W/2, y), s, font=f, fill=rgba(cor, a), anchor='mm')
def balao(d, alvo, centro, linhas, cor, a):
    """Balão de fala com rabinho apontando para quem fala."""
    if a <= 0.01: return
    f = estilo.sem_serifa(40, 600)
    larg = max(d.textlength(l, font=f) for l in linhas) + 70
    alt = 56 * len(linhas) + 44
    x0, y0 = centro[0] - larg / 2, centro[1] - alt / 2
    d.rounded_rectangle((x0, y0, x0 + larg, y0 + alt), radius=30, fill=(14, 14, 14, int(235 * a)), outline=rgba(cor, a), width=3)
    bx = max(x0 + 40, min(x0 + larg - 40, alvo[0]))
    base = y0 + alt
    d.polygon([(bx - 16, base - 2), (bx + 16, base - 2), (alvo[0], alvo[1])], fill=(14, 14, 14, int(235 * a)))
    d.line([(bx - 16, base), (alvo[0], alvo[1]), (bx + 16, base)], fill=rgba(cor, a), width=3)
    for i, l in enumerate(linhas):
        d.text((centro[0], y0 + 22 + 28 + i * 56), l, font=f, fill=rgba(B, a), anchor='mm')
F1, F2, F3 = estilo.serifa(64, 700), estilo.serifa_italica(62, 700), estilo.serifa_italica(34, 600)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    img = Image.fromarray(fundo).convert('RGBA'); cam = Image.new('RGBA', img.size, (0, 0, 0, 0))
    cena = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(cena)
    d.line([(90, CHAO + 40), (990, CHAO + 40)], fill=rgba(C, 0.35 * ap(t, 0.2)), width=2)
    flor(d, 860, ap(t, 0.3, 0.8))
    # cena: o besouro passa atropelando as pedrinhas
    PASSA0, PASSA1 = 10.4, 12.2
    bx = lerp(-120, 1200, cl((t - PASSA0) / (PASSA1 - PASSA0)))
    for px in PEDRAS:
        pulo = 30 * (1 - abs(bx - px) / 50) if (PASSA0 < t < PASSA1 + 0.2 and abs(bx - px) < 50) else 0
        d.ellipse((px - 7, CHAO + 26 - pulo, px + 7, CHAO + 40 - pulo), fill=rgba(C, 0.6 * ap(t, 10.0)))
    # fio do casulo
    if t < T_CHOQUE:
        pts = [voo1(t - i * 0.08) for i in range(18)]
        pts = [(px - 8, py + 34 + i * 2) for i, (px, py) in enumerate(pts)]
        d.line(pts, fill=rgba(G, 0.8 * ap(t, 0.3)), width=2)
        ex, ey = pts[-1]; c = el(ex, ey + 10, 9, 15)
        d.line(c + [c[0]], fill=rgba(G, 0.8 * ap(t, 0.3)), width=2)
    else:
        q = cl((t - T_CHOQUE) / 1.4)
        n = max(2, int(len(EMBOLO) * q))
        d.line(EMBOLO[:n], fill=rgba(G, 0.8), width=2)
        c = el(EMBOLO[n - 1][0] + 6, EMBOLO[n - 1][1], 9, 15)
        d.line(c + [c[0]], fill=rgba(G, 0.8), width=2)
    # impacto do atropelo
    if T_CHOQUE < t < T_CHOQUE + 0.7:
        a = 1 - (t - T_CHOQUE) / 0.7
        for j in range(8):
            ang = j * math.pi / 4
            d.line([(560 + 50 * math.cos(ang), 1010 + 50 * math.sin(ang)), (560 + 80 * math.cos(ang), 1010 + 80 * math.sin(ang))], fill=rgba(VERM, a), width=3)
    # borboleta
    bate = abs(math.sin(t * 7))
    VOA = 25.5
    if t < T_CHOQUE:
        x, y = voo1(t); borboleta(d, x, y, 0.35 + 0.65 * bate, ap(t, 0.2))
    elif t < VOA:
        q = cl((t - T_CHOQUE) / 1.4)
        x = lerp(560, 380, q); y = lerp(1000, CHAO - 10, q * q)
        borboleta(d, x, y, lerp(0.5, 0.25, q), 1, rot=lerp(0, 1.2 + 4 * math.pi, q) if q < 1 else 1.2, cor=B if q < 1 else (200, 200, 200))
    else:
        q = cl((t - VOA) / 1.4); x = lerp(380, 300, q); y = lerp(CHAO - 10, 860, q) + 22 * math.sin(t * 2.6) * q
        borboleta(d, x, y, 0.35 + 0.65 * bate * cl(q * 4), 1 - ap(t, T - 0.8, 0.6), rot=lerp(1.2, 0, cl(q * 3)))
    # besouro
    if 3.2 < t < 7.4:
        x = lerp(1200, -150, (t - 3.2) / 4.2); besouro(d, x, CHAO - 2, 1, t * 16)
    if PASSA0 < t < PASSA1:
        besouro(d, bx, CHAO - 2, 0.9, t * 22, s=0.8, dirx=1)
    ABX = 540                       # onde a abelha pousa, ferrão para a direita
    PONTA = ABX + 60
    CORRE, BATE = 19.7, 21.1
    if t > CORRE:
        if t < BATE:
            x = lerp(1200, PONTA + 59, cl((t - CORRE) / (BATE - CORRE)) ** 1.3); besouro(d, x, CHAO - 2, 1, t * 20)
        else:
            q = cl((t - BATE) / 1.1)
            x = lerp(PONTA + 59, 800, q); y = CHAO - 2 - 90 * math.sin(q * math.pi)
            besouro(d, x, y, 1 - ap(t, T - 0.8, 0.6), t * (10 if q >= 1 else 16), virado=q)
    if BATE < t < BATE + 0.8:
        a = 1 - (t - BATE) / 0.8
        for j in range(8):
            ang = j * math.pi / 4
            d.line([(PONTA + 30 * math.cos(ang), CHAO - 26 + 30 * math.sin(ang)), (PONTA + 60 * math.cos(ang), CHAO - 26 + 60 * math.sin(ang))], fill=rgba(G, a), width=3)
    # abelha
    if t > 9.6:
        if t < 15.6:
            q = cl((t - 9.6) / 0.9); x = lerp(1150, 600, q); y = lerp(700, 900, q) + 10 * math.sin(t * 3); dx = -1
        elif t < VOA:
            q = cl((t - 15.6) / 0.9); x = lerp(600, ABX, q); y = lerp(900, CHAO - 26, q * q); dx = -1
        else:
            q = cl((t - VOA) / 1.2); x = lerp(ABX, 845, q); y = lerp(CHAO - 26, 852, q) + 6 * math.sin(t * 3) * q; dx = 1
        abelha(d, x, y, ap(t, 9.6) * (1 - ap(t, T - 0.8, 0.6)), t * 30, dx)
    cena = cena.transform(img.size, Image.AFFINE, (1/K, 0, CX - CX/K, 0, 1/K, CY - CY/K), resample=Image.BICUBIC)
    cam = Image.alpha_composite(cam, cena); d = ImageDraw.Draw(cam)
    # narradora (topo) e falas (balões)
    txt(d, 470, 'Ela só seguia', F1, B, jan(t, 0.4, 3.4)); txt(d, 545, 'o próprio caminho.', F2, G, jan(t, 0.8, 3.4))
    balao(d, tela(380, CHAO - 50), (400, 930), ['Por que ele fez', 'isso comigo?'], B, jan(t, 6.8, 9.6))
    balao(d, tela(600, 870), (560, 660), ['Não era sobre você.', 'Era sobre a pressa dele.'], G, jan(t, 12.3, 15.5))
    balao(d, tela(ABX, CHAO - 60), (560, 930), ['Não vou atacar.', 'Só não saio do meu lugar.'], G, jan(t, 16.6, 19.6))
    txt(d, 470, '“Quem erra,', F2, G, jan(t, 22.3, 25.5)); txt(d, 548, 'erra contra si mesmo.”', F2, G, jan(t, 22.7, 25.5))
    txt(d, 620, 'Marco Aurélio, Meditações, 9.4', F3, C, jan(t, 23.1, 25.5))
    fim = 1 - ap(t, T - 0.8, 0.6)
    txt(d, 470, 'Seja leve como a borboleta', F1, B, ap(t, 26.8) * fim)
    txt(d, 550, 'e firme como a abelha.', F2, G, ap(t, 27.3) * fim)
    if ap(t, 27.6) > 0:
        estilo.texto_espacado(d, (W/2, 1400), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(22, 500), rgba(C, ap(t, 27.6) * fim), 6)
    img = Image.alpha_composite(img, cam)
    q = np.asarray(img.convert('RGB'), np.float32) * (1 - ap(t, T - 0.6, 0.6))
    ff.stdin.write(estilo.para_bytes(q))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); saida.with_suffix('.mudo.mp4').unlink(missing_ok=True)
print('ok')
