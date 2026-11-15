"""O guarda-chuva: quando ela tem guarda-chuva, todos se abrigam. Quando a chuva cai só nela (sem guarda-chuva),
todos vão embora; só uma pessoa volta e divide o dela. Toda relação é troca: a diferença é o que buscam.
Base: Sêneca, Cartas a Lucílio 9. Ideia de contraste inspirada em @thequietfixx (cena própria).
Uso: python3 guarda_chuva.py saida.mp4
"""
import sys, math, random, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia, personagens
from personagens import ela, ele
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
W, H, FPS, T = 1080, 1920, 30, 28.0
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
TX = (205, 200, 194)
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.5): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
def rgba(c, a): return c + (int(255 * cl(a)),)
def lerp(a, b, p): return a + (b - a) * p
def seg(t, t0, t1): return estilo.suavizar(cl((t - t0) / (t1 - t0)))
CHAO = 1250; HY = CHAO - 6 - 240; XE = 540
CINZA0 = personagens.CINZA
# pessoas: (x embaixo do guarda-chuva, lado de onde vêm/para onde vão, chega)
PES = [(390, -1, 1.0), (690, 1, 1.4), (300, -1, 1.8), (780, 1, 2.2)]
AMIGA_X = 690
T_VAO, T_CHUVA2, T_VOLTA, T_FIM = 6.4, 10.4, 15.2, 20.4
random.seed(2)
GOTAS = [(random.uniform(0, W), random.uniform(0, H), random.uniform(900, 1300)) for _ in range(140)]

def guarda_chuva(d, x, topo, a, cor=G, larg=300):
    if a < 0.02: return
    d.pieslice((x - larg / 2, topo - larg / 4, x + larg / 2, topo + larg / 4), 180, 360, fill=rgba(cor, a))
    for i in range(1, 4):
        sx = x - larg / 2 + i * larg / 4
        d.line([(x, topo - larg / 4), (sx, topo)], fill=(16, 16, 16, int(120 * a)), width=2)
    d.line([(x, topo - larg / 4), (x, topo + 210)], fill=rgba(cor, a), width=5)
    d.arc((x - 30, topo + 190, x, topo + 230), 0, 180, fill=rgba(cor, a), width=5)

fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
FT = estilo.sem_serifa(54, 500)
saida = Path(sys.argv[1]); ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    a = ap(t, 0.05, 0.5)
    cena = a * (1 - 0.95 * ap(t, T_FIM, 0.8))
    cen = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(cen, 'RGBA')
    d.line([(0, CHAO), (W, CHAO)], fill=rgba(C, cena), width=4)
    tem_gc = 1 - seg(t, T_VAO - 0.2, T_VAO + 0.6)            # o guarda-chuva dela some (ela não tem mais o que oferecer)
    chuva1 = jan(t, 0.2, T_VAO + 0.4); chuva2 = ap(t, T_CHUVA2, 0.8)
    # luz: quente com todos, fria quando sozinha, volta morna com a amiga
    luz = 0.8 * tem_gc + 0.35 * seg(t, T_VOLTA + 1.0, T_VOLTA + 2.5)
    if luz > 0.02:
        gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl)
        gd.ellipse((XE - 420, HY - 300, XE + 420, CHAO + 60), fill=G + (int(55 * luz * cena),))
        cen = Image.alpha_composite(gl.filter(ImageFilter.GaussianBlur(70)), cen); d = ImageDraw.Draw(cen, 'RGBA')
    # chuva: geral no começo; só sobre ela depois
    for x, y0, v in GOTAS:
        y = (y0 + v * t) % (H + 60) - 30
        if chuva1 > 0.02 and not (XE - 150 < x < XE + 150 and y > HY - 180 and tem_gc > 0.5):
            d.line([(x, y), (x - 4, y + 22)], fill=(150, 170, 200, int(110 * chuva1 * cena)), width=2)
        if chuva2 > 0.02 and abs(x - XE) < 160 and y < CHAO:
            abrigada = seg(t, T_VOLTA + 1.2, T_VOLTA + 1.8) and y > HY - 150
            if not abrigada:
                d.line([(x, y), (x - 3, y + 22)], fill=(160, 180, 210, int(220 * chuva2 * cena)), width=3)
    # pessoas que se abrigavam
    for i, (xp, lado, ch) in enumerate(PES):
        chega = seg(t, ch, ch + 1.0)
        sai = seg(t, T_VAO + 0.6 + i * 0.4, T_VAO + 2.0 + i * 0.4)
        volta = seg(t, T_VOLTA, T_VOLTA + 1.6) if xp == AMIGA_X else 0.0
        fora = xp + lado * 520
        x = lerp(fora, xp, chega)
        x = lerp(x, fora, sai)
        x = lerp(x, AMIGA_X - 20, volta)
        if -120 < x < W + 120:
            personagens.CINZA = (190, 190, 196) if xp == AMIGA_X and volta > 0 else (150, 150, 158)
            ele(d, x, CHAO - 6, cena, braco=0.0, lado=-lado, t=t,
                emo=dict(sorriso=0.6 * chega * (1 - sai) + 0.7 * volta))
            personagens.CINZA = CINZA0
    triste = seg(t, T_VAO + 1.5, T_VAO + 3.0) * (1 - seg(t, T_VOLTA + 1.0, T_VOLTA + 2.0))
    ela(d, XE, CHAO - 6, cena, braco=0.0, lado=1, cabeca_baixa=0.6 * triste, t=t,
        emo=dict(sorriso=0.7 * tem_gc + 0.8 * seg(t, T_VOLTA + 1.2, T_VOLTA + 2.0), triste=0.8 * triste))
    guarda_chuva(d, XE, HY - 110, cena * tem_gc)
    # a amiga volta com um guarda-chuva pequeno, cinza, e divide
    gv = seg(t, T_VOLTA + 0.6, T_VOLTA + 1.4)
    if gv > 0.02: guarda_chuva(d, (XE + AMIGA_X - 20) / 2, HY - 100, cena * gv, cor=(195, 195, 200), larg=360)
    K = 1.45
    big = cen.resize((int(W * K), int(H * K)), Image.BICUBIC)
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.paste(big, (int(W / 2 - XE * K), int(H * 0.58 - (HY + 60) * K)))
    im = Image.alpha_composite(fundo, cam)
    im = Image.fromarray((np.asarray(im.convert('RGB'), np.float32) * (1 - 0.35 * seg(t, T_VAO + 2, T_CHUVA2 + 1) * (1 - seg(t, T_VOLTA + 1, T_VOLTA + 2.5)))).astype(np.uint8)).convert('RGBA')
    d2 = ImageDraw.Draw(im, 'RGBA')
    for t0, t1, s in [(0.4, 6.2, 'Quando ela tinha guarda-chuva…'), (7.0, 14.8, '…e quando a chuva caiu só nela.'), (15.2, 20.2, 'Alguém voltou.')]:
        fa = jan(t, t0, t1)
        if fa > 0.02: d2.text((W / 2, 330), s, font=FT, fill=rgba(TX, fa), anchor='mm')
    f1 = jan(t, T_FIM + 0.4, 27.6); f2 = jan(t, T_FIM + 1.8, 27.6); f3 = jan(t, T_FIM + 3.2, 27.6)
    if f1 > 0.02: d2.text((W / 2, 640), 'Toda relação é troca.', font=estilo.playfair(62), fill=rgba(B, f1), anchor='mm')
    if f2 > 0.02: d2.text((W / 2, 740), 'A diferença é o que buscam:', font=estilo.playfair(62), fill=rgba(B, f2), anchor='mm')
    if f3 > 0.02:
        d2.text((W / 2, 860), 'o seu guarda-chuva, ou você.', font=estilo.playfair(64, True), fill=rgba(G, f3), anchor='mm')
        estilo.texto_espacado(d2, (W / 2, 1080), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(26, 500), rgba((150, 146, 140), f3), 6)
    ff.stdin.write(estilo.para_bytes(np.asarray(im.convert('RGB'), np.float32) * (1 - ap(t, T - 0.3, 0.3))))
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); print('ok', saida)
