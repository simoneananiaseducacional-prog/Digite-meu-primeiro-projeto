"""Design de STORY (diferente do feed): papel creme com textura, tinta preta, detalhe dourado escuro,
anotação manuscrita. O feed (Mapas da mente) continua preto e dourado.
Uso: python3 story_papel.py saida.png
"""
import sys
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, numpy as np
import personagens as P
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H = 1080, 1920
PAPEL = (239, 232, 220); TINTA = (28, 26, 24); OURO = (150, 116, 52); CINZA = (110, 104, 96)
rng = np.random.default_rng(3)
base = np.ones((H, W, 3), np.float32) * PAPEL
base += rng.normal(0, 6, (H, W, 1)); base += np.asarray(Image.fromarray((rng.random((H // 8, W // 8)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32)[..., None] * 0.04 - 5
yy, xx = np.mgrid[0:H, 0:W]
base *= (1 - 0.18 * (((xx - W/2) / (W/2)) ** 2 + ((yy - H/2) / (H/2)) ** 2) / 2)[..., None]
im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert('RGBA')
d = ImageDraw.Draw(im)
mao = ImageFont.truetype(str(estilo.FONTES / 'Sacramento-Regular.ttf'), 70)
# personagens em tinta sobre papel
P.DOURADO = TINTA; P.CABELO = TINTA; P.ROSTO = PAPEL
# porta em tinta, com o vão em dourado claro
d.rectangle((580, 830, 770, 1230), outline=TINTA, width=4)
d.rectangle((586, 836, 712, 1226), fill=(226, 196, 132))
d.polygon([(712, 836), (770, 812), (770, 1256), (712, 1226)], fill=PAPEL, outline=TINTA)
d.ellipse((748, 1030, 758, 1040), fill=TINTA)
for i in range(0, 900, 14):   # chão em traço de caneta
    d.line([(90 + i, 1230 + (i % 28 == 0)), (98 + i, 1230)], fill=TINTA, width=3)
P.ela(d, 390, 1230, 1.0, braco=0.7, lado=1)
d.text((W/2, 300), 'Ninguém pode libertar', font=estilo.playfair(60), fill=TINTA, anchor='mm')
d.text((W/2, 380), 'a sua mente por você.', font=estilo.playfair(60), fill=TINTA, anchor='mm')
d.text((W/2, 490), 'Podem te mostrar a porta.', font=estilo.playfair(56, True), fill=OURO, anchor='mm')
d.text((W/2, 565), 'Atravessar é com você.', font=estilo.playfair(56, True), fill=OURO, anchor='mm')
d.line([(W/2 - 60, 640), (W/2 + 60, 640)], fill=OURO, width=2)
d.text((W/2, 1380), '“Ninguém é livre se não for senhor de si.”', font=estilo.playfair(40, True), fill=TINTA, anchor='mm')
d.text((W/2, 1440), 'Epicteto, Fragmentos, 35', font=estilo.playfair(30, True), fill=CINZA, anchor='mm')
d.text((820, 760), 'a sua', font=mao, fill=OURO, anchor='mm')
d.line([(800, 790), (775, 840)], fill=OURO, width=3); d.line([(775, 840), (770, 815)], fill=OURO, width=3); d.line([(775, 840), (795, 830)], fill=OURO, width=3)
estilo.texto_espacado(d, (W/2, 1620), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(22, 500), CINZA, 6)
im.convert('RGB').save(sys.argv[1]); print('ok')
