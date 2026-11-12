"""Carrossel 6 telas: Senna e o estoicismo (sem fotos dele; desenho próprio de capacete e pista).
Uso: python3 carrossel_senna.py pasta_saida
"""
import sys, math
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, numpy as np
from PIL import Image, ImageDraw
from pathlib import Path
W, H = 1080, 1350
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
fundo = np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)[285:285 + H]
def tela(n):
    im = Image.fromarray(fundo).convert('RGB'); d = ImageDraw.Draw(im)
    d.text((W/2, H - 70), f'{n}/6', font=estilo.playfair(26), fill=C, anchor='mm')
    return im, d
def bloco(d, y, linhas, f, cor, alt):
    for i, l in enumerate(linhas): d.text((W/2, y + i * alt), l, font=f, fill=cor, anchor='mm')
def capacete(d, cx, cy, s=1.0):
    # casco
    d.chord((cx - 170 * s, cy - 150 * s, cx + 170 * s, cy + 170 * s), 180, 360, outline=G, width=5)
    d.line([(cx - 170 * s, cy + 10 * s), (cx - 170 * s, cy + 90 * s), (cx + 150 * s, cy + 90 * s), (cx + 170 * s, cy + 10 * s)], fill=G, width=5, joint='curve')
    # viseira
    d.rounded_rectangle((cx - 40 * s, cy - 55 * s, cx + 165 * s, cy + 15 * s), 26, outline=G, width=5)
    # faixa
    d.arc((cx - 150 * s, cy - 130 * s, cx + 150 * s, cy + 150 * s), 200, 300, fill=G, width=3)
def pista(d, y):
    pts = [(80 + i * 10, y + 30 * math.sin(i / 14)) for i in range(93)]
    for i in range(0, 92, 3): d.line(pts[i:i + 2], fill=C, width=3)

im, d = tela(1)
capacete(d, W/2, 470); pista(d, 700)
bloco(d, 860, ['Ayrton Senna viveu', 'só 34 anos.'], estilo.playfair(70), B, 88)
d.text((W/2, 1060), 'Mas não desperdiçou um dia.', font=estilo.playfair(60, True), fill=G, anchor='mm')
im.save(out / '1.png')

im, d = tela(2)
bloco(d, 430, ['Treinava até a exaustão.', 'Conhecia cada curva', 'antes de correr.'], estilo.playfair(62), B, 82)
d.line([(W/2 - 50, 680), (W/2 + 50, 680)], fill=G, width=2)
bloco(d, 790, ['“Nenhuma grande coisa', 'nasce de repente.”'], estilo.playfair(58, True), G, 78)
d.text((W/2, 960), 'Epicteto, Discursos, 1.15', font=estilo.playfair(32, True), fill=C, anchor='mm')
im.save(out / '2.png')

im, d = tela(3)
bloco(d, 400, ['Dava tudo de si.', 'Mas o carro, a chuva', 'e a sorte', 'não dependiam dele.'], estilo.playfair(62), B, 82)
d.line([(W/2 - 50, 720), (W/2 + 50, 720)], fill=G, width=2)
bloco(d, 830, ['“Algumas coisas dependem', 'de nós; outras, não.”'], estilo.playfair(56, True), G, 76)
d.text((W/2, 1000), 'Epicteto, Encheirídion, 1', font=estilo.playfair(32, True), fill=C, anchor='mm')
im.save(out / '3.png')

im, d = tela(4)
d.text((W/2, 300), 'UM CUIDADO', font=estilo.sem_serifa(30, 600), fill=G, anchor='mm')
bloco(d, 430, ['Muitas frases atribuídas', 'a ele não têm fonte.'], estilo.playfair(60), B, 80)
bloco(d, 650, ['“Vencer sem risco', 'é triunfar sem glória”'], estilo.playfair(54, True), C, 72)
bloco(d, 840, ['é de Pierre Corneille,', 'na peça O Cid, de 1637.'], estilo.playfair(54), B, 72)
d.text((W/2, 1040), 'Admirar alguém também é cuidar da verdade sobre ele.', font=estilo.playfair(34, True), fill=G, anchor='mm')
im.save(out / '4.png')

im, d = tela(5)
bloco(d, 520, ['“Não recebemos', 'uma vida curta.'], estilo.playfair(72), B, 92)
d.text((W/2, 730), 'Nós a tornamos curta.”', font=estilo.playfair(72, True), fill=G, anchor='mm')
d.text((W/2, 880), 'Sêneca, Sobre a brevidade da vida, 1', font=estilo.playfair(34, True), fill=C, anchor='mm')
im.save(out / '5.png')

im, d = tela(6)
bloco(d, 480, ['Se a sua vida', 'fosse curta como a dele,'], estilo.playfair(62), B, 82)
bloco(d, 700, ['em que você pararia', 'de desperdiçar tempo?'], estilo.playfair(62, True), G, 82)
estilo.texto_espacado(d, (W/2, 1120), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(26, 500), C, 6)
im.save(out / '6.png')
print('ok')
