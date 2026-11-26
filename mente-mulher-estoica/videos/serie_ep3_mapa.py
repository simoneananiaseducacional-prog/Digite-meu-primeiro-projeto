"""Série "Padrões em relacionamentos", Ep. 3 (mapa): Você tem duvidado da própria memória?
Coluna "O que você viveu" x "O que te dizem": a cada frase do outro, a lembrança perde a cor e ganha um ponto de interrogação.
Base: gaslighting (Paige Sweet, The Sociology of Gaslighting, 2019); Epicteto, Encheirídion, 1.5.
Uso: python3 serie_ep3_mapa.py saida.mp4
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
    'selo': [em(W / 2, 110, camada('SÉRIE  ·  EP. 3', F('Medium', 34), OURO))],
    'gan': [em(W / 2, 200, camada('Você tem duvidado', F('Regular', 76))), em(W / 2, 290, camada('da própria memória?', F('Italic', 80)))],
    'fim': [em(W / 2, 200, camada('Salva para reler', F('Italic', 60))), em(W / 2, 278, camada('quando duvidar de você.', F('Italic', 60)))],
    'voce': [pilula(270, 470, 'O que você viveu', F('Medium', 40))],
    'outra': [pilula(810, 470, 'O que te dizem', F('Medium', 40), (245, 236, 228), VINHO)],
    'v1': [em(W / 2, 1230, camada('Duvidar de si é o efeito.', F('Regular', 56)))],
    'v2': [em(W / 2, 1302, camada('Não é um defeito seu.', F('Italic', 60), VINHO))],
    'v3': [em(W / 2, 1362, camada('Gaslighting, Paige Sweet, 2019', F('Italic', 30), CINZA))],
    's1': [em(W / 2, 1480, camada('Diga à versão que te contam:', F('Regular', 50))), em(W / 2, 1548, camada('“Você é uma impressão, não o fato.”', F('Italic', 58)))],
    's2': [em(W / 2, 1604, camada('Inspirado em Epicteto, Encheirídion, 1.5', F('Italic', 30), CINZA))],
    'ped': [],
    'av': [em(W / 2, 1800, camada('Isto não é diagnóstico. Se dói, procure apoio profissional.', F('Regular', 30), CINZA))],
    'arr': [em(W / 2, 1860, camada('@mente_mulher_estoica', F('Regular', 28), CINZA))],
}
PARES = [('Houve gritos', 'Ninguém gritou aqui.'), ('Aquilo te magoou', 'Você é sensível demais.'),
         ('O combinado era outro', 'Isso é coisa da sua cabeça.'), ('Você lembra bem', 'Você sempre exagera.')]
fi = F('Italic', 40)
LAY = [(camada(a + '.', fi), camada(a + '?', fi, CINZA), camada(b, fi, VINHO)) for a, b in PARES]
T_ESQ = [2.6 + i * 3.4 for i in range(4)]
T_DIR = [t0 + 1.6 for t0 in T_ESQ]

saida = Path(sys.argv[1]); ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    im = Image.fromarray(PAPEL_IM).convert('RGBA'); d = ImageDraw.Draw(im)
    colar(im, E['selo'], 1)
    colar(im, E['gan'], 1 - ap(t, 23.6, 0.4)); colar(im, E['fim'], ap(t, 24.0, 0.5))
    colar(im, E['voce'], ap(t, 1.0)); colar(im, E['outra'], ap(t, 1.6))
    if t > 1.8: d.line([(W / 2 + 10, 430), (W / 2 + 10, 430 + 700 * ap(t, 1.8, 1.0))], fill=CINZA, width=2)
    for i, ((l0, l0q, l2), te, td) in enumerate(zip(LAY, T_ESQ, T_DIR)):
        y = 620 + i * 140
        a = ap(t, te, 0.4); q = ap(t, td + 0.5, 0.8)
        if a > 0:
            colar(im, [em(270, y, l0)], a * (1 - q)); colar(im, [em(270, y, l0q)], a * q)
        colar(im, [em(810, y, l2)], ap(t, td, 0.4))
    colar(im, E['v1'], ap(t, 16.8)); colar(im, E['v2'], ap(t, 17.6)); colar(im, E['v3'], ap(t, 18.4))
    colar(im, E['s1'], ap(t, 19.8)); colar(im, E['s2'], ap(t, 20.4))
    colar(im, E['av'], ap(t, 25.0)); colar(im, E['arr'], 1)
    ff.stdin.write((np.asarray(im.convert('RGB'), np.float32) * cl((T - t) / 0.5)).astype(np.uint8).tobytes())
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida)
saida.with_suffix('.mudo.mp4').unlink(missing_ok=True); print('ok', saida)
