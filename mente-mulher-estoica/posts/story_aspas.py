"""Story no modelo 'Prefiro desagradar...': fundo preto, aspas douradas grandes, sem serifa grossa à esquerda,
linhas finais em dourado, fonte pequena e assinatura. Uso:
python3 story_aspas.py saida.png "linha|linha|*linha dourada*" "fonte linha 1|fonte linha 2"
"""
import sys
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, numpy as np
from PIL import Image, ImageDraw
W, H = 1080, 1920
B = (240, 236, 228); G = (196, 160, 92); C = (150, 146, 140)
linhas = sys.argv[2].split('|'); fonte = sys.argv[3].split('|') if len(sys.argv) > 3 else []
im = Image.new('RGB', (W, H), (10, 10, 10)); d = ImageDraw.Draw(im)
X = 95; ALT = 98
f = estilo.sem_serifa(80, 800)
y = H / 2 - len(linhas) * ALT / 2 + 40
d.text((X - 8, y - 250), '“', font=estilo.sem_serifa(300, 900), fill=G, anchor='lt')
for l in linhas:
    dour = l.startswith('*')
    d.text((X, y), l.strip('*'), font=f, fill=G if dour else B, anchor='lm'); y += ALT
y += 40
for i, l in enumerate(fonte):
    d.text((X, y + i * 46), l, font=estilo.sem_serifa(32, 500 if i == 0 else 400), fill=C if i else B, anchor='lm')
d.text((X, H - 330), 'Mente Mulher Estoica', font=estilo.sem_serifa(34, 700), fill=B, anchor='lm')
d.text((X, H - 285), '@mente_mulher_estoica', font=estilo.sem_serifa(28, 400), fill=C, anchor='lm')
im.save(sys.argv[1]); print('ok')
