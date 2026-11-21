"""Variação do "Curar" (1.834 nos reels de teste): ela segura um fio preso a alguém que está de costas, no celular.
Ele não se vira. Ela solta, põe a mão no peito e o dourado acende. Fecho: Sêneca, Cartas a Lucílio, 9.13.
Uso: python3 companhia.py saida.mp4
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia, personagens
from personagens import ela, ele
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
W, H, FPS, T = 1080, 1920, 30, 19.0
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.5): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
def rgba(c, a): return c + (int(255 * cl(a)),)
def lerp(a, b, p): return a + (b - a) * p
def mix(a, b, p): return tuple(int(lerp(a[i], b[i], p)) for i in range(3))

XE, XH, CHAO, K = 420, 690, 1250, 1.6
PEITO = (XE, 1090)
CENTRO = (555, 1090)          # centro da câmera
T_PUXA, T_SOLTA, T_VAI, T_MAO, T_OURO = 2.2, 5.6, 6.6, 9.2, 9.8

def fio(d, p0, p1, t, a, tenso, cor):
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]; L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    pts = []
    for k in range(41):
        u = k / 40
        w = (4 + 10 * (1 - tenso)) * math.sin(u * math.pi) * math.sin(t * 7 + u * 9) + 26 * (1 - tenso) * math.sin(u * math.pi)
        pts.append((p0[0] + dx * u + nx * w, p0[1] + dy * u + ny * w))
    d.line(pts, fill=rgba(cor, a), width=4, joint='curve')

fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
FQ = estilo.playfair(66); FQ2 = estilo.playfair(66, True)
saida = Path(sys.argv[1]); ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    cena_a = 1 - 0.8 * ap(t, 11.6, 0.8)
    solta = ap(t, T_SOLTA, 1.0); vai = ap(t, T_VAI, 2.2)
    mao = ap(t, T_MAO, 0.9); ouro = ap(t, T_OURO, 1.2)
    puxa = ap(t, T_PUXA, 0.8) * (1 - solta)
    cen = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(cen, 'RGBA')
    d.line([(CENTRO[0] - 360, CHAO), (CENTRO[0] + 360, CHAO)], fill=rgba(C, cena_a * 0.8), width=4)
    # ele, de costas, olhando o celular; depois vai embora
    xh = XH + 20 * puxa + 380 * vai; ah = cena_a * (1 - vai)
    if ah > 0.02:
        personagens.CINZA = (150, 150, 158)
        ele(d, xh, CHAO - 6, ah, braco=0.0, lado=1, cabeca_baixa=0.7, t=t)
        personagens.CINZA = (175, 175, 175)
        hy = CHAO - 6 - 240 + 16 * 0.7; hx = xh + 8 * 0.7
        # de costas: cobre o rosto e desenha a nuca com cabelo
        d.ellipse((hx - 38, hy - 38, hx + 38, hy + 38), fill=(120, 120, 128, int(255 * ah)), outline=rgba((150, 150, 158), ah), width=5)
        for i in range(-2, 3):   # mechas da nuca
            d.arc((hx - 30 + i * 12, hy - 30, hx + 30 + i * 12, hy + 34), 60, 120, fill=(95, 95, 102, int(255 * ah)), width=3)
        d.rounded_rectangle((xh + 34, hy + 52, xh + 52, hy + 84), radius=3, fill=(30, 30, 32, int(255 * ah)), outline=rgba((190, 190, 196), ah), width=2)
        d.rectangle((xh + 37, hy + 56, xh + 49, hy + 76), fill=(120, 150, 200, int(200 * ah)))
    # o fio: do peito dela até as costas dele; tenso quando ela puxa, cai quando ela solta
    costas = (xh - 4, 1095)
    if solta < 1:
        p_ini = (lerp(PEITO[0] + 14, costas[0] - 40, solta), lerp(PEITO[1], CHAO - 10, solta * 0.8))
        fio(d, p_ini, (costas[0], lerp(costas[1], CHAO - 8, solta)), t, cena_a * (1 - solta) * (1 - vai), puxa, (150, 150, 158))
    triste = 1 - ouro
    pc = mix((110, 110, 116), G, ouro); r = 12 + 6 * ouro
    d.ellipse((PEITO[0] - r, PEITO[1] - r, PEITO[0] + r, PEITO[1] + r), fill=rgba(pc, cena_a))
    personagens.MAO_PEITO = mao
    ela(d, XE - 12 * puxa, CHAO - 6, cena_a, braco=0.25 * puxa, lado=1, cabeca_baixa=0.5 * triste * ap(t, T_SOLTA - 0.6, 0.8), t=t,
        emo=dict(triste=0.8 * triste * ap(t, 1.0, 1.0), sorriso=0.8 * ap(t, T_OURO + 0.4, 1.0)))
    personagens.MAO_PEITO = 0.0
    big = cen.resize((int(W * K), int(H * K)), Image.BICUBIC)
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.paste(big, (int(W / 2 - CENTRO[0] * K), int(1060 - CENTRO[1] * K)))
    im = fundo.copy()
    if ouro > 0.02:
        px = W / 2 + (PEITO[0] - CENTRO[0]) * K
        gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl)
        gd.ellipse((px - 320, 1060 - 320, px + 320, 1060 + 320), fill=G + (int(80 * ouro * cena_a),))
        im = Image.alpha_composite(im, gl.filter(ImageFilter.GaussianBlur(90)))
    im = Image.alpha_composite(im, cam); d2 = ImageDraw.Draw(im, 'RGBA')
    q = 1 - ap(t, 5.4, 0.5)   # pergunta inteira desde o quadro zero
    if q > 0.02:
        d2.text((W / 2, 300), 'Você quer amor…', font=FQ, fill=rgba(B, q), anchor='mm')
        d2.text((W / 2, 395), 'ou só não ficar só?', font=FQ2, fill=rgba(G, q), anchor='mm')
    f1 = jan(t, 12.0, 15.2); f2 = jan(t, 12.9, 15.2)
    if f1 > 0.02:
        d2.text((W / 2, 800), 'Quem se encontra', font=estilo.playfair(72), fill=rgba(B, f1), anchor='mm')
    if f2 > 0.02:
        d2.text((W / 2, 900), 'não aceita qualquer companhia.', font=estilo.playfair(62, True), fill=rgba(G, f2), anchor='mm')
    f3 = jan(t, 15.5, 18.6)
    if f3 > 0.02:
        d2.text((W / 2, 800), '“O sábio basta a si mesmo', font=estilo.playfair(60, True), fill=rgba(B, f3), anchor='mm')
        d2.text((W / 2, 880), 'para viver feliz.”', font=estilo.playfair(60, True), fill=rgba(G, f3), anchor='mm')
        d2.text((W / 2, 990), 'Sêneca, Cartas a Lucílio, 9.13', font=estilo.playfair(32, True), fill=rgba(C, f3), anchor='mm')
    estilo.texto_espacado(d2, (W / 2, 1640), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(24, 500), rgba((170, 165, 158), 0.8), 6)
    ff.stdin.write(estilo.para_bytes(np.asarray(im.convert('RGB'), np.float32) * (1 - ap(t, T - 0.4, 0.4))))
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); print('ok', saida)
