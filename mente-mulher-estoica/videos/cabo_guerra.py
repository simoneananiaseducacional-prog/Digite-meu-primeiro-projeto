"""Cabo de guerra (v3, simples, no molde do vídeo de 82 mil): uma ideia, uma ação, texto curto no alto.
Os dois puxam, o chão racha e se abre, a corda arrebenta e cada um cai do seu lado.
Sem balões e sem citação na tela (Sêneca e Gottman vão na legenda).
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
TXT = (200, 196, 190)
saida = Path(sys.argv[1])
fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1): return ap(t, t0) * (1 - ap(t, t1 - 0.5, 0.5))
def rgba(c, a): return c + (int(255 * cl(a)),)
def lerp(a, b, p): return a + (b - a) * p

class Desenho(ImageDraw.ImageDraw):
    def __init__(self, im): super().__init__(im, 'RGBA')
    def text(self, xy, s, fill=None, **kw):
        if fill is not None and len(fill) == 4 and fill[3] < 3: return
        super().text(xy, s, fill=fill, **kw)

T = 24.0
CHAO = 1250
K, CX, CY = 1.18, 540, 1150
ARREBENTA = 13.0
# frases (uma por vez, no alto)
FRASES = [(0.4, 4.6, ['Numa briga, cada um', 'puxa para o seu lado.']),
          (4.8, 8.8, ['Quanto mais força…']),
          (9.0, 12.8, ['…maior a distância.']),
          (14.2, 23.2, ['Se um ganha,', 'os dois perdem.'])]

def afasta(t): return estilo.suavizar(cl((t - 5.0) / 7.5))          # 0..1 até arrebentar
def x_ela(t): return 380 - 110 * afasta(t) - 6 * abs(math.sin(t * 6)) * (t < ARREBENTA)
def x_ele(t): return 700 + 110 * afasta(t) + 6 * abs(math.sin(t * 6 + 1)) * (t < ARREBENTA)
def abertura(t): return 16 + 230 * afasta(t)
def caiu(t): return ap(t, ARREBENTA, 0.45)
def inclina(t):
    if t < ARREBENTA: return (8 + 10 * afasta(t)) * ap(t, 0.3, 0.8)
    return 18 * (1 - caiu(t))

def chao(d, t, a):
    ab = abertura(t)
    d.line([(0, CHAO), (540 - ab / 2, CHAO)], fill=rgba(C, a), width=4)
    d.line([(540 + ab / 2, CHAO), (W, CHAO)], fill=rgba(C, a), width=4)
    pe = [(540 - ab / 2 + dx, CHAO + y) for dx, y in [(0, 0), (-14, 80), (10, 160), (-8, 250), (0, 360)]]
    pd = [(540 + ab / 2 + dx, CHAO + y) for dx, y in [(0, 0), (14, 80), (-6, 160), (12, 250), (0, 360)]]
    d.line(pe, fill=rgba(C, a), width=4); d.line(pd, fill=rgba(C, a), width=4)

def mao(t, quem):
    x = x_ela(t) if quem == 'ela' else x_ele(t); lado = 1 if quem == 'ela' else -1
    sent = caiu(t)
    hy = CHAO - 6 - 240 + 95 * sent
    px, py = x + lado * 150, hy + 50
    th = math.radians(inclina(t)) * lado; dx, dy = px - x, py - (CHAO - 6)
    return x + dx * math.cos(th) + dy * math.sin(th), (CHAO - 6) - dx * math.sin(th) + dy * math.cos(th)

def corda(d, t, a):
    me, md = mao(t, 'ela'), mao(t, 'ele')
    if t < ARREBENTA:
        pts = [(lerp(me[0], md[0], i / 40), lerp(me[1], md[1], i / 40) + 3 * math.sin(t * 40 + i) * afasta(t)) for i in range(41)]
        d.line(pts, fill=rgba(B, a), width=9, joint='curve')
        for i in range(2, 39, 3):
            x, y = pts[i]; d.line([(x - 4, y - 4), (x + 4, y + 4)], fill=rgba((40, 38, 36), a), width=2)
    else:   # arrebentou: cada metade cai no chão, à frente de cada um
        q = caiu(t)
        for m, lado, xp in ((me, 1, x_ela(t)), (md, -1, x_ele(t))):
            fim = (lerp(m[0] + lado * 150, xp + lado * 170, q), lerp(m[1], CHAO - 5, q))
            ini = (lerp(m[0], xp + lado * 50, q), lerp(m[1], CHAO - 5, q))
            d.line([ini, fim], fill=rgba(B, a), width=9)

def figura(t, quem, a):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(lay, 'RGBA')
    x = x_ela(t) if quem == 'ela' else x_ele(t)
    s = caiu(t); baixa = ap(t, ARREBENTA + 1.2, 1.2)
    if quem == 'ela': ela(dd, x, CHAO - 6, a, braco=1.0 - 0.6 * baixa, lado=1, sentada=s, cabeca_baixa=baixa, t=t)
    else: ele(dd, x, CHAO - 6, a, braco=1.0 - 0.6 * baixa, lado=-1, sentado=s, cabeca_baixa=baixa, t=t)
    g = inclina(t) * (1 if quem == 'ela' else -1)
    return lay.rotate(g, resample=Image.BICUBIC, center=(x, CHAO - 6)) if abs(g) > 0.2 else lay

F = estilo.sem_serifa(54, 500)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    a = ap(t, 0.1, 0.6)
    cen = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = Desenho(cen)
    chao(d, t, a); corda(d, t, a)
    cen = Image.alpha_composite(cen, figura(t, 'ela', a))
    cen = Image.alpha_composite(cen, figura(t, 'ele', a))
    big = cen.resize((int(W * K), int(H * K)), Image.BICUBIC)
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.paste(big, (int(CX - CX * K), int(CY - CY * K)))
    d = Desenho(cam)
    for t0, t1, linhas in FRASES:
        al = jan(t, t0, t1)
        for i, l in enumerate(linhas):
            d.text((W/2, 470 + i * 74), l, font=F, fill=rgba(TXT, al), anchor='mm')
    d.text((W/2, 1720), '@mente_mulher_estoica', font=estilo.sem_serifa(30, 400), fill=rgba(C, a * 0.8), anchor='mm')
    im = Image.alpha_composite(fundo, cam).convert('RGB')
    ff.stdin.write(estilo.para_bytes(np.asarray(im, np.float32) * (1 - ap(t, T - 0.8, 0.8))))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida)
print('ok', saida)
