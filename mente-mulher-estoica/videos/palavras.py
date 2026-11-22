"""Palavras x atitudes: ele diz coisas bonitas em balões dourados, mas a cada frase volta ao celular e a
deixa falando com o vazio. Fecho: Sêneca, Cartas a Lucílio, 20.2 (a filosofia ensina a agir, não a falar).
Uso: python3 palavras.py saida.mp4
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia, personagens
from personagens import ela, ele
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
W, H, FPS, T = 1080, 1920, 30, 20.0
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.4): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
def rgba(c, a): return c + (int(255 * cl(a)),)
def texto(im, xy, s, font, cor, a):
    if a < 0.02: return im
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).text(xy, s, font=font, fill=cor + (255,), anchor='mm')
    lay.putalpha(lay.getchannel('A').point(lambda v: int(v * cl(a))))
    return Image.alpha_composite(im, lay)

CHAO, K = 1250, 1.55
CENTRO = (540, 1080)
XE, XH = 400, 680
BEATS = [  # (início, frase dele)
    (1.0, 'Você é prioridade.'),
    (4.2, 'Pode contar comigo.'),
    (7.4, 'Eu me importo.'),
]
FB = estilo.sem_serifa(40, 600)

def balao(im, cx, cy, s, a, cor_fundo, cor_txt, ponta):
    if a < 0.02: return im
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    w = FB.getlength(s) + 70; h = 92
    x0 = min(max(cx - w / 2, 40), W - 40 - w)
    d.rounded_rectangle((x0, cy - h / 2, x0 + w, cy + h / 2), radius=40, fill=cor_fundo + (245,))
    d.polygon([(cx - 18, cy + h / 2 - 2), (cx + 18, cy + h / 2 - 2), (cx + 14 * ponta, cy + h / 2 + 34)], fill=cor_fundo + (245,))
    d.text((x0 + w / 2, cy + 2), s, font=FB, fill=cor_txt + (255,), anchor='mm')
    lay.putalpha(lay.getchannel('A').point(lambda v: int(v * cl(a))))
    return Image.alpha_composite(im, lay)

fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
saida = Path(sys.argv[1]); ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    cena = 1 - 0.85 * ap(t, 11.2, 0.8)
    # celular: depois de cada frase ele baixa a cabeça para o celular
    cel = 0.0
    for t0, _ in BEATS:
        cel = max(cel, ap(t, t0 + 1.4, 0.4) * (1 - ap(t, t0 + 3.0, 0.3)))
    cel = max(cel, ap(t, 9.8, 0.4))
    triste = cl(sum(ap(t, t0 + 2.0, 0.6) for t0, _ in BEATS) / 3)
    ve = ap(t, 10.0, 0.8)   # ela percebe: olha para as mãos dele
    cen = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(cen, 'RGBA')
    d.line([(CENTRO[0] - 360, CHAO), (CENTRO[0] + 360, CHAO)], fill=rgba(C, cena * 0.8), width=4)
    ele(d, XH, CHAO - 6, cena, braco=0.0, lado=-1, cabeca_baixa=0.8 * cel, t=t, emo=dict(sorriso=0.6 * (1 - cel)))
    if cel > 0.05:
        hy = CHAO - 6 - 240 + 16 * 0.8 * cel
        px, py = XH - 34, hy + 70
        d.rounded_rectangle((px - 10, py - 18, px + 10, py + 18), radius=3, fill=(30, 30, 32, int(255 * cena * cel)), outline=rgba((200, 200, 206), cena * cel), width=2)
        d.rectangle((px - 7, py - 14, px + 7, py + 10), fill=(120, 150, 200, int(220 * cena * cel)))
    ela(d, XE, CHAO - 6, cena, braco=0.0, lado=1, cabeca_baixa=0.35 * triste, t=t,
        emo=dict(triste=0.7 * triste * (1 - ve), sorriso=0.6 * ve))
    big = cen.resize((int(W * K), int(H * K)), Image.BICUBIC)
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.paste(big, (int(W / 2 - CENTRO[0] * K), int(1060 - CENTRO[1] * K)))
    im = Image.alpha_composite(fundo, cam)
    hx = W / 2 + (XH - CENTRO[0]) * K; ex = W / 2 + (XE - CENTRO[0]) * K
    for i, (t0, s) in enumerate(BEATS):   # a frase bonita dele
        im = balao(im, hx - 40, 640, s, jan(t, t0, t0 + 1.8) * cena, (236, 214, 160), (40, 30, 20), 1)
        im = balao(im, ex + 30, 680, 'Podemos conversar?', jan(t, t0 + 1.9, t0 + 3.1) * cena, (236, 232, 224), (24, 22, 20), -1)
    q = 1 - ap(t, 10.6, 0.6)   # pergunta inteira desde o quadro zero
    im = texto(im, (W / 2, 290), 'Você escuta as palavras', estilo.playfair(62), B, q)
    im = texto(im, (W / 2, 380), 'ou observa as atitudes?', estilo.playfair(64, True), G, q)
    f1 = jan(t, 11.6, 15.2); f2 = jan(t, 12.4, 15.2)
    im = texto(im, (W / 2, 800), 'Palavras se ouvem.', estilo.playfair(76), B, f1)
    im = texto(im, (W / 2, 900), 'Atitudes se veem.', estilo.playfair(76, True), G, f2)
    f3 = jan(t, 15.5, 19.6)
    im = texto(im, (W / 2, 800), '“A filosofia ensina', estilo.playfair(62, True), B, f3)
    im = texto(im, (W / 2, 885), 'a agir, não a falar.”', estilo.playfair(62, True), G, f3)
    im = texto(im, (W / 2, 990), 'Sêneca, Cartas a Lucílio, 20.2', estilo.playfair(32, True), C, f3)
    d2 = ImageDraw.Draw(im, 'RGBA')
    estilo.texto_espacado(d2, (W / 2, 1640), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(24, 500), rgba((170, 165, 158), 0.8), 6)
    ff.stdin.write(estilo.para_bytes(np.asarray(im.convert('RGB'), np.float32) * (1 - ap(t, T - 0.4, 0.4))))
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); print('ok', saida)
