"""Os fios do tempo: a vida passa de cima para baixo e os caminhos se encontram e se despedem.
Pouco texto; a animação conduz. Uso: python3 fios_do_tempo.py saida.mp4 (vídeo mudo)
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
ROSA = (196, 110, 118)
OURO_CLARO = (226, 196, 140)
saida = Path(sys.argv[1])
fundo = np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1): return ap(t, t0) * (1 - ap(t, t1 - 0.4, 0.4))
def cl(p): return max(0.0, min(1.0, p))
def sm(p): return estilo.suavizar(cl(p))
TOPO, FUNDO_Y = 370, 1440
T0, T1 = 4.2, 19.5          # o tempo corre (a linha do presente desce)
T = 27.0

# cada fio: função x(y), início, fim, cor, espessura, rótulo
def junto(x0, x1, y0, y1):
    """Fio que entra pela lateral (x0) e se aproxima (x1) entre y0 e y1."""
    return lambda y: x0 + (x1 - x0) * sm((y - y0) / (y1 - y0))
def sai(f, x2, y2, y3):
    """Depois de y2, o fio se afasta até x2 e termina em y3 (despedida)."""
    return lambda y: f(y) + (x2 - f(y)) * sm((y - y2) / (y3 - y2))
FIOS = [   # despedidas: o fio termina com um ponto, sem cruzar ninguém
    (lambda y: 540, TOPO, FUNDO_Y, G, 6, 'você', (540, TOPO - 34)),
    (lambda y: 470, TOPO, 1000, B, 3, 'família', (400, TOPO + 30)),
    (lambda y: 610, TOPO, 1080, B, 3, None, None),
    (junto(-20, 400, 560, 680), 560, 900, C, 3, 'amigos', (70, 585)),
    (junto(1100, 690, 640, 760), 640, 980, C, 3, None, None),
    (junto(-20, 300, 760, 880), 760, FUNDO_Y, C, 3, None, None),
    (junto(1100, 770, 880, 1010), 880, FUNDO_Y, ROSA, 4, 'amor', (900, 905)),
    (junto(655, 620, 1150, 1240), 1150, FUNDO_Y, OURO_CLARO, 3, 'filhos', (655, 1118)),
    (junto(655, 700, 1250, 1340), 1250, FUNDO_Y, OURO_CLARO, 3, None, None),
]
def cabeca(t): return TOPO + (FUNDO_Y - TOPO) * sm((t - T0) / (T1 - T0)) if t > T0 else TOPO - 1
F_L = estilo.playfair(34, True)
F1, F2 = estilo.playfair(56), estilo.playfair(56, True)
def txt(d, xy, s, f, cor, a, anc='mm'):
    if a > 0.01: d.text(xy, s, font=f, fill=cor + (int(255 * cl(a)),), anchor=anc)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    img = Image.fromarray(fundo).convert('RGBA'); cam = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
    fim = 1 - ap(t, T - 0.8, 0.6)
    yh = cabeca(t)
    lembra = ap(t, T1 + 0.3, 1.2)          # no fim, o que passou vira lembrança (esmaece)
    for f, y0, y1, cor, w, rot, pos in FIOS:
        if yh <= y0: continue
        ys = list(range(int(y0), int(min(y1, yh)), 6)) + [min(y1, yh)]
        if len(ys) < 2: continue
        pts = [(f(y), y) for y in ys]
        terminou = yh >= y1 and y1 < FUNDO_Y
        a = (1 - 0.55 * lembra) if terminou else 1.0
        d.line(pts, fill=cor + (int(235 * a * fim),), width=w, joint='curve')
        px, py = pts[-1]
        if terminou:
            d.ellipse((px - 6, py - 6, px + 6, py + 6), fill=cor + (int(200 * a * fim),))
        else:
            d.ellipse((px - 7, py - 7, px + 7, py + 7), fill=cor + (int(255 * fim),))
        if rot:
            txt(d, pos, rot, F_L, cor, cl((yh - y0) / 60) * fim * (1 - 0.4 * lembra), 'mm' if rot in ('você', 'filhos', 'família') else 'lm')
    # a linha do presente
    if T0 < t < T1 + 0.6:
        a = 0.35 * (1 - ap(t, T1, 0.5))
        for x in range(80, 1000, 24):
            d.line([(x, yh), (x + 12, yh)], fill=C + (int(255 * a),), width=1)
    txt(d, (W/2, 185), 'Enquanto a vida passa,', F1, B, jan(t, 0.3, 4.2))
    txt(d, (W/2, 260), 'nossos caminhos se encontram.', F2, G, jan(t, 0.8, 4.2))
    txt(d, (W/2, 185), 'Um dia, o tempo juntos vira lembrança.', estilo.playfair(48), B, ap(t, T1 + 0.4) * fim)
    txt(d, (W/2, 260), 'Hoje, ainda pode ser presença.', estilo.playfair(52, True), G, ap(t, T1 + 1.4) * fim)
    if ap(t, T1 + 2.4) > 0:
        estilo.texto_espacado(d, (W/2, 1520), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(22, 500), C + (int(255 * ap(t, T1 + 2.4) * fim),), 6)
    img = Image.alpha_composite(img, cam)
    q = np.asarray(img.convert('RGB'), np.float32) * (1 - ap(t, T - 0.6, 0.6))
    ff.stdin.write(estilo.para_bytes(q))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); saida.with_suffix('.mudo.mp4').unlink(missing_ok=True)
print('ok')
