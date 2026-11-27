"""Série "Padrões em relacionamentos", Ep. 1 em versão MAPA (página de papel desenhada aos poucos).
A frase "Eu só me preocupo com você" se divide em dois caminhos: cuidado (o seu mundo cresce) e controle
(o seu mundo encolhe). Base: controle coercitivo (Evan Stark, 2007); Epicteto, Encheirídion, 1.
Uso: python3 serie_ep1_mapa.py saida.mp4
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
    'selo': [em(W / 2, 110, camada('SÉRIE  ·  EP. 1', F('Medium', 34), OURO))],
    'gan': [em(W / 2, 200, camada('Isso é cuidado', F('Regular', 76))), em(W / 2, 290, camada('ou é controle?', F('Italic', 80)))],
    'frase': [pilula(W / 2, 450, '“Eu só me preocupo com você.”', F('Italic', 46))],
    'cuid': [pilula(290, 650, 'Cuidado', F('Medium', 46))],
    'cont': [pilula(790, 650, 'Controle', F('Medium', 46), (245, 236, 228), VINHO)],
    'ped': [em(W / 2, 200, camada('Salva para reler quando alguém', F('Italic', 56))), em(W / 2, 278, camada('disser que é pelo seu bem.', F('Italic', 56)))],
    'av': [em(W / 2, 1800, camada('Isto não é diagnóstico. Se dói, procure apoio profissional.', F('Regular', 30), CINZA))],
    'arr': [em(W / 2, 1860, camada('@mente_mulher_estoica', F('Regular', 28), CINZA))],
    'v1': [em(W / 2, 1520, camada('Cuidado amplia a sua vida.', F('Regular', 56)))],
    'v2': [em(W / 2, 1592, camada('Controle encolhe o seu mundo.', F('Italic', 58), VINHO))],
    'v3': [em(W / 2, 1650, camada('Controle coercitivo, Evan Stark, 2007', F('Italic', 30), CINZA))],
    'epi': [em(W / 2, 1712, camada('“Algumas coisas dependem de nós.” As suas escolhas são suas.  Epicteto, Encheirídion, 1', F('Italic', 27), CINZA))],
}
ESQ = ['Pergunta como você está', 'Respeita o seu tempo', 'Apoia os seus amigos', 'Confia nas suas escolhas']
DIR = ['Exige saber onde você está', 'Cobra cada atraso', 'Afasta os seus amigos', 'Decide por você']
fi = F('Italic', 38)
ITENS = [(em(290, 770 + i * 92, camada(s, fi)), 3.8 + i * 2.1) for i, s in enumerate(ESQ)]
ITENS += [(em(790, 770 + i * 92, camada(s, fi, VINHO)), 4.8 + i * 2.1) for i, s in enumerate(DIR)]
mundo = camada('seu mundo', F('Italic', 36))

def pontos(d, p0, p1, frac, passo=10, cor=CINZA):
    n = max(1, int(math.dist(p0, p1) / passo))
    for i in range(int(n * frac)):
        x = p0[0] + (p1[0] - p0[0]) * i / n; y = p0[1] + (p1[1] - p0[1]) * i / n
        d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=cor)

saida = Path(sys.argv[1]); ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    im = Image.fromarray(PAPEL_IM).convert('RGBA'); d = ImageDraw.Draw(im)
    colar(im, E['selo'], 1)
    colar(im, E['gan'], 1 - ap(t, 22.0, 0.4)); colar(im, E['ped'], ap(t, 22.4, 0.5))
    colar(im, E['frase'], ap(t, 1.0))
    pontos(d, (W / 2 - 20, 490), (300, 610), ap(t, 2.0, 0.8)); pontos(d, (W / 2 + 20, 490), (780, 610), ap(t, 2.0, 0.8), cor=VINHO)
    colar(im, E['cuid'], ap(t, 2.8)); colar(im, E['cont'], ap(t, 3.0))
    if t > 3.2: d.line([(W / 2, 600), (W / 2, 600 + 520 * ap(t, 3.2, 1.0))], fill=CINZA + (255,), width=2)
    for it, t0 in ITENS: colar(im, [it], ap(t, t0, 0.4))
    # o seu mundo: cresce no cuidado, encolhe no controle
    g = ap(t, 13.0, 3.0)
    if g > 0:
        r1 = 70 + 80 * g; r2 = 150 - 95 * g; cy = 1270
        d.ellipse((290 - r1, cy - r1, 290 + r1, cy + r1), outline=TINTA, width=4)
        d.ellipse((790 - r2, cy - r2, 790 + r2, cy + r2), outline=VINHO, width=4)
        colar(im, [em(290, cy, mundo)], ap(t, 13.0)); 
        m2 = mundo.resize((max(1, int(mundo.width * (0.45 + 0.55 * (1 - g)))), max(1, int(mundo.height * (0.45 + 0.55 * (1 - g))))), Image.LANCZOS)
        colar(im, [em(790, cy, m2)], ap(t, 13.0))
    colar(im, E['v1'], ap(t, 16.6)); colar(im, E['v2'], ap(t, 17.4)); colar(im, E['v3'], ap(t, 18.2))
    colar(im, E['epi'], ap(t, 19.4))
    colar(im, E['av'], ap(t, 23.0)); colar(im, E['arr'], 1)
    ff.stdin.write((np.asarray(im.convert('RGB'), np.float32) * cl((T - t) / 0.5)).astype(np.uint8).tobytes())
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida)
saida.with_suffix('.mudo.mp4').unlink(missing_ok=True); print('ok', saida)
