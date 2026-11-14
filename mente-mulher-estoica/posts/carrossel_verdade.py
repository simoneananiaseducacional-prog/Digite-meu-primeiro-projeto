"""Carrossel 7 telas: você quer ter razão ou descobrir a verdade? (Marco Aurélio, Meditações 6.21)
Uso: python3 carrossel_verdade.py pasta_saida
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
def tela(n):
    im = Image.fromarray(fundo).convert('RGB'); d = ImageDraw.Draw(im)
    d.text((W/2, H - 70), f'{n}/7', font=estilo.playfair(26), fill=C, anchor='mm')
    d.line([(W/2 - 40, 110), (W/2 + 40, 110)], fill=G, width=2)
    return im, d
def bloco(d, y, linhas, f, cor, alt):
    for i, l in enumerate(linhas):
        d.text((W/2, y + i * alt), l, font=f, fill=cor, anchor='mm')

im, d = tela(1)
bloco(d, 560, ['VOCÊ QUER', 'TER RAZÃO'], estilo.playfair(96), B, 115)
d.text((W/2, 790), 'ou descobrir a verdade?', font=estilo.playfair(78, True), fill=G, anchor='mm')
im.save(out / '1.png')

im, d = tela(2)
bloco(d, 500, ['Às vezes, alguém questiona', 'uma ideia nossa e,', 'antes mesmo de ouvir,'], estilo.playfair(56), B, 80)
bloco(d, 790, ['começamos a preparar', 'a defesa.'], estilo.playfair(60, True), G, 82)
im.save(out / '2.png')

im, d = tela(3)
bloco(d, 520, ['Mas existe uma diferença', 'entre defender', 'uma convicção'], estilo.playfair(58), B, 82)
bloco(d, 800, ['e se recusar', 'a examiná-la.'], estilo.playfair(66, True), G, 88)
im.save(out / '3.png')

im, d = tela(4)
d.text((W/2, 330), '“', font=estilo.playfair(180), fill=G, anchor='mm')
bloco(d, 480, ['Marco Aurélio escreveu que', 'mudaria de opinião ou de conduta', 'com satisfação se alguém', 'demonstrasse seu erro.'], estilo.playfair(48), B, 70)
bloco(d, 820, ['Porque o compromisso dele', 'era com a verdade.'], estilo.playfair(56, True), G, 78)
d.text((W/2, 1010), 'Meditações, VI, 21. Paráfrase.', font=estilo.playfair(30, True), fill=C, anchor='mm')
im.save(out / '4.png')

im, d = tela(5)
bloco(d, 470, ['Isso não significa', 'concordar com qualquer crítica.'], estilo.playfair(54), B, 78)
bloco(d, 720, ['Significa avaliar os argumentos', 'sem transformar toda discordância', 'em ataque pessoal.'], estilo.playfair(50, True), G, 74)
im.save(out / '5.png')

im, d = tela(6)
bloco(d, 330, ['Na próxima conversa difícil,', 'experimente perguntar:'], estilo.playfair(54), B, 78)
perguntas = [['O que exatamente', 'está sendo questionado?'], ['Que evidências', 'sustentam essa crítica?'], ['Existe algo que', 'preciso rever?']]
for i, p in enumerate(perguntas):
    y = 560 + i * 190
    d.text((170, y + 30), str(i + 1), font=estilo.playfair(90, True), fill=G, anchor='mm')
    d.line([(225, y - 15), (225, y + 85)], fill=G, width=2)
    for j, l in enumerate(p):
        d.text((260, y + j * 64), l, font=estilo.playfair(50, True), fill=B, anchor='lm')
im.save(out / '6.png')

im, d = tela(7)
bloco(d, 520, ['Maturidade não é', 'nunca estar errado.'], estilo.playfair(66), B, 90)
bloco(d, 770, ['É ter discernimento para', 'reconhecer quando', 'precisamos mudar.'], estilo.playfair(56, True), G, 78)
estilo.texto_espacado(d, (W/2, 1130), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(26, 500), C, 6)
im.save(out / '7.png')
print('ok')
