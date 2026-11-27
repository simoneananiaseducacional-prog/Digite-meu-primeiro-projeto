"""Mapa "Você vive no agora": página de livro com linha do tempo (passado, agora, futuro), raios do que puxa
para trás e para a frente, presença no centro. Formato inspirado em @satori.108 (texto e conceito próprios, sem
"vibração" nem "frequência"). Fonte: Marco Aurélio, Meditações, 3.10. Uso: python3 mapa_agora.py saida.png
"""
import sys, math, random, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
W, H = 1080, 1350
FT = Path('/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos/fontes')
def F(n, t): return ImageFont.truetype(str(FT / f'EBGaramond-{n}.ttf'), t)
TINTA, CINZA, PAPEL, PILULA = (38, 35, 32), (95, 90, 84), (238, 234, 226), (222, 217, 207)
# papel com textura leve e vinheta
rng = np.random.default_rng(7)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
vin = 1 - 0.10 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
base = np.array(PAPEL, np.float32)[None, None] * vin[..., None] + rng.normal(0, 3.2, (H, W, 1))
im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert('RGBA')
d = ImageDraw.Draw(im)

def pilula(cx, cy, s, f, ital=True):
    w = f.getlength(s) + 44
    d.rounded_rectangle((cx - w / 2, cy - 27, cx + w / 2, cy + 27), radius=27, fill=PILULA)
    d.text((cx, cy), s, font=f, fill=TINTA, anchor='mm')
def pontilhado(p0, p1, passo=9):
    n = int(math.dist(p0, p1) / passo)
    for i in range(n):
        x = p0[0] + (p1[0] - p0[0]) * i / n; y = p0[1] + (p1[1] - p0[1]) * i / n
        d.ellipse((x - 1.3, y - 1.3, x + 1.3, y + 1.3), fill=CINZA)
def rotulo(s, xy, ang, f):
    w = int(f.getlength(s)) + 10; h = f.size + 14
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ImageDraw.Draw(lay).text((5, h / 2), s, font=f, fill=TINTA + (255,), anchor='lm')
    lay = lay.rotate(ang, resample=Image.BICUBIC, expand=True)
    im.alpha_composite(lay, (int(xy[0] - lay.width / 2), int(xy[1] - lay.height / 2)))

# cabeçalho de página
d.text((W - 110, 78), '@mente_mulher_estoica   |   12', font=F('Regular', 28), fill=CINZA, anchor='rm')
# título
d.text((110, 160), 'O passado já foi.', font=F('Regular', 60), fill=TINTA, anchor='lm')
d.text((110, 228), 'O futuro ainda não chegou.', font=F('Regular', 60), fill=TINTA, anchor='lm')
d.text((110, 300), 'Você vive no agora.', font=F('Italic', 64), fill=TINTA, anchor='lm')
d.line([(112, 350), (240, 350)], fill=TINTA, width=2)
for i, l in enumerate(['Remoer o que passou e temer o que virá', 'tiram você do único lugar onde a vida', 'acontece: este momento.']):
    d.text((110, 390 + i * 34), l, font=F('Regular', 27), fill=CINZA, anchor='lm')

# linha do tempo
C = (540, 760)
d.line([(85, C[1]), (985, C[1])], fill=TINTA, width=3)
d.polygon([(1000, C[1]), (982, C[1] - 9), (982, C[1] + 9)], fill=TINTA)
pilula(185, C[1] - 52, 'Seu passado', F('Italic', 32))
pilula(880, C[1] + 52, 'Seu futuro', F('Italic', 32))
pilula(C[0], 560, 'Agora', F('Italic', 34))
pontilhado((C[0], 592), (C[0], 905))
fr = F('Italic', 30)
def raio(s, ang, L, lado):
    a = math.radians(ang); u = (lado * math.cos(a), -lado * math.sin(a))   # lado 1: futuro (sobe à direita); -1: passado
    end = (C[0] + L * u[0], C[1] + L * u[1]); pontilhado(C, end)
    k = L - fr.getlength(s) / 2 - 18; n = (-math.sin(a), -math.cos(a))    # normal para cima
    rotulo(s, (C[0] + k * u[0] + 18 * n[0], C[1] + k * u[1] + 18 * n[1]), ang, fr)
for i, s in enumerate(['Ansiedade', 'E se…?', 'Expectativas', 'Medo de errar']):
    raio(s, 40 - i * 9, 455, 1)
for i, s in enumerate(['Arrependimentos', 'Mágoas', 'Crenças antigas', 'Culpa']):
    raio(s, 11 + i * 9, 440, -1)
d.ellipse((C[0] - 9, C[1] - 9, C[0] + 9, C[1] + 9), fill=TINTA)

# presença
pilula(C[0], 935, 'Presença', F('Italic', 34))
for i, s in enumerate(['Atenção', 'Escolha', 'Ação', 'Serenidade']):
    d.text((C[0], 985 + i * 34), s, font=F('Italic', 29), fill=TINTA, anchor='mm')

# colunas
d.line([(C[0], 1145), (C[0], 1240)], fill=TINTA, width=2)
pilula(290, 1145, 'O que te prende', F('Medium', 28), False)
pilula(800, 1145, 'O que te liberta', F('Medium', 28), False)
for i, l in enumerate(['Reviver o que passou e', 'antecipar o que não veio.', 'Os dois tiram você daqui.']):
    d.text((110, 1190 + i * 30), l, font=F('Regular', 25), fill=TINTA, anchor='lm')
for i, l in enumerate(['Agir no que depende de você,', 'aqui e agora. É onde a', 'vida acontece.']):
    d.text((590, 1190 + i * 30), l, font=F('Regular', 25), fill=TINTA, anchor='lm')
# rodapé
d.text((W / 2, 1300), '“Cada um vive apenas o presente.”  Marco Aurélio, Meditações, 3.10', font=F('Italic', 25), fill=CINZA, anchor='mm')
im.convert('RGB').save(sys.argv[1]); print('ok')
