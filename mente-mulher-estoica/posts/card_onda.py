"""Card com foto no alto, onda escura e citação embaixo (feed 4:5).
Uso: python3 card_onda.py foto.jpg saida.png "linha 1|linha 2" "AUTORA" "subtítulo" [corte_altura]
corte_altura: fração da altura da foto usada (padrão 0.55, para mostrar só rosto e ombros).
A foto nunca entra no repositório.
"""
import sys, math
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo
from PIL import Image, ImageDraw, ImageOps
W, H = 1080, 1350
foto, saida, frase, autora, sub = sys.argv[1:6]
corte = float(sys.argv[6]) if len(sys.argv) > 6 else 0.55
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
FUNDO = (16, 16, 16)
im = ImageOps.exif_transpose(Image.open(foto)).convert('RGB')
im = im.crop((0, 0, im.width, int(im.height * corte)))
esc = W / im.width
im = im.resize((W, int(im.height * esc)), Image.LANCZOS)
card = Image.new('RGB', (W, H), FUNDO)
card.paste(im, (0, 0))
# a base da foto se dissolve no fundo, para não aparecer borda reta
for i in range(140):
    yy = im.height - 140 + i
    a = int(255 * (i / 139) ** 1.5)
    ImageDraw.Draw(card, 'RGBA').line([(0, yy), (W, yy)], fill=FUNDO + (a,))
# onda: começa alta à esquerda, desce até o meio e sobe à direita
def onda(x):
    p = x / W
    return 600 + 300 * math.sin(p * math.pi * 0.95) - 120 * p
pts = [(x, onda(x)) for x in range(0, W + 1, 6)]
d = ImageDraw.Draw(card, 'RGBA')
d.polygon(pts + [(W, H), (0, H)], fill=FUNDO)
d.line(pts, fill=G + (255,), width=3)
y = max(onda(x) for x in range(0, 500)) + 50
d.text((84, y), '“', font=estilo.serifa(190, 700), fill=G, anchor='lt')
y += 105
f = estilo.serifa(62, 600)
for linha in frase.split('|'):
    d.text((90, y), linha, font=f, fill=B, anchor='lt'); y += 74
y += 30
d.line([(92, y + 14), (122, y + 14)], fill=G, width=2)
estilo.texto_espacado(d, (136, y + 2), autora.upper(), estilo.sem_serifa(26, 600), G, 4) if False else d.text((136, y), autora.upper(), font=estilo.sem_serifa(26, 600), fill=G, anchor='lt')
d.text((136, y + 40), sub, font=estilo.serifa_italica(32, 500), fill=C, anchor='lt')
card.save(saida)
print('ok')
