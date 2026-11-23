"""Reels do mapa "Você vive no agora": a página vai sendo desenhada (linha do tempo, raios do passado e do futuro,
presença no centro). Formato do mapa inspirado em @satori.108; fonte: Marco Aurélio, Meditações, 3.10.
Uso: python3 mapa_agora_video.py saida.mp4
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import midia
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
W, H, FPS, T = 1080, 1920, 30, 28.0
OY = 0
FT = Path(__file__).with_name('fontes')
def F(n, t): return ImageFont.truetype(str(FT / f'EBGaramond-{n}.ttf'), t)
TINTA, CINZA, PAPEL, PILULA = (38, 35, 32), (95, 90, 84), (238, 234, 226), (222, 217, 207)
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.6): return cl((t - t0) / d)

rng = np.random.default_rng(7)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
vin = 1 - 0.10 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
PAPEL_IM = np.clip(np.array(PAPEL, np.float32)[None, None] * vin[..., None] + rng.normal(0, 3.2, (H, W, 1)), 0, 255).astype(np.uint8)

# ---- elementos pré-desenhados: (camada recortada, x, y) ----
def camada_texto(s, f, cor=TINTA, anchor='mm', ang=0):
    w = int(f.getlength(s)) + 20; h = int(f.size * 1.7)
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ImageDraw.Draw(lay).text((w / 2, h / 2), s, font=f, fill=cor + (255,), anchor='mm')
    if ang: lay = lay.rotate(ang, resample=Image.BICUBIC, expand=True)
    return lay
def em(xy, lay, anchor='mm'):
    x, y = xy; y += OY
    if anchor == 'lm': x -= 10
    else: x -= lay.width / 2
    return (lay, int(x), int(y - lay.height / 2))
def pilula(cx, cy, s, f):
    w = int(f.getlength(s) + 44); lay = Image.new('RGBA', (w + 4, 60), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((2, 3, w + 2, 57), radius=27, fill=PILULA + (255,)); d.text((w / 2 + 2, 30), s, font=f, fill=TINTA + (255,), anchor='mm')
    return (lay, int(cx - lay.width / 2), int(cy + OY - 30))

C = (540, 1010)
E = {}
E['cab'] = []
E['tit'] = [em((90, 370), camada_texto('O passado já foi.', F('Regular', 76)), 'lm'),
            em((90, 458), camada_texto('O futuro ainda não chegou.', F('Regular', 76)), 'lm'),
            em((90, 552), camada_texto('Você vive no agora.', F('Italic', 84)), 'lm')]
E['par'] = []
E['pas'] = [pilula(200, C[1] - 64, 'Seu passado', F('Italic', 42))]
E['fut'] = [pilula(870, C[1] + 64, 'Seu futuro', F('Italic', 42))]
E['ago'] = [pilula(C[0], 760, 'Agora', F('Italic', 46))]
E['pre'] = [pilula(C[0], 1250, 'Presença', F('Italic', 46))]
E['pal'] = [[em((C[0], 1318 + i * 50), camada_texto(s, F('Italic', 40)))] for i, s in enumerate(['Atenção', 'Escolha', 'Ação', 'Serenidade'])]
E['col'] = [pilula(285, 1555, 'O que te prende', F('Medium', 36)), pilula(805, 1555, 'O que te liberta', F('Medium', 36))]
E['col'] += [em((70, 1615 + i * 42), camada_texto(l, F('Regular', 34)), 'lm') for i, l in enumerate(['Reviver o passado', 'e antecipar o futuro.'])]
E['col'] += [em((580, 1615 + i * 42), camada_texto(l, F('Regular', 34)), 'lm') for i, l in enumerate(['Agir no que depende', 'de você, agora.'])]
E['rod'] = [em((W / 2, 1730), camada_texto('“Cada um vive apenas o presente.”', F('Italic', 36), CINZA)),
            em((W / 2, 1778), camada_texto('Marco Aurélio, Meditações, 3.10', F('Italic', 32), CINZA))]
E['gan'] = [(camada_texto('Quantas vezes hoje', F('Italic', 66)), 0, 0), (camada_texto('você esteve aqui de verdade?', F('Italic', 66)), 0, 0)]
E['gan'] = [(l, int(W / 2 - l.width / 2), int(140 + i * 80 - l.height / 2)) for i, (l, _, _) in enumerate(E['gan'])]
E['ped'] = [(l, int(W / 2 - l.width / 2), int(140 + i * 80 - l.height / 2)) for i, l in
            enumerate([camada_texto('Salve este mapa para os dias', F('Italic', 62)), camada_texto('em que a cabeça estiver longe.', F('Italic', 62))])]
E['arr'] = [(l, int(W / 2 - l.width / 2), int(1860 - l.height / 2)) for l in [camada_texto('@mente_mulher_estoica', F('Regular', 30), CINZA)]]
fr = F('Italic', 40)
RAIOS = []   # (fim, camada do rótulo, posição, início)
def raio(s, ang, L, lado, t0):
    a = math.radians(ang); u = (lado * math.cos(a), -lado * math.sin(a))
    end = (C[0] + L * u[0], C[1] + L * u[1]); k = L - fr.getlength(s) / 2 - 18; n = (-math.sin(a), -math.cos(a))
    lay = camada_texto(s, fr, ang=ang); p = (C[0] + k * u[0] + 30 * n[0], C[1] + k * u[1] + 30 * n[1])
    RAIOS.append((end, (lay, int(p[0] - lay.width / 2), int(p[1] + OY - lay.height / 2)), t0))
for i, s in enumerate(['Arrependimentos', 'Mágoas', 'Crenças antigas', 'Culpa']): raio(s, 11 + i * 10, 500, -1, 6.6 + i * 1.1)
for i, s in enumerate(['Ansiedade', 'E se…?', 'Expectativas', 'Medo de errar']): raio(s, 42 - i * 10, 510, 1, 11.2 + i * 1.1)

def colar(base, itens, a):
    if a <= 0.01: return
    for lay, x, y in itens:
        if a < 0.99:
            lay = lay.copy(); lay.putalpha(lay.getchannel('A').point(lambda v: int(v * a)))
        base.alpha_composite(lay, (x, y))
def pontos(d, p0, p1, frac, passo=9):
    n = int(math.dist(p0, p1) / passo)
    for i in range(int(n * frac)):
        x = p0[0] + (p1[0] - p0[0]) * i / n; y = p0[1] + (p1[1] - p0[1]) * i / n + OY
        d.ellipse((x - 1.8, y - 1.8, x + 1.8, y + 1.8), fill=CINZA)

saida = Path(sys.argv[1]); ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    im = Image.fromarray(PAPEL_IM).convert('RGBA'); d = ImageDraw.Draw(im)
    colar(im, E['gan'], 1 - ap(t, 21.0, 0.5))
    colar(im, E['cab'], 1); colar(im, E['tit'], 1)             # título inteiro desde o primeiro quadro
    colar(im, E['par'], ap(t, 1.2))
    lp = ap(t, 3.0, 1.4)                                         # linha do tempo
    if lp > 0:
        x1 = 40 + (1020 - 40) * lp; d.line([(40, C[1] + OY), (x1, C[1] + OY)], fill=TINTA, width=3)
        if lp >= 1: d.polygon([(1040, C[1] + OY), (1018, C[1] + OY - 11), (1018, C[1] + OY + 11)], fill=TINTA)
    colar(im, E['pas'], ap(t, 4.2)); colar(im, E['fut'], ap(t, 4.6))
    colar(im, E['ago'], ap(t, 5.2)); pontos(d, (C[0], 798), (C[0], 1212), ap(t, 5.4, 1.0))
    for end, rot, t0 in RAIOS:
        pontos(d, C, end, ap(t, t0, 0.7)); colar(im, [rot], ap(t, t0 + 0.5, 0.4))
    if t >= 4.0: d.ellipse((C[0] - 11, C[1] + OY - 11, C[0] + 11, C[1] + OY + 11), fill=TINTA)
    colar(im, E['pre'], ap(t, 15.8))
    for i, it in enumerate(E['pal']): colar(im, it, ap(t, 16.4 + i * 0.5, 0.4))
    if t > 18.6: d.line([(C[0], 1555 + OY), (C[0], 1555 + OY + 110 * ap(t, 18.6))], fill=TINTA, width=2)
    colar(im, E['col'], ap(t, 18.8))
    colar(im, E['rod'], ap(t, 20.2))
    colar(im, E['ped'], ap(t, 21.6))
    colar(im, E['arr'], 1)
    fade = cl((T - t) / 0.5)
    ff.stdin.write((np.asarray(im.convert('RGB'), np.float32) * fade).astype(np.uint8).tobytes())
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); print('ok', saida)
