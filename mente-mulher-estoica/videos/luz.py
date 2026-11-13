"""A luz (gaslighting): ele abaixa a luz, ela percebe, ele diz que ela está imaginando.
Com o tempo ela perde o brilho e deixa de confiar no que vê. No fim ela mesma acende a luz.
Origem do termo: peça Gas Light, de Patrick Hamilton (1938). Molde simples. Uso: python3 luz.py saida.mp4
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia, personagens
from personagens import ela, ele
from PIL import Image, ImageDraw
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
TXT = (200, 196, 190)
OURO = personagens.DOURADO
saida = Path(sys.argv[1])
fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1): return ap(t, t0) * (1 - ap(t, t1 - 0.5, 0.5))
def rgba(c, a): return c + (int(255 * cl(a)),)
def lerp(a, b, p): return a + (b - a) * p
def pulso(t, t0, t1, sobe=0.4): return ap(t, t0, sobe) * (1 - ap(t, t1 - sobe, sobe))

class Desenho(ImageDraw.ImageDraw):
    def __init__(self, im): super().__init__(im, 'RGBA')
    def text(self, xy, s, fill=None, **kw):
        if fill is not None and len(fill) == 4 and fill[3] < 3: return
        super().text(xy, s, fill=fill, **kw)

T = 26.0
CHAO = 1250
K, CX, CY = 1.5, 560, 1120
LX, LY = 610, CHAO - 330          # lâmpada
X_ELE = 790
FRASES = [(0.4, 4.6, ['Ele apaga um pouco a luz.']),
          (4.8, 9.4, ['Ela percebe.', 'Ele diz: “você está imaginando.”']),
          (9.6, 15.8, ['Com o tempo, ela deixa', 'de confiar no que vê.']),
          (16.4, 25.2, ['Confie no que você vê.'])]
ACENDE = 18.6

def luz(t):
    v = 1.0 - 0.25 * ap(t, 1.8, 0.6) - 0.25 * ap(t, 10.2, 0.6) - 0.25 * ap(t, 12.8, 0.6)
    return lerp(v, 1.0, ap(t, ACENDE, 0.8))
def brilho_ela(t):
    return lerp(1.0 - 0.65 * ap(t, 11.0, 4.0), 1.0, ap(t, ACENDE, 1.0))
def x_ela(t): return lerp(330, 480, estilo.suavizar(cl((t - 16.4) / 2.0)))
def braco_ele(t): return max(pulso(t, 1.0, 2.6), pulso(t, 9.6, 10.8), pulso(t, 12.2, 13.4))
def braco_ela(t): return max(pulso(t, 5.0, 7.8), pulso(t, 10.6, 12.0), pulso(t, 17.6, 19.6))
def nega(t):   # ele balança a cabeça (o corpo inteiro, de leve)
    return 7 * math.sin(t * 16) * max(pulso(t, 6.0, 7.8), pulso(t, 11.2, 12.2))
def baixa_ela(t): return ap(t, 13.6, 1.0) * (1 - ap(t, 16.2, 0.6))

# brilho radial da lâmpada (pré-calculado)
yy, xx = np.mgrid[0:H, 0:W]
DIST = np.sqrt((xx - LX) ** 2 + ((yy - LY) * 0.9) ** 2)
HALO = np.clip(1 - DIST / 520, 0, 1) ** 2

def luminaria(d, a, L):
    d.ellipse((LX - 60, CHAO - 14, LX + 60, CHAO + 6), outline=rgba(C, a), width=4)
    d.line([(LX, CHAO - 6), (LX, LY + 30)], fill=rgba(C, a), width=5)
    d.polygon([(LX - 70, LY + 30), (LX + 70, LY + 30), (LX + 42, LY - 60), (LX - 42, LY - 60)], fill=(20, 18, 16, int(255 * a)), outline=rgba(C, a))
    d.line([(LX - 70, LY + 30), (LX + 70, LY + 30)], fill=rgba(G, a * (0.3 + 0.7 * L)), width=5)

F = estilo.sem_serifa(54, 500)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    a = ap(t, 0.1, 0.6); L = luz(t)
    cen = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = Desenho(cen)
    # halo dourado da luz
    halo = (HALO * 150 * L * a).astype(np.uint8)
    camada = np.zeros((H, W, 4), np.uint8); camada[..., 0], camada[..., 1], camada[..., 2] = G
    camada[..., 3] = halo
    cen = Image.alpha_composite(cen, Image.fromarray(camada, 'RGBA')); d = Desenho(cen)
    d.line([(0, CHAO), (W, CHAO)], fill=rgba(C, a), width=4)
    luminaria(d, a, L)
    personagens.DOURADO = tuple(int(lerp(70, OURO[i], brilho_ela(t))) if i == 0 else int(lerp(64 if i == 1 else 50, OURO[i], brilho_ela(t))) for i in range(3))
    ela(d, x_ela(t), CHAO - 6, a, braco=braco_ela(t), lado=1, cabeca_baixa=baixa_ela(t), t=t)
    personagens.DOURADO = OURO
    ele(d, X_ELE + nega(t), CHAO - 6, a, braco=braco_ele(t), lado=-1, t=t)
    big = cen.resize((int(W * K), int(H * K)), Image.BICUBIC)
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.paste(big, (int(CX - CX * K), int(CY - CY * K)))
    # a sala escurece junto com a luz
    arr = np.asarray(Image.alpha_composite(fundo, cam).convert('RGB'), np.float32) * (0.45 + 0.55 * L)
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert('RGBA')
    d = Desenho(im)
    for t0, t1, linhas in FRASES:
        al = jan(t, t0, t1)
        for i, l in enumerate(linhas):
            d.text((W/2, 440 + i * 76), l, font=F, fill=rgba(TXT, al), anchor='mm')
    d.text((W/2, 1740), '@mente_mulher_estoica', font=estilo.sem_serifa(30, 400), fill=rgba(C, a * 0.8), anchor='mm')
    ff.stdin.write(estilo.para_bytes(np.asarray(im.convert('RGB'), np.float32) * (1 - ap(t, T - 0.8, 0.8))))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida)
print('ok', saida)
