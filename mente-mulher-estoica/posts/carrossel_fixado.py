"""Carrossel para FIXAR no perfil (quem chega agora): o que é estoicismo, a ideia central (o que depende de mim)
e convite ao Desafio Estoico. Tema escolhido pelos dados de 16-22/11: "controle" (Senna, 20 mil) e capa em diálogo.
Uso: python3 carrossel_fixado.py pasta_saida
"""
import sys
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, personagens, numpy as np
from personagens import ela
from PIL import Image, ImageDraw
from pathlib import Path
W, H = 1080, 1350
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
fundo = np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)[285:285 + H]
P = estilo.playfair
N = 5
def tela(n):
    im = Image.fromarray(fundo).convert('RGBA'); d = ImageDraw.Draw(im)
    d.text((W/2, H - 70), f'{n}/{N}', font=P(26), fill=C, anchor='mm')
    return im, d
def bloco(d, y, linhas, f, cor, alt):
    for i, l in enumerate(linhas): d.text((W/2, y + i * alt), l, font=f, fill=cor, anchor='mm')
def traco(d, y): d.line([(W/2 - 50, y), (W/2 + 50, y)], fill=G, width=2)
def bonequinha(im, x, y, k=1.5, **kw):
    cen = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ela(ImageDraw.Draw(cen, 'RGBA'), 540, 760, 1.0, **kw)
    cen = cen.resize((int(W * k), int(H * k)), Image.BICUBIC)
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.paste(cen, (int(x - 540 * k), int(y - 760 * k)))
    return Image.alpha_composite(im, cam)

# 1. capa
im, d = tela(1)
estilo.texto_espacado(d, (W/2, 170), 'COMECE POR AQUI', estilo.sem_serifa(36, 600), G, 10)
bloco(d, 330, ['Você reage', 'ou responde?'], P(92), B, 112)
im = bonequinha(im, W/2, 1130, emo=dict(sorriso=0.5))
d = ImageDraw.Draw(im)
d.text((W/2, 1185), 'arrasta para o lado →', font=P(32, True), fill=C, anchor='mm')
im.convert('RGB').save(out / '1.png')

# 2. o que é
im, d = tela(2)
estilo.texto_espacado(d, (W/2, 330), 'O QUE É ESTOICISMO?', estilo.sem_serifa(34, 600), G, 8)
bloco(d, 500, ['Uma filosofia de mais de', '2 mil anos para viver', 'com mais calma e clareza.'], P(62), B, 86)
traco(d, 760)
bloco(d, 870, ['Não é ser fria.', 'É ser consciente.'], P(64, True), G, 88)
im.convert('RGB').save(out / '2.png')

# 3. a ideia central
im, d = tela(3)
bloco(d, 330, ['A ideia central:'], P(56), C, 0)
x1, x2, y0 = 290, 790, 520
d.rounded_rectangle((x1 - 220, y0, x1 + 220, y0 + 420), radius=36, outline=G, width=4)
d.rounded_rectangle((x2 - 220, y0, x2 + 220, y0 + 420), radius=36, outline=C, width=3)
d.text((x1, y0 + 70), 'Depende', font=P(48, True), fill=G, anchor='mm'); d.text((x1, y0 + 130), 'de mim', font=P(48, True), fill=G, anchor='mm')
d.text((x2, y0 + 70), 'Não depende', font=P(46), fill=C, anchor='mm'); d.text((x2, y0 + 130), 'de mim', font=P(46), fill=C, anchor='mm')
for i, s in enumerate(['minhas escolhas', 'minhas palavras', 'meus limites']):
    d.text((x1, y0 + 220 + i * 56), s, font=estilo.sem_serifa(34, 500), fill=B, anchor='mm')
for i, s in enumerate(['o que pensam', 'o que fazem', 'o passado']):
    d.text((x2, y0 + 220 + i * 56), s, font=estilo.sem_serifa(34, 500), fill=(170, 168, 175), anchor='mm')
d.text((W/2, 1080), 'Epicteto, Encheirídion, 1', font=P(30, True), fill=C, anchor='mm')
im.convert('RGB').save(out / '3.png')

# 4. o que tem aqui
im, d = tela(4)
estilo.texto_espacado(d, (W/2, 330), 'POR AQUI VOCÊ ENCONTRA', estilo.sem_serifa(34, 600), G, 8)
for i, s in enumerate(['Relações e limites', 'Autoconhecimento', 'Inteligência emocional', 'Fé e recomeços']):
    d.text((W/2, 500 + i * 120), s, font=P(62), fill=B, anchor='mm')
    d.ellipse((W/2 - 8, 556 + i * 120, W/2 + 8, 572 + i * 120), fill=G) if i < 3 else None
d.text((W/2, 1030), 'Filosofia antiga para a vida de hoje.', font=P(44, True), fill=G, anchor='mm')
im.convert('RGB').save(out / '4.png')

# 5. convite
im, d = tela(5)
bloco(d, 380, ['E você?', 'Reage ou responde?'], P(78), B, 100)
traco(d, 570)
bloco(d, 680, ['Faça o Desafio Estoico:', '5 situações do dia a dia', 'e o seu resultado.'], P(56), B, 76)
d.rounded_rectangle((W/2 - 230, 930, W/2 + 230, 1030), radius=50, fill=G)
d.text((W/2, 980), 'Link na bio', font=P(54, True), fill=(30, 24, 16), anchor='mm')
estilo.texto_espacado(d, (W/2, 1150), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(26, 500), C, 6)
im.convert('RGB').save(out / '5.png')
print('ok')
