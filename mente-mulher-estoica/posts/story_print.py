"""Story de agradecimento com o print de um post (rostos de terceiros desfocados).
Uso: python3 story_print.py print.jpg saida.png   (o print não entra no repositório)
"""
import sys
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, numpy as np
from PIL import Image, ImageDraw, ImageFilter
W, H = 1080, 1920
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
src = Image.open(sys.argv[1]).convert('RGB')
vis = src.crop((28, 1688, 250, 1758))   # o olho e o número de visualizações
# desfoca as fotos de quem compartilhou (faixa dos avatares)
box = (30, 1370, 620, 1630)
src.paste(src.crop(box).filter(ImageFilter.GaussianBlur(22)), box[:2])
# faixa real de números, sem retoque (prova): opcional, substitui a do print original
faixa = sys.argv[4] if len(sys.argv) > 4 else None
if faixa:
    f = Image.open(faixa).convert('RGB').resize((1179, 325))
    src.paste(f, (0, 1640))
if len(sys.argv) > 3 and sys.argv[3] == 'humor':
    # círculo oval "à mão" em volta das visualizações, duas voltas levemente desencontradas
    import math
    cx, cy, rx, ry = 140, 1747, 150, 46
    dd = ImageDraw.Draw(src)
    for volta, (dx, dy, k) in enumerate(((0, 0, 1.0), (6, -4, 1.06))):
        pts = [(cx + dx + rx * k * math.cos(a) + 4 * math.sin(3 * a + volta), cy + dy + ry * k * math.sin(a) + 3 * math.cos(2 * a)) for a in [i / 60 * 2 * math.pi * 1.05 for i in range(61)]]
        dd.line(pts, fill=(222, 186, 110), width=6, joint='curve')
# recorta do título até a linha de curtidas
recorte = src.crop((0, 120, 1179, 1930))
LARG = 740 if (len(sys.argv) > 3 and sys.argv[3] == 'humor') else 820
esc = LARG / recorte.width
recorte = recorte.resize((LARG, int(recorte.height * esc)), Image.LANCZOS)
im = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGB')
x, y = (W - recorte.width) // 2, 440
mask = Image.new('L', recorte.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, *recorte.size), 34, fill=255)
sombra = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sombra).rounded_rectangle((x - 4, y - 4, x + recorte.width + 4, y + recorte.height + 4), 38, outline=G + (150,), width=3)
inclina = -3 if len(sys.argv) > 3 and sys.argv[3] == 'humor' else 0
rc = recorte.convert('RGBA'); rc.putalpha(mask)
if inclina:
    rc = rc.rotate(inclina, resample=Image.BICUBIC, expand=True)
    sombra = Image.new('RGBA', (W, H), (0, 0, 0, 0))
im = im.convert('RGBA'); im.alpha_composite(rc, (x - (rc.width - recorte.width) // 2, y - (rc.height - recorte.height) // 2))
im = Image.alpha_composite(im.convert('RGBA'), sombra)
d = ImageDraw.Draw(im)
modo = sys.argv[3] if len(sys.argv) > 3 else 'agradecimento'
if modo == 'humor':
    d.text((W/2, 260), 'Estoicismo?', font=estilo.playfair(66), fill=B, anchor='mm')
    d.text((W/2, 350), 'Quem vai querer saber disso?', font=estilo.playfair(60, True), fill=B, anchor='mm')
    yb = y + recorte.height + 215
    d.text((W/2, yb), 'Spoiler: era sobre a sua vida', font=estilo.playfair(52), fill=B, anchor='mm')
    d.text((W/2, yb + 72), 'o tempo todo.', font=estilo.playfair(56, True), fill=G, anchor='mm')
    # anotação manuscrita com seta apontando para o círculo
    from PIL import ImageFont
    mao = ImageFont.truetype(str(estilo.FONTES / 'Sacramento-Regular.ttf'), 92)
    # seta pela margem esquerda, fora do print, subindo até o círculo
    d.text((290, 1655), 'a prova', font=mao, fill=G, anchor='mm')
    seta = [(185, 1660), (120, 1625), (100, 1540), (125, 1478)]
    d.line(seta, fill=G, width=5, joint='curve')
    d.line([(125, 1478), (100, 1500)], fill=G, width=5); d.line([(125, 1478), (130, 1510)], fill=G, width=5)
else:
    d.text((W/2, 230), '40,6 mil pessoas pararam', font=estilo.playfair(60), fill=B, anchor='mm')
    d.text((W/2, 310), 'para pensar no próprio tempo.', font=estilo.playfair(60, True), fill=G, anchor='mm')
    d.text((W/2, 395), 'Filosofia não é distante. É sobre a sua vida.', font=estilo.playfair(36, True), fill=C, anchor='mm')
    yb = y + recorte.height + 80
    d.text((W/2, yb), 'Obrigada por estarem aqui.', font=estilo.playfair(48, True), fill=B, anchor='mm')
    estilo.texto_espacado(d, (W/2, yb + 80), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(22, 500), C, 6)
im.convert('RGB').save(sys.argv[2])
print('ok', y + recorte.height)
