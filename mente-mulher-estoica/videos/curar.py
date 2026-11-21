"""Curar ou só parar de doer: ela tem fios cinzas presos ao peito (uma pessoa, o celular, um copo).
Solta um por vez, põe a mão no peito e só então o dourado acende (a cura vem de dentro). Fecho: Sêneca, Cartas a Lucílio, 50.4.
Ideia inspirada em @italoramon.neuro (cena própria; a frase atribuída a Hipócrates não tem fonte, por isso Sêneca).
Uso: python3 curar.py saida.mp4
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

XE, CHAO = 540, 1250
PEITO = (XE, 1090)
K = 1.6
FIOS = [  # (ponta no objeto, quando solta, para onde vai)
    ('pessoa', (300, 1080), 5.6, (-260, 0)),
    ('celular', (790, 975), 7.8, (260, -120)),
    ('copo', (770, 1175), 10.0, (260, 60)),
]
DUR = 1.3

def fio(d, p0, p1, t, fase, a, cor=(150, 150, 158)):
    pts = []
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]; L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    for k in range(41):
        u = k / 40
        w = 7 * math.sin(u * math.pi) * math.sin(t * 7 + fase + u * 9)
        pts.append((p0[0] + dx * u + nx * w, p0[1] + dy * u + ny * w))
    d.line(pts, fill=rgba(cor, a), width=4, joint='curve')

def celular(d, x, y, a):
    d.rounded_rectangle((x - 28, y - 50, x + 28, y + 50), radius=9, fill=(30, 30, 32, int(255 * a)), outline=rgba((170, 170, 176), a), width=4)
    d.line([(x - 10, y + 40), (x + 10, y + 40)], fill=rgba((170, 170, 176), a), width=3)
    d.ellipse((x + 10, y - 58, x + 34, y - 34), fill=(190, 70, 70, int(230 * a)))   # notificação

def copo(d, x, y, a):
    c = rgba((170, 170, 176), a)
    d.polygon([(x - 30, y - 60), (x + 30, y - 60), (x + 8, y - 10), (x - 8, y - 10)], outline=c, fill=(60, 30, 36, int(200 * a)))
    d.line([(x, y - 10), (x, y + 30)], fill=c, width=4); d.line([(x - 22, y + 30), (x + 22, y + 30)], fill=c, width=4)

fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
FQ = estilo.playfair(66); FQ2 = estilo.playfair(66, True)
saida = Path(sys.argv[1]); ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    cena_a = 1 - 0.8 * ap(t, 13.6, 0.8)
    mao = ap(t, 11.4, 0.9); ouro = ap(t, 12.0, 1.2)
    soltos = sum(ap(t, ts, DUR) for _, _, ts, _ in FIOS) / 3
    cen = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(cen, 'RGBA')
    d.line([(XE - 360, CHAO), (XE + 360, CHAO)], fill=rgba(C, cena_a * 0.8), width=4)
    for i, (nome, ponta, ts, saida_v) in enumerate(FIOS):
        s = ap(t, ts, DUR)
        oa = cena_a * (1 - s)
        ox, oy = ponta[0] + saida_v[0] * s, ponta[1] + saida_v[1] * s
        if oa > 0.02:
            # o fio se solta do peito e vai junto com o objeto
            ini = (lerp(PEITO[0], ox, 0.85 * s), lerp(PEITO[1], oy, 0.85 * s))
            fio(d, ini, (ox, oy), t, i * 2.1, oa * (1 - 0.3 * s))
            if nome == 'pessoa':
                personagens.CINZA = (150, 150, 158)
                ele(d, ox - 10, CHAO - 6, oa, braco=0.6 * (1 - s), lado=1, t=t)
                personagens.CINZA = (175, 175, 175)
            elif nome == 'celular': celular(d, ox, oy, oa)
            else: copo(d, ox, oy + 60, oa)
    triste = 1 - ouro
    # peito: ponto cinza que só acende quando ela põe a mão
    pc = mix((120, 120, 126), G, ouro); r = 12 + 6 * ouro
    d.ellipse((PEITO[0] - r, PEITO[1] - r, PEITO[0] + r, PEITO[1] + r), fill=rgba(pc, cena_a))
    personagens.MAO_PEITO = mao
    ela(d, XE, CHAO - 6, cena_a, braco=0.0, lado=1, cabeca_baixa=0.6 * triste * (1 - 0.3 * soltos), t=t,
        emo=dict(triste=0.8 * triste, sorriso=0.8 * ap(t, 12.4, 1.0)))
    personagens.MAO_PEITO = 0.0
    big = cen.resize((int(W * K), int(H * K)), Image.BICUBIC)
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.paste(big, (int(W / 2 - PEITO[0] * K), int(1060 - PEITO[1] * K)))
    im = fundo.copy()
    if ouro > 0.02:
        gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl)
        gd.ellipse((W / 2 - 330, 1060 - 330, W / 2 + 330, 1060 + 330), fill=G + (int(80 * ouro * cena_a),))
        im = Image.alpha_composite(im, gl.filter(ImageFilter.GaussianBlur(90)))
    im = Image.alpha_composite(im, cam); d2 = ImageDraw.Draw(im, 'RGBA')
    q = 1 - ap(t, 5.0, 0.5)   # pergunta inteira desde o quadro zero
    if q > 0.02:
        d2.text((W / 2, 300), 'Você quer se curar…', font=FQ, fill=rgba(B, q), anchor='mm')
        d2.text((W / 2, 395), 'ou só parar de doer?', font=FQ2, fill=rgba(G, q), anchor='mm')
    f1 = jan(t, 14.0, 18.6); f2 = jan(t, 15.2, 18.6)
    if f1 > 0.02:
        d2.text((W / 2, 760), 'O nosso mal', font=estilo.playfair(72), fill=rgba(B, f1), anchor='mm')
        d2.text((W / 2, 860), 'não vem de fora:', font=estilo.playfair(72), fill=rgba(B, f1), anchor='mm')
    if f2 > 0.02:
        d2.text((W / 2, 980), 'está dentro de nós.', font=estilo.playfair(74, True), fill=rgba(G, f2), anchor='mm')
        d2.text((W / 2, 1100), 'Sêneca, Cartas a Lucílio, 50.4', font=estilo.playfair(32, True), fill=rgba(C, f2), anchor='mm')
    estilo.texto_espacado(d2, (W / 2, 1640), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(24, 500), rgba((170, 165, 158), 0.8), 6)
    ff.stdin.write(estilo.para_bytes(np.asarray(im.convert('RGB'), np.float32) * (1 - ap(t, T - 0.4, 0.4))))
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); print('ok', saida)
