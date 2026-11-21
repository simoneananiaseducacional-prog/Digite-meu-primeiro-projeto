"""Põe o pé que Deus coloca o chão: passos no escuro e, sob cada um, surge uma pedra dourada.
Ou ação, ou texto. Uso: python3 passo_chao.py saida.mp4 (vídeo mudo)
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
saida = Path(sys.argv[1])
fundo = np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1): return ap(t, t0) * (1 - ap(t, t1 - 0.4, 0.4))
def cl(p): return max(0.0, min(1.0, p))
def rgba(c, a): return c + (int(255 * cl(a)),)
T = 24.0
# pedras de baixo para cima, alternando lados (o caminho sobe para o desconhecido)
PEDRAS = [(470, 1380), (610, 1250), (480, 1120), (620, 990), (490, 860), (600, 740)]
T_PASSO = [5.0, 6.4, 7.8, 13.2, 14.4, 15.6]   # cada pedra nasce quando o pé desce
def pe(d, x, y, a, lado):
    """Pegada simples: sola oval e cinco dedinhos."""
    if a <= 0.01: return
    d.ellipse((x - 26, y - 46, x + 26, y + 40), outline=rgba(B, a), width=4)
    for i, (dx, dy, r) in enumerate([(-18, -62, 8), (-6, -68, 8), (6, -68, 7), (17, -63, 6), (26, -55, 5)]):
        dx *= lado
        d.ellipse((x + dx - r, y + dy - r, x + dx + r, y + dy + r), outline=rgba(B, a), width=3)
def pedra(d, x, y, a, brilho):
    if a <= 0.01: return
    r = 70 * (0.6 + 0.4 * a)
    for k, al in ((1.6, 0.08 * brilho), (1.25, 0.16 * brilho)):
        d.ellipse((x - r * k, y - r * 0.45 * k, x + r * k, y + r * 0.45 * k), fill=rgba(G, al * a))
    d.ellipse((x - r, y - r * 0.4, x + r, y + r * 0.4), fill=(30, 26, 18, int(255 * a)), outline=rgba(G, a), width=4)
F1, F2 = estilo.playfair(64), estilo.playfair(64, True)
def txt(d, y, s, f, cor, a):
    if a > 0.01: d.text((W/2, y), s, font=f, fill=rgba(cor, a), anchor='mm')
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    img = Image.fromarray(fundo).convert('RGBA'); cam = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
    fim = 1 - ap(t, T - 0.8, 0.6)
    # névoa escura acima: o que ainda não se vê
    for i, ((x, y), tp) in enumerate(zip(PEDRAS, T_PASSO)):
        a = ap(t, tp, 0.45) * fim
        pedra(d, x, y, a, 1 + 0.3 * math.sin(t * 2 + i))
        # o pé desce logo antes e pousa sobre a pedra
        desce = cl((t - (tp - 0.6)) / 0.6)
        if desce > 0:
            pe(d, x, y - 10 - 50 * (1 - desce), min(1, desce * 1.5) * fim * (1 - 0.6 * ap(t, tp + 1.6, 0.6)), 1 if i % 2 else -1)
    txt(d, 300, 'Às vezes, o próximo passo', F1, B, jan(t, 0.3, 4.6)); txt(d, 385, 'não aparece antes.', F2, G, jan(t, 0.8, 4.6))
    txt(d, 300, 'Põe o pé', F1, B, jan(t, 8.8, 12.8)); txt(d, 385, 'que Deus coloca o chão.', F2, G, jan(t, 9.3, 12.8))
    txt(d, 260, '“Sofremos mais', estilo.playfair(54, True), G, ap(t, 17.0) * fim)
    txt(d, 330, 'na imaginação do que na realidade.”', estilo.playfair(54, True), G, ap(t, 17.3) * fim)
    txt(d, 400, 'Sêneca, Cartas a Lucílio, 13', estilo.playfair(32, True), C, ap(t, 17.9) * fim)
    if ap(t, 18.6) > 0:
        estilo.texto_espacado(d, (W/2, 1540), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(22, 500), rgba(C, ap(t, 18.6) * fim), 6)
    img = Image.alpha_composite(img, cam)
    ff.stdin.write(estilo.para_bytes(np.asarray(img.convert('RGB'), np.float32) * (1 - ap(t, T - 0.6, 0.6))))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); saida.with_suffix('.mudo.mp4').unlink(missing_ok=True)
print('ok')
