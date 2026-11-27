"""Não é sobre a queda: ela caminha (ação no quadro zero), tropeça numa pedra, cai, senta, respira, levanta,
sacode a poeira e segue. Fecho com Sêneca, Sobre a providência, 3.3. Ideia da frase: lugar-comum adaptado; cena autoral.
Uso: python3 queda_levanta.py saida.mp4 [capa.png]
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia, personagens
from personagens import ela
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pathlib import Path
W, H, FPS, T = 1080, 1920, 30, 24.0
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
FT = Path(__file__).with_name('fontes')
def ebg(n, t): return ImageFont.truetype(str(FT / f'EBGaramond-{n}.ttf'), t)
def cl(p): return max(0.0, min(1.0, p))
def sv(p): p = cl(p); return p * p * (3 - 2 * p)
def ap(t, t0, d=0.3): return sv((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.25): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
saida = Path(sys.argv[1]); capa = Path(sys.argv[2]) if len(sys.argv) > 2 else None
CHAO, K, CENTRO = 1250, 1.5, (540, 1080)
PEDRA = 540
T_TROPECA, T_SENTA, T_RESPIRA, T_LEVANTA, T_SEGUE, T_CENA = 2.6, 5.4, 6.6, 8.6, 9.8, 12.4

def estado(t):
    """x, ângulo da queda, sentada, cabeça baixa, emoção, mão no peito, brilho"""
    if t < T_TROPECA:
        x = 330 + (PEDRA - 45 - 330) * t / T_TROPECA; return x, 0, 0, 0.0, dict(sorriso=0.4), 0, 0
    x0 = PEDRA - 45
    if t < T_SENTA:
        ang = -76 * sv((t - T_TROPECA) / 0.45)
        return x0 + 30 * sv((t - T_TROPECA) / 0.45), ang, 0, 0.3, dict(triste=0.6, aberta=0.5), 0, 0
    if t < T_LEVANTA:
        sob = sv((t - T_SENTA) / 0.8)
        resp = ap(t, T_RESPIRA, 0.8) * (1 - ap(t, T_LEVANTA - 0.4, 0.4))
        return x0 + 30, -76 * (1 - sob), sob, 0.6 * (1 - resp * 0.6), dict(triste=0.7 * (1 - resp)), resp, resp
    lev = sv((t - T_LEVANTA) / 0.9)
    if t < T_SEGUE:
        return x0 + 30, 0, 1 - lev, 0.2 * (1 - lev), dict(sorriso=0.5 * lev), 0, 0.6 + 0.4 * lev
    x = x0 + 30 + 190 * cl((t - T_SEGUE) / 2.4)
    return x, 0, 0, 0, dict(sorriso=0.9), 0, 1.0

def texto(im, xy, s, font, cor, a):
    if a < 0.02: return im
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).text(xy, s, font=font, fill=cor + (255,), anchor='mm')
    lay.putalpha(lay.getchannel('A').point(lambda v: int(v * cl(a))))
    return Image.alpha_composite(im, lay)

fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
POEIRA = [(np.random.default_rng(i).uniform(-60, 60), np.random.default_rng(i + 50).uniform(0.4, 1.0)) for i in range(10)]
def quadro(t):
    cena = 1 - 0.85 * ap(t, T_CENA, 0.6)
    x, ang, sentada, cab, emo, mao, br = estado(t)
    cen = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(cen, 'RGBA')
    d.line([(CENTRO[0] - 400, CHAO), (CENTRO[0] + 400, CHAO)], fill=C + (int(200 * cena),), width=4)
    d.polygon([(PEDRA - 22, CHAO), (PEDRA - 14, CHAO - 20), (PEDRA + 6, CHAO - 26), (PEDRA + 22, CHAO - 12), (PEDRA + 26, CHAO)],
              fill=(70, 68, 66, int(255 * cena)), outline=C + (int(255 * cena),))
    # passos dourados depois de levantar
    if t > T_SEGUE:
        for k in range(int(6 * cl((t - T_SEGUE) / 2.4))):
            px = PEDRA + 70 + k * 50; d.ellipse((px - 6, CHAO + 10, px + 6, CHAO + 16), fill=G + (int(200 * cena),))
    pers = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dp = ImageDraw.Draw(pers, 'RGBA')
    bob = -6 * abs(math.sin(t * 7)) if (t < T_TROPECA or t > T_SEGUE + 0.1 and t < T_SEGUE + 2.4) else 0
    personagens.MAO_PEITO = mao
    ela(dp, x, CHAO - 6 + bob, cena, braco=0.15, lado=1, sentada=sentada, cabeca_baixa=cab, t=t, emo=emo)
    personagens.MAO_PEITO = 0.0
    if abs(ang) > 0.5: pers = pers.rotate(ang, resample=Image.BICUBIC, center=(x, CHAO))
    cen = Image.alpha_composite(cen, pers); d = ImageDraw.Draw(cen, 'RGBA')
    pz = jan(t, T_TROPECA + 0.4, T_TROPECA + 1.6, 0.3) + jan(t, T_LEVANTA + 0.5, T_LEVANTA + 1.6, 0.3)
    if pz > 0.02:   # poeira na queda e ao sacudir
        for dx, v in POEIRA:
            px = x + 60 + dx; py = CHAO - 20 - 40 * v * ((t * 1.3) % 1)
            d.ellipse((px - 5, py - 5, px + 5, py + 5), fill=(160, 150, 135, int(160 * pz * cena)))
    big = cen.resize((int(W * K), int(H * K)), Image.BICUBIC)
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.paste(big, (int(W / 2 - CENTRO[0] * K), int(1060 - CENTRO[1] * K)))
    im = fundo.copy()
    if br > 0.02:
        gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); px = W / 2 + (x - CENTRO[0]) * K
        ImageDraw.Draw(gl).ellipse((px - 240, 1000 - 300, px + 240, 1000 + 300), fill=G + (int(65 * br * cena),))
        im = Image.alpha_composite(im, gl.filter(ImageFilter.GaussianBlur(80)))
    im = Image.alpha_composite(im, cam)
    q = 1 - ap(t, T_CENA - 0.2, 0.4)
    im = texto(im, (W / 2, 260), 'Não é sobre a queda.', ebg('Regular', 80), B, q)
    im = texto(im, (W / 2, 355), 'É sobre o que você faz depois.', ebg('Italic', 72), G, q)
    f1 = jan(t, 12.8, 16.4)
    im = texto(im, (W / 2, 820), 'Cair não depende só de você.', ebg('Regular', 68), B, f1)
    im = texto(im, (W / 2, 915), 'Levantar, sim.', ebg('Italic', 84), G, f1 * ap(t, 13.6))
    f2 = jan(t, 16.6, 21.0)
    im = texto(im, (W / 2, 760), '“Nada me parece mais infeliz', ebg('Italic', 62), B, f2)
    im = texto(im, (W / 2, 840), 'do que quem nunca', ebg('Italic', 62), B, f2)
    im = texto(im, (W / 2, 920), 'enfrentou uma adversidade.”', ebg('Italic', 62), G, f2)
    im = texto(im, (W / 2, 1010), 'Sêneca, Sobre a providência, 3.3', ebg('Italic', 34), C, f2)
    f3 = ap(t, 21.2)
    im = texto(im, (W / 2, 840), 'Manda para quem caiu', ebg('Regular', 72), B, f3)
    im = texto(im, (W / 2, 935), 'e está se levantando.', ebg('Italic', 74), G, f3)
    estilo.texto_espacado(ImageDraw.Draw(im, 'RGBA'), (W / 2, 1720), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(26, 500), (170, 165, 158, 210), 6)
    return im.convert('RGB')

if capa: quadro(3.8).save(capa)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    ff.stdin.write(estilo.para_bytes(np.asarray(quadro(t), np.float32) * cl((T - t) / 0.4)))
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida)
saida.with_suffix('.mudo.mp4').unlink(missing_ok=True); print('ok', saida)
