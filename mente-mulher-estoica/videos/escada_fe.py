"""Fé de manhã: a escada no escuro; cada degrau acende quando ela pisa; no alto, o sol nasce.
Personagem fixa (ela). Ou ação, ou texto. Uso: python3 escada_fe.py saida.mp4
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from personagens import ela
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
saida = Path(sys.argv[1])
fundo = np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1): return ap(t, t0) * (1 - ap(t, t1 - 0.4, 0.4))
def cl(p): return max(0.0, min(1.0, p))
def lerp(a, b, p): return a + (b - a) * p
def rgba(c, a): return c + (int(255 * cl(a)),)
T = 28.0
N = 7
X0, Y0, DX, DY, LG = 150, 1560, 82, 100, 130     # degrau 0 (chão) e passo
def degrau(i): return X0 + i * DX, Y0 - i * DY  # canto esquerdo do topo do degrau i
SUB = [5.0, 6.4, 7.8, 13.6, 15.0, 16.4, 17.8]   # quando ela chega em cada degrau
def posicao(t):
    i = 0
    for k, tk in enumerate(SUB):
        if t >= tk: i = k + 1
    if i >= N: x, y = degrau(N); return x + 60, y, 0
    q = cl((t - (SUB[i] - 0.9)) / 0.9) if i < N else 1
    xa, ya = degrau(i); xb, yb = degrau(i + 1)
    x = lerp(xa + 60, xb + 60, q); y = lerp(ya, yb, q) - 40 * math.sin(math.pi * q)
    return x, y, q
F1, F2 = estilo.playfair(60), estilo.playfair(60, True)
def txt(d, y, s, f, cor, a):
    if a > 0.01: d.text((W/2, y), s, font=f, fill=rgba(cor, a), anchor='mm')
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    img = Image.fromarray(fundo).convert('RGBA'); fim = 1 - ap(t, T - 0.8, 0.6)
    # sol nascendo no alto, atrás de tudo
    sol = ap(t, 19.0, 3.0) * fim
    if sol > 0:
        lz = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lz)
        cx, cy = degrau(N)[0] + 60, degrau(N)[1] - 20
        for r, a in ((520, 0.10), (340, 0.16), (200, 0.30)):
            dl.ellipse((cx - r, cy - r, cx + r, cy + r), fill=rgba(G, a * sol))
        img = Image.alpha_composite(img, lz.filter(ImageFilter.GaussianBlur(40)))
        dd = ImageDraw.Draw(img)
        dd.pieslice((cx - 110, cy - 110 + 60 * (1 - sol), cx + 110, cy + 110 + 60 * (1 - sol)), 180, 360, fill=rgba((235, 200, 130), sol))
    cam = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
    a0 = ap(t, 0.2, 0.8) * fim
    d.line([(60, Y0), (X0 + 40, Y0)], fill=rgba(C, a0), width=4)
    # degraus: contorno apagado; acendem em dourado quando ela pisa
    for i in range(1, N + 1):
        x, y = degrau(i)
        aceso = ap(t, SUB[i - 1] - 0.3, 0.4) * fim
        d.line([(x - DX + 40, y + DY), (x - DX + 40, y), (x + 40 + LG - DX, y)], fill=rgba(C, 0.18 * a0), width=3)
        if aceso > 0:
            d.ellipse((x - DX + 10, y - 30, x + 70 + LG - DX, y + 30), fill=rgba(G, 0.12 * aceso))
            d.rectangle((x - DX + 40, y - 3, x + 40 + LG - DX, y + 9), fill=rgba((235, 200, 130), aceso))
    x, y, q = posicao(t)
    ela(d, x, y, a0, braco=0.25 * (1 if 0 < q < 1 else 0), lado=1, t=t)
    # textos com a cena parada
    txt(d, 380, 'Você não precisa', F1, B, jan(t, 0.3, 4.6)); txt(d, 460, 'ver a escada inteira.', F2, G, jan(t, 0.8, 4.6))
    txt(d, 380, 'Só o próximo degrau.', F1, B, jan(t, 9.0, 13.0)); txt(d, 460, 'O resto vem no caminho.', F2, G, jan(t, 9.5, 13.0))
    txt(d, 330, '“O destino conduz quem aceita', estilo.playfair(48, True), G, ap(t, 22.0) * fim)
    txt(d, 395, 'e arrasta quem resiste.”', estilo.playfair(48, True), G, ap(t, 22.4) * fim)
    txt(d, 460, 'Sêneca, Cartas a Lucílio, 107', estilo.playfair(30, True), C, ap(t, 23.0) * fim)
    if ap(t, 23.6) > 0:
        estilo.texto_espacado(d, (W/2, 1700), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(22, 500), rgba(C, ap(t, 23.6) * fim), 6)
    img = Image.alpha_composite(img, cam)
    ff.stdin.write(estilo.para_bytes(np.asarray(img.convert('RGB'), np.float32) * (1 - ap(t, T - 0.6, 0.6))))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); saida.with_suffix('.mudo.mp4').unlink(missing_ok=True)
print('ok')
