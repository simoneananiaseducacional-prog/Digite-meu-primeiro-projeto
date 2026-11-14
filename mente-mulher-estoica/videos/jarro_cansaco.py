"""Mapas da mente, variação de desenho: o jarro que enche com o que você engole.
Ou ação, ou texto (base 017). Uso: python3 jarro_cansaco.py saida.mp4 (vídeo mudo)
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
VERM, VINHO = (190, 60, 60), (110, 32, 36)
saida = Path(sys.argv[1])
fundo = np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)
def ap(t, t0, d=0.4): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1): return ap(t, t0) * (1 - ap(t, t1 - 0.3, 0.3))
def cl(p): return max(0.0, min(1.0, p))
def lerp(a, b, p): return a + (b - a) * p
def mix(a, b, p): return tuple(int(a[i] + (b[i] - a[i]) * p) for i in range(3))
def rgba(c, a): return c + (int(255 * cl(a)),)

CX, TOPO, BASE = 540, 820, 1320
def raio(y):
    """Perfil do jarro: gargalo estreito, bojo largo, base firme."""
    p = (y - TOPO) / (BASE - TOPO)
    if p < 0.12: return 62
    if p < 0.28: return lerp(62, 150, estilo.suavizar((p - 0.12) / 0.16))
    return 150 + 45 * math.sin(math.pi * cl((p - 0.28) / 0.72)) - 30 * cl((p - 0.85) / 0.15)

GOTAS = [('A conversa adiada.', 3.4), ('O limite não dito.', 6.2), ('O “tudo bem” que', 9.0)]
CAI = 1.9                     # a gota cai depois de a frase ficar na tela
NIVEIS = [BASE - 8, 1170, 1030, 900]
ESVAZIA0, ESVAZIA1 = 15.0, 17.4
T = 27.0

def nivel(t):
    n = NIVEIS[0]
    for i, (_, t0) in enumerate(GOTAS):
        q = cl((t - (t0 + CAI + 0.55)) / 0.6)
        n = lerp(n, NIVEIS[i + 1], q) if q > 0 else n
    q = cl((t - ESVAZIA0) / (ESVAZIA1 - ESVAZIA0))
    return lerp(n, BASE - 40, estilo.suavizar(q))

def txt(d, y, s, f, cor, a):
    if a > 0.01: d.text((W/2, y), s, font=f, fill=rgba(cor, a), anchor='mm')
F1, F2 = estilo.serifa(64, 700), estilo.serifa_italica(62, 700)
F3 = estilo.playfair(30, True)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    img = Image.fromarray(fundo).convert('RGBA'); cam = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
    a_j = ap(t, 0.5, 1.2)
    # líquido
    L = nivel(t)
    clara = ap(t, ESVAZIA0, 2.4)
    cor_liq = mix(VINHO, (196, 160, 92), clara)
    if L < BASE - 10:
        topo = [(CX - raio(L) + 8 + i * (2 * raio(L) - 16) / 30, L + 6 * math.sin(t * 2.2 + i * 0.6)) for i in range(31)]
        lado_d = [(CX + raio(y) - 8, y) for y in range(int(L) + 4, BASE - 6, 6)]
        lado_e = [(CX - raio(y) + 8, y) for y in range(BASE - 6, int(L) + 4, -6)]
        d.polygon(topo + lado_d + lado_e, fill=rgba(cor_liq, 0.85 * a_j))
    # contorno do jarro, desenhado de baixo para cima no início
    alt = int(TOPO + (BASE - TOPO) * (1 - a_j))
    ys = list(range(BASE, alt - 1, -5))
    if len(ys) > 1:
        for s in (-1, 1):
            d.line([(CX + s * raio(y), y) for y in ys], fill=rgba(B, 0.9), width=4)
        d.line([(CX - raio(BASE), BASE), (CX + raio(BASE), BASE)], fill=rgba(B, 0.9), width=4)
    if a_j >= 1:
        d.arc((CX - 78, TOPO - 14, CX + 78, TOPO + 14), 0, 360, fill=rgba(B, 0.9), width=4)
    # gotas caindo
    for i, (s, t0) in enumerate(GOTAS):
        q = (t - (t0 + CAI)) / 0.6
        if 0 < q < 1:
            y = lerp(640, NIVEIS[i] - 10, q * q); r = 14
            d.ellipse((CX - r, y - r, CX + r, y + r), fill=rgba(VERM, 1))
            d.polygon([(CX - r + 2, y - 4), (CX + r - 2, y - 4), (CX, y - 34)], fill=rgba(VERM, 1))
        q2 = (t - (t0 + CAI + 0.6)) / 0.5
        if 0 < q2 < 1:
            d.ellipse((CX - 60 * q2, NIVEIS[i] - 8 * q2, CX + 60 * q2, NIVEIS[i] + 8 * q2), outline=rgba(VERM, 1 - q2), width=3)
    # bica e fio dourado
    yb = BASE - 70
    a_b = ap(t, ESVAZIA0 - 0.5, 0.5)
    if a_b > 0:
        xb = CX + raio(yb)
        d.line([(xb, yb - 14), (xb + 50, yb - 24)], fill=rgba(B, a_b), width=4)
        d.line([(xb, yb + 14), (xb + 50, yb + 4)], fill=rgba(B, a_b), width=4)
        fio = 1 - ap(t, ESVAZIA1 + 0.2, 0.8)
        if t > ESVAZIA0 and fio > 0:
            n = 40
            pts = [(xb + 50 + 260 * (i / n), yb - 10 + 150 * (i / n) ** 2 + 2 * math.sin(t * 6 - i * 0.5)) for i in range(n + 1)]
            m = int(n * cl((t - ESVAZIA0) / 0.6))
            if m > 1: d.line(pts[:m], fill=rgba(G, fio), width=14, joint="curve")
            for j in range(5):
                u = ((t * 1.3 + j / 5) % 1)
                if u * n < m:
                    px, py = pts[int(u * n)]
                    d.ellipse((px - 8, py - 8, px + 8, py + 8), fill=rgba(G, fio))
    # textos no topo: ou ação, ou texto
    txt(d, 470, 'De onde vem', F1, B, jan(t, 0.3, 3.2)); txt(d, 550, 'o seu cansaço?', F2, G, jan(t, 0.8, 3.2))
    txt(d, 520, GOTAS[0][0], F2, B, jan(t, GOTAS[0][1], GOTAS[0][1] + CAI + 0.6))
    txt(d, 520, GOTAS[1][0], F2, B, jan(t, GOTAS[1][1], GOTAS[1][1] + CAI + 0.6))
    txt(d, 480, GOTAS[2][0], F2, B, jan(t, GOTAS[2][1], GOTAS[2][1] + CAI + 0.6)); txt(d, 556, 'não estava.', F2, B, jan(t, GOTAS[2][1], GOTAS[2][1] + CAI + 0.6))
    txt(d, 480, 'Descansar não esvazia', F1, B, jan(t, 12.0, 14.6)); txt(d, 556, 'o que você engole.', F2, VERM, jan(t, 12.4, 14.6))
    txt(d, 480, 'O que descansa é', F1, B, jan(t, 17.6, 21.0)); txt(d, 556, 'dizer com calma.', F2, G, jan(t, 18.0, 21.0))
    txt(d, 470, '“De que adianta o silêncio ao redor,', estilo.serifa_italica(50, 700), G, ap(t, 21.2) * (1 - ap(t, T - 0.8, 0.6)))
    txt(d, 535, 'se por dentro tudo grita?”', estilo.serifa_italica(50, 700), G, ap(t, 21.6) * (1 - ap(t, T - 0.8, 0.6)))
    txt(d, 600, 'Sêneca, Cartas a Lucílio, 56', F3, C, ap(t, 22.2) * (1 - ap(t, T - 0.8, 0.6)))
    if ap(t, 23.0) > 0:
        estilo.texto_espacado(d, (W/2, 1430), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(22, 500), rgba(C, ap(t, 23.0) * (1 - ap(t, T - 0.8, 0.6))), 6)
    img = Image.alpha_composite(img, cam)
    q = np.asarray(img.convert('RGB'), np.float32) * (1 - ap(t, T - 0.6, 0.6))
    ff.stdin.write(estilo.para_bytes(q))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); saida.with_suffix('.mudo.mp4').unlink(missing_ok=True)
print('ok')
