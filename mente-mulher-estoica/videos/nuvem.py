"""A nuvem (Epicteto, Encheirídion 5): os dois cafés derramados ao mesmo tempo; sobre ele cresce uma nuvem de tempestade,
sobre ela a nuvem some com uma respiração. No fim ele olha para ela e a nuvem dele se desfaz.
Molde inspirado no ritmo de @project.vglyb (sem texto, rostos com emoção, cortes de câmera, @ no fim),
com história e desenho próprios. Uso: python3 nuvem.py saida.mp4
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from personagens import ela, ele
from PIL import Image, ImageDraw
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
F = 2.4                                   # desenha em alta resolução para os closes ficarem nítidos
saida = Path(sys.argv[1])
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1): return ap(t, t0) * (1 - ap(t, t1 - 0.5, 0.5))
def rgba(c, a): return c + (int(255 * cl(a)),)
def lerp(a, b, p): return a + (b - a) * p
def pulso(t, t0, t1, s=0.2): return ap(t, t0, s) * (1 - ap(t, t1 - s, s))
def seg(t, t0, t1): return estilo.suavizar(cl((t - t0) / (t1 - t0)))

class Esc:
    """Repassa as chamadas de desenho multiplicando coordenadas e espessuras por F."""
    def __init__(self, d, f): self.d, self.f = d, f
    def _xy(self, xy):
        if isinstance(xy[0], (tuple, list)): return [(p[0] * self.f, p[1] * self.f) for p in xy]
        return [v * self.f for v in xy]
    def __getattr__(self, nome):
        orig = getattr(self.d, nome)
        def chama(xy, *args, **kw):
            for k in ('width', 'radius'):
                if k in kw: kw[k] = max(1, int(round(kw[k] * self.f)))
            return orig(self._xy(xy), *args, **kw)
        return chama

T = 23.0
CHAO = 1250
XE, XH = 380, 700
MESA = (480, 620, CHAO - 120)            # x0, x1, altura do tampo
PLANOS = [  # (início, K, CX, CY)
    (0.0, 1.9, 540, 1110),     # geral: o café cai
    (3.2, 3.0, XH, 930),        # close nele: raiva e nuvem
    (6.4, 3.0, XE, 960),        # close nela: susto e respiração
    (9.6, 1.9, 540, 1100),     # geral: a chuva nele, ela arruma o copo
    (13.0, 3.0, XH, 930),       # close nele: a nuvem se desfaz
    (16.0, 1.5, 540, 1060)]    # geral + frase + @
def plano(t):
    p = PLANOS[0]
    for q in PLANOS:
        if t >= q[0]: p = q
    k = p[1] * (1 + 0.03 * (t - p[0]))      # leve aproximação dentro de cada plano
    return k, p[2], p[3]

def nuvem(d, cx, cy, s, a, chuva=0.0, t=0.0):
    if s < 0.03 or a < 0.02: return
    for dx, dy, r in [(-46, 8, 34), (-14, -14, 42), (24, -4, 38), (52, 12, 28), (0, 16, 36)]:
        d.ellipse((cx + dx * s - r * s, cy + dy * s - r * s, cx + dx * s + r * s, cy + dy * s + r * s),
                  fill=(52, 52, 58, int(255 * a)), outline=rgba(C, a), width=3)
    for i in range(7):
        if chuva < 0.05: break
        x = cx + (-60 + i * 20) * s
        y0 = cy + 40 * s + ((t * 260 + i * 37) % 120) * s
        d.line([(x, y0), (x - 4 * s, y0 + 18 * s)], fill=rgba((150, 170, 200), a * chuva), width=3)

def copo(d, t, a):
    """Mesa com dois copos, um de cada. A mesa balança sozinha e os dois caem juntos."""
    x0, x1, ym = MESA
    bal = 6 * math.sin(t * 40) * pulso(t, 1.4, 2.2)
    d.line([(x0, ym + bal), (x1, ym - bal)], fill=rgba(C, a), width=5)
    for x in (x0 + 12, x1 - 12): d.line([(x, ym), (x, CHAO)], fill=rgba(C, a), width=4)
    cai = seg(t, 1.8, 2.3); volta = seg(t, 10.6, 11.4)
    mancha = cai * (1 - seg(t, 11.0, 12.0))
    for cx, lado in ((512, -1), (588, 1)):        # copo dela (esquerda) e dele (direita)
        ang = -lado * 90 * cai * (1 - volta)
        base = ym
        if mancha > 0.02:
            if lado < 0: d.ellipse((cx - 10 - 40 * mancha, ym - 3, cx + 10, ym + 5), fill=(70, 45, 30, int(230 * a)))
            else: d.ellipse((cx - 10, ym - 3, cx + 10 + 40 * mancha, ym + 5), fill=(70, 45, 30, int(230 * a)))
        r = math.radians(ang)
        def gira(px, py):
            return (cx + (px - cx) * math.cos(r) + (py - base) * math.sin(r), base - (px - cx) * math.sin(r) + (py - base) * math.cos(r))
        pts = [gira(cx - 14, base), gira(cx + 14, base), gira(cx + 18, base - 40), gira(cx - 18, base - 40)]
        d.polygon(pts, fill=(18, 17, 16, int(255 * a)), outline=rgba(B, a), width=4)

def emo_ele(t):
    raiva = ap(t, 2.4, 0.6) * (1 - seg(t, 14.0, 15.2))
    grita = max(0.0, math.sin((t - 3.6) * 7)) * (3.6 < t < 6.2) * 0.9
    return dict(raiva=raiva, aberta=grita, sorriso=seg(t, 15.0, 16.0) * 0.8 + 0.4 * (t < 1.6), triste=0.3 * seg(t, 13.2, 14.2) * (1 - seg(t, 15, 16)))
def emo_ela(t):
    susto = ap(t, 2.0, 0.3) * (1 - seg(t, 7.6, 8.4))
    return dict(triste=0.5 * susto, aberta=0.5 * susto * (t < 7.4), sorriso=0.4 * (t < 1.6) + 0.8 * seg(t, 8.2, 8.9))
def nuvem_ele(t): return seg(t, 3.4, 6.0) * (1 - seg(t, 13.8, 15.4))
def nuvem_ela(t): return 0.45 * seg(t, 6.8, 7.4) * (1 - seg(t, 7.8, 8.5))

FT = estilo.sem_serifa(52, 500); TXT = (200, 196, 190)
fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    a = ap(t, 0.1, 0.5)
    cena_a = a * (1 - 0.75 * ap(t, 16.2, 0.8))
    big = Image.new('RGBA', (int(W * F), int(H * F)), (0, 0, 0, 0))
    d = Esc(ImageDraw.Draw(big, 'RGBA'), F)
    d.line([(0, CHAO), (W, CHAO)], fill=rgba(C, cena_a), width=4)
    copo(d, t, cena_a)
    # ele esbarra no copo; ela se abaixa um pouco para arrumar
    br_ele = 0.0
    ele(d, XH, CHAO - 6, cena_a, braco=br_ele, lado=-1, cabeca_baixa=0.0, t=t, emo=emo_ele(t))
    xe = XE + 80 * math.sin(math.pi * seg(t, 10.0, 12.2))
    ela(d, xe, CHAO - 6, cena_a, braco=0.8 * math.sin(math.pi * seg(t, 10.2, 12.0)), lado=1, t=t, emo=emo_ela(t))
    nuvem(d, XH, CHAO - 6 - 240 - 120, 1.6 * nuvem_ele(t), cena_a, chuva=nuvem_ele(t) * (t > 5.0), t=t)
    nuvem(d, xe, CHAO - 6 - 240 - 100, 1.0 * nuvem_ela(t), cena_a)
    # câmera
    K, cx, cy = plano(t)
    w, h = W / K * F, H / K * F
    x0 = max(0, min(big.width - w, cx * F - w / 2)); y0 = max(0, min(big.height - h, cy * F - h / 2))
    cam = big.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((W, H), Image.LANCZOS)
    im = Image.alpha_composite(fundo, cam); d2 = ImageDraw.Draw(im, 'RGBA')
    # frase final
    fa = jan(t, 16.6, 20.4)
    if fa > 0.02:
        for i, l in enumerate(['Não são as coisas', 'que nos perturbam,', 'mas o que pensamos delas.']):
            d2.text((W/2, 520 + i * 74), l, font=FT, fill=rgba(TXT if i < 2 else G, fa), anchor='mm')
        d2.text((W/2, 780), 'Epicteto, Encheirídion, 5', font=estilo.playfair(32, True), fill=rgba(C, fa), anchor='mm')
    # @ no fim, com o ícone desenhado
    ia = ap(t, 20.4, 0.6)
    if ia > 0.02:
        s = 70
        d2.rounded_rectangle((W/2 - s, 760 - s, W/2 + s, 760 + s), radius=40, outline=rgba(B, ia), width=10)
        d2.ellipse((W/2 - 34, 760 - 34, W/2 + 34, 760 + 34), outline=rgba(B, ia), width=10)
        d2.ellipse((W/2 + 36, 760 - 50, W/2 + 50, 760 - 36), fill=rgba(B, ia))
        d2.text((W/2, 900), '@mente_mulher_estoica', font=estilo.sem_serifa(46, 600), fill=rgba(B, ia), anchor='mm')
    ff.stdin.write(estilo.para_bytes(np.asarray(im.convert('RGB'), np.float32) * (1 - ap(t, T - 0.5, 0.5))))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida)
print('ok', saida)
