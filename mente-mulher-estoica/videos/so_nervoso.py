"""Ele estava "só nervoso": caso real (técnico Rafael Soriano agride com cabeçada a árbitra assistente Marcielly Netto,
Campeonato Capixaba, abril de 2022; suspensão de 200 dias pelo TJD-ES). Cena com bonecos: ela com a bandeira,
ele avança gritando; a cena congela antes da agressão (não é mostrada). Fatores (pesquisa 2026-11-27),
feminicídios (Anuário FBSP 2026: 1.571 em 2025), Epicteto, Encheirídion, 1; fala final da Simone.
Uso: python3 so_nervoso.py saida.mp4 [capa.png]
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia, personagens
from personagens import ela, ele
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
W, H, FPS, T = 1080, 1920, 30, 33.0
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
VERM = (200, 90, 90)
FT = Path(__file__).with_name('fontes')
def ebg(n, t): return ImageFont.truetype(str(FT / f'EBGaramond-{n}.ttf'), t)
def cl(p): return max(0.0, min(1.0, p))
def sv(p): p = cl(p); return p * p * (3 - 2 * p)
def ap(t, t0, d=0.3): return sv((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.25): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
saida = Path(sys.argv[1]); capa = Path(sys.argv[2]) if len(sys.argv) > 2 else None
CHAO, K, CENTRO = 1250, 1.5, (540, 1080)
XE = 400
T_CONGELA = 3.8
def texto(im, xy, s, font, cor, a):
    if a < 0.02: return im
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).text(xy, s, font=font, fill=cor + (255,), anchor='mm')
    lay.putalpha(lay.getchannel('A').point(lambda v: int(v * cl(a))))
    return Image.alpha_composite(im, lay)
fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
RAB = [(math.sin(i * 1.7), math.cos(i * 2.3)) for i in range(8)]
def cena_img(t):
    tc = min(t, T_CONGELA)
    xh = 860 - (860 - 560) * sv(tc / T_CONGELA)
    cen = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(cen, 'RGBA')
    d.line([(CENTRO[0] - 420, CHAO), (CENTRO[0] + 420, CHAO)], fill=(120, 150, 110, 220), width=4)   # gramado
    for k in range(5): d.line([(CENTRO[0] - 400 + k * 200, CHAO + 30), (CENTRO[0] - 360 + k * 200, CHAO + 30)], fill=(90, 120, 85, 160), width=3)
    ela(d, XE, CHAO - 6, 1, braco=0.35, lado=1, cabeca_baixa=0.0, t=tc, emo=dict(aberta=0.4 * sv(tc / T_CONGELA)))
    hy = CHAO - 6 - 240; mx, my = XE + 78, hy + 64       # bandeira na mão dela
    d.line([(mx, my), (mx + 6, my - 120)], fill=(220, 220, 220, 255), width=4)
    d.polygon([(mx + 6, my - 120), (mx + 66, my - 104), (mx + 6, my - 84)], fill=(240, 200, 40, 255))
    ele(d, xh, CHAO - 6, 1, braco=0.7, lado=-1, t=tc, emo=dict(raiva=1.0, aberta=0.8))
    bx, by = xh - 70, CHAO - 6 - 230
    for i, (u, v) in enumerate(RAB):
        f = (tc * 1.4 + i / len(RAB)) % 1
        x0, y0 = bx - 120 * f, by + 40 * v * f
        d.line([(x0, y0), (x0 - 24, y0 + 9 * u)], fill=VERM + (int(255 * (1 - f)),), width=4)
    big = cen.resize((int(W * K), int(H * K)), Image.BICUBIC)
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.paste(big, (int(W / 2 - CENTRO[0] * K), int(1060 - CENTRO[1] * K)))
    return cam
def quadro(t):
    im = fundo.copy()
    cam = cena_img(t)
    esc = 1 - 0.88 * ap(t, T_CONGELA, 0.5)
    if esc < 0.999: cam.putalpha(cam.getchannel('A').point(lambda v: int(v * esc)))
    im = Image.alpha_composite(im, cam)
    q = 1 - ap(t, T_CONGELA, 0.4)
    im = texto(im, (W / 2, 260), 'Ele estava “só nervoso”.', ebg('Regular', 78), B, q)
    im = texto(im, (W / 2, 355), 'Ela estava trabalhando.', ebg('Italic', 78), G, q)
    f = jan(t, 4.2, 8.4)
    im = texto(im, (W / 2, 820), 'Segundos depois,', ebg('Regular', 70), B, f)
    im = texto(im, (W / 2, 910), 'ele deu uma cabeçada nela.', ebg('Italic', 70), G, f)
    im = texto(im, (W / 2, 1000), 'Campeonato Capixaba, abril de 2022', ebg('Italic', 34), C, f)
    f = jan(t, 8.6, 12.8)
    im = texto(im, (W / 2, 760), 'A pena: 200 dias de suspensão.', ebg('Regular', 64), B, f)
    im = texto(im, (W / 2, 880), 'A árbitra respondeu:', ebg('Regular', 52), C, f * ap(t, 9.4))
    im = texto(im, (W / 2, 960), '“Nós, mulheres,', ebg('Italic', 70), G, f * ap(t, 9.6))
    im = texto(im, (W / 2, 1045), 'não podemos nos calar.”', ebg('Italic', 70), G, f * ap(t, 9.6))
    im = texto(im, (W / 2, 1125), 'Marcielly Netto', ebg('Italic', 34), C, f * ap(t, 9.6))
    f = jan(t, 13.0, 20.0)
    im = texto(im, (W / 2, 560), 'Por que isso acontece?', ebg('Regular', 72), B, f)
    for i, (s1, s2) in enumerate([('Aprendeu que raiva', 'se resolve na força.'), ('Cresceu vendo violência:', 'risco maior, não destino.'),
                                  ('Ouviu a vida toda:', '“ele só ficou nervoso”.')]):
        a = f * ap(t, 14.0 + i * 1.6)
        im = texto(im, (W / 2, 730 + i * 200), s1, ebg('Regular', 56), B, a)
        im = texto(im, (W / 2, 800 + i * 200), s2, ebg('Italic', 56), G, a)
    f = jan(t, 20.2, 24.0)
    im = texto(im, (W / 2, 820), '1.571 feminicídios', ebg('Regular', 84), B, f)
    im = texto(im, (W / 2, 915), 'registrados no Brasil em 2025.', ebg('Italic', 60), G, f)
    im = texto(im, (W / 2, 1000), 'Recorde. Anuário Brasileiro de Segurança Pública, 2026', ebg('Italic', 32), C, f)
    f = jan(t, 24.2, 28.0)
    im = texto(im, (W / 2, 820), 'Nervoso todo mundo fica.', ebg('Regular', 76), B, f)
    im = texto(im, (W / 2, 920), 'Agredir é escolha.', ebg('Italic', 84), G, f * ap(t, 24.8))
    im = texto(im, (W / 2, 1010), 'Inspirado em Epicteto, Encheirídion, 1', ebg('Italic', 32), C, f * ap(t, 24.8))
    f = ap(t, 28.2)
    im = texto(im, (W / 2, 720), 'Mulheres, amigas:', ebg('Regular', 70), B, f)
    im = texto(im, (W / 2, 805), 'precisamos falar mais sobre isso.', ebg('Regular', 62), B, f)
    im = texto(im, (W / 2, 910), 'Conhecer o porquê é o primeiro', ebg('Italic', 58), G, f * ap(t, 28.9))
    im = texto(im, (W / 2, 985), 'passo para não normalizar.', ebg('Italic', 58), G, f * ap(t, 28.9))
    im = texto(im, (W / 2, 1130), 'Manda para quem ainda acha', ebg('Medium', 48), B, ap(t, 29.8))
    im = texto(im, (W / 2, 1195), 'que foi só nervoso.', ebg('Medium', 48), B, ap(t, 29.8))
    estilo.texto_espacado(ImageDraw.Draw(im, 'RGBA'), (W / 2, 1720), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(26, 500), (170, 165, 158, 210), 6)
    return im.convert('RGB')
if capa: quadro(2.6).save(capa)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    ff.stdin.write(estilo.para_bytes(np.asarray(quadro(t), np.float32) * cl((T - t) / 0.4)))
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida)
saida.with_suffix('.mudo.mp4').unlink(missing_ok=True); print('ok', saida)
