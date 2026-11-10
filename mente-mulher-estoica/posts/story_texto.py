"""Story só de texto, fundo preto, serifa centralizada, destaque em itálico dourado (modelo do grid da Simone).
Uso: python3 story_texto.py saida.png "linha|*linha dourada*||linha após espaço" ["fonte"]
"""
import sys
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, numpy as np
from PIL import Image, ImageDraw
W, H = 1080, 1920
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
linhas = sys.argv[2].split('|'); fonte = sys.argv[3] if len(sys.argv) > 3 else ''
im = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGB')
d = ImageDraw.Draw(im)
ALT, ESP = 78, 60
altura = sum(ESP if l == '' else ALT for l in linhas)
y = H / 2 - altura / 2 - 60
for l in linhas:
    if l == '': y += ESP; continue
    dour = l.startswith('*')
    d.text((W/2, y), l.strip('*'), font=estilo.playfair(56, dour), fill=G if dour else B, anchor='mm'); y += ALT
if fonte:
    d.text((W/2, y + 50), fonte, font=estilo.playfair(30, True), fill=C, anchor='mm')
estilo.texto_espacado(d, (W/2, 1600), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(22, 500), C, 6)
im.save(sys.argv[1]); print('ok')
