"""A mochila: amar alguém não é carregar o peso do outro; é caminhar ao lado.
Ele passa a mochila para ela, ela se curva; ela a coloca no chão, ele a pega de volta e seguem lado a lado.
Molde simples (uma ação, texto curto no alto). Ideia da frase: @eltoneuler. Uso: python3 mochila.py saida.mp4
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from personagens import ela, ele
from PIL import Image, ImageDraw
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
TXT = (200, 196, 190)
saida = Path(sys.argv[1])
fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1): return ap(t, t0) * (1 - ap(t, t1 - 0.5, 0.5))
def rgba(c, a): return c + (int(255 * cl(a)),)
def lerp(a, b, p): return a + (b - a) * p
def seg(t, t0, t1): return estilo.suavizar(cl((t - t0) / (t1 - t0)))

class Desenho(ImageDraw.ImageDraw):
    def __init__(self, im): super().__init__(im, 'RGBA')
    def text(self, xy, s, fill=None, **kw):
        if fill is not None and len(fill) == 4 and fill[3] < 3: return
        super().text(xy, s, fill=fill, **kw)

T = 24.0
CHAO = 1250
K, CX, CY = 1.65, 540, 1130
PASSA, PARA, LARGA, PEGA, SEGUE = 4.6, 11.0, 11.6, 13.4, 15.2
FRASES = [(0.4, 4.6, ['Amar alguém…']),
          (6.2, 11.0, ['…não é carregar', 'o peso do outro.']),
          (15.4, 23.2, ['É caminhar ao lado.'])]

def andando(t):   # 1 quando o mundo anda (chão rola)
    return 1 - ap(t, PARA, 0.6) + ap(t, SEGUE, 0.6)
def curva(t):     # quanto ela está curvada
    return seg(t, PASSA + 1.2, PASSA + 3.5) * (1 - seg(t, LARGA, LARGA + 1.2))
def x_ela(t): return 420 - 40 * curva(t)
def x_ele(t):
    x = 640 + 110 * seg(t, PASSA + 1.5, PARA)          # ele segue leve e se adianta
    return lerp(x, 650, seg(t, LARGA + 0.4, PEGA))     # volta para perto dela
def balanco(t, fase): return -6 * abs(math.sin(t * 7 + fase)) * andando(t)

def mochila(d, x, y, a, s=1.0):
    """Mochila pesada: corpo arredondado, bolso e alça."""
    w, h = 80 * s, 112 * s
    d.rounded_rectangle((x - w / 2, y - h / 2, x + w / 2, y + h / 2), radius=18 * s, fill=(30, 28, 26, int(255 * a)), outline=rgba(B, a), width=5)
    d.rounded_rectangle((x - w / 2 + 12, y + 4, x + w / 2 - 12, y + h / 2 - 12), radius=8, outline=rgba(B, a * 0.8), width=3)
    d.arc((x - 18, y - h / 2 - 22, x + 18, y - h / 2 + 10), 180, 360, fill=rgba(B, a), width=4)

def onde_mochila(t):
    """Posição da mochila e em quem ela está."""
    he = CHAO - 6 - 240   # cabeça em pé
    costas_ele = (x_ele(t) - 64, he + 120 + balanco(t, 1))
    costas_ela = (x_ela(t) - 64, he + 120 + balanco(t, 0))
    chao_meio = (540, CHAO - 58)
    if t < PASSA: return costas_ele, None
    if t < PASSA + 1.2:   # passa por cima, em arco
        p = seg(t, PASSA, PASSA + 1.2)
        x = lerp(costas_ele[0], costas_ela[0], p); y = lerp(costas_ele[1], costas_ela[1], p) - 120 * math.sin(math.pi * p)
        return (x, y), None
    if t < LARGA: return None, 'ela'                     # desenhada no corpo dela (curva junto)
    if t < LARGA + 1.0:
        p = seg(t, LARGA, LARGA + 1.0)
        return (lerp(costas_ela[0] + 10, chao_meio[0], p), lerp(costas_ela[1] + 20, chao_meio[1], p)), None
    if t < PEGA: return chao_meio, None
    if t < PEGA + 0.9:
        p = seg(t, PEGA, PEGA + 0.9)
        return (lerp(chao_meio[0], costas_ele[0], p), lerp(chao_meio[1], costas_ele[1], p) - 60 * math.sin(math.pi * p)), None
    return costas_ele, None

def figura(t, quem, a, com_mochila):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(lay, 'RGBA')
    if quem == 'ela':
        x, y = x_ela(t), CHAO - 6 + balanco(t, 0)
        if com_mochila: mochila(dd, x - 64, CHAO - 6 - 120 + balanco(t, 0), a, 1.15)
        ela(dd, x, y, a, braco=0.1, lado=1, cabeca_baixa=curva(t), t=t)
        ang = -15 * curva(t)
        return lay.rotate(ang, resample=Image.BICUBIC, center=(x, CHAO - 6)) if abs(ang) > 0.2 else lay
    x, y = x_ele(t), CHAO - 6 + balanco(t, 1)
    ele(dd, x, y, a, braco=0.1, lado=1, t=t)
    return lay

def chao(d, t, a):
    d.line([(0, CHAO), (W, CHAO)], fill=rgba(C, a), width=4)
    # marcas no chão que passam para trás (dá a ideia de caminhar)
    desloc = (t * 120 * 1.0)
    for i in range(-2, 14):
        x = (i * 110 - (desloc * 1.0 if True else 0)) % (W + 220) - 110
        d.line([(x, CHAO + 22), (x + 40, CHAO + 22)], fill=rgba(C, a * 0.5), width=3)

# o chão só rola quando andam: integra a velocidade
vel_acum = [0.0]
F = estilo.sem_serifa(56, 500)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
pos = 0.0
for k in range(int(T * FPS)):
    t = k / FPS
    pos += 120 / FPS * andando(t)
    a = ap(t, 0.1, 0.6)
    cen = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = Desenho(cen)
    d.line([(0, CHAO), (W, CHAO)], fill=rgba(C, a), width=4)
    for i in range(-2, 14):
        x = (i * 110 - pos) % (W + 220) - 110
        d.line([(x, CHAO + 22), (x + 40, CHAO + 22)], fill=rgba(C, a * 0.5), width=3)
    m, quem = onde_mochila(t)
    cen = Image.alpha_composite(cen, figura(t, 'ele', a, False))
    cen = Image.alpha_composite(cen, figura(t, 'ela', a, quem == 'ela'))
    if m: mochila(Desenho(cen), m[0], m[1], a)
    big = cen.resize((int(W * K), int(H * K)), Image.BICUBIC)
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.paste(big, (int(CX - CX * K), int(CY - CY * K)))
    d = Desenho(cam)
    for t0, t1, linhas in FRASES:
        al = jan(t, t0, t1)
        for i, l in enumerate(linhas):
            d.text((W/2, 470 + i * 76), l, font=F, fill=rgba(TXT, al), anchor='mm')
    d.text((W/2, 1720), '@mente_mulher_estoica', font=estilo.sem_serifa(30, 400), fill=rgba(C, a * 0.8), anchor='mm')
    im = Image.alpha_composite(fundo, cam).convert('RGB')
    ff.stdin.write(estilo.para_bytes(np.asarray(im, np.float32) * (1 - ap(t, T - 0.8, 0.8))))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida)
print('ok', saida)
