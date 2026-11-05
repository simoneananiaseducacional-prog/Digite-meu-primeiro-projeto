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
T = 28.5
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

def abelha(d, x, y, a, bate):
    for s in (-1, 1):
        w = el(x + s * 4, y - 30, 14, 22 * (0.6 + 0.4 * abs(math.sin(bate))), s * 0.4)
        d.line(w + [w[0]], fill=rgba(B, a * 0.7), width=2)
    corpo = el(x, y, 38, 24)
    d.polygon(corpo, fill=rgba(G, a * 0.18)); d.line(corpo + [corpo[0]], fill=rgba(G, a), width=4)
    for dx in (-8, 10):
        hh = 24 * math.sqrt(max(0, 1 - (dx / 38) ** 2))
        d.line([(x + dx, y - hh + 2), (x + dx, y + hh - 2)], fill=rgba(G, a), width=5)
    d.ellipse((x + 34, y - 15, x + 60, y + 11), outline=rgba(G, a), width=4)
    d.polygon([(x - 38, y - 6), (x - 38, y + 6), (x - 56, y)], fill=rgba(G, a))

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

def voo1(t):  # caminho da borboleta antes do choque
    x = lerp(-80, 560, cl(t / 5.4)); return x, 1000 + 34 * math.sin(t * 2.4)

def txt(d, y, s, f, cor, a):
    if a > 0.01: d.text((W/2, y), s, font=f, fill=rgba(cor, a), anchor='mm')
