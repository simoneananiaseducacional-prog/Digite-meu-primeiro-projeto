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
HS = SL[0].height; Y0 = (H - HS) // 2 - 40
DUR = [6.5] + [4.6] * 8 + [7.5]; CF = 0.5
def fundo(s):
    b = s.resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(40))
    return Image.fromarray((np.asarray(b, np.float32) * 0.28).astype(np.uint8))
FUN = [fundo(s) for s in SL]
mask = Image.new('L', (W, HS), 255); dm = ImageDraw.Draw(mask)
for k in range(60): dm.line([(0, k), (W, k)], fill=int(255 * k / 60)); dm.line([(0, HS - 1 - k), (W, HS - 1 - k)], fill=int(255 * k / 60))
top = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(top)
estilo.texto_espacado(d, (W / 2, Y0 - 70), 'A ODISSEIA  ·  UMA LEITURA ESTOICA', estilo.sem_serifa(28, 600), estilo.DOURADO + (230,), 8)
estilo.texto_espacado(d, (W / 2, Y0 + HS + 90), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(26, 500), (200, 194, 184, 220), 6)
def render(i, t):
    s = SL[i]; z = 1 + 0.04 * t / DUR[i]
    sz = s.resize((int(W * z), int(HS * z)), Image.BICUBIC); ox = (sz.width - W) // 2; oy = (sz.height - HS) // 2
    sz = sz.crop((ox, oy, ox + W, oy + HS))
    f = FUN[i].copy(); f.paste(sz, (0, Y0), mask)
    return Image.alpha_composite(f.convert('RGBA'), top).convert('RGB')
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
