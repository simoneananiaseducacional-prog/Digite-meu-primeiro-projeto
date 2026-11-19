"""Adesivos de story (PNG transparente) no estilo das referências que a Simone mandou: letras brancas,
mistura de fonte fina, maiúscula grossa e letra de mão, emojis, corações e traço sublinhado.
Uso: python3 adesivos_story.py pasta_saida
"""
import sys, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F = Path('/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos/fontes')
def fonte(n, t): return ImageFont.truetype(str(F / n), t)
def fina(t): return fonte('Poppins-Light.ttf', t)
def grossa(t): return fonte('Poppins-ExtraBold.ttf', t)
def mao(t): return fonte('CaveatBrush-Regular.ttf', t)
def alta(t): return fonte('BebasNeue-Regular.ttf', t)
def script(t): return fonte('Sacramento-Regular.ttf', t)
def gfina(t): return fonte('ShadowsIntoLightTwo-Regular.ttf', t)
def ggrossa(t): return fonte('GochiHand-Regular.ttf', t)
EMO = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', 109)
BR = (255, 255, 255, 255); ROSA = (244, 114, 182, 255); OURO = (242, 214, 150, 255)
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)

def emojis(txt, alt=70):
    ims = []
    for ch in txt:
        im = Image.new('RGBA', (140, 140), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((70, 70), ch, font=EMO, embedded_color=True, anchor='mm')
        im = im.crop(im.getbbox()); s = alt / im.height
        ims.append(im.resize((int(im.width * s), alt), Image.LANCZOS))
    w = sum(i.width for i in ims) + 8 * (len(ims) - 1)
    linha = Image.new('RGBA', (w, alt), (0, 0, 0, 0)); x = 0
    for i in ims: linha.alpha_composite(i, (x, 0)); x += i.width + 8
    return linha

def coracao(d, cx, cy, r, cor):
    pts = [(cx + r * 16 * math.sin(u) ** 3 / 16, cy - r * (13 * math.cos(u) - 5 * math.cos(2 * u) - 2 * math.cos(3 * u) - math.cos(4 * u)) / 16)
           for u in [k / 60 * 2 * math.pi for k in range(61)]]
    d.polygon(pts, fill=cor)

def montar(itens, largura=1300):
    """itens: ('t', texto, fonte, cor) | ('e', emojis) | ('sub',) sublinhado | ('oval', texto, fonte) palavra circulada"""
    blocos = []
    for it in itens:
        if it[0] == 'e':
            blocos.append(emojis(it[1]))
            continue
        im = Image.new('RGBA', (largura, 260), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        if it[0] == 't':
            _, txt, f, cor = it
            heart = txt.endswith('♡'); txt = txt.rstrip('♡ ')
            d.text((largura / 2, 130), txt, font=f, fill=cor, anchor='mm')
            if heart:
                r = max(16, f.size * 0.28)
                coracao(d, largura / 2 + f.getlength(txt) / 2 + r * 1.6, 130 - r * 0.2, r, ROSA)
        elif it[0] == 'oval':
            _, txt, f = it
            w = f.getlength(txt)
            d.text((largura / 2, 130), txt, font=f, fill=BR, anchor='mm')
            d.ellipse((largura / 2 - w / 2 - 40, 130 - 62, largura / 2 + w / 2 + 40, 130 + 58), outline=BR, width=5)
            d.arc((largura / 2 - w / 2 - 30, 130 - 70, largura / 2 + w / 2 + 50, 130 + 50), 190, 250, fill=BR, width=4)
        elif it[0] == 'seg':   # linha com parte circulada: ('seg', [(texto, circular)], fonte)
            _, partes, f = it
            tot = sum(f.getlength(tx) for tx, _ in partes); x = largura / 2 - tot / 2
            for tx, circ in partes:
                w = f.getlength(tx)
                d.text((x, 130), tx, font=f, fill=BR, anchor='lm')
                if circ:
                    d.ellipse((x - 18, 130 - f.size * 0.42, x + w + 14, 130 + f.size * 0.36), outline=BR, width=4)
                    d.arc((x - 8, 130 - f.size * 0.5, x + w + 30, 130 + f.size * 0.3), 195, 300, fill=BR, width=3)
                x += w
        elif it[0] == 'sub':
            d.line([(largura / 2 - 230, 120), (largura / 2 + 200, 126)], fill=BR, width=7)
            d.ellipse((largura / 2 + 206, 116, largura / 2 + 222, 132), fill=BR)
        elif it[0] == 'cor':
            coracao(d, largura / 2 + it[1], 130, 34, ROSA)
        bb = im.getbbox()
        if bb: blocos.append(im.crop((0, bb[1], largura, bb[3])))
    H = sum(b.height for b in blocos) + 18 * (len(blocos) - 1) + 40
    lay = Image.new('RGBA', (largura, H), (0, 0, 0, 0)); y = 20
    for b in blocos:
        lay.alpha_composite(b, ((largura - b.width) // 2, y)); y += b.height + 18
    sombra = Image.new('RGBA', lay.size, (0, 0, 0, 0)); sombra.putalpha(lay.getchannel('A').point(lambda v: int(v * 0.6)))
    im = Image.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(7)), lay)
    return im.crop(im.getbbox())

ADESIVOS = {
    'cafe': [('e', '🤭☕💖'), ('t', 'correndo contra o tempo', fina(50), BR),
             ('t', 'MAS SEMPRE PRESENTE', grossa(72), BR), ('t', 'NO AGORA ♡', grossa(72), BR)],
    'vida_nao_posta': [('e', '🙈🥴'), ('t', 'A VIDA QUE A', alta(130), BR), ('t', 'GENTE NÃO POSTA', alta(130), BR),
                       ('t', 'TAMBÉM É PRÁTICA ESTOICA', mao(62), BR), ('sub',)],
    'silencio': [('t', 'Café, silêncio', grossa(84), BR), ('t', 'e o que depende de mim', script(96), BR), ('e', '☕🤍')],
    'bom_dia': [('t', 'Bom dia!', grossa(130), BR), ('t', 'hoje eu escolho responder,', fina(52), BR), ('t', 'não reagir ♡', fina(52), BR)],
    'transito': [('t', 'NÃO CONTROLO', mao(110), BR), ('t', 'O TRÂNSITO.', mao(110), BR),
                 ('t', 'controlo o meu', fina(54), BR), ('oval', 'humor', script(110)), ('e', '🚗💖')],
    'cabe_a_mim': [('t', 'mais um dia de trabalho,', fina(52), BR), ('t', 'fazendo o que', mao(96), BR), ('oval', 'cabe a mim', mao(96))],
    'escola': [('e', '📚✨💖'), ('t', 'DIA DE ESCOLA', mao(120), BR), ('t', 'cada aluno,', fina(54), BR), ('t', 'uma história inteira ♡', fina(54), BR)],
    'pausa': [('t', 'PAUSA', alta(190), BR), ('t', 'para lembrar', fina(54), BR), ('oval', 'o que importa', script(96))],
    'bom_dia_trabalho': [('t', 'bom dia pra quem já está trabalhando,', gfina(70), BR),
                         ('seg', [('fazendo o ', False), ('melhor', True), (' com', False)], ggrossa(100)),
                         ('t', 'o que tem hoje', ggrossa(100), BR)],
    'bom_dia_responder': [('t', 'bom dia pra quem já está na luta,', gfina(70), BR),
                          ('seg', [('e escolhendo ', False), ('responder', True)], ggrossa(100)),
                          ('t', 'não reagir', ggrossa(100), BR)],
    'bom_dia_calma': [('t', 'mais um dia de trabalho,', gfina(70), BR),
                      ('seg', [('porque ', False), ('a calma', True)], ggrossa(100)),
                      ('t', 'também é força', ggrossa(100), BR)],
}
for nome, itens in ADESIVOS.items():
    montar(itens).save(out / f'{nome}.png')
print('ok', len(ADESIVOS))
