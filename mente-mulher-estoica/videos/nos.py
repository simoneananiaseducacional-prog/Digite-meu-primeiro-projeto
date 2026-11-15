"""Os nós (texto autoral da Simone): ela segura um fio cheio de nós. Os nós cinzas (dos outros) ela solta;
o dourado (dela) guarda para depois; por fim, senta e descansa. Base: Epicteto, Encheirídion 1.
Uso: python3 nos.py saida.mp4
"""
import sys, math, random, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from personagens import ela
from PIL import Image, ImageDraw
from pathlib import Path
W, H, FPS, T = 1080, 1920, 30, 26.0
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
TX = (205, 200, 194)
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.5): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
def rgba(c, a): return c + (int(255 * cl(a)),)
def lerp(a, b, p): return a + (b - a) * p
def seg(t, t0, t1): return estilo.suavizar(cl((t - t0) / (t1 - t0)))
CHAO, XE = 1250, 330
HY = CHAO - 6 - 240
# nós: (x, cor, quando sai, para onde)
NOS = [(540, C, 3.6, (880, 760)), (640, C, 4.8, (930, 900)), (740, G, None, None), (840, C, 12.0, (960, 780))]
random.seed(4)
def no(d, x, y, cor, a, t):
    if a < 0.02: return
    for i in range(5):
        r = 30 + 8 * math.sin(i * 1.7)
        dx, dy = 10 * math.cos(i * 1.3 + t * 0.6), 8 * math.sin(i * 2.1 + t * 0.5)
        d.ellipse((x + dx - r, y + dy - r * 0.7, x + dx + r, y + dy + r * 0.7), outline=rgba(cor, a), width=5)
fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
FRASES = [(1.0, 5.8, 'Nem todo nó é meu para desatar.'), (7.0, 11.4, 'Nem tudo precisa ser resolvido hoje.'),
          (11.6, 15.6, 'E nem tudo merece a minha energia.'), (16.4, 25.4, 'Às vezes, o mais sensato é descansar.')]
saida = Path(sys.argv[1]); ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    a = ap(t, 0.05, 0.5)
    cen = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(cen, 'RGBA')
    d.line([(0, CHAO), (W, CHAO)], fill=rgba(C, a), width=4)
    senta = seg(t, 16.6, 18.0)
    noite = seg(t, 16.4, 19.0)
    for i in range(40 * (noite > 0)):
        x, y = random.Random(i).uniform(40, 1040), random.Random(i + 99).uniform(380, 900)
        d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(230, 225, 215, int(200 * noite * (0.5 + 0.5 * math.sin(t * 2 + i)))))
    if noite > 0.02:
        d.ellipse((700, 420, 780, 500), fill=rgba((235, 225, 200), noite)); d.ellipse((720, 410, 800, 490), fill=(18, 18, 18, int(255 * noite)))
    # fio
    y_fio = HY + 70 + 140 * senta
    mao = (XE + 150, y_fio)
    ativos = [n for n in NOS if n[2] is None or t < n[2] + 1.2]
    fim_x = max([n[0] for n in ativos if n[2] is None or t < n[2]] + [mao[0]]) + 60
    fio_a = a * (1 - senta) * (1 - seg(t, 12.4, 13.4))
    d.line([mao, (fim_x * (1 - senta) + mao[0] * senta, y_fio + 20 * math.sin(t))], fill=rgba(TX, fio_a), width=3)
    for x, cor, sai, alvo in NOS:
        if sai is None:   # o dourado: guarda ao lado dela
            gx = lerp(x, XE - 120, seg(t, 9.0, 10.4)); gy = lerp(y_fio, CHAO - 40, seg(t, 9.0, 10.4))
            no(d, gx, gy, cor, a, t)
        else:
            p = seg(t, sai, sai + 1.6)
            no(d, lerp(x, alvo[0], p), lerp(y_fio, alvo[1], p), cor, a * (1 - p), t)
    ela(d, XE, CHAO - 6, a, braco=0.6 * (1 - senta), lado=1, sentada=senta, t=t,
        emo=dict(sorriso=0.3 + 0.6 * seg(t, 5.0, 6.0), triste=0.4 * jan(t, 0.5, 4.2)))
    K, CX, CY = 1.3, 590, 1080
    big = cen.resize((int(W * K), int(H * K)), Image.BICUBIC)
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.paste(big, (int(W / 2 - CX * K), int(H * 0.58 - CY * K)))
    im = Image.alpha_composite(fundo, cam); d2 = ImageDraw.Draw(im, 'RGBA')
    for t0, t1, s in FRASES:
        fa = jan(t, t0, t1)
        if fa > 0.02:
            f = estilo.playfair(56, t0 > 16) if True else None
            d2.text((W / 2, 440), s, font=f, fill=rgba(G if t0 > 16 else B, fa), anchor='mm')
    fa = jan(t, 20.0, 25.4)
    if fa > 0.02: estilo.texto_espacado(d2, (W / 2, 1560), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(26, 500), rgba((150, 146, 140), fa), 6)
    ff.stdin.write(estilo.para_bytes(np.asarray(im.convert('RGB'), np.float32) * (1 - ap(t, T - 0.4, 0.4))))
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); print('ok', saida)
