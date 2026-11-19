"""Adesivos de story (PNG transparente) no padrão da página, para colar sobre fotos do dia a dia
(café, trabalho, carro, escola). Uso: python3 adesivos_story.py pasta_saida
"""
import sys
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
B, G = estilo.BRANCO, estilo.DOURADO
P, S = estilo.playfair, estilo.sem_serifa
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)

ADESIVOS = [  # nome, [(texto, fonte, cor)]
    ('cafe', [('correndo contra o tempo', S(40, 400), B), ('mas presente', P(84, True), G), ('no agora.', P(84, True), G)]),
    ('vida_nao_posta', [('A VIDA QUE A GENTE', S(66, 700), B), ('NÃO POSTA', S(66, 700), B), ('também é prática.', P(52, True), G)]),
    ('silencio', [('Café, silêncio', P(72), B), ('e o que depende de mim.', P(56, True), G)]),
    ('bom_dia', [('Bom dia.', P(96, True), G), ('Hoje eu escolho responder,', S(40, 500), B), ('não reagir.', S(40, 500), B)]),
    ('transito', [('NÃO CONTROLO O TRÂNSITO.', S(50, 700), B), ('Controlo o meu humor.', P(64, True), G)]),
    ('cabe_a_mim', [('mais um dia', S(40, 400), B), ('de fazer', P(78), B), ('o que cabe a mim.', P(78, True), G)]),
    ('escola', [('Dia de escola.', P(76), B), ('Cada aluno,', P(58, True), G), ('uma história inteira.', P(58, True), G)]),
    ('pausa', [('PAUSA', S(88, 700), B), ('para lembrar o que importa.', P(46, True), G)]),
]

def adesivo(linhas):
    W = 1080; esp = 14
    alts = [f.getbbox(t)[3] - f.getbbox(t)[1] for t, f, _ in linhas]
    H = sum(alts) + esp * (len(linhas) - 1) + 120
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    y = 60; larg = 0
    for (t, f, c), h in zip(linhas, alts):
        d.text((W / 2, y + h / 2), t, font=f, fill=c + (255,), anchor='mm'); y += h + esp
        larg = max(larg, f.getlength(t))
    d.line([(W / 2 - 40, y + 16), (W / 2 + 40, y + 16)], fill=G + (255,), width=3)   # traço dourado
    sombra = Image.new('RGBA', lay.size, (0, 0, 0, 0)); sombra.putalpha(lay.getchannel('A').point(lambda v: int(v * 0.55)))
    sombra = sombra.filter(ImageFilter.GaussianBlur(6))
    im = Image.alpha_composite(sombra, lay)
    return im.crop(im.getbbox())

for nome, linhas in ADESIVOS:
    adesivo(linhas).save(out / f'{nome}.png')
print('ok', len(ADESIVOS))
