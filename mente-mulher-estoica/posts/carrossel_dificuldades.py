"""Carrossel 6 telas: as dificuldades revelam quem somos. Capa em diálogo com as personagens da página.
Fontes: Sêneca, Sobre a providência, 5.10; Epicteto, Discursos, 1.24.1.
Formato inspirado em @o_caminho_da_sabedoria (capa em diálogo + telas de texto).
Uso: python3 carrossel_dificuldades.py pasta_saida
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
def tela(n):
    im = Image.fromarray(fundo).convert('RGBA'); d = ImageDraw.Draw(im)
    d.text((W/2, H - 70), f'{n}/6', font=P(26), fill=C, anchor='mm')
    return im, d
def bloco(d, y, linhas, f, cor, alt):
    for i, l in enumerate(linhas): d.text((W/2, y + i * alt), l, font=f, fill=cor, anchor='mm')
def traco(d, y): d.line([(W/2 - 50, y), (W/2 + 50, y)], fill=G, width=2)
def balao(d, cx, cy, linhas, f, ponta):
    w = max(f.getlength(l) for l in linhas) + 70; h = 70 * len(linhas) + 30
    d.rounded_rectangle((cx - w/2, cy - h/2, cx + w/2, cy + h/2), radius=36, fill=(236, 232, 224))
    d.polygon([(cx + ponta * 20 - 16, cy + h/2 - 2), (cx + ponta * 20 + 16, cy + h/2 - 2), (cx + ponta * 40, cy + h/2 + 34)], fill=(236, 232, 224))
    for i, l in enumerate(linhas):
        d.text((cx, cy - h/2 + 50 + i * 70), l, font=f, fill=(24, 22, 20), anchor='mm')

# 1. capa: diálogo entre duas mulheres
im, d = tela(1)
estilo.texto_espacado(d, (W/2, 150), 'ESTOICISMO', estilo.sem_serifa(40, 600), G, 12)
cen = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dc = ImageDraw.Draw(cen, 'RGBA')
ela(dc, 380, 760, 1.0, braco=0.4, lado=1, emo=dict(sorriso=0.5))
ouro = personagens.DOURADO; personagens.DOURADO = (175, 175, 182)
ela(dc, 700, 760, 1.0, braco=0.0, lado=-1, t=1.3, emo=dict(aberta=0.4))
personagens.DOURADO = ouro
K = 1.45
cen = cen.resize((int(W * K), int(H * K)), Image.BICUBIC)
cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.paste(cen, (int(W/2 - 540 * K), int(1050 - 760 * K)))
im = Image.alpha_composite(im, cam); d = ImageDraw.Draw(im)
f = estilo.sem_serifa(40, 600)
balao(d, 330, 330, ['Uma estoica', 'disse uma vez:'], f, 1)
balao(d, 790, 420, ['Disse o quê?'], f, -1)
d.line([(80, 1050), (W - 80, 1050)], fill=C, width=3)
d.text((W/2, 1150), 'arrasta para o lado', font=P(30, True), fill=C, anchor='mm')
im.convert('RGB').save(out / '1.png')

im, d = tela(2)
bloco(d, 500, ['“O fogo prova o ouro;'], P(66, True), B, 0)
bloco(d, 600, ['a adversidade, os fortes.”'], P(66, True), G, 0)
traco(d, 720)
d.text((W/2, 800), 'Sêneca, Sobre a providência, 5.10', font=P(32, True), fill=C, anchor='mm')
im.convert('RGB').save(out / '2.png')

im, d = tela(3)
bloco(d, 450, ['Você pede uma vida', 'sem problemas.'], P(66), B, 90)
traco(d, 640)
bloco(d, 760, ['Mas é no problema', 'que você descobre', 'do que é capaz.'], P(62, True), G, 84)
im.convert('RGB').save(out / '3.png')

im, d = tela(4)
bloco(d, 470, ['“São as dificuldades', 'que mostram'], P(66, True), B, 90)
bloco(d, 650, ['quem as pessoas são.”'], P(66, True), G, 0)
traco(d, 770)
d.text((W/2, 850), 'Epicteto, Discursos, 1.24.1', font=P(32, True), fill=C, anchor='mm')
im.convert('RGB').save(out / '4.png')

im, d = tela(5)
bloco(d, 380, ['Quando algo der errado,', 'troque a pergunta.'], P(62), B, 86)
traco(d, 560)
bloco(d, 660, ['Em vez de “Por que comigo?”'], P(58), C, 0)
bloco(d, 790, ['pergunte:', '“O que isso quer me ensinar?”'], P(60, True), G, 86)
im.convert('RGB').save(out / '5.png')

im, d = tela(6)
bloco(d, 460, ['Não peça uma vida', 'mais fácil.'], P(70), B, 94)
bloco(d, 680, ['Construa uma mente', 'mais firme.'], P(70, True), G, 94)
traco(d, 870)
d.text((W/2, 960), 'Qual dificuldade está te mostrando quem você é?', font=P(34, True), fill=B, anchor='mm')
estilo.texto_espacado(d, (W/2, 1130), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(26, 500), C, 6)
im.convert('RGB').save(out / '6.png')
print('ok')
