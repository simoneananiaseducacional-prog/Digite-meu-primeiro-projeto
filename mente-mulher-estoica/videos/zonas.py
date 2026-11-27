"""Zonas: círculos aninhados que se tocam embaixo (conforto, medo, aprendizado, crescimento). Um ponto dourado sobe
de dentro para fora e acende cada zona. Formato inspirado em vídeo de @iluminesuamente_ (sem "sucesso" no topo).
Base: modelo das zonas de aprendizagem (Senninger, 2000); Sêneca, Cartas a Lucílio, 104.26.
Uso: python3 zonas.py saida.mp4 [capa.png]
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pathlib import Path
W, H, FPS, T = 1080, 1920, 30, 24.0
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
VERM = (215, 60, 70)
FT = Path(__file__).with_name('fontes')
def ebg(n, t): return ImageFont.truetype(str(FT / f'EBGaramond-{n}.ttf'), t)
def cl(p): return max(0.0, min(1.0, p))
def sv(p): p = cl(p); return p * p * (3 - 2 * p)
def ap(t, t0, d=0.4): return sv((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.3): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
saida = Path(sys.argv[1]); capa = Path(sys.argv[2]) if len(sys.argv) > 2 else None
BASE_Y = 1420
ZONAS = [(170, 'Zona de conforto', VERM), (290, 'Zona do medo', G), (400, 'Zona de aprendizado', G), (500, 'Zona de crescimento', G)]
SUB = ['tudo conhecido, nada novo', 'desculpas e medo do julgamento', 'novas habilidades, erros que ensinam', 'propósito e novos desafios']
T_ZONA = [0.0, 3.0, 6.2, 9.4]       # quando o ponto entra em cada zona
fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
def texto(im, xy, s, font, cor, a):
    if a < 0.02: return im
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).text(xy, s, font=font, fill=cor + (255,), anchor='mm')
    lay.putalpha(lay.getchannel('A').point(lambda v: int(v * cl(a))))
    return Image.alpha_composite(im, lay)
def topo_label(i): r = ZONAS[i][0]; return BASE_Y - 2 * r + 70
def ponto_y(t):
    ys = [BASE_Y - 140] + [topo_label(i) - 50 for i in range(1, 4)]
    for i in range(3):
        a, b = T_ZONA[i + 1] - 1.2, T_ZONA[i + 1]
        if t < a: return ys[i]
        if t < b: return ys[i] + (ys[i + 1] - ys[i]) * sv((t - a) / 1.2)
    return ys[3]
T_FIM_MAPA = 13.2
def quadro(t):
    im = fundo.copy()
    rec = 1 - 0.95 * ap(t, T_FIM_MAPA, 0.6)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for i, (r, nome, cor) in enumerate(ZONAS):
        aceso = 1.0 if i == 0 else ap(t, T_ZONA[i] - 0.3, 0.6)
        base_a = 0.35 + 0.65 * aceso
        if i == 0:
            pul = 0.75 + 0.25 * math.sin(t * 6)
            box = (W / 2 - r, BASE_Y - 2 * r, W / 2 + r, BASE_Y)
            d.ellipse(box, outline=VERM + (int(255 * pul * rec),), width=6)
        else:
            d.ellipse((W / 2 - r, BASE_Y - 2 * r, W / 2 + r, BASE_Y), outline=cor + (int(230 * base_a * rec),), width=4)
    glow = lay.filter(ImageFilter.GaussianBlur(10))
    im = Image.alpha_composite(Image.alpha_composite(im, glow), lay)
    for i, (r, nome, cor) in enumerate(ZONAS):
        aceso = 1.0 if i == 0 else ap(t, T_ZONA[i] - 0.3, 0.6)
        destaque = 1.0 if (i == 3 and t > T_ZONA[3]) or (i < 3 and T_ZONA[i] <= t < T_ZONA[i + 1]) else 0.55
        y = topo_label(i) if i else BASE_Y - 2 * r + 95
        im = texto(im, (W / 2, y), nome, ebg('Medium', 44), B, (0.35 + 0.65 * aceso) * destaque * rec)
        im = texto(im, (W / 2, y + 48), SUB[i], ebg('Italic', 32), C, (ap(t, T_ZONA[i] + 0.2, 0.5) if i else ap(t, 0.6)) * destaque * rec)
    # ponto que sobe
    py = ponto_y(t)
    pt = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dp = ImageDraw.Draw(pt)
    dp.ellipse((W / 2 - 34, py - 34, W / 2 + 34, py + 34), fill=G + (int(140 * rec),))
    pt = pt.filter(ImageFilter.GaussianBlur(14)); dp = ImageDraw.Draw(pt)
    dp.polygon([(W / 2, py - 22), (W / 2 - 20, py + 14), (W / 2 + 20, py + 14)], fill=(250, 220, 150, int(255 * rec)))
    im = Image.alpha_composite(im, pt)
    q = 1 - ap(t, T_FIM_MAPA - 0.2, 0.4)
    im = texto(im, (W / 2, 240), 'Onde você está agora?', ebg('Regular', 80), B, q)
    im = texto(im, (W / 2, 335), 'Crescer começa fora do conhecido.', ebg('Italic', 60), G, q * ap(t, 0.4, 0.5))
    f1 = jan(t, 13.6, 18.6)
    im = texto(im, (W / 2, 760), '“Não é porque as coisas são difíceis', ebg('Italic', 56), B, f1)
    im = texto(im, (W / 2, 840), 'que não ousamos. É porque não ousamos', ebg('Italic', 56), B, f1)
    im = texto(im, (W / 2, 920), 'que elas são difíceis.”', ebg('Italic', 62), G, f1)
    im = texto(im, (W / 2, 1010), 'Sêneca, Cartas a Lucílio, 104.26', ebg('Italic', 34), C, f1)
    f2 = ap(t, 18.8)
    im = texto(im, (W / 2, 800), 'O medo é passagem,', ebg('Regular', 78), B, f2)
    im = texto(im, (W / 2, 895), 'não endereço.', ebg('Italic', 84), G, f2)
    im = texto(im, (W / 2, 1040), 'Em qual zona você está hoje?', ebg('Medium', 48), G, ap(t, 19.8))
    estilo.texto_espacado(ImageDraw.Draw(im, 'RGBA'), (W / 2, 1720), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(26, 500), (170, 165, 158, 210), 6)
    return im.convert('RGB')
if capa: quadro(11.0).save(capa)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    ff.stdin.write(estilo.para_bytes(np.asarray(quadro(t), np.float32) * cl((T - t) / 0.4)))
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida)
saida.with_suffix('.mudo.mp4').unlink(missing_ok=True); print('ok', saida)
