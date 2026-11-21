"""Série A borracha, Parte 2: A flor (vínculo traumático / reforço intermitente).
Depois de cada apagão vem uma flor. Ela guarda as flores e vai se apagando, esperando o começo voltar.
Base: Dutton & Painter 1993 (apego por maus-tratos intermitentes). Cartão final de série (aprendizado 027).
Uso: python3 flor.py saida.mp4
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from personagens import ela, ele
from continua import cartao
from PIL import Image, ImageDraw
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
TXT = (200, 196, 190)
saida = Path(sys.argv[1])
fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1): return ap(t, t0) * (1 - ap(t, t1 - 0.5, 0.5))
def rgba(c, a): return c + (int(255 * cl(a)),)
def lerp(a, b, p): return a + (b - a) * p
def pulso(t, t0, t1, s=0.35): return ap(t, t0, s) * (1 - ap(t, t1 - s, s))
def seg(t, t0, t1): return estilo.suavizar(cl((t - t0) / (t1 - t0)))

class Desenho(ImageDraw.ImageDraw):
    def __init__(self, im): super().__init__(im, 'RGBA')
    def text(self, xy, s, fill=None, **kw):
        if fill is not None and len(fill) == 4 and fill[3] < 3: return
        super().text(xy, s, fill=fill, **kw)

T = 26.5
CHAO = 1250
K, CX, CY = 1.6, 540, 1120
XE = 380
FIM = 19.2
FRASES = [(0.4, 6.4, ['Depois de cada apagão,']), (3.4, 6.4, [None, 'vinha uma flor.']),
          (6.6, 13.6, ['E ela guardava as flores.']),
          (13.8, 19.0, ['Esperando voltar', 'quem ele era no começo.'])]
# ciclos: (apaga_ini, apaga_fim, centro do apagão, entrega_ini, entrega_fim)
CICLOS = [(1.4, 2.8, (470, 1052), 3.4, 4.8),
          (6.8, 7.8, (372, 1205), 8.0, 9.0),
          (9.6, 10.4, (410, 1120), 10.5, 11.3),
          (11.8, 12.4, (350, 1060), 12.5, 13.1)]
def borracha_pos(t):
    for a0, a1, (cx, cy), *_ in CICLOS:
        if a0 <= t <= a1:
            u = (t - a0) / (a1 - a0)
            return (cx + 34 * math.sin(u * 2 * math.pi * 2), cy + 14 * math.sin(u * 2 * math.pi * 1.3))
    return None
def x_ele(t):
    x = 720
    for a0, a1, (cx, cy), e0, e1 in CICLOS:
        x = lerp(x, cx + 175, pulso(t, a0 - 0.5, a1 + 0.2, 0.4))
        x = lerp(x, 600, pulso(t, e0 - 0.3, e1 + 0.2, 0.4))
    return x
def braco_ele(t):
    v = 0.0
    for a0, a1, _, e0, e1 in CICLOS: v = max(v, pulso(t, a0 - 0.2, a1 + 0.1, 0.25), pulso(t, e0, e1, 0.3))
    return v
MAO_ELA = (XE + 40 + 66, CHAO - 6 - 240 + 72 - 13)
def flores_dela(t):
    """Flores já guardadas e a que está sendo entregue."""
    lista = []
    for i, (a0, a1, _, e0, e1) in enumerate(CICLOS):
        dx, dy = [(0, 0), (-22, -18), (20, -24), (-4, -40)][i]
        alvo = (MAO_ELA[0] + dx, MAO_ELA[1] + dy)
        if t < e0: continue
        if t < e1:
            mao_ele = (x_ele(t) - 150, CHAO - 6 - 240 + 50)
            p = seg(t, e0 + 0.2, e1)
            lista.append((lerp(mao_ele[0], alvo[0], p), lerp(mao_ele[1], alvo[1], p)))
        else: lista.append(alvo)
    return lista
def flor(d, p, a):
    x, y = p
    d.line([(x, y), (x - 6, y + 66)], fill=rgba(C, a), width=4)
    for k in range(5):
        ang = k * 2 * math.pi / 5 - math.pi / 2
        px, py = x + 15 * math.cos(ang), y + 15 * math.sin(ang)
        d.ellipse((px - 11, py - 11, px + 11, py + 11), fill=rgba(G, a))
    d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=rgba(B, a))

MASK = np.ones((H, W), np.float32)
yy, xx = np.mgrid[0:H, 0:W]
def apagar_em(p, r=20):
    x0, x1 = int(max(p[0] - r, 0)), int(min(p[0] + r, W)); y0, y1 = int(max(p[1] - r, 0)), int(min(p[1] + r, H))
    sub = (xx[y0:y1, x0:x1] - p[0]) ** 2 + (yy[y0:y1, x0:x1] - p[1]) ** 2 < r * r
    MASK[y0:y1, x0:x1][sub] = 0.0

F = estilo.sem_serifa(56, 500)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    a = ap(t, 0.1, 0.6)
    cena = a * (1 - 0.7 * ap(t, FIM, 0.8))
    bp = borracha_pos(t)
    if bp: apagar_em(bp)
    cen = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = Desenho(cen)
    d.line([(0, CHAO), (W, CHAO)], fill=rgba(C, cena), width=4)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay, 'RGBA')
    tem_flor = t > CICLOS[0][3] + 1.0
    ela(dl, XE, CHAO - 6, 1.0, braco=0.6 if tem_flor else 0.0, lado=1, cabeca_baixa=0.5 * ap(t, 13.8, 1.5), t=t)
    arr = np.asarray(lay).astype(np.float32).copy()
    arr[..., 3] *= MASK * cena * (1 - 0.55 * seg(t, 4.0, 14.0))
    cen = Image.alpha_composite(cen, Image.fromarray(arr.astype(np.uint8), 'RGBA')); d = Desenho(cen)
    ele(d, x_ele(t), CHAO - 6, cena, braco=braco_ele(t), lado=-1, t=t)
    for p in flores_dela(t): flor(d, p, cena)
    if bp:
        d.rounded_rectangle((bp[0] - 26, bp[1] - 16, bp[0] + 26, bp[1] + 16), radius=6, fill=(225, 160, 160, int(255 * cena)), outline=rgba(B, cena), width=3)
    big = cen.resize((int(W * K), int(H * K)), Image.BICUBIC)
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.paste(big, (int(CX - CX * K), int(CY - CY * K)))
    d = Desenho(cam)
    for t0, t1, linhas in FRASES:
        al = jan(t, t0, t1)
        for i, l in enumerate(linhas):
            if l: d.text((W/2, 440 + i * 76), l, font=F, fill=rgba(TXT, al), anchor='mm')
    cartao(d, t, FIM + 0.4, parte=2, pergunta=['Então por que', 'ela não vai embora?'], y=640)
    d.text((W/2, 1740), '@mente_mulher_estoica', font=estilo.sem_serifa(30, 400), fill=rgba(C, a * 0.8), anchor='mm')
    im = Image.alpha_composite(fundo, cam).convert('RGB')
    ff.stdin.write(estilo.para_bytes(np.asarray(im, np.float32) * (1 - ap(t, T - 0.8, 0.8))))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida)
print('ok', saida)
