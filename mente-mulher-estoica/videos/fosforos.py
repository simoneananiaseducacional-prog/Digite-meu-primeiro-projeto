"""Às vezes, a distância te salva: fila de fósforos, o fogo já queima no quadro zero e se espalha; um fósforo se
afasta e o fogo para ali. Ideia de @matheus.noventa (recriada por código, fundo escuro da página).
Fecho: Sêneca, Cartas a Lucílio, 7.8. Uso: python3 fosforos.py saida.mp4 [capa.png]
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pathlib import Path
W, H, FPS, T = 1080, 1920, 30, 22.0
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
FT = Path(__file__).with_name('fontes')
def ebg(n, t): return ImageFont.truetype(str(FT / f'EBGaramond-{n}.ttf'), t)
def cl(p): return max(0.0, min(1.0, p))
def sv(p): p = cl(p); return p * p * (3 - 2 * p)
def ap(t, t0, d=0.4): return sv((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.3): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
saida = Path(sys.argv[1]); capa = Path(sys.argv[2]) if len(sys.argv) > 2 else None
N, X0, DX, BASE, HS, WS = 19, 125, 46, 1300, 340, 20
GAP = 9
def acende(i):
    if i <= 3: return -2.0 + 0.3 * i
    if i < GAP: return 0.9 * (i - 3)
    return 1e9
T_SAI = 2.2
rng = np.random.default_rng(5)
FASE = rng.uniform(0, 6.28, N)
fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
def texto(im, xy, s, font, cor, a):
    if a < 0.02: return im
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).text(xy, s, font=font, fill=cor + (255,), anchor='mm')
    lay.putalpha(lay.getchannel('A').point(lambda v: int(v * cl(a))))
    return Image.alpha_composite(im, lay)
def fosforo(d, x, y, ang, queimado, a=1.0):
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    def p(dx, dy): return (x + dx * ca - dy * sa, y + dx * sa + dy * ca)
    q = queimado
    pal = tuple(int(c * (1 - 0.75 * q) + 25 * q) for c in (214, 170, 110))
    d.polygon([p(-WS / 2, 0), p(WS / 2, 0), p(WS / 2, -HS), p(-WS / 2, -HS)], fill=pal + (int(255 * a),))
    cab = tuple(int(c * (1 - q) + 20 * q) for c in (170, 40, 35))
    hx, hy = p(0, -HS - 12)
    d.ellipse((hx - 15, hy - 22, hx + 15, hy + 22), fill=cab + (int(255 * a),))
def chama(d, x, y, h, w, t, f):
    for k, (cor, esc) in enumerate([((255, 120, 30), 1.0), ((255, 170, 50), 0.75), ((255, 225, 120), 0.45)]):
        hh = h * esc; ww = w * esc
        pts = []
        for j in range(25):
            u = j / 24; ang = math.pi * u
            r = ww * math.sin(ang) * (1 - 0.15 * u)
            yy = y - hh * (1 - math.cos(ang)) / 2 * 1.0
            pts.append((x - r + 6 * math.sin(t * 9 + f + u * 4) * u, yy))
        top = (x + 10 * math.sin(t * 7 + f), y - hh * 1.25)
        pts2 = [(2 * x - px, py) for px, py in reversed(pts)]
        d.polygon(pts + [top] + pts2, fill=cor + (230,))
def quadro(t):
    im = fundo.copy()
    cena = 1 - 0.75 * ap(t, 9.4, 0.8)
    chamas = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dc = ImageDraw.Draw(chamas)
    fumaca = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dfu = ImageDraw.Draw(fumaca)
    pal = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dp = ImageDraw.Draw(pal)
    brilho = 0.0
    for i in range(N):
        x = X0 + i * DX; y = BASE; ang = 0
        if i == GAP:   # o fósforo que se afasta
            p = sv((t - T_SAI) / 1.2)
            x += 0 * p; y += 0; ang = -0 * p
            x = X0 + i * DX - 20 * p; y = BASE + 70 * p; ang = 90 * p
        ti = acende(i); ida = t - ti
        inten = cl(ida / 0.5) * (1 - cl((ida - 4.5) / 2.0)) if ida > 0 else 0.0
        queim = cl((ida - 1.0) / 3.0) if ida > 0 else 0.0
        fosforo(dp, x, y, ang, queim, cena)
        if inten > 0.02:
            brilho = max(brilho, inten)
            f = FASE[i]; hh = (150 + 35 * math.sin(t * 6 + f)) * inten
            chama(dc, x, y - HS - 10, hh, 30 + 6 * inten, t, f)
        if ida > 0.6:
            for k in range(3):
                u = ((t - ti) * 0.35 + k / 3) % 1
                r = 20 + 60 * u; sy = y - HS - 120 - 520 * u
                dfu.ellipse((x - r + 30 * math.sin(u * 5 + i), sy - r, x + r + 30 * math.sin(u * 5 + i), sy + r),
                            fill=(60, 58, 56, int(90 * (1 - u) * cl(ida - 0.6) * cena)))
    if brilho > 0.02:
        gl = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(gl).ellipse((X0 - 160, BASE - 650, X0 + 8 * DX + 160, BASE + 80), fill=(255, 140, 40, int(60 * cena)))
        im = Image.alpha_composite(im, gl.filter(ImageFilter.GaussianBlur(120)))
    im = Image.alpha_composite(im, fumaca.filter(ImageFilter.GaussianBlur(22)))
    im = Image.alpha_composite(im, pal)
    ch = chamas.filter(ImageFilter.GaussianBlur(3)); chg = chamas.filter(ImageFilter.GaussianBlur(18))
    if cena < 1: ch.putalpha(ch.getchannel('A').point(lambda v: int(v * cena))); chg.putalpha(chg.getchannel('A').point(lambda v: int(v * cena)))
    im = Image.alpha_composite(Image.alpha_composite(im, chg), ch)
    d = ImageDraw.Draw(im, 'RGBA'); d.line([(80, BASE + 2), (1000, BASE + 2)], fill=C + (int(120 * cena),), width=2)
    q = 1 - ap(t, 9.2, 0.4)
    im = texto(im, (W / 2, 330), 'Às vezes,', ebg('Regular', 84), B, q)
    im = texto(im, (W / 2, 430), 'a distância te salva.', ebg('Italic', 88), G, q)
    f1 = jan(t, 9.8, 14.0)
    im = texto(im, (W / 2, 780), 'Nem todo incêndio', ebg('Regular', 80), B, f1)
    im = texto(im, (W / 2, 880), 'precisa ser seu.', ebg('Italic', 84), G, f1 * ap(t, 10.4))
    f2 = jan(t, 14.2, 19.0)
    im = texto(im, (W / 2, 740), '“Conviva com aqueles', ebg('Italic', 66), B, f2)
    im = texto(im, (W / 2, 825), 'que vão te tornar melhor.”', ebg('Italic', 66), G, f2)
    im = texto(im, (W / 2, 920), 'Sêneca, Cartas a Lucílio, 7.8', ebg('Italic', 36), C, f2)
    f3 = ap(t, 19.2)
    im = texto(im, (W / 2, 800), 'Manda para quem precisa', ebg('Regular', 70), B, f3)
    im = texto(im, (W / 2, 890), 'se afastar do fogo.', ebg('Italic', 74), G, f3)
    d = ImageDraw.Draw(im, 'RGBA')
    d.text((W / 2, 1700), 'Ideia: @matheus.noventa', font=estilo.sem_serifa(24, 500), fill=(170, 165, 158, 200), anchor='mm')
    estilo.texto_espacado(d, (W / 2, 1760), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(26, 500), (170, 165, 158, 220), 6)
    return im.convert('RGB')
if capa: quadro(4.5).save(capa)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    ff.stdin.write(estilo.para_bytes(np.asarray(quadro(t), np.float32) * cl((T - t) / 0.4)))
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida)
saida.with_suffix('.mudo.mp4').unlink(missing_ok=True); print('ok', saida)