F1, F2, F3 = estilo.serifa(58, 600), estilo.serifa_italica(56, 600), estilo.serifa_italica(32, 500)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    img = Image.fromarray(fundo).convert('RGBA'); cam = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
    cena = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(cena)
    d.line([(90, CHAO + 40), (990, CHAO + 40)], fill=rgba(C, 0.35 * ap(t, 0.2)), width=2)
    flor(d, 860, ap(t, 0.3, 0.8))
    # pedrinhas que o besouro atropela na cena 4
    for px in PEDRAS:
        bx = lerp(-120, 1200, cl((t - 12.3) / 2.6))
        pulo = 0
        if 12.3 < t < 15.2 and abs(bx - px) < 50: pulo = 30 * (1 - abs(bx - px) / 50)
        d.ellipse((px - 7, CHAO + 26 - pulo, px + 7, CHAO + 40 - pulo), fill=rgba(C, 0.6 * ap(t, 11.8)))
    # fio do casulo
    if t < 5.4:
        pts = [voo1(t - i * 0.08) for i in range(18)]
        pts = [(px - 8, py + 34 + i * 2) for i, (px, py) in enumerate(pts)]
        d.line(pts, fill=rgba(G, 0.8 * ap(t, 0.3)), width=2)
        ex, ey = pts[-1]; c = el(ex, ey + 10, 9, 15)
        d.line(c + [c[0]], fill=rgba(G, 0.8 * ap(t, 0.3)), width=2)
    else:
        q = cl((t - 5.4) / 0.8)
        n = max(2, int(len(EMBOLO) * q))
        d.line(EMBOLO[:n], fill=rgba(G, 0.8), width=2)
        c = el(EMBOLO[n - 1][0] + 6, EMBOLO[n - 1][1], 9, 15)
        d.line(c + [c[0]], fill=rgba(G, 0.8), width=2)
    # borboleta
    bate = abs(math.sin(t * 9))
    if t < 5.4:
        x, y = voo1(t); borboleta(d, x, y, 0.35 + 0.65 * bate, ap(t, 0.2))
    elif t < 21.4:
        q = cl((t - 5.4) / 0.7)
        x = lerp(560, 380, q); y = lerp(1000, CHAO - 10, q * q)
        borboleta(d, x, y, lerp(0.5, 0.25, q), 1, rot=lerp(0, 1.2, q) + 0.05 * math.sin(t * 2), cor=B if t < 6 else (200, 200, 200))
    else:
        q = cl((t - 21.4) / 5.0)
        x = lerp(380, 1150, q ** 1.6); y = lerp(CHAO - 10, 800, q) + 30 * math.sin(t * 2.6) * q
        borboleta(d, x, y, 0.35 + 0.65 * bate * cl(q * 4), 1 - ap(t, 27.6, 0.6), rot=lerp(1.2, 0, cl(q * 3)))
    # besouro
    if 4.5 < t < 7.2:
        x = lerp(1200, -150, (t - 4.5) / 2.7); besouro(d, x, CHAO - 2, 1, t * 22)
    if 12.3 < t < 15.2:
        x = lerp(-120, 1200, (t - 12.3) / 2.6); besouro(d, x, CHAO - 2, 0.9, t * 22, s=0.8, dirx=1)
    if t > 17.2:
        if t < 18.6:
            x = lerp(1200, 740, (t - 17.2) / 1.4); besouro(d, x, CHAO - 2, 1, t * 22)
        else:
            q = cl((t - 18.6) / 0.5)
            x = lerp(740, 800, q); y = CHAO - 2 - 60 * math.sin(q * math.pi)
            besouro(d, x, y, 1 - ap(t, 27.6, 0.6), t * (14 if q >= 1 else 22), virado=q)
    # abelha
    if t > 12.0:
        if t < 16.2:
            q = cl((t - 12.0) / 1.2); x = lerp(1150, 600, q); y = lerp(700, 860, q) + 12 * math.sin(t * 3)
        elif t < 21.4:
            q = cl((t - 16.2) / 1.0); x = 500; y = lerp(860, CHAO - 26, q * q)
        else:
            q = cl((t - 21.4) / 1.4); x = lerp(500, 845, q); y = lerp(CHAO - 26, 852, q) + 6 * math.sin(t * 3) * q
        abelha(d, x, y, ap(t, 12.0) * (1 - ap(t, 27.6, 0.6)), t * 30)
    K, CX, CY = 1.35, 540, 1100
    cena = cena.transform(img.size, Image.AFFINE, (1/K, 0, CX - CX/K, 0, 1/K, CY - CY/K), resample=Image.BICUBIC)
    cam = Image.alpha_composite(cam, cena); d = ImageDraw.Draw(cam)
    # textos
    txt(d, 470, 'Ela só seguia', F1, B, jan(t, 0.4, 4.4)); txt(d, 545, 'o próprio caminho.', F2, G, jan(t, 0.8, 4.4))
    txt(d, 470, 'Até que alguém', F1, B, jan(t, 4.5, 8.2)); txt(d, 545, 'passou por cima.', F2, VERM, jan(t, 4.9, 8.2))
    txt(d, 505, '“Por que ele fez isso comigo?”', F2, B, jan(t, 8.4, 12.2))
    txt(d, 470, 'Não era sobre você.', F1, B, jan(t, 12.4, 16.2)); txt(d, 545, 'Era sobre a pressa dele.', F2, G, jan(t, 13.4, 16.2))
    txt(d, 470, '“Quem erra,', F2, G, jan(t, 16.4, 21.3)); txt(d, 545, 'erra contra si mesmo.”', F2, G, jan(t, 16.9, 21.3))
    txt(d, 615, 'Marco Aurélio, Meditações, 9.4', F3, C, jan(t, 17.4, 21.3))
    txt(d, 470, '“A melhor vingança é não se', F2, G, jan(t, 21.4, 25.0)); txt(d, 545, 'tornar igual a quem te feriu.”', F2, G, jan(t, 21.6, 25.0))
    txt(d, 615, 'Marco Aurélio, Meditações, 6.6', F3, C, jan(t, 22.0, 25.0))
    txt(d, 470, 'Cuide da sua vida.', F1, B, ap(t, 25.1)); txt(d, 545, 'Faça o seu mel.', F2, G, ap(t, 25.6))
    if ap(t, 26.0) > 0:
        estilo.texto_espacado(d, (W/2, 1330), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(22, 500), rgba(C, ap(t, 26.0)), 6)
    img = Image.alpha_composite(img, cam)
    q = np.asarray(img.convert('RGB'), np.float32) * (1 - ap(t, T - 0.6, 0.6))
    ff.stdin.write(estilo.para_bytes(q))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); saida.with_suffix('.mudo.mp4').unlink(missing_ok=True)
print('ok')
