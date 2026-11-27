"""Série Estoicismo nos relacionamentos, ep. 1: o que depende de você.
Desenho: duas mãos em concha, uma dourada (o que é seu) e uma cinza, fora de alcance.
Ou ação, ou texto (base 017). Playfair por causa dos acentos. Uso: python3 maos_controle.py saida.mp4
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
CINZA2 = (150, 150, 150)
saida = Path(sys.argv[1])
fundo = np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)
def ap(t, t0, d=0.4): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1): return ap(t, t0) * (1 - ap(t, t1 - 0.3, 0.3))
def cl(p): return max(0.0, min(1.0, p))
def lerp(a, b, p): return a + (b - a) * p
def rgba(c, a): return c + (int(255 * cl(a)),)
T = 29.8
fim = lambda t: 1 - ap(t, T - 0.8, 0.6)
FT, FI = estilo.playfair(58), estilo.playfair(58, True)
FP = estilo.playfair(48)
FR = estilo.playfair(38, True)

def capsula(cx, cy, w, h, ang, off):
    r = w / 2 + off; pts = []
    for k in range(13):
        a = math.pi + math.pi * k / 12
        pts.append((r * math.cos(a), -h / 2 + w / 2 + r * math.sin(a)))
    for k in range(13):
        a = math.pi * k / 12
        pts.append((r * math.cos(a), h / 2 - w / 2 + r * math.sin(a)))
    ca, sa = math.cos(ang), math.sin(ang)
    return [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]

def mao(d, cx, cor, a, s=1):
    """Mão aberta, palma para a frente: contorno único da palma, dedos, polegar e pulso."""
    if a <= 0.01: return
    def formas(off, cor_f):
        d.rounded_rectangle((cx - 95 - off, 905 - off, cx + 95 + off, 1095 + off), radius=48 + off, fill=cor_f)
        d.rounded_rectangle((cx - 68 - off, 1060 - off, cx + 68 + off, 1170 + off), radius=20 + off, fill=cor_f)
        for dx, h in ((-68, 120), (-23, 150), (23, 140), (68, 105)):
            d.polygon(capsula(cx + dx, 935 - h / 2 + 20, 42, h, 0, off), fill=cor_f)
        d.polygon(capsula(cx + s * 112, 1010, 46, 125, s * -0.62, off), fill=cor_f)
    formas(4, rgba(cor, a))
    formas(0, (22, 22, 22, int(255 * a)))
    for dx in (-45, 0, 45):   # vincos dos dedos
        d.line([(cx + dx, 912), (cx + dx, 935)], fill=rgba(cor, 0.5 * a), width=2)

ESQ, DIR = 290, 790
MEUS = [('suas palavras', 7.9), ('suas decisões', 9.5), ('suas atitudes', 11.1)]
DELE = [('o caráter dele', 12.9), ('a honestidade dele', 14.5), ('a vontade dele', 16.1)]
YS = [1225, 1290, 1355]
def txt(d, xy, s, f, cor, a):
    if a > 0.01: d.text(xy, s, font=f, fill=rgba(cor, a), anchor='mm')
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    img = Image.fromarray(fundo).convert('RGBA'); cam = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
    f = fim(t)
    am = ap(t, 3.6, 1.2)
    mao(d, ESQ, G, am * f, 1); mao(d, DIR, CINZA2, am * f, -1)
    # fronteira tracejada: o limite do seu alcance
    for y in range(700, 1390, 28):
        if am > 0: d.line([(W/2, y), (W/2, y + 14)], fill=rgba(C, 0.6 * am * f), width=2)
    txt(d, (ESQ, 740), 'depende de você', FR, G, ap(t, 4.9) * f)
    txt(d, (DIR, 740), 'não depende de você', FR, CINZA2, ap(t, 5.3) * f)
    for i, (s, t0) in enumerate(MEUS):     # caem e assentam na mão dourada
        q = cl((t - t0) / 0.8)
        if q > 0: txt(d, (ESQ, lerp(YS[i] + 40, YS[i], estilo.suavizar(q))), s, FP, B, q * f)
    for i, (s, t0) in enumerate(DELE):     # surgem e se afastam para cima, fora do alcance
        a = ap(t, t0, 0.5)
        sobe = -50 * cl((t - 17.4) / 1.6)
        if a > 0: txt(d, (DIR - sobe, YS[i]), s, FP, CINZA2, a * (1 - 0.5 * cl((t - 17.4) / 1.6)) * f)
    # topo: ou ação, ou texto
    txt(d, (W/2, 470), 'Você já tentou de tudo', FT, B, jan(t, 0.3, 3.5)); txt(d, (W/2, 550), 'para ser compreendida?', FI, G, jan(t, 0.8, 3.5))
    txt(d, (W/2, 470), 'Você responde pela sua conduta.', FT, B, jan(t, 18.0, 21.4)); txt(d, (W/2, 550), 'Não pelo caráter do outro.', FI, G, jan(t, 18.5, 21.4))
    txt(d, (W/2, 440), 'Domínio próprio não é calar.', FT, B, jan(t, 21.6, 25.6))
    txt(d, (W/2, 520), 'É não deixar o medo, a culpa', FI, G, jan(t, 22.1, 25.6)); txt(d, (W/2, 590), 'ou a esperança decidirem por você.', FI, G, jan(t, 22.1, 25.6))
    txt(d, (W/2, 470), '“Algumas coisas dependem de nós;', FI, G, ap(t, 25.8) * f); txt(d, (W/2, 545), 'outras, não.”', FI, G, ap(t, 26.1) * f)
    txt(d, (W/2, 615), 'Epicteto, Encheirídion, 1', estilo.playfair(30, True), C, ap(t, 26.5) * f)
    if ap(t, 26.8) > 0:
        estilo.texto_espacado(d, (W/2, 1450), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(22, 500), rgba(C, ap(t, 26.8) * f), 6)
    img = Image.alpha_composite(img, cam)
    q = np.asarray(img.convert('RGB'), np.float32) * (1 - ap(t, T - 0.6, 0.6))
    ff.stdin.write(estilo.para_bytes(q))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); saida.with_suffix('.mudo.mp4').unlink(missing_ok=True)
print('ok')
