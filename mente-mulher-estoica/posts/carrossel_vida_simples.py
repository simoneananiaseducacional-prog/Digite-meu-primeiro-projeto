"""Carrossel 6 telas: vida simples e silêncio por dentro (Epicteto, Encheirídion 33; Sêneca, Cartas 56).
Uso: python3 carrossel_vida_simples.py pasta_saida
"""
import sys
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, numpy as np
from PIL import Image, ImageDraw
from pathlib import Path
W, H = 1080, 1350
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
fundo = np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)[285:285 + H]
P = estilo.playfair
def tela(n):
    im = Image.fromarray(fundo).convert('RGB'); d = ImageDraw.Draw(im)
    d.text((W/2, H - 70), f'{n}/6', font=P(26), fill=C, anchor='mm')
    return im, d
def bloco(d, y, linhas, f, cor, alt):
    for i, l in enumerate(linhas): d.text((W/2, y + i * alt), l, font=f, fill=cor, anchor='mm')
def traco(d, y): d.line([(W/2 - 50, y), (W/2 + 50, y)], fill=G, width=2)

im, d = tela(1)
bloco(d, 560, ['A paz parece tédio'], P(76), B, 0)
bloco(d, 680, ['para quem se acostumou', 'ao caos.'], P(70, True), G, 90)
im.save(out / '1.png')

im, d = tela(2)
bloco(d, 470, ['Caminhar. Ler.', 'Beber água. Dormir bem.', 'Estar com quem importa.'], P(62), B, 86)
traco(d, 760)
bloco(d, 870, ['Parece pouco.', 'É o que sustenta tudo.'], P(60, True), G, 80)
im.save(out / '2.png')

im, d = tela(3)
bloco(d, 470, ['Nem toda discussão', 'merece a sua resposta.'], P(64), B, 86)
traco(d, 680)
bloco(d, 790, ['“Fique em silêncio na maior', 'parte do tempo, ou diga', 'só o necessário.”'], P(52, True), G, 72)
d.text((W/2, 1040), 'Epicteto, Encheirídion, 33 (tradução livre)', font=P(30, True), fill=C, anchor='mm')
im.save(out / '3.png')

im, d = tela(4)
bloco(d, 520, ['A vida não precisa', 'ser barulhenta'], P(72), B, 94)
d.text((W/2, 760), 'para ter significado.', font=P(70, True), fill=G, anchor='mm')
im.save(out / '4.png')

im, d = tela(5)
bloco(d, 500, ['“De nada adianta', 'o silêncio do lugar'], P(66), B, 88)
bloco(d, 710, ['se as emoções', 'fazem barulho.”'], P(66, True), G, 88)
d.text((W/2, 940), 'Sêneca, Cartas a Lucílio, 56 (tradução livre)', font=P(30, True), fill=C, anchor='mm')
im.save(out / '5.png')

im, d = tela(6)
bloco(d, 560, ['Qual barulho', 'você vai deixar'], P(68), B, 90)
d.text((W/2, 760), 'de ouvir hoje?', font=P(70, True), fill=G, anchor='mm')
estilo.texto_espacado(d, (W/2, 1120), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(26, 500), C, 6)
im.save(out / '6.png')
print('ok')
