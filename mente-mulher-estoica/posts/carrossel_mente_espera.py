"""Carrossel: 6 mecanismos da mente que fazem a gente esperar em vez de começar.
Formato (um conceito por tela, título em caixa alta, fecho "não basta... é preciso") inspirado em @unvellum.
Tema escolhido pelos dados de 09-22/11: "Põe o pé que Deus coloca o chão" (778 envios) e Senna (358 envios).
Uso: python3 carrossel_mente_espera.py pasta_saida
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
P, S = estilo.playfair, estilo.sem_serifa
N = 9

def quebra(s, f, larg):
    linhas, cur = [], ''
    for p in s.split():
        t = (cur + ' ' + p).strip()
        if f.getlength(t) <= larg: cur = t
        else: linhas.append(cur); cur = p
    return linhas + [cur]

def tela(n):
    im = Image.fromarray(fundo).convert('RGBA'); d = ImageDraw.Draw(im)
    d.text((W / 2, H - 70), f'{n}/{N}', font=P(26), fill=C, anchor='mm')
    return im, d

def conceito(n, num, titulo, texto, fonte):
    im, d = tela(n)
    d.text((W / 2, 300), num, font=P(120, True), fill=G + (90,), anchor='mm')
    estilo.texto_espacado(d, (W / 2, 420), titulo, S(40, 600), G, 8)
    d.line([(W / 2 - 50, 480), (W / 2 + 50, 480)], fill=G, width=2)
    f = P(54); y = 580
    for l in quebra(texto, f, 860):
        d.text((W / 2, y), l, font=f, fill=B, anchor='mm'); y += 78
    d.text((W / 2, 1160), fonte, font=P(28, True), fill=C, anchor='mm')
    im.convert('RGB').save(out / f'{n}.png')

# 1. capa
im, d = tela(1)
estilo.texto_espacado(d, (W / 2, 250), 'MENTE E AÇÃO', S(34, 600), G, 10)
y = 470
for l in ['Se você entender', 'essas 6 coisas,', 'para de esperar', 'o momento perfeito', 'para começar.']:
    cor, f = (G, P(80, True)) if l.startswith(('para de', 'o momento')) else (B, P(80))
    d.text((W / 2, y), l, font=f, fill=cor, anchor='mm'); y += 104
d.text((W / 2, 1120), 'arrasta para o lado →', font=P(32, True), fill=C, anchor='mm')
im.convert('RGB').save(out / '1.png')

conceito(2, '01', 'VIÉS DO STATUS QUO',
         'Seu cérebro prefere o conhecido, mesmo quando o conhecido não está bom. Mudar parece risco. Ficar parece seguro, mas nem sempre é.',
         'Samuelson e Zeckhauser, 1988')
conceito(3, '02', 'AVERSÃO À PERDA',
         'Perder dói mais do que ganhar alegra. Por isso você pesa tudo o que pode dar errado e esquece o que pode dar certo.',
         'Kahneman e Tversky, 1979')
conceito(4, '03', 'PROCRASTINAÇÃO',
         'Não é preguiça. É fuga de um desconforto. Você adia a tarefa para adiar a emoção que ela traz.',
         'Sirois e Pychyl, 2013')
conceito(5, '04', 'EFEITO HOLOFOTE',
         'Você acha que todos vão reparar no seu erro. Quase ninguém repara tanto quanto você imagina.',
         'Gilovich, Medvec e Savitsky, 2000')
conceito(6, '05', 'RUMINAÇÃO',
         'Pensar de novo no mesmo problema parece resolver. Mas só alimenta a ansiedade. Pensar demais não é planejar.',
         'Nolen-Hoeksema, 2000')
conceito(7, '06', 'AÇÃO ANTES DA VONTADE',
         'Você espera a motivação para agir. Muitas vezes é agir que traz a motivação. O primeiro passo vem antes da vontade.',
         'Ativação comportamental, Martell, Addis e Jacobson, 2001')

# 8. não basta... é preciso
im, d = tela(8)
y = 330
for a, b in [('Não basta reconhecer o medo.', 'É preciso dar um passo com ele.'),
             ('Não basta entender a procrastinação.', 'É preciso acolher o desconforto.'),
             ('Não basta planejar.', 'É preciso começar pequeno.')]:
    d.text((W / 2, y), a, font=P(50), fill=B, anchor='mm')
    d.text((W / 2, y + 68), b, font=P(50, True), fill=G, anchor='mm')
    y += 250
im.convert('RGB').save(out / '8.png')

# 9. fecho
im, d = tela(9)
d.text((W / 2, 400), '“Enquanto adiamos,', font=P(72, True), fill=B, anchor='mm')
d.text((W / 2, 495), 'a vida passa.”', font=P(72, True), fill=G, anchor='mm')
d.text((W / 2, 590), 'Sêneca, Cartas a Lucílio, 1.3', font=P(32, True), fill=C, anchor='mm')
d.line([(W / 2 - 50, 680), (W / 2 + 50, 680)], fill=G, width=2)
for i, l in enumerate(['Envie para alguém que vive', 'esperando o momento certo.']):
    d.text((W / 2, 790 + i * 76), l, font=P(54), fill=B, anchor='mm')
estilo.texto_espacado(d, (W / 2, 1060), '@MENTE_MULHER_ESTOICA', S(26, 500), C, 6)
d.text((W / 2, 1180), 'Formato inspirado em @unvellum', font=S(22, 500), fill=C, anchor='mm')
im.convert('RGB').save(out / '9.png')
print('ok')
