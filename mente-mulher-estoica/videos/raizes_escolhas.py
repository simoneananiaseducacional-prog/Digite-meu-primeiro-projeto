"""Raízes e escolhas: raízes que se unem num fio dourado; as marcas ficam, e ao lado de cada uma nasce uma resposta nova.
Texto autoral (não é citação). Fonte filosófica: Epicteto, Encheirídion, 1. Uso: python3 raizes_escolhas.py saida.mp4
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
VERM = (196, 96, 96)
CORES = [(196, 170, 220), (220, 220, 200), (220, 130, 150), (150, 180, 230)]
saida = Path(sys.argv[1])
fundo = np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1): return ap(t, t0) * (1 - ap(t, t1 - 0.4, 0.4))
def cl(p): return max(0.0, min(1.0, p))
def rgba(c, a): return c + (int(255 * cl(a)),)
T = 28.0
BASE = (540, 1180)
RAIZES = [((190, 1400), 'avó'), ((390, 1420), 'avô'), ((690, 1420), 'mãe'), ((890, 1400), 'pai')]
NOS = [(1000, 'medo de desagradar', 'aprender a dizer não', 5.5),
       (820, 'crenças que limitam', 'questionar o que aprendi', 9.5),
       (640, 'marcas que doem', 'buscar cuidado', 13.5)]
CRESCE = [(4.4, 1000), (8.6, 820), (12.6, 640), (16.6, 520)]
def topo_fio(t):
    y = BASE[1]
    for t0, alvo in CRESCE:
        q = estilo.suavizar(cl((t - t0) / 0.9))
        if q > 0: y = y + (alvo - y) * q
    return y
def x_fio(y, t): return 540 + 10 * math.sin(y / 90 + t * 0.8)
F1, F2 = estilo.playfair(58), estilo.playfair(58, True)
FL, FR = estilo.playfair(40, True), estilo.playfair(40, True)
def txt(d, xy, s, f, cor, a, anc='mm'):
    if a > 0.01: d.text(xy, s, font=f, fill=rgba(cor, a), anchor=anc)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    img = Image.fromarray(fundo).convert('RGBA'); cam = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
    fim = 1 - ap(t, T - 0.8, 0.6)
    # raízes: de quem veio antes até a base do fio
    for i, ((rx, ry), nome) in enumerate(RAIZES):
        q = cl((t - 1.0 - i * 0.4) / 1.6)
        if q <= 0: continue
        n = 30; m = max(2, int(n * q))
        pts = [(rx + (BASE[0] - rx) * u + 30 * math.sin(u * math.pi) * (1 if rx < 540 else -1), ry + (BASE[1] - ry) * (u ** 0.8)) for u in [j / n for j in range(n + 1)]][:m]
        d.line(pts, fill=rgba(CORES[i], 0.8 * fim), width=4, joint='curve')
        txt(d, (rx, ry + 34), nome, estilo.playfair(32, True), CORES[i], ap(t, 1.2 + i * 0.4) * fim)
    # o fio dourado sobe
    yt = topo_fio(t)
    if yt < BASE[1] - 2:
        pts = [(x_fio(y, t), y) for y in np.arange(BASE[1], yt, -6)] + [(x_fio(yt, t), yt)]
        for w, a in ((14, 0.12), (6, 1.0)):
            d.line(pts, fill=rgba(G, a * fim), width=w, joint='curve')
        d.ellipse((x_fio(yt, t) - 8, yt - 8, x_fio(yt, t) + 8, yt + 8), fill=rgba(G, fim))
    # as marcas ficam no fio; ao lado, uma resposta nova
    for y, marca, resposta, t0 in NOS:
        a = ap(t, t0, 0.5) * fim
        if a <= 0: continue
        x = x_fio(y, t)
        d.ellipse((x - 16, y - 16, x + 16, y + 16), outline=rgba(VERM, a), width=4)
        txt(d, (x - 40, y), marca, FL, VERM, a, 'rm')
        txt(d, (x + 40, y), resposta, FR, G, ap(t, t0 + 1.3, 0.5) * fim, 'lm')
    # textos no topo
    txt(d, (W/2, 230), 'Minha história', F1, B, jan(t, 0.3, 4.3)); txt(d, (W/2, 310), 'me influencia.', F2, G, jan(t, 0.7, 4.3))
    txt(d, (W/2, 230), 'Não precisa decidir', F1, B, jan(t, 17.8, 21.8)); txt(d, (W/2, 310), 'todas as minhas escolhas.', F2, G, jan(t, 18.2, 21.8))
    txt(d, (W/2, 200), '“Diga a cada impressão difícil:', estilo.playfair(48, True), G, ap(t, 22.0) * fim)
    txt(d, (W/2, 265), 'você é só uma impressão,', estilo.playfair(48, True), G, ap(t, 22.3) * fim)
    txt(d, (W/2, 330), 'não aquilo que parece ser.”', estilo.playfair(48, True), G, ap(t, 22.6) * fim)
    txt(d, (W/2, 395), 'Epicteto, Encheirídion, 1', estilo.playfair(30, True), C, ap(t, 23.2) * fim)
    if ap(t, 23.8) > 0:
        estilo.texto_espacado(d, (W/2, 1500), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(22, 500), rgba(C, ap(t, 23.8) * fim), 6)
    img = Image.alpha_composite(img, cam)
    q2 = np.asarray(img.convert('RGB'), np.float32) * (1 - ap(t, T - 0.6, 0.6))
    ff.stdin.write(estilo.para_bytes(q2))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); saida.with_suffix('.mudo.mp4').unlink(missing_ok=True)
print('ok')
