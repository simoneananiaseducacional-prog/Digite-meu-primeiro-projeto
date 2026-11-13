"""A borracha (gaslighting): a cada "não é nada" / "você está louca" ele apaga um pedaço dela;
no meio, um carinho (a flor) confunde. Ela vai se apagando, até pegar o lápis dourado e se redesenhar.
Lápis = a capacidade de julgar (prohairesis, Epicteto, Discursos 1.1.23). Molde simples.
Base: Sweet 2019; Klein et al. 2023; Dutton & Painter 1993. Uso: python3 borracha.py saida.mp4
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
def pulso(t, t0, t1, s=0.4): return ap(t, t0, s) * (1 - ap(t, t1 - s, s))
def seg(t, t0, t1): return estilo.suavizar(cl((t - t0) / (t1 - t0)))

class Desenho(ImageDraw.ImageDraw):
    def __init__(self, im): super().__init__(im, 'RGBA')
    def text(self, xy, s, fill=None, **kw):
        if fill is not None and len(fill) == 4 and fill[3] < 3: return
        super().text(xy, s, fill=fill, **kw)

T = 27.0
CHAO = 1250
K, CX, CY = 1.6, 540, 1130
XE = 380
FRASES = [(0.4, 4.6, ['“Não é nada.”']),
          (4.8, 9.2, ['Depois, um carinho.']),
          (9.4, 13.6, ['“Você está louca.”']),
          (13.8, 17.6, ['E ela vai se apagando.']),
          (17.8, 26.2, ['Até ela voltar a confiar', 'no que viu.'])]

# apagões: (início, fim, centro, meia-largura, meia-altura)
APAGA = [(2.2, 3.5, (480, 1052), 55, 18),     # a mão que apontou
         (10.4, 11.8, (375, 1200), 40, 40),   # parte das pernas
         (12.0, 13.2, (415, 1080), 22, 50)]   # um pedaço do cabelo e do braço
def borracha_pos(t):
    for t0, t1, (cx, cy), rx, ry in APAGA:
        if t0 <= t <= t1:
            u = (t - t0) / (t1 - t0)
            return (cx + rx * math.sin(u * 2 * math.pi * 2.0), cy + ry * math.sin(u * 2 * math.pi * 1.2 - 1.2))
    return None
def x_ele(t):
    alvo = 720
    for t0, t1, (cx, cy), rx, ry in APAGA:
        alvo = lerp(alvo, cx + 175, pulso(t, t0 - 0.8, t1 + 0.6, 0.6))
    alvo = lerp(alvo, 560, pulso(t, 5.2, 8.2, 0.7))          # vem trazer a flor
    return alvo
def braco_ele(t):
    v = 0.0
    for t0, t1, *_ in APAGA: v = max(v, pulso(t, t0 - 0.3, t1 + 0.2, 0.3))
    return max(v, pulso(t, 5.8, 7.6, 0.4))
def braco_ela(t): return max(pulso(t, 0.8, 3.0, 0.4), pulso(t, 6.6, 9.6, 0.4) * 0.6, pulso(t, 18.2, 22.0, 0.4) * 0.7)
def flor_pos(t):
    if t < 5.6: return None
    mao_ele = (x_ele(t) - 150, CHAO - 6 - 240 + 50)
    mao_ela = (XE + 40 + 66, CHAO - 6 - 240 + 72 - 13)
    if t < 6.6: return mao_ele
    if t < 7.2: p = seg(t, 6.6, 7.2); return (lerp(mao_ele[0], mao_ela[0], p), lerp(mao_ele[1], mao_ela[1], p))
    if t < 11.6: return mao_ela
    p = seg(t, 11.6, 12.3); return (mao_ela[0] + 20 * p, lerp(mao_ela[1], CHAO - 74, p))   # cai no chão
def flor(d, p, a, murcha=0.0):
    x, y = p
    d.line([(x, y), (x, y + 70)], fill=rgba(C, a), width=4)
    for k in range(5):
        ang = k * 2 * math.pi / 5 - math.pi / 2 + murcha * 0.8
        px, py = x + 15 * math.cos(ang), y + 15 * math.sin(ang) + 12 * murcha
        d.ellipse((px - 11, py - 11, px + 11, py + 11), fill=rgba(G, a * (1 - 0.6 * murcha)))
    d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=rgba(B, a))

# máscara do que foi apagado (1 = visível)
MASK = np.ones((H, W), np.float32)
yy, xx = np.mgrid[0:H, 0:W]
def apagar_em(p, r=20):
    x0, x1 = int(max(p[0] - r, 0)), int(min(p[0] + r, W)); y0, y1 = int(max(p[1] - r, 0)), int(min(p[1] + r, H))
    sub = (xx[y0:y1, x0:x1] - p[0]) ** 2 + (yy[y0:y1, x0:x1] - p[1]) ** 2 < r * r
    MASK[y0:y1, x0:x1][sub] = 0.0
TOPO_ELA, BASE_ELA = CHAO - 300, CHAO + 10

F = estilo.sem_serifa(56, 500)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    a = ap(t, 0.1, 0.6)
    bp = borracha_pos(t)
    if bp: apagar_em(bp)
    cen = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = Desenho(cen)
    d.line([(0, CHAO), (W, CHAO)], fill=rgba(C, a), width=4)
    # ela, numa camada própria, com a máscara do que foi apagado
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay, 'RGBA')
    ela(dl, XE, CHAO - 6, 1.0, braco=braco_ela(t), lado=1, cabeca_baixa=ap(t, 13.8, 1.5) * (1 - ap(t, 18.0, 1.0)), t=t)
    # redesenho: a máscara volta de baixo para cima com o lápis
    volta = seg(t, 18.6, 22.0)
    linha = lerp(BASE_ELA, TOPO_ELA - 40, volta)
    m = MASK.copy()
    if volta > 0: m[int(max(linha, 0)):, :] = 1.0
    fade = lerp(1.0 - 0.6 * ap(t, 13.8, 3.5), 1.0, volta)
    arr = np.asarray(lay).copy().astype(np.float32)
    arr[..., 3] *= m * fade * a
    cen = Image.alpha_composite(cen, Image.fromarray(arr.astype(np.uint8), 'RGBA')); d = Desenho(cen)
    ele(d, x_ele(t), CHAO - 6, a * (1 - 0.5 * ap(t, 19.0, 2.0)), braco=braco_ele(t), lado=-1, t=t)
    fp = flor_pos(t)
    if fp: flor(d, fp, a * (1 - 0.6 * ap(t, 13.8, 2.0)), murcha=ap(t, 11.6, 1.0))
    if bp:   # a borracha
        d.rounded_rectangle((bp[0] - 26, bp[1] - 16, bp[0] + 26, bp[1] + 16), radius=6, fill=(225, 160, 160, int(255 * a)), outline=rgba(B, a), width=3)
    if 18.0 < t < 22.6:   # o lápis dourado, riscando a linha que redesenha
        lx = XE + 70 + 26 * math.sin(t * 9); ly = linha
        pa = pulso(t, 18.0, 22.6, 0.4)
        d.line([(lx, ly), (lx + 60, ly - 90)], fill=rgba(G, pa), width=10)
        d.polygon([(lx - 6, ly + 4), (lx + 6, ly - 4), (lx - 4, ly + 16)], fill=rgba(B, pa))
    big = cen.resize((int(W * K), int(H * K)), Image.BICUBIC)
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.paste(big, (int(CX - CX * K), int(CY - CY * K)))
    d = Desenho(cam)
    for t0, t1, linhas in FRASES:
        al = jan(t, t0, t1)
        for i, l in enumerate(linhas):
            d.text((W/2, 440 + i * 76), l, font=F, fill=rgba(TXT, al), anchor='mm')
    d.text((W/2, 1740), '@mente_mulher_estoica', font=estilo.sem_serifa(30, 400), fill=rgba(C, a * 0.8), anchor='mm')
    im = Image.alpha_composite(fundo, cam).convert('RGB')
    ff.stdin.write(estilo.para_bytes(np.asarray(im, np.float32) * (1 - ap(t, T - 0.8, 0.8))))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida)
print('ok', saida)
