"""Reconstrução: o raio parte o chão dela; ela cai, sobe sozinha e a rachadura vira ouro.
Personagem fixa (ela). Ou ação, ou texto. Uso: python3 tronco_ouro.py saida.mp4
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from personagens import ela
from PIL import Image, ImageDraw
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
T = 30.0
CHAO, TOPO, X0, X1 = 1500, 980, 420, 660
RAIO, QUEDA, SOBE0, SOBE1 = 4.6, 5.0, 12.4, 19.6
rng = np.random.default_rng(5)
RACHA = [(540 + rng.uniform(-22, 22), TOPO + i * (CHAO - TOPO) / 14) for i in range(15)]
def subida(t): return estilo.suavizar(cl((t - SOBE0) / (SOBE1 - SOBE0)))
F1, F2 = estilo.playfair(58), estilo.playfair(58, True)
def txt(d, y, s, f, cor, a):
    if a > 0.01: d.text((W/2, y), s, font=f, fill=rgba(cor, a), anchor='mm')
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    img = Image.fromarray(fundo).convert('RGBA'); cam = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
    fim = 1 - ap(t, T - 0.8, 0.6)
    a0 = ap(t, 0.2, 0.8) * fim
    # chão e tronco
    d.line([(80, CHAO), (1000, CHAO)], fill=rgba(C, a0), width=4)
    d.rectangle((X0, TOPO, X1, CHAO), fill=(22, 21, 19, int(255 * a0)))
    d.line([(X0, CHAO), (X0, TOPO), (X1, TOPO), (X1, CHAO)], fill=rgba(B, a0), width=4)
    for i, xv in enumerate((470, 520, 600, 630)):       # veios da casca
        d.line([(xv, TOPO + 60 + 40 * i), (xv + 6, CHAO - 40)], fill=rgba(C, 0.35 * a0), width=2)
    # rachadura: aparece no raio; se enche de ouro conforme ela sobe
    if t > RAIO + 0.1:
        d.line(RACHA, fill=rgba(B, fim), width=4)
        s = subida(t) if t < SOBE1 else 1.0
        ouro_ate = CHAO - (CHAO - TOPO) * s
        pts = [p for p in RACHA if p[1] >= ouro_ate]
        if len(pts) > 1:
            d.line(pts, fill=rgba(G, fim), width=9, joint='curve')
            for p in pts[::3]:
                d.ellipse((p[0] - 6, p[1] - 6, p[0] + 6, p[1] + 6), fill=rgba(G, 0.5 * fim))
    # raio
    if RAIO < t < RAIO + 0.6:
        f = 1 - (t - RAIO) / 0.6
        pts = [(540, 0)] + [(540 + rng.uniform(-60, 60), y) for y in range(120, TOPO, 120)] + [(540, TOPO)]
        d.line(pts, fill=rgba((255, 250, 225), f), width=7)
        cam2 = Image.new('RGBA', img.size, (255, 245, 220, int(55 * f))); img = Image.alpha_composite(img, cam2)
    # ela: em pé no topo, cai, senta, sobe pela lateral, fica de pé no topo
    if t < QUEDA:
        ela(d, 540, TOPO, a0, t=t)
    elif t < QUEDA + 1.0:
        q = estilo.suavizar((t - QUEDA) / 1.0)
        x = lerp(540, 300, q); y = lerp(TOPO, CHAO, q * q) - 120 * math.sin(math.pi * q)
        ela(d, x, y, fim, t=t)
    elif t < SOBE0:
        ela(d, 300, CHAO, fim, sentada=ap(t, QUEDA + 1.0, 0.6) * (1 - ap(t, SOBE0 - 1.4, 0.8)),
            cabeca_baixa=ap(t, QUEDA + 1.2, 0.6) * (1 - ap(t, SOBE0 - 2.0, 0.6)), t=t)
    elif t < SOBE1:
        s = subida(t)
        y = lerp(CHAO, TOPO + 60, s) + 8 * math.sin(t * 9)
        ela(d, X0 - 40, y, fim, braco=0.6 + 0.3 * math.sin(t * 9), lado=1, t=t)
    else:
        q = estilo.suavizar(cl((t - SOBE1) / 0.8))
        ela(d, lerp(X0 - 40, 540, q), lerp(TOPO + 60, TOPO, q), fim, t=t)
    # textos (cena parada)
    txt(d, 420, 'Às vezes, o chão que você conhecia', estilo.playfair(52), B, jan(t, 0.3, 4.5)); txt(d, 500, 'se parte de uma vez.', F2, G, jan(t, 0.8, 4.5))
    txt(d, 420, 'Ninguém pode', F1, B, jan(t, 8.0, 12.2)); txt(d, 500, 'subir por você.', F2, G, jan(t, 8.4, 12.2))
    txt(d, 420, 'A rachadura continua lá.', F1, B, jan(t, 20.6, 24.4)); txt(d, 500, 'Mas agora ela brilha.', F2, G, jan(t, 21.2, 24.4))
    txt(d, 380, '“Infeliz é quem nunca passou', estilo.playfair(48, True), G, ap(t, 24.6) * fim)
    txt(d, 445, 'por uma adversidade.”', estilo.playfair(48, True), G, ap(t, 24.9) * fim)
    txt(d, 510, 'Sêneca, Sobre a providência, 3 (paráfrase)', estilo.playfair(30, True), C, ap(t, 25.4) * fim)
    if ap(t, 25.9) > 0:
        estilo.texto_espacado(d, (W/2, 1640), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(22, 500), rgba(C, ap(t, 25.9) * fim), 6)
    img = Image.alpha_composite(img, cam)
    ff.stdin.write(estilo.para_bytes(np.asarray(img.convert('RGB'), np.float32) * (1 - ap(t, T - 0.6, 0.6))))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); saida.with_suffix('.mudo.mp4').unlink(missing_ok=True)
print('ok')
