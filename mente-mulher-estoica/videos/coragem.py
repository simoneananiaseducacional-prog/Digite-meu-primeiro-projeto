"""Coragem: sentir medo + fazer assim mesmo. Ela atravessa a ponte tremendo; no cruzamento dos círculos acende CORAGEM.
Ideia do diagrama: @alfredosoares (crédito na legenda). Desenho próprio, personagens fixos. Ou ação, ou texto.
Uso: python3 coragem.py saida.mp4
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from personagens import ela
from PIL import Image, ImageDraw, ImageChops
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
saida = Path(sys.argv[1])
fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGB')
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1): return ap(t, t0) * (1 - ap(t, t1 - 0.5, 0.5))
def rgba(c, a): return c + (int(255 * max(0, min(1, a))),)
class Texto:
    """Desenha texto com transparência de verdade (o Pillow ignora o alfa do texto neste modo)."""
    def __init__(self, im): self.im = im
    def text(self, xy, s, font, fill, anchor='mm'):
        a = fill[3] if len(fill) == 4 else 255
        if a < 3: return
        cam = Image.new('RGBA', self.im.size, (0, 0, 0, 0))
        ImageDraw.Draw(cam).text(xy, s, font=font, fill=fill[:3] + (255,), anchor=anchor)
        if a < 255: cam.putalpha(cam.getchannel('A').point(lambda v: v * a // 255))
        self.im.paste(cam, (0, 0), cam)
T = 29.0
CHAO = 1250; R = 260
C1, C2 = (340, 1130), (740, 1130)
BORDA_E, BORDA_D = 380, 700
# lente (cruzamento dos círculos)
m1 = Image.new('L', (W, H)); ImageDraw.Draw(m1).ellipse((C1[0] - R, C1[1] - R, C1[0] + R, C1[1] + R), fill=255)
m2 = Image.new('L', (W, H)); ImageDraw.Draw(m2).ellipse((C2[0] - R, C2[1] - R, C2[0] + R, C2[1] + R), fill=255)
LENTE = ImageChops.multiply(m1, m2)
OURO = Image.new('RGB', (W, H), G)

def x_dela(t):
    if t < 5: return 250
    if t < 6.5: return 250 - 30 * estilo.suavizar((t - 5) / 1.5)          # recua
    if t < 11: return 220
    if t < 15: return 220 + 320 * estilo.suavizar((t - 11) / 4)          # passo a passo até o meio
    if t < 17.5: return 540
    if t < 20.5: return 540 + 290 * estilo.suavizar((t - 17.5) / 3)      # chega do outro lado
    return 830
def tremor(t):
    if 4.5 < t < 17.5: return 4 * math.sin(t * 47) * (1 - ap(t, 15, 2.5))
    return 0

def cena(im, d, tx, t, brilho):
    # penhascos
    d.line([(60, CHAO), (BORDA_E, CHAO), (BORDA_E - 20, CHAO + 260)], fill=rgba(C, brilho), width=4)
    d.line([(1020, CHAO), (BORDA_D, CHAO), (BORDA_D + 20, CHAO + 260)], fill=rgba(C, brilho), width=4)
    # ponte de tábuas e corda
    for i in range(10):
        x = BORDA_E + 6 + i * 32
        sag = 14 * math.sin(math.pi * (x - BORDA_E) / (BORDA_D - BORDA_E))
        d.rectangle((x, CHAO + sag - 4, x + 24, CHAO + sag + 6), outline=rgba(C, brilho), width=2)
    # círculo 1: sentir medo
    p1 = ap(t, 3.2, 1.6)
    if p1: d.arc((C1[0] - R, C1[1] - R, C1[0] + R, C1[1] + R), 90, 90 + 360 * p1, fill=rgba(B, brilho), width=4)
    for i, l in enumerate(['SENTIR', 'MEDO']):
        tx.text((235, 1450 + i * 52), l, font=estilo.sem_serifa(44, 700), fill=rgba(B, ap(t, 4.6) * brilho), anchor='mm')
    # círculo 2: fazer assim mesmo
    p2 = ap(t, 7.5, 1.6)
    if p2: d.arc((C2[0] - R, C2[1] - R, C2[0] + R, C2[1] + R), 90, 90 + 360 * p2, fill=rgba(B, brilho), width=4)
    for i, l in enumerate(['FAZER', 'ASSIM MESMO']):
        tx.text((850, 1450 + i * 52), l, font=estilo.sem_serifa(40, 700), fill=rgba(B, ap(t, 8.9) * brilho), anchor='mm')
    # cruzamento acende quando ela pisa no meio
    acende = ap(t, 14.6, 1.0)
    if acende:
        im.paste(Image.blend(im, OURO, 0.55 * acende * brilho), (0, 0), LENTE)
        d.line([(540, 790), (540, 940 * 1.0)], fill=rgba(G, acende * brilho), width=3)
        tx.text((540, 740), 'CORAGEM', font=estilo.playfair(84), fill=rgba(G, acende * brilho), anchor='mm')
    ela(d, x_dela(t) + tremor(t), CHAO - 6, brilho, braco=0.15, lado=1, t=t)

P = estilo.playfair
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    im = fundo.copy(); d = ImageDraw.Draw(im, 'RGBA'); tx = Texto(im)
    # gancho (texto) -> ação -> fecho (texto)
    g = jan(t, 0, 3.2)
    for i, l in enumerate(['Você espera o medo passar', 'para dar o passo?']):
        tx.text((W/2, 420 + i * 86), l, font=P(66), fill=rgba(B, g), anchor='mm')
    brilho = ap(t, 0.2, 0.8) * (1 - 0.75 * ap(t, 21, 0.8))
    cena(im, d, tx, t, brilho)
    f1 = ap(t, 21.6, 0.7)
    tx.text((W/2, 300), 'Coragem não é não ter medo.', font=P(64), fill=rgba(B, f1), anchor='mm')
    tx.text((W/2, 400), 'É dar o passo tremendo.', font=P(70, True), fill=rgba(G, ap(t, 23, 0.7)), anchor='mm')
    f3 = ap(t, 25, 0.7)
    for i, l in enumerate(['“Há mais coisas que nos assustam', 'do que coisas que nos ferem.”']):
        tx.text((W/2, 1640 + i * 56), l, font=P(42, True), fill=rgba(B, f3), anchor='mm')
    tx.text((W/2, 1770), 'Sêneca, Cartas a Lucílio, 13.4 (tradução livre)', font=P(30, True), fill=rgba(C, f3), anchor='mm')
    ff.stdin.write(estilo.para_bytes(np.asarray(im, np.float32) * (1 - ap(t, T - 0.8, 0.8))))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida)
print('ok', saida)
