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
# desfoca as fotos de quem compartilhou (faixa dos avatares)
box = (30, 1370, 620, 1630)
src.paste(src.crop(box).filter(ImageFilter.GaussianBlur(22)), box[:2])
# cobre a faixa de insights e 'Turbinar post' (visível só para a dona da conta)
ImageDraw.Draw(src).rectangle((0, 1650, 1179, 1790), fill=src.getpixel((600, 1640)))
# recorta do título até a linha de curtidas
recorte = src.crop((0, 120, 1179, 1910))
esc = 820 / recorte.width
recorte = recorte.resize((820, int(recorte.height * esc)), Image.LANCZOS)
im = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGB')
x, y = (W - recorte.width) // 2, 450
mask = Image.new('L', recorte.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, *recorte.size), 34, fill=255)
sombra = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sombra).rounded_rectangle((x - 4, y - 4, x + recorte.width + 4, y + recorte.height + 4), 38, outline=G + (150,), width=3)
im.paste(recorte, (x, y), mask)
im = Image.alpha_composite(im.convert('RGBA'), sombra)
d = ImageDraw.Draw(im)
modo = sys.argv[3] if len(sys.argv) > 3 else 'agradecimento'
if modo == 'humor':
    d.text((W/2, 260), 'Estoicismo?', font=estilo.playfair(66), fill=B, anchor='mm')
    d.text((W/2, 350), 'Quem vai querer saber disso?', font=estilo.playfair(60, True), fill=B, anchor='mm')
    yb = y + recorte.height + 75
    d.text((W/2, yb), 'Eu, três posts depois:', font=estilo.playfair(48), fill=B, anchor='mm')
    d.text((W/2, yb + 70), 'Sêneca, precisamos conversar.', font=estilo.playfair(56, True), fill=G, anchor='mm')
else:
    d.text((W/2, 230), '40,6 mil pessoas pararam', font=estilo.playfair(60), fill=B, anchor='mm')
    d.text((W/2, 310), 'para pensar no próprio tempo.', font=estilo.playfair(60, True), fill=G, anchor='mm')
    d.text((W/2, 395), 'Filosofia não é distante. É sobre a sua vida.', font=estilo.playfair(36, True), fill=C, anchor='mm')
    yb = y + recorte.height + 80
    d.text((W/2, yb), 'Obrigada por estarem aqui.', font=estilo.playfair(48, True), fill=B, anchor='mm')
    estilo.texto_espacado(d, (W/2, yb + 80), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(22, 500), C, 6)
im.convert('RGB').save(sys.argv[2])
print('ok', y + recorte.height)
