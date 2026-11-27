"""Story com foto da Simone e frase sobre faixa escura na parte de baixo.
Uso: python3 story_foto_frase.py foto.jpg saida.png "linha|*linha dourada*"  (a foto não entra no repositório)
"""
import sys
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, numpy as np
from PIL import Image, ImageDraw, ImageOps
W, H = 1080, 1920
B = (245, 240, 232); G = (214, 178, 108)
im = ImageOps.exif_transpose(Image.open(sys.argv[1])).convert('RGB')
esc = max(W / im.width, H / im.height); im = im.resize((int(im.width * esc) + 1, int(im.height * esc) + 1), Image.LANCZOS)
im = im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width - W) // 2 + W, (im.height - H) // 2 + H))
f = np.asarray(im, np.float32)
yy = np.arange(H)[:, None, None]
f *= np.clip(1 - 0.82 * np.clip((yy - 1080) / 420, 0, 1), 0.18, 1)
im = Image.fromarray(np.clip(f, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(im)
linhas = sys.argv[3].split('|'); y = 1430
for l in linhas:
    dour = l.startswith('*'); fo = estilo.playfair(66, dour)
    d.text((W/2 + 2, y + 3), l.strip('*'), font=fo, fill=(0, 0, 0), anchor='mm')
    d.text((W/2, y), l.strip('*'), font=fo, fill=G if dour else B, anchor='mm'); y += 82
estilo.texto_espacado(d, (W/2, y + 30), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(20, 500), (200, 195, 188), 6)
im.save(sys.argv[2]); print('ok')
