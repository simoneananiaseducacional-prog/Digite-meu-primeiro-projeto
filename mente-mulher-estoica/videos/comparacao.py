"""Comparação: ela olha a vida dos outros na tela do celular e vai ficando cinza; o jardim a seus pés está seco.
Ela baixa o celular, olha para o próprio jardim, ele floresce e ela volta a ser dourada.
Marco Aurélio, Meditações, 3.4. Uso: python3 comparacao.py saida.mp4
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia, personagens
from personagens import ela
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
W, H, FPS, T = 1080, 1920, 30, 20.0
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.4): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
def rgba(c, a): return c + (int(255 * cl(a)),)
def lerp(a, b, p): return a + (b - a) * p
def mix(a, b, p): return tuple(int(lerp(a[i], b[i], p)) for i in range(3))
def texto(im, xy, s, font, cor, a):
    if a < 0.02: return im
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).text(xy, s, font=font, fill=cor + (255,), anchor='mm')
    lay.putalpha(lay.getchannel('A').point(lambda v: int(v * cl(a))))
    return Image.alpha_composite(im, lay)

CHAO, K = 1250, 1.5
CENTRO = (540, 1080)
XE = 380
FLORES = [(560, 0.0), (640, 0.4), (720, 0.15), (800, 0.6), (870, 0.3), (500, 0.75)]
T_BAIXA, T_FLOR = 7.4, 8.6
OURO0, CINZA_ELA = personagens.DOURADO, (120, 120, 128)

def tela_celular(im, a, t):
    """Tela grande flutuante com a vida perfeita dos outros (posts trocando)."""
    if a < 0.02: return im
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    x0, y0, w, h = 560, 470, 400, 560
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), radius=38, fill=(22, 22, 26, 255), outline=(200, 200, 206, 255), width=4)
    k = int(t / 1.6) % 3
    cx, cy = x0 + w / 2, y0 + 230
    d.rectangle((x0 + 30, y0 + 50, x0 + w - 30, y0 + 410), fill=[(70, 110, 160), (200, 120, 90), (90, 150, 110)][k] + (255,))
    if k == 0:   # praia: sol e mar
        d.ellipse((cx - 50, cy - 110, cx + 50, cy - 10), fill=(250, 210, 120, 255)); d.rectangle((x0 + 30, cy + 40, x0 + w - 30, y0 + 410), fill=(40, 80, 140, 255))
    elif k == 1:   # festa: balões
        for i, c in enumerate([(240, 220, 120), (240, 140, 160), (150, 200, 240)]):
            bx = cx - 90 + i * 90; d.ellipse((bx - 34, cy - 80, bx + 34, cy - 4), fill=c + (255,)); d.line([(bx, cy - 4), (bx, cy + 110)], fill=(240, 240, 240, 255), width=2)
    else:   # jardim perfeito
        for i in range(7):
            fx = x0 + 60 + i * 47; d.line([(fx, y0 + 410), (fx, cy + 20)], fill=(40, 90, 50, 255), width=4)
            d.ellipse((fx - 16, cy + 4, fx + 16, cy + 36), fill=(250, 200, 220, 255))
    d.text((x0 + 40, y0 + 470), '12 mil curtidas', font=estilo.sem_serifa(34, 700), fill=(240, 90, 110, 255), anchor='lm')
    d.rounded_rectangle((x0 + 40, y0 + 505, x0 + w - 120, y0 + 520), radius=6, fill=(90, 90, 96, 255))
    lay.putalpha(lay.getchannel('A').point(lambda v: int(v * cl(a))))
    return Image.alpha_composite(im, lay)

def flor(d, x, cresce, abre, a, cor):
    if cresce < 0.02: return
    hgt = 110 * cresce; top = (x, CHAO - hgt)
    d.line([(x, CHAO), (x + 6 * math.sin(x), CHAO - hgt * 0.5), top], fill=rgba(mix((110, 100, 80), (120, 160, 90), abre), a), width=4, joint='curve')
    d.line([(x, CHAO - hgt * 0.45), (x - 18 * cresce, CHAO - hgt * 0.62)], fill=rgba((120, 150, 90), a * abre), width=3)
    if abre > 0.02:
        r = 16 * abre
        for k in range(6):
            ang = k * math.pi / 3; px, py = top[0] + r * math.cos(ang), top[1] + r * math.sin(ang)
            d.ellipse((px - r * 0.7, py - r * 0.7, px + r * 0.7, py + r * 0.7), fill=rgba(cor, a))
        d.ellipse((top[0] - 6, top[1] - 6, top[0] + 6, top[1] + 6), fill=rgba((255, 236, 190), a))
    else:   # broto seco caído
        d.line([top, (top[0] + 14, top[1] + 12)], fill=rgba((110, 100, 80), a), width=3)

fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
saida = Path(sys.argv[1]); ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    cena = 1 - 0.85 * ap(t, 11.6, 0.8)
    olhando = ap(t, 0.6, 0.5) * (1 - ap(t, T_BAIXA, 0.8))
    cinza = ap(t, 1.5, 4.5) * (1 - ap(t, T_FLOR + 1.0, 1.5))
    olha_chao = ap(t, T_BAIXA + 0.4, 0.8)
    brilho = ap(t, T_FLOR + 1.2, 1.2)
    cen = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(cen, 'RGBA')
    d.line([(CENTRO[0] - 380, CHAO), (CENTRO[0] + 380, CHAO)], fill=rgba(C, cena * 0.8), width=4)
    for i, (fx, atraso) in enumerate(FLORES):
        abre = ap(t, T_FLOR + atraso, 0.9)
        flor(d, fx, 0.45 + 0.55 * abre, abre, cena, mix((236, 214, 160), G, 0.5) if i % 2 else (240, 190, 200))
    personagens.DOURADO = mix(OURO0, CINZA_ELA, cinza)
    ela(d, XE, CHAO - 6, cena, braco=0.5 * olhando, lado=1, cabeca_baixa=0.25 * olhando + 0.7 * olha_chao * (1 - brilho * 0.6), t=t,
        emo=dict(triste=0.7 * cinza, sorriso=0.8 * brilho))
    personagens.DOURADO = OURO0
    if olhando > 0.05:   # celular na mão dela
        hy = CHAO - 6 - 240 + 4
        px, py = XE + 70, hy + 60
        d.rounded_rectangle((px - 11, py - 20, px + 11, py + 20), radius=3, fill=(30, 30, 32, int(255 * cena * olhando)), outline=rgba((210, 210, 216), cena * olhando), width=2)
    big = cen.resize((int(W * K), int(H * K)), Image.BICUBIC)
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.paste(big, (int(W / 2 - CENTRO[0] * K), int(1060 - CENTRO[1] * K)))
    im = fundo.copy()
    if brilho > 0.02:
        gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(gl).ellipse((200, 900, 1000, 1400), fill=G + (int(60 * brilho * cena),))
        im = Image.alpha_composite(im, gl.filter(ImageFilter.GaussianBlur(90)))
    im = Image.alpha_composite(im, cam)
    im = tela_celular(im, olhando * cena * ap(t, 1.0, 0.5), t)
    q = 1 - ap(t, 11.0, 0.6)   # pergunta inteira desde o quadro zero
    im = texto(im, (W / 2, 290), 'Você também se pega comparando', estilo.playfair(60), B, q)
    im = texto(im, (W / 2, 380), 'a sua vida com a que vê na tela?', estilo.playfair(62, True), G, q)
    f1 = jan(t, 12.0, 15.6); f2 = jan(t, 12.8, 15.6)
    im = texto(im, (W / 2, 790), 'A grama do vizinho é bonita.', estilo.playfair(66), B, f1)
    im = texto(im, (W / 2, 890), 'A sua precisa de você.', estilo.playfair(70, True), G, f2)
    f3 = jan(t, 15.9, 19.6)
    im = texto(im, (W / 2, 780), '“Não desperdice o que resta', estilo.playfair(56, True), B, f3)
    im = texto(im, (W / 2, 860), 'da sua vida pensando', estilo.playfair(56, True), B, f3)
    im = texto(im, (W / 2, 940), 'na vida dos outros.”', estilo.playfair(56, True), G, f3)
    im = texto(im, (W / 2, 1040), 'Marco Aurélio, Meditações, 3.4', estilo.playfair(32, True), C, f3)
    d2 = ImageDraw.Draw(im, 'RGBA')
    estilo.texto_espacado(d2, (W / 2, 1640), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(24, 500), rgba((170, 165, 158), 0.8), 6)
    ff.stdin.write(estilo.para_bytes(np.asarray(im.convert('RGB'), np.float32) * (1 - ap(t, T - 0.4, 0.4))))
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); print('ok', saida)
