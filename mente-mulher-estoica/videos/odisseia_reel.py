import sys, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pathlib import Path
U = '/root/.claude/uploads/fe1db7e1-a242-55eb-8116-11f11488b586/'
ARQ = ['dea4d96c', '6762ff9c', 'd66bd2ff', 'f71b7350', '606db133', 'e3ff5c68', '2b86735b', 'a9137fb6', '4760adcf', '9104bf35']
W, H, FPS = 1080, 1920, 30
FT = Path('/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos/fontes')
def ebg(n, t): return ImageFont.truetype(str(FT / f'EBGaramond-{n}.ttf'), t)
def limpa_badge(im, texto_embaixo=False):
    x0, y0, x1, y1 = 1000, 530, 1160, 635
    w, h = x1 - x0, y1 - y0
    a = np.asarray(im.crop((x0 - 60, 502, x1 + 19, 528)).convert('RGB'), np.float32).reshape(-1, 3)
    cor = tuple(int(v) for v in np.median(a, 0))
    if texto_embaixo:   # slide 6: só a parte de cima do selo, para não apagar o texto
        y1 = 604; h = y1 - y0
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((4, 4, w - 4, h - 4), radius=26, fill=255)
    im.paste(Image.new('RGB', (w, h), cor), (x0, y0), m.filter(ImageFilter.GaussianBlur(7))); return im
SL = []
for i, a in enumerate(ARQ):
    im = Image.open(U + a + '-image.png').convert('RGB')
    if i > 0: im = limpa_badge(im, texto_embaixo=(i == 5))
    s = im.crop((0, 500, 1179, 1532)).resize((W, int(1032 * W / 1179)), Image.LANCZOS)
    SL.append(s)
HS = SL[0].height
# faixa horizontal do texto em cada cartão (fração da largura): o cartão é ampliado até o texto ocupar a tela
TXT = [(0.49, 0.94), (0.07, 0.62), (0.08, 0.73), (0.09, 0.82), (0.49, 0.96), (0.49, 0.95), (0.06, 0.88), (0.44, 0.90), (0.51, 1.0), (0.04, 0.57)]
DUR = [6.5] + [4.6] * 8 + [7.5]; CF = 0.5
def fundo(s):
    b = s.resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(40))
    return Image.fromarray((np.asarray(b, np.float32) * 0.28).astype(np.uint8))
FUN = [fundo(s) for s in SL]
GRANDE = []
for i, s in enumerate(SL):
    a_, b_ = TXT[i]; k = min(2.0, 1010 / ((b_ - a_) * W))
    g = Image.open(U + ARQ[i] + '-image.png').convert('RGB')
    if i > 0: g = limpa_badge(g, texto_embaixo=(i == 5))
    g = g.crop((0, 500, 1179, 1532)).resize((int(W * k), int(HS * k)), Image.LANCZOS)
    ox = int(W / 2 - (a_ + b_) / 2 * g.width); ox = max(min(ox, 0), W - g.width) if g.width >= W else (W - g.width) // 2
    oy = max(190, (H - g.height) // 2 + 60)
    m = Image.new('L', g.size, 255); dm = ImageDraw.Draw(m)
    for q in range(70): dm.line([(0, q), (g.width, q)], fill=int(255 * q / 70)); dm.line([(0, g.height - 1 - q), (g.width, g.height - 1 - q)], fill=int(255 * q / 70))
    GRANDE.append((g, ox, oy, m))
top = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(top)
estilo.texto_espacado(d, (W / 2, 120), 'A ODISSEIA  ·  UMA LEITURA ESTOICA', estilo.sem_serifa(30, 600), estilo.DOURADO + (230,), 8)
estilo.texto_espacado(d, (W / 2, 1840), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(26, 500), (200, 194, 184, 220), 6)
LEG = {1: ['aquilo que continua dando', 'direção à sua vida.'], 2: ['o conforto que seduz e faz você', 'adiar quem nasceu para ser.'],
       3: ['cada pessoa escuta a voz capaz', 'de desviá-la do próprio caminho.'], 6: ['a guerra terminou.', 'Dentro de você, talvez ainda não.']}
CAP = {}
for i, ls in LEG.items():
    c = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dc = ImageDraw.Draw(c)
    yb = 1560
    sombra = Image.new('L', (W, H), 0); ImageDraw.Draw(sombra).rectangle((0, yb - 90, W, yb + 150), fill=200)
    c.putalpha(sombra.filter(ImageFilter.GaussianBlur(40))); dc = ImageDraw.Draw(c)
    for j, l in enumerate(ls): dc.text((W / 2, yb + j * 66), l, font=ebg('Italic', 54), fill=(236, 228, 214, 255), anchor='mm')
    CAP[i] = c
def render(i, t):
    g, ox, oy, m = GRANDE[i]; z = 1 + 0.03 * t / DUR[i]
    gz = g.resize((int(g.width * z), int(g.height * z)), Image.BICUBIC); mz = m.resize(gz.size)
    f = FUN[i].copy(); f.paste(gz, (int(ox - (gz.width - g.width) / 2), int(oy - (gz.height - g.height) / 2)), mz)
    f = f.convert('RGBA')
    if i in CAP: f = Image.alpha_composite(f, CAP[i])
    return Image.alpha_composite(f, top).convert('RGB')
OUT = sys.argv[1]; ff = midia.gravador(Path(OUT).with_suffix('.mudo.mp4'), estatico=False)
T = sum(DUR); inicio = np.cumsum([0] + DUR[:-1])
for k in range(int(T * FPS)):
    t = k / FPS; i = int(np.searchsorted(inicio, t, side='right') - 1); tl = t - inicio[i]
    fr = render(i, tl)
    if i + 1 < len(SL) and tl > DUR[i] - CF:
        p = (tl - (DUR[i] - CF)) / CF; fr = Image.blend(fr, render(i + 1, 0), p)
    fade = min(1, (T - t) / 0.6)
    ff.stdin.write((np.asarray(fr, np.float32) * fade).astype(np.uint8).tobytes())
ff.stdin.close(); ff.wait(); midia.juntar_audio(Path(OUT).with_suffix('.mudo.mp4'), Path(OUT)); Path(OUT).with_suffix('.mudo.mp4').unlink(missing_ok=True)
render(0, 0).save(Path(OUT).with_name('odisseia_capa.png')); print('ok', T)
