"""Série de dezembro "O preço de dar conta de tudo": Reel em mapa animado "Você precisa dar conta de tudo?".
Padrão dos diagramas anteriores (diagrama_energia.py): fundo escuro, serifa, setas finas em dourado, pergunta inteira no
quadro zero e primeira seta antes de 1 s. Ramificações: DEMANDAS REAIS x AUTOCOBRANÇA; convergência em três orientações;
fecho com reflexão autoral inspirada em Epicteto, Manual, § 1 (não é citação literal).
Base científica da legenda: Hill e Curran (2016), doi:10.1177/1088868315596286.
Uso: python3 reel_dar_conta_de_tudo.py saida.mp4 [capa.png]
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
W, H, FPS, T = 1080, 1920, 30, 30.0
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
saida = Path(sys.argv[1]); capa = Path(sys.argv[2]) if len(sys.argv) > 2 else None
FT = Path(__file__).with_name('fontes')
def ebg(nome, t): return ImageFont.truetype(str(FT / f'EBGaramond-{nome}.ttf'), t)   # acentos corretos (a Cormorant desloca o circunflexo)
fundo = np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.6): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0

# posições fixas (nada muda de lugar ou tamanho depois de aparecer)
O = (540, 560)                       # ponto central
ESQ, DIR = 280, 800                  # centros das colunas
Y_TIT, Y_ITEM0, PASSO = 760, 870, 88
CONV = (540, 1215)                   # ponto de convergência
Y_ORI = [1315, 1395, 1475]
F_TIT1, F_TIT2 = ebg('Regular', 80), ebg('Italic', 84)
F_RAMO, F_ITEM, F_ORI = ebg('Medium', 40), ebg('Regular', 46), ebg('Italic', 56)
DEM = [(3.0, 'Trabalho'), (4.3, 'Família'), (5.6, 'Responsabilidades')]
AUT = [(8.0, 'Não posso falhar.'), (9.3, 'Não posso descansar.'), (10.6, 'Tenho que ser forte.')]
ORI = [(14.2, 'Priorize o necessário.'), (15.6, 'Questione suas exigências.'), (17.0, 'Respeite seus limites.')]
T_FECHO = 19.2
REFLEXAO = [('Ser estoico não é aprender', B, False), ('a suportar tudo.', B, False), ('', None, False),
            ('É desenvolver sabedoria', G, True), ('para reconhecer o que realmente', G, True),
            ('precisa ser suportado', G, True), ('e o que pode ser mudado.', G, True)]

def seta(d, a, b, p, a8, w=3, ponta=True):
    if p <= 0: return
    x = a[0] + (b[0] - a[0]) * p; y = a[1] + (b[1] - a[1]) * p
    d.line((a[0], a[1], x, y), fill=G + (a8,), width=w)
    if ponta and p > 0.98:
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        for s in (-1, 1):
            d.line((x, y, x - 20 * math.cos(ang + s * 0.45), y - 20 * math.sin(ang + s * 0.45)), fill=G + (a8,), width=w)
def txt(d, xy, s, f, cor, a, anc='mm'):
    if a > 0.01 and s: d.text(xy, s, font=f, fill=cor + (int(255 * cl(a)),), anchor=anc)

def quadro(t):
    img = Image.fromarray(fundo).convert('RGBA')
    mapa = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(mapa)
    # título inteiro desde o quadro zero
    txt(d, (W / 2, 330), 'Você precisa', F_TIT1, B, 1)
    txt(d, (W / 2, 425), 'dar conta de tudo?', F_TIT2, B, 1)
    # ponto central e as duas setas (começam antes de 1 s)
    pc = ap(t, 0.2, 0.4)
    if pc > 0: d.ellipse((O[0] - 9, O[1] - 9, O[0] + 9, O[1] + 9), fill=G + (int(255 * pc),))
    seta(d, (O[0] - 14, O[1] + 10), (ESQ + 40, Y_TIT - 50), ap(t, 0.6, 1.2), 235)
    seta(d, (O[0] + 14, O[1] + 10), (DIR - 40, Y_TIT - 50), ap(t, 0.6, 1.2), 235)
    # ramificações
    txt(d, (ESQ, Y_TIT), 'DEMANDAS REAIS', F_RAMO, G, ap(t, 2.0, 0.5))
    txt(d, (DIR, Y_TIT), 'AUTOCOBRANÇA', F_RAMO, G, ap(t, 7.0, 0.5))
    for i, (t0, s) in enumerate(DEM):
        y = Y_ITEM0 + i * PASSO
        seta(d, (ESQ, y - PASSO + 32), (ESQ, y - 30), ap(t, t0 - 0.4, 0.4), 150, w=2, ponta=False)
        txt(d, (ESQ, y), s, F_ITEM, B, ap(t, t0, 0.5))
    for i, (t0, s) in enumerate(AUT):
        y = Y_ITEM0 + i * PASSO
        seta(d, (DIR, y - PASSO + 32), (DIR, y - 30), ap(t, t0 - 0.4, 0.4), 150, w=2, ponta=False)
        txt(d, (DIR, y), s, F_ITEM, B, ap(t, t0, 0.5))
    # convergência
    y_fim = Y_ITEM0 + 2 * PASSO + 40
    seta(d, (ESQ, y_fim), (CONV[0] - 12, CONV[1] - 12), ap(t, 12.0, 1.3), 235, ponta=False)
    seta(d, (DIR, y_fim), (CONV[0] + 12, CONV[1] - 12), ap(t, 12.0, 1.3), 235, ponta=False)
    pv = ap(t, 13.2, 0.4)
    if pv > 0: d.ellipse((CONV[0] - 9, CONV[1] - 9, CONV[0] + 9, CONV[1] + 9), fill=G + (int(255 * pv),))
    seta(d, (CONV[0], CONV[1] + 14), (CONV[0], Y_ORI[0] - 48), ap(t, 13.4, 0.6), 235)
    for t0, s in ORI: txt(d, (W / 2, Y_ORI[ORI.index((t0, s))]), s, F_ORI, B, ap(t, t0, 0.6))
    # no fecho, o mapa recua para dar lugar à reflexão
    rec = 1 - ap(t, T_FECHO, 0.7)
    if rec < 0.999: mapa.putalpha(mapa.getchannel('A').point(lambda v: int(v * rec)))
    img = Image.alpha_composite(img, mapa)
    if t > T_FECHO:
        top = Image.new('RGBA', img.size, (0, 0, 0, 0)); dt = ImageDraw.Draw(top)
        y = 760
        for i, (s, cor, it) in enumerate(REFLEXAO):
            if s: txt(dt, (W / 2, y), s, ebg('Italic', 58) if it else ebg('Regular', 60), cor, ap(t, T_FECHO + 0.6 + (0 if i < 3 else 1.4), 0.7))
            y += 40 if not s else 80
        txt(dt, (W / 2, y + 60), 'Reflexão autoral inspirada em', ebg('Italic', 36), C, ap(t, 23.0, 0.6))
        txt(dt, (W / 2, y + 108), 'Epicteto, Manual, § 1', ebg('Italic', 36), C, ap(t, 23.0, 0.6))
        img = Image.alpha_composite(img, top)
    dd = ImageDraw.Draw(img, 'RGBA')
    estilo.texto_espacado(dd, (W / 2, 1690), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(26, 500), (170, 165, 158, 210), 6)
    return img.convert('RGB')

if capa:
    quadro(18.9).save(capa)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    ff.stdin.write(estilo.para_bytes(np.asarray(quadro(t), np.float32) * cl((T - t) / 0.5)))
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida)
saida.with_suffix('.mudo.mp4').unlink(missing_ok=True); print('ok', saida)
