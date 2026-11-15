"""O barulho: ela cercada de ruído (notificações, discussões, "!!!"). Escolhe o simples (livro, água, caminhar).
Um círculo de calma se forma; o barulho bate e não a alcança. Base: Sêneca, Cartas a Lucílio 56.
Ideia inspirada em post de @drfernandokleis (crédito na legenda). Uso: python3 barulho.py saida.mp4
"""
import sys, math, random, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from personagens import ela
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
W, H, FPS, T = 1080, 1920, 30, 24.0
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
TX = (205, 200, 194)
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.5): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
def rgba(c, a): return c + (int(255 * cl(a)),)
def seg(t, t0, t1): return estilo.suavizar(cl((t - t0) / (t1 - t0)))
CHAO, X = 1250, 540
HY = CHAO - 6 - 240
CX, CY = X, HY + 110
random.seed(11)
ROT = ['!!!', '@#%', 'opinião', '🔔', 'urgente', 'discussão', '???', 'notícia', 'cobrança', '!!', 'comparação', 'pressa']
ROT = [r for r in ROT if r != '🔔']
RU = [(ROT[i % len(ROT)], random.uniform(0, 2 * math.pi), random.uniform(250, 380), random.uniform(0.5, 1.2), random.uniform(0, 3)) for i in range(16)]
F_RU = estilo.sem_serifa(32, 700)

def ruido(d, t, a, escudo):
    for i, (txt, ang0, r0, vel, t0) in enumerate(RU):
        aa = a * ap(t, 0.4 + t0 * 0.6, 0.4)
        if aa < 0.02: continue
        ang = ang0 + vel * t * 0.5
        r = r0 + 30 * math.sin(t * 2.3 + i)
        rmin = 240 * escudo
        if escudo > 0: r = max(r, rmin + 40 * abs(math.sin(t * 3 + i)))   # bate no círculo e volta
        x, y = CX + r * math.cos(ang), CY - 60 + r * math.sin(ang) * 0.75
        x += 6 * math.sin(t * 17 + i) * (1 - escudo)
        lw = d.textlength(txt, font=F_RU) + 34
        cor = (150, 60, 60) if i % 3 == 0 else (110, 110, 118)
        al = aa * (1 - 0.55 * escudo)
        d.rounded_rectangle((x - lw / 2, y - 26, x + lw / 2, y + 26), radius=22, fill=(22, 22, 24, int(235 * al)), outline=rgba(cor, al), width=3)
        d.text((x, y), txt, font=F_RU, fill=rgba((215, 205, 200), al), anchor='mm')

def livro(d, x, y, a):
    d.polygon([(x - 34, y - 4), (x, y + 6), (x, y + 30), (x - 34, y + 20)], outline=rgba(B, a), width=3)
    d.polygon([(x + 34, y - 4), (x, y + 6), (x, y + 30), (x + 34, y + 20)], outline=rgba(B, a), width=3)
def copo(d, x, y, a):
    d.polygon([(x - 14, y - 22), (x + 14, y - 22), (x + 10, y + 22), (x - 10, y + 22)], outline=rgba(B, a), width=3)
    d.rectangle((x - 11, y - 4, x + 11, y + 20), fill=(110, 160, 210, int(140 * a)))

fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
FT = estilo.sem_serifa(54, 500)
saida = Path(sys.argv[1]); ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    a = ap(t, 0.05, 0.5)
    cena = a * (1 - 0.97 * ap(t, 19.0, 0.8))
    cen = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(cen, 'RGBA')
    d.line([(0, CHAO), (W, CHAO)], fill=rgba(C, cena), width=4)
    escudo = seg(t, 11.0, 13.0)
    if escudo > 0.02:
        gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl)
        R = 230 * escudo
        gd.ellipse((CX - R, CY - R * 0.9, CX + R, CY + R * 0.9), fill=G + (int(45 * cena),))
        cen = Image.alpha_composite(gl.filter(ImageFilter.GaussianBlur(30)), cen); d = ImageDraw.Draw(cen, 'RGBA')
        d.ellipse((CX - R, CY - R * 0.9, CX + R, CY + R * 0.9), outline=rgba(G, cena * 0.8), width=3)
    ruido(d, t, cena, escudo)
    # o simples: livro, água (aparecem e ficam ao lado dela)
    la = jan(t, 6.0, 19.0); ca = jan(t, 7.4, 19.0)
    if la > 0.02: livro(d, X - 120, CHAO - 30, cena * la)
    if ca > 0.02: copo(d, X + 120, CHAO - 26, cena * ca)
    aflita = jan(t, 1.0, 6.4)
    calma = seg(t, 5.6, 7.0)
    tremor = 3 * math.sin(t * 30) * aflita
    ela(d, X + tremor, CHAO - 6, cena, braco=0.15, lado=1, cabeca_baixa=0.3 * aflita, t=t,
        emo=dict(triste=0.8 * aflita * (1 - calma), aberta=0.3 * aflita * (1 - calma), sorriso=0.8 * calma))
    K = 1.3
    big = cen.resize((int(W * K), int(H * K)), Image.BICUBIC)
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.paste(big, (int(W / 2 - CX * K), int(H * 0.56 - CY * K)))
    im = Image.alpha_composite(fundo, cam); d2 = ImageDraw.Draw(im, 'RGBA')
    for t0, t1, s in [(0.6, 5.6, 'O mundo está barulhento.'), (6.0, 10.6, 'Ela escolheu o simples.'), (11.2, 18.6, 'E o barulho já não a alcança.')]:
        fa = jan(t, t0, t1)
        if fa > 0.02: d2.text((W / 2, 300), s, font=FT, fill=rgba(TX, fa), anchor='mm')
    f1 = jan(t, 19.4, 23.6); f2 = jan(t, 20.6, 23.6)
    if f1 > 0.02: d2.text((W / 2, 760), 'Paz não é falta de barulho.', font=estilo.playfair(60), fill=rgba(B, f1), anchor='mm')
    if f2 > 0.02:
        d2.text((W / 2, 870), 'É silêncio por dentro.', font=estilo.playfair(64, True), fill=rgba(G, f2), anchor='mm')
        d2.text((W / 2, 980), 'Sêneca, Cartas a Lucílio, 56', font=estilo.playfair(32, True), fill=rgba(C, f2), anchor='mm')
        estilo.texto_espacado(d2, (W / 2, 1180), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(26, 500), rgba((150, 146, 140), f2), 6)
    ff.stdin.write(estilo.para_bytes(np.asarray(im.convert('RGB'), np.float32) * (1 - ap(t, T - 0.3, 0.3))))
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); print('ok', saida)
