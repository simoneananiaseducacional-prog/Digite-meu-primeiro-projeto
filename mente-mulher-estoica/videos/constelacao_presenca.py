"""Constelação (metáfora artística, sem alegação terapêutica): pessoas viram estrelas ligadas por linhas finas.
Uso: python3 constelacao_presenca.py saida.mp4
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
saida = Path(sys.argv[1])
fundo = np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)
rng = np.random.default_rng(3)
CEU = [(int(rng.uniform(40, 1040)), int(rng.uniform(420, 1440)), rng.uniform(0, 6)) for _ in range(70)]
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1): return ap(t, t0) * (1 - ap(t, t1 - 0.4, 0.4))
def cl(p): return max(0.0, min(1.0, p))
def rgba(c, a): return c + (int(255 * cl(a)),)
ESTRELAS = [('Avó', (200, 600), (196, 170, 220)), ('Avô', (860, 520), (230, 225, 200)), ('Pai', (720, 700), (150, 180, 230)),
            ('Mãe', (330, 780), (225, 130, 150)), ('Amor', (250, 1010), (230, 170, 150)), ('Amiga', (880, 1080), (170, 220, 210)),
            ('Eu', (540, 1110), G), ('Filho', (730, 1260), (220, 230, 220))]
LIGA = [(0, 1), (0, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)]
T0, PASSO = 4.6, 0.95
T = 23.0
def estrela(d, x, y, cor, a, t, s=1.0):
    if a <= 0.01: return
    br = 1 + 0.15 * math.sin(t * 3 + x)
    for r, al in ((26, 0.12), (14, 0.3)):
        rr = r * br * s
        d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=rgba(cor, al * a))
    L = 22 * s * br
    d.line([(x - L, y), (x + L, y)], fill=rgba(cor, a), width=2); d.line([(x, y - L), (x, y + L)], fill=rgba(cor, a), width=2)
    d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=rgba((255, 255, 250), a))
F1, F2 = estilo.playfair(58), estilo.playfair(58, True)
def txt(d, xy, s, f, cor, a):
    if a > 0.01: d.text(xy, s, font=f, fill=rgba(cor, a), anchor='mm')
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    img = Image.fromarray(fundo).convert('RGBA'); cam = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
    fim = 1 - ap(t, T - 0.8, 0.6)
    for x, y, ph in CEU:
        a = (0.25 + 0.2 * math.sin(t * 1.5 + ph)) * ap(t, 0.2, 1.5) * fim
        d.ellipse((x - 1.5, y - 1.5, x + 1.5, y + 1.5), fill=rgba(B, a))
    for i, j in LIGA:
        q = cl((t - (T0 + max(i, j) * PASSO) - 0.3) / 0.6)
        if q > 0:
            (x0, y0), (x1, y1) = ESTRELAS[i][1], ESTRELAS[j][1]
            d.line([(x0, y0), (x0 + (x1 - x0) * q, y0 + (y1 - y0) * q)], fill=rgba(G, 0.45 * fim), width=2)
    for n, (nome, (x, y), cor) in enumerate(ESTRELAS):
        a = ap(t, T0 + n * PASSO, 0.5) * fim
        estrela(d, x, y, cor, a, t, 1.25 if nome == 'Eu' else 1.0)
        if a > 0: d.text((x, y - 48), nome, font=estilo.playfair(36), fill=rgba(cor, a), anchor='mm')
    txt(d, (W/2, 230), 'O que vivemos juntos', F1, B, jan(t, 0.3, 4.5)); txt(d, (W/2, 310), 'também fica em nós.', F2, G, jan(t, 0.7, 4.5))
    txt(d, (W/2, 230), 'Um dia, o tempo juntos', F1, B, jan(t, 12.8, 17.2)); txt(d, (W/2, 310), 'vira lembrança.', F2, B, jan(t, 13.2, 17.2))
    txt(d, (W/2, 250), 'Hoje, ainda pode', F1, B, ap(t, 17.4) * fim); txt(d, (W/2, 330), 'ser presença.', F2, G, ap(t, 17.8) * fim)
    if ap(t, 18.8) > 0:
        estilo.texto_espacado(d, (W/2, 1500), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(22, 500), rgba(C, ap(t, 18.8) * fim), 6)
    img = Image.alpha_composite(img, cam)
    q2 = np.asarray(img.convert('RGB'), np.float32) * (1 - ap(t, T - 0.6, 0.6))
    ff.stdin.write(estilo.para_bytes(q2))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); saida.with_suffix('.mudo.mp4').unlink(missing_ok=True)
print('ok')
