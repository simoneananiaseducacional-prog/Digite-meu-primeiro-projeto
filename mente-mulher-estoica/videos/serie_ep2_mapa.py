"""Série "Padrões em relacionamentos", Ep. 2 (mapa): Quantas decisões suas você terceirizou?
Decisões do dia a dia passam, uma a uma, de "Você decide" para "Outra pessoa decide".
Base: controle coercitivo instalado na rotina (Evan Stark, 2007); Sêneca, Cartas a Lucílio, 1.1.
Uso: python3 serie_ep2_mapa.py saida.mp4
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import midia
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
W, H, FPS, T = 1080, 1920, 30, 30.0
FT = Path(__file__).with_name('fontes')
def F(n, t): return ImageFont.truetype(str(FT / f'EBGaramond-{n}.ttf'), t)
TINTA, CINZA, PAPEL, PILULA, VINHO, OURO = (38, 35, 32), (95, 90, 84), (238, 234, 226), (222, 217, 207), (128, 38, 38), (150, 112, 52)
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.5): return cl((t - t0) / d)
def suave(p): return p * p * (3 - 2 * p)
rng = np.random.default_rng(7)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
vin = 1 - 0.10 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
PAPEL_IM = np.clip(np.array(PAPEL, np.float32)[None, None] * vin[..., None] + rng.normal(0, 3.2, (H, W, 1)), 0, 255).astype(np.uint8)
def camada(s, f, cor=TINTA):
    w = int(f.getlength(s)) + 20; h = int(f.size * 1.7)
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ImageDraw.Draw(lay).text((w / 2, h / 2), s, font=f, fill=cor + (255,), anchor='mm')
    return lay
def em(cx, cy, lay): return (lay, int(cx - lay.width / 2), int(cy - lay.height / 2))
def pilula(cx, cy, s, f, cor=TINTA, fundo=PILULA):
    w = int(f.getlength(s) + 60); h = int(f.size * 1.55)
    lay = Image.new('RGBA', (w + 4, h + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((2, 2, w + 2, h + 2), radius=h // 2, fill=fundo + (255,)); d.text((w / 2 + 2, h / 2 + 2), s, font=f, fill=cor + (255,), anchor='mm')
    return (lay, int(cx - lay.width / 2), int(cy - lay.height / 2))
def colar(base, itens, a):
    if a <= 0.01: return
    for lay, x, y in itens:
        if a < 0.99:
            lay = lay.copy(); lay.putalpha(lay.getchannel('A').point(lambda v: int(v * a)))
        base.alpha_composite(lay, (x, y))

E = {
    'selo': [em(W / 2, 110, camada('SÉRIE  ·  EP. 2', F('Medium', 34), OURO))],
    'gan': [em(W / 2, 200, camada('Quantas decisões suas', F('Regular', 76))), em(W / 2, 290, camada('você já terceirizou?', F('Italic', 80)))],
    'fim': [em(W / 2, 200, camada('Quando foi a última vez que você', F('Italic', 56))), em(W / 2, 278, camada('decidiu algo só por você?', F('Italic', 60)))],
    'voce': [pilula(270, 470, 'Você decide', F('Medium', 44))],
    'outra': [pilula(810, 470, 'Outra pessoa decide', F('Medium', 40), (245, 236, 228), VINHO)],
    'v1': [em(W / 2, 1230, camada('Ninguém tira tudo de uma vez.', F('Regular', 56)))],
    'v2': [em(W / 2, 1302, camada('Vai pedindo uma decisão por vez.', F('Italic', 58), VINHO))],
    'v3': [em(W / 2, 1362, camada('Controle coercitivo, Evan Stark, 2007', F('Italic', 30), CINZA))],
    's1': [em(W / 2, 1490, camada('“Reivindique-se para si mesmo.”', F('Italic', 64)))],
    's2': [em(W / 2, 1556, camada('Sêneca, Cartas a Lucílio, 1.1', F('Italic', 32), CINZA))],
    'ped': [em(W / 2, 1680, camada('Manda para quem precisa ouvir isso.', F('Medium', 44), OURO))],
    'av': [em(W / 2, 1800, camada('Isto não é diagnóstico. Se dói, procure apoio profissional.', F('Regular', 30), CINZA))],
    'arr': [em(W / 2, 1860, camada('@mente_mulher_estoica', F('Regular', 28), CINZA))],
}
ITENS = ['A roupa que você veste', 'Com quem você sai', 'Como gasta o seu dinheiro', 'O que você posta', 'Quando vê a sua família']
fi = F('Italic', 40)
LAY = [(camada(s, fi), camada(s, fi, VINHO)) for s in ITENS]
ENTRA = [2.6 + i * 0.7 for i in range(5)]
MOVE = [7.6 + i * 1.7 for i in range(5)]

saida = Path(sys.argv[1]); ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    im = Image.fromarray(PAPEL_IM).convert('RGBA'); d = ImageDraw.Draw(im)
    colar(im, E['selo'], 1)
    colar(im, E['gan'], 1 - ap(t, 23.4, 0.4)); colar(im, E['fim'], ap(t, 23.8, 0.5))
    colar(im, E['voce'], ap(t, 1.0)); colar(im, E['outra'], ap(t, 1.6))
    if t > 1.8: d.line([(W / 2 + 10, 430), (W / 2 + 10, 430 + 700 * ap(t, 1.8, 1.0))], fill=CINZA, width=2)
    for i, ((l0, l1), te, tm) in enumerate(zip(LAY, ENTRA, MOVE)):
        a = ap(t, te, 0.4)
        if a <= 0: continue
        p = suave(ap(t, tm, 1.1)); y = 610 + i * 112
        x = 270 + (810 - 270) * p
        if p > 0 and p < 1:   # rastro pontilhado do caminho
            for j in range(0, int((x - 270) / 14)):
                xx_ = 270 + 14 * j + l0.width / 2 if 270 + 14 * j + l0.width / 2 < x - l0.width / 2 else None
        if p < 1: colar(im, [em(x, y, l0)], a * (1 - p))
        if p > 0: colar(im, [em(x, y, l1)], a * p)
        if p >= 1:   # deixa um espaço vazio marcado na coluna de origem
            d.line([(200, y), (340, y)], fill=CINZA, width=2)
    colar(im, E['v1'], ap(t, 16.8)); colar(im, E['v2'], ap(t, 17.6)); colar(im, E['v3'], ap(t, 18.4))
    colar(im, E['s1'], ap(t, 19.8)); colar(im, E['s2'], ap(t, 20.4))
    colar(im, E['ped'], ap(t, 24.6)); colar(im, E['av'], ap(t, 25.0)); colar(im, E['arr'], 1)
    ff.stdin.write((np.asarray(im.convert('RGB'), np.float32) * cl((T - t) / 0.5)).astype(np.uint8).tobytes())
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida)
saida.with_suffix('.mudo.mp4').unlink(missing_ok=True); print('ok', saida)
