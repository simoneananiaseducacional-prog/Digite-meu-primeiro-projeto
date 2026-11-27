"""Post único para fixar no perfil: o que é estoicismo em uma linha + convite ao Desafio Estoico.
Uso: python3 post_fixado.py saida.png
"""
import sys
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, numpy as np
from personagens import ela
from PIL import Image, ImageDraw
W, H = 1080, 1350
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
P = estilo.playfair
im = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)[285:285 + H]).convert('RGBA')
d = ImageDraw.Draw(im)
estilo.texto_espacado(d, (W/2, 150), 'ESTOICISMO', estilo.sem_serifa(34, 600), G, 12)
d.text((W/2, 300), 'Você reage', font=P(96), fill=B, anchor='mm')
d.text((W/2, 415), 'ou responde?', font=P(96, True), fill=G, anchor='mm')
d.text((W/2, 540), 'Uma filosofia para viver com mais', font=P(42), fill=(215, 210, 202), anchor='mm')
d.text((W/2, 595), 'calma, clareza e consciência.', font=P(42), fill=(215, 210, 202), anchor='mm')
k = 1.3
cen = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ela(ImageDraw.Draw(cen, 'RGBA'), 540, 760, 1.0, emo=dict(sorriso=0.5))
cen = cen.resize((int(W * k), int(H * k)), Image.BICUBIC)
cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.paste(cen, (int(W/2 - 540 * k), int(1010 - 760 * k)))
im = Image.alpha_composite(im, cam); d = ImageDraw.Draw(im)
d.rounded_rectangle((W/2 - 300, 1080, W/2 + 300, 1190), radius=55, fill=G)
d.text((W/2, 1135), 'Faça o teste • link na bio', font=P(46, True), fill=(30, 24, 16), anchor='mm')
estilo.texto_espacado(d, (W/2, 1280), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(24, 500), C, 6)
im.convert('RGB').save(sys.argv[1], quality=95)
print('ok')
