"""Rabisco que vira lótus: uma linha desenha laços que parecem caos (pétalas em ordem embaralhada pelo
ângulo de ouro); no fim formam uma flor-mandala que fica dourada. Fé e ordem (Logos): Marco Aurélio, Meditações 4.10.
Formato inspirado em @marcela.santosmentora (desenho próprio). Uso: python3 rabisco_lotus.py saida.mp4
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
W, H, FPS, T = 1080, 1920, 30, 25.0
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
TX = (215, 210, 202)
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.6): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.6): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
def rgba(c, a): return c + (int(255 * cl(a)),)
def mix(a, b, p): return tuple(int(a[i] + (b[i] - a[i]) * p) for i in range(3))

CX, CY = 540, 1020
BX, BY = 540, 1230          # base do lótus
def petala(ang, L, Wd, n=120):
    """Pétala de lótus (ponta fina) saindo da base, inclinada em ang (0 = para cima)."""
    lado1, lado2 = [], []
    for k in range(n // 2 + 1):
        u = k / (n // 2)
        meia = Wd * math.sin(math.pi * u) ** 0.9 * (1 - 0.45 * u)
        lado1.append((meia, -L * u)); lado2.append((-meia, -L * u))
    pts = lado1 + lado2[::-1]
    ca, sa = math.cos(ang), math.sin(ang)
    return [(BX + x * ca - y * sa, BY + x * sa + y * ca) for x, y in pts]
CAMADAS = [(11, 78, 380, 95), (9, 56, 330, 92), (7, 36, 290, 85), (5, 16, 250, 75)]   # (qtd, abertura em graus, comprimento, largura)
PET = []
for qtd, ab, L, Wd in CAMADAS:
    for i in range(qtd):
        g = -ab + 2 * ab * i / (qtd - 1)
        PET.append(petala(math.radians(g), L, Wd))
for r_ in (190, 260):     # linhas da água
    PET.append([(BX + r_ * math.cos(math.radians(a_)), BY + 18 + 0.18 * r_ * math.sin(math.radians(a_))) for a_ in range(0, 361, 6)])
N = len(PET)
ORDEM = [(i * 7) % N for i in range(N)] if math.gcd(7, N) == 1 else [(i * 5) % N for i in range(N)]
CAMINHO = [PET[i] for i in ORDEM]
TOT = sum(len(p) for p in CAMINHO)
rng = np.random.default_rng(7)
CAOS = [dict(dx=rng.uniform(-170, 170), dy=rng.uniform(-60, 240), esc=rng.uniform(0.6, 1.35), rot=rng.uniform(-1.6, 1.6),
             amp=rng.uniform(30, 80), fq=rng.uniform(2, 5)) for _ in range(N)]
def deformar(p, j, m):
    """m = 1: caos total; m = 0: pétala perfeita."""
    if m <= 0.001: return p
    c = CAOS[j]; out = []
    for q, (x, y) in enumerate(p):
        u = q / len(p)
        dx, dy = x - CX, y - CY
        ca, sa = math.cos(c['rot'] * m), math.sin(c['rot'] * m)
        e = 1 + (c['esc'] - 1) * m
        nx, ny = (dx * ca - dy * sa) * e, (dx * sa + dy * ca) * e
        w = c['amp'] * m * math.sin(u * math.pi * c['fq'])
        out.append((CX + nx + c['dx'] * m + w, CY + ny + c['dy'] * m + w * 0.6))
    return out
T0, T1 = 0.8, 13.0      # tempo do desenho
fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
saida = Path(sys.argv[1]); ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
F1 = estilo.playfair(62); F2 = estilo.playfair(62, True)
for k in range(int(T * FPS)):
    t = k / FPS
    prog = estilo.suavizar(cl((t - T0) / (T1 - T0))) ** 1.15
    quantos = int(TOT * prog)
    ouro = ap(t, 12.6, 2.0)
    cor = mix((225, 222, 215), G, ouro)
    im = fundo.copy()
    if ouro > 0.02:
        gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl)
        gd.ellipse((CX - 360, CY - 360, CX + 360, CY + 360), fill=G + (int(60 * ouro),))
        im = Image.alpha_composite(im, gl.filter(ImageFilter.GaussianBlur(90)))
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay, 'RGBA')
    resto = quantos; ponta = None
    morph = 1 - ap(t, 9.8, 3.0)
    for j, p0 in enumerate(CAMINHO):
        p = deformar(p0, j, morph)
        if resto <= 1: break
        seg_ = p[:min(len(p), resto)]
        d.line(seg_, fill=rgba(cor, 0.85), width=2, joint='curve')
        ponta = seg_[-1]; resto -= len(p)
    if ponta and prog < 1:
        d.ellipse((ponta[0] - 5, ponta[1] - 5, ponta[0] + 5, ponta[1] + 5), fill=rgba(B, 1))
    if ouro > 0.02:
        pass
    im = Image.alpha_composite(im, lay)
    fim = 1 - 0.75 * ap(t, 15.2, 0.8)
    if fim < 1:
        im = Image.fromarray((np.asarray(im.convert('RGB'), np.float32) * fim + np.asarray(fundo.convert('RGB'), np.float32) * (1 - fim)).astype(np.uint8)).convert('RGBA')
    d2 = ImageDraw.Draw(im, 'RGBA')
    a1 = jan(t, 0.4, 7.4)
    if a1 > 0.02:
        d2.text((W / 2, 330), 'Quando a vida parece', font=F1, fill=rgba(B, a1), anchor='mm')
        d2.text((W / 2, 410), 'um rabisco sem sentido…', font=F1, fill=rgba(B, a1), anchor='mm')
    a2 = jan(t, 7.8, 15.0)
    if a2 > 0.02:
        for i, l in enumerate(['talvez ela só esteja desenhando', 'algo que você ainda', 'não consegue ver.']):
            d2.text((W / 2, 300 + i * 76), l, font=F2 if i == 2 else F1, fill=rgba(G if i == 2 else B, a2), anchor='mm')
    a3 = jan(t, 15.6, 24.6)
    if a3 > 0.02:
        d2.text((W / 2, 820), 'Confie no processo.', font=estilo.playfair(68), fill=rgba(B, a3), anchor='mm')
        a4 = jan(t, 16.8, 24.6)
        d2.text((W / 2, 930), 'Deus e o tempo', font=estilo.playfair(68, True), fill=rgba(G, a4), anchor='mm')
        d2.text((W / 2, 1015), 'sabem o que fazem.', font=estilo.playfair(68, True), fill=rgba(G, a4), anchor='mm')
        a5 = jan(t, 18.6, 24.6)
        d2.text((W / 2, 1200), 'Leia a legenda.', font=estilo.sem_serifa(34, 500), fill=rgba(TX, a5), anchor='mm')
    estilo.texto_espacado(d2, (W / 2, 1640), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(24, 500), rgba((170, 165, 158), 0.8 * ap(t, 0.1)), 6)
    ff.stdin.write(estilo.para_bytes(np.asarray(im.convert('RGB'), np.float32) * (1 - ap(t, T - 0.4, 0.4))))
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); print('ok', saida)
