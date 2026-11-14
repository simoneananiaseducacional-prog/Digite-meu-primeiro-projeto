"""Story: a porta (frase do filme Matrix, 1999, dita por Morpheus) com a personagem fixa diante de uma porta de luz.
Uso: python3 story_porta.py saida.png
"""
import sys, math
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, numpy as np
from personagens import ela
from PIL import Image, ImageDraw, ImageFilter
W, H = 1080, 1920
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
im = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
# luz saindo da porta entreaberta
luz = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(luz)
dl.polygon([(566, 1236), (700, 1236), (520, 1240), (300, 1240)], fill=G + (90,))
dl.ellipse((380, 1215, 720, 1265), fill=G + (70,))
luz = luz.filter(ImageFilter.GaussianBlur(30)); im = Image.alpha_composite(im, luz)
d = ImageDraw.Draw(im)
# porta: batente, vão iluminado, folha entreaberta
d.rectangle((560, 820, 760, 1240), outline=B + (255,), width=4)
d.rectangle((566, 826, 700, 1236), fill=(235, 205, 140, 255))
d.polygon([(700, 826), (760, 800), (760, 1268), (700, 1236)], fill=(22, 21, 19, 255), outline=B + (255,))
d.ellipse((738, 1030, 748, 1040), fill=G + (255,))
d.line([(80, 1240), (1000, 1240)], fill=C + (255,), width=4)
ela(d, 380, 1240, 1.0, braco=0.7, lado=1)
d.text((W/2, 330), 'Ninguém pode libertar', font=estilo.playfair(60), fill=B, anchor='mm')
d.text((W/2, 410), 'a sua mente por você.', font=estilo.playfair(60), fill=B, anchor='mm')
d.text((W/2, 520), 'Podem te mostrar a porta.', font=estilo.playfair(56, True), fill=G, anchor='mm')
d.text((W/2, 595), 'Atravessar é com você.', font=estilo.playfair(56, True), fill=G, anchor='mm')
d.text((W/2, 1390), '“Ninguém é livre se não for senhor de si.”', font=estilo.playfair(40, True), fill=G, anchor='mm')
d.text((W/2, 1450), 'Epicteto, Fragmentos, 35', font=estilo.playfair(30, True), fill=C, anchor='mm')
estilo.texto_espacado(d, (W/2, 1620), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(22, 500), C, 6)
im.convert('RGB').save(sys.argv[1]); print('ok')
