"""Ayrton Senna era estoico? Reel com bonecos (sem imagem dele, sem capacete): um carro genérico em movimento no quadro zero,
para ao lado de um carro batido, o piloto desce e socorre o rival (Spa, 1992). Depois: Instituto (1994), Suzuka (1990)
e o fecho com Sêneca, Cartas a Lucílio 90.44. Pesquisa: mente-mulher-estoica/pesquisas/2026-11-28-senna-era-estoico.md
Uso: python3 senna_era_estoico.py saida.mp4 [capa.png]
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from personagens import ele
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pathlib import Path
W, H, FPS, T = 1080, 1920, 30, 28.5
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
FT = Path(__file__).with_name('fontes')
def ebg(n, t): return ImageFont.truetype(str(FT / f'EBGaramond-{n}.ttf'), t)
def cl(p): return max(0.0, min(1.0, p))
def sv(p): p = cl(p); return p * p * (3 - 2 * p)
def ap(t, t0, d=0.3): return sv((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.3): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
saida = Path(sys.argv[1]); capa = Path(sys.argv[2]) if len(sys.argv) > 2 else None
CHAO, K, CENTRO, TELA_Y = 1250, 1.25, (540, 1150), 1160
X_PARA, X_BATIDO, X_SOCORRO = 330, 800, 650
T_PARA, T_DESCE, T_CHEGA, T_DESLIGA, T_CENA = 3.4, 3.9, 5.3, 5.9, 10.2

def carro(d, x, y, cor, a, lado=1):
    """Carro de corrida genérico, de perfil, apontando para `lado`."""
    if a <= 0.01: return
    f = lambda px, py: (x + lado * px, y + py)
    c = cor + (int(255 * a),)
    d.polygon([f(-150, -30), f(-150, -68), f(-118, -74), f(-40, -74), f(-12, -98), f(28, -98), f(48, -70),
               f(150, -42), f(158, -30)], fill=(24, 23, 22, int(255 * a)), outline=c, width=5)
    d.line([f(-150, -70), f(-150, -112)], fill=c, width=5)
    d.line([f(-172, -112), f(-128, -112)], fill=c, width=9)
    d.line([f(118, -18), f(170, -18)], fill=c, width=7)
    d.line([f(26, -50), f(110, -42)], fill=G + (int(200 * a),), width=4)
    for wx in (-100, 96):
        cx, cy = f(wx, -28)
        d.ellipse((cx - 30, cy - 30, cx + 30, cy + 30), fill=(14, 14, 14, int(255 * a)), outline=c, width=5)
        d.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill=c)

def x_carro(t):
    p = cl(t / T_PARA); return 60 + (X_PARA - 60) * (1 - (1 - p) ** 2)

def texto(im, xy, s, font, cor, a):
    if a < 0.02: return im
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).text(xy, s, font=font, fill=cor + (255,), anchor='mm')
    lay.putalpha(lay.getchannel('A').point(lambda v: int(v * cl(a))))
    return Image.alpha_composite(im, lay)

def linhas(im, y0, itens, a, passo=84):
    for k, (s, f, cor, atraso) in enumerate(itens):
        im = texto(im, (W / 2, y0 + k * passo), s, f, cor, a * atraso)
    return im

fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
FUMACA = [(np.random.default_rng(i).uniform(-50, 50), np.random.default_rng(i + 9).uniform(0, 1)) for i in range(9)]
VELOC = [(np.random.default_rng(i + 30).uniform(-110, -20), np.random.default_rng(i + 60).uniform(0, 1)) for i in range(7)]

def quadro(t):
    cena = 1 - 0.9 * ap(t, T_CENA, 0.6)
    cen = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(cen, 'RGBA')
    d.line([(-200, CHAO), (1300, CHAO)], fill=C + (int(200 * cena),), width=4)
    xc = x_carro(t); vel = 1 - cl(t / T_PARA)
    for dy, fase in VELOC:   # linhas de velocidade enquanto o carro anda
        if vel > 0.05:
            px = xc - 190 - 260 * ((t * 2.2 + fase) % 1)
            d.line([(px, CHAO + dy), (px + 120 * vel, CHAO + dy)], fill=C + (int(170 * vel * cena),), width=4)
    carro(d, xc, CHAO, B, cena, lado=1)
    # carro batido, inclinado, com fumaça até o motor ser desligado
    bat = Image.new('RGBA', (W, H), (0, 0, 0, 0)); db = ImageDraw.Draw(bat, 'RGBA')
    carro(db, X_BATIDO, CHAO, C, cena, lado=-1)
    hx, hy = X_BATIDO - 8, CHAO - 112   # rival desacordado no cockpit, olhos fechados
    db.ellipse((hx - 26, hy - 26, hx + 26, hy + 26), fill=(18, 17, 16, int(255 * cena)), outline=C + (int(255 * cena),), width=5)
    for sx in (-1, 1): db.line([(hx + sx * 10 - 5, hy), (hx + sx * 10 + 5, hy)], fill=C + (int(255 * cena),), width=4)
    cen = Image.alpha_composite(cen, bat.rotate(9, resample=Image.BICUBIC, center=(X_BATIDO, CHAO))); d = ImageDraw.Draw(cen, 'RGBA')
    fum = 1 - ap(t, T_DESLIGA, 1.0)
    for dx, fase in FUMACA:
        sub = (t * 0.6 + fase) % 1; r = 14 + 30 * sub
        px, py = X_BATIDO - 40 + dx * 0.6 + 30 * sub, CHAO - 110 - 260 * sub
        d.ellipse((px - r, py - r, px + r, py + r), fill=(150, 146, 140, int(120 * (1 - sub) * fum * cena)))
    # o piloto desce, corre até o cockpit do rival e estende a mão
    a_p = ap(t, T_DESCE, 0.3) * cena
    if a_p > 0.01:
        corrida = cl((t - T_DESCE - 0.2) / (T_CHEGA - T_DESCE - 0.2))
        px = X_PARA + 20 + (X_SOCORRO - X_PARA - 20) * sv(corrida)
        bob = -7 * abs(math.sin(t * 9)) if 0 < corrida < 1 else 0
        abaixa = ap(t, T_CHEGA, 0.5)
        emo = dict(aberta=0.4) if t < T_DESLIGA else dict(triste=0.3 * (1 - ap(t, 7.5, 1)), sorriso=0.4 * ap(t, 7.5, 1))
        ele(d, px, CHAO + bob, a_p, braco=0.3 + 0.6 * abaixa, lado=1, cabeca_baixa=0.5 * abaixa, t=t, emo=emo)
    big = cen.resize((int(W * K), int(H * K)), Image.BICUBIC)
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.paste(big, (int(W / 2 - CENTRO[0] * K), int(TELA_Y - CENTRO[1] * K)))
    im = fundo.copy()
    br = ap(t, T_DESLIGA, 0.8) * cena
    if br > 0.02:   # luz dourada quando o perigo passa
        gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gx = W / 2 + (X_SOCORRO + 60 - CENTRO[0]) * K
        ImageDraw.Draw(gl).ellipse((gx - 300, 1000, gx + 300, 1460), fill=G + (int(70 * br),))
        im = Image.alpha_composite(im, gl.filter(ImageFilter.GaussianBlur(80)))
    im = Image.alpha_composite(im, cam)
    # textos
    q = 1 - ap(t, 4.2, 0.4)
    im = texto(im, (W / 2, 330), 'Ayrton Senna', ebg('Regular', 96), B, q)
    im = texto(im, (W / 2, 440), 'era estoico?', ebg('Italic', 104), G, q)
    a1 = jan(t, 4.5, 10.2)
    im = linhas(im, 300, [('Spa, 1992.', ebg('Italic', 60), G, 1),
                          ('Ele parou o próprio carro', ebg('Regular', 62), B, 1),
                          ('para socorrer um rival desacordado.', ebg('Regular', 58), B, ap(t, 5.2)),
                          ('O outro antes da corrida.', ebg('Italic', 70), G, ap(t, 7.0))], a1)
    a2 = jan(t, 10.5, 15.4)
    im = linhas(im, 600, [('1994.', ebg('Italic', 62), G, 1),
                          ('Pediu à irmã ajuda', ebg('Regular', 66), B, 1),
                          ('para cuidar das crianças do Brasil.', ebg('Regular', 60), B, ap(t, 11.2)),
                          ('Nasceu o Instituto Ayrton Senna.', ebg('Italic', 64), G, ap(t, 12.6))], a2, 92)
    a3 = jan(t, 15.6, 20.6)
    im = linhas(im, 600, [('Era estoico?', ebg('Regular', 76), B, 1),
                          ('Ninguém é estoico.', ebg('Regular', 68), B, ap(t, 16.4)),
                          ('A gente está estoico,', ebg('Italic', 70), G, ap(t, 17.4)),
                          ('a cada atitude.', ebg('Italic', 70), G, ap(t, 17.9))], a3, 96)
    a4 = jan(t, 20.8, 25.6)
    im = linhas(im, 640, [('“A natureza não dá a virtude.', ebg('Italic', 64), B, 1),
                          ('Tornar-se bom é uma arte.”', ebg('Italic', 64), G, ap(t, 21.6)),
                          ('Sêneca, Cartas a Lucílio, 90.44', ebg('Italic', 38), C, ap(t, 21.6))], a4, 96)
    a5 = ap(t, 25.8)
    im = texto(im, (W / 2, 700), 'Manda para quem', ebg('Regular', 76), B, a5)
    im = texto(im, (W / 2, 800), 'é fã do Senna.', ebg('Italic', 80), G, a5)
    estilo.texto_espacado(ImageDraw.Draw(im, 'RGBA'), (W / 2, 1720), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(26, 500), (170, 165, 158, 210), 6)
    return im.convert('RGB')

if __name__ == '__main__':
    if capa: quadro(1.2).save(capa)
    ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
    for k in range(int(T * FPS)):
        t = k / FPS
        ff.stdin.write(estilo.para_bytes(np.asarray(quadro(t), np.float32) * cl((T - t) / 0.4)))
    ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida)
    saida.with_suffix('.mudo.mp4').unlink(missing_ok=True); print('ok', saida)
