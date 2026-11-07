"""Capas de destaque (1080x1920; o Instagram usa o círculo do centro).
Uso: python3 capa_destaque.py pasta_saida
"""
import sys, math
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, numpy as np
from PIL import Image, ImageDraw
from pathlib import Path
W, H = 1080, 1920
G, B = estilo.DOURADO, estilo.BRANCO
CX, CY = 540, 960
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
def tela():
    f = np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)
    im = Image.fromarray(f).convert('RGBA'); d = ImageDraw.Draw(im)
    d.ellipse((CX - 430, CY - 430, CX + 430, CY + 430), outline=G + (110,), width=3)
    return im, d
def el(cx, cy, rx, ry, ang=0, n=60):
    ca, sa = math.cos(ang), math.sin(ang)
    return [(cx + rx * math.cos(2 * math.pi * k / n) * ca - ry * math.sin(2 * math.pi * k / n) * sa,
             cy + rx * math.cos(2 * math.pi * k / n) * sa + ry * math.sin(2 * math.pi * k / n) * ca) for k in range(n)]
def fechado(d, p, cor, w): d.line(p + [p[0]], fill=cor, width=w, joint='curve')

# FÁBULAS: borboleta, abelha e o fio do casulo entre elas
im, d = tela()
bx, by, s = CX - 150, CY - 70, 2.2
for sd in (-1, 1):
    fechado(d, el(bx + sd * 34 * s, by - 18 * s, 34 * s, 26 * s, sd * -0.5), B, 7)
    fechado(d, el(bx + sd * 24 * s, by + 18 * s, 22 * s, 17 * s, sd * 0.5), B, 7)
    d.line([(bx, by - 26 * s), (bx + sd * 14 * s, by - 46 * s)], fill=B, width=5)
d.line([(bx, by - 26 * s), (bx, by + 30 * s)], fill=B, width=9)
ax, ay, s = CX + 160, CY + 100, 2.6
for sd in (-1, 1):
    fechado(d, el(ax + sd * 6 * s, ay - 32 * s, 13 * s, 21 * s, sd * 0.45), B, 5)
corpo = el(ax, ay, 38 * s, 24 * s); fechado(d, corpo, G, 6)
for dx in (-8, 10):
    hh = 24 * math.sqrt(1 - (dx / 38) ** 2)
    d.line([(ax + dx * s, ay - hh * s + 6), (ax + dx * s, ay + hh * s - 6)], fill=G, width=6)
d.ellipse((ax + 36 * s, ay - 12 * s, ax + 60 * s, ay + 12 * s), outline=G, width=6)
d.polygon([(ax - 38 * s, ay - 7 * s), (ax - 38 * s, ay + 7 * s), (ax - 60 * s, ay)], fill=G)
fio = [(bx + 10 + (ax - 140 - bx) * u, by + 80 + 150 * math.sin(u * math.pi) * (1 - u) + 40 * u) for u in [i / 40 for i in range(41)]]
for i in range(0, 40, 2): d.line(fio[i:i + 2], fill=G + (200,), width=4)
im.convert('RGB').save(out / 'destaque-fabulas.png')

# HUMOR: máscara de teatro sorrindo, só o contorno
im, d = tela()
s = 1.0
masc = []
for k in range(61):
    a = math.pi * k / 60
    masc.append((CX - 230 * math.cos(a), CY - 250 + 60 * math.sin(a) * -1))
lado = [(CX + 230 - 20 * (u ** 2) * 1.0 - 120 * u ** 3, CY - 250 + 520 * u) for u in [i / 30 for i in range(31)]]
bico = [(CX, CY + 300)]
contorno = [(CX - 230, CY - 250)] + [(CX - 230 + 30 * u ** 2 + 120 * u ** 3 * 1.0, CY - 250 + 520 * u) for u in [i / 30 for i in range(31)]]
topo = [(CX - 230 + 460 * u, CY - 250 - 70 * math.sin(math.pi * u)) for u in [i / 40 for i in range(41)]]
dir_ = [(CX + 230 - 30 * u ** 2 - 120 * u ** 3, CY - 250 + 520 * u) for u in [i / 30 for i in range(31)]]
pontos = topo + dir_ + [(CX, CY + 300)] + list(reversed([(CX - 230 + 30 * u ** 2 + 120 * u ** 3, CY - 250 + 520 * u) for u in [i / 30 for i in range(31)]]))
d.line(pontos + [pontos[0]], fill=G, width=8, joint='curve')
for sd in (-1, 1):   # olhos sorrindo (arcos para cima)
    ex = CX + sd * 95
    d.arc((ex - 60, CY - 120, ex + 60, CY - 20), 200, 340, fill=G, width=8)
d.arc((CX - 140, CY - 40, CX + 140, CY + 170), 20, 160, fill=G, width=9)   # sorriso
im.convert('RGB').save(out / 'destaque-humor.png')
print('ok')
