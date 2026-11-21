"""O exame da noite de Sêneca (Sobre a ira, 3.36): uma vela, três perguntas, a chama que se apaga.
Ou ação, ou texto. Uso: python3 vela_seneca.py saida.mp4 (vídeo mudo)
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
T = 26.0
CX, BASE = 540, 1330          # base da vela
TOPO = 1080                   # topo da vela (pavio)
PERG = [('Que mal eu curei hoje?', 6.2), ('A que impulso eu resisti?', 9.4), ('Em que estou melhor?', 12.6)]
APAGA = 17.0
def chama(d, t, forca):
    """Chama em gota, tremulando; forca 0..1.3 controla tamanho e brilho."""
    if forca <= 0.01: return
    tre = 1 + 0.07 * math.sin(t * 11) + 0.04 * math.sin(t * 17 + 1)
    inc = 6 * math.sin(t * 5)
    h, w = 120 * forca * tre, 34 * forca
    py = TOPO - 6
    pts = []
    for i in range(41):
        a = math.pi * 2 * i / 40
        x = w * math.sin(a); y = -h * (0.5 - 0.5 * math.cos(a)) if True else 0
        # gota: larga embaixo, pontuda em cima
        s = (1 - math.cos(a)) / 2
        x *= (1 - 0.75 * s ** 1.6)
        pts.append((CX + x + inc * s, py + y))
    d.polygon(pts, fill=rgba((255, 214, 140), 0.9 * min(forca, 1)))
    d.line(pts + [pts[0]], fill=rgba(G, min(forca, 1)), width=3)
    ih = h * 0.45
    d.ellipse((CX - w * 0.35, py - ih, CX + w * 0.35, py), fill=rgba((255, 250, 225), 0.85 * min(forca, 1)))
def halo(d, t, forca):
    if forca <= 0.01: return
    h = 120 * forca
    for k, al in ((3.2, 0.06), (2.2, 0.10), (1.5, 0.16)):
        r = h * 0.55 * k
        d.ellipse((CX - r, TOPO - 6 - h * 0.55 - r, CX + r, TOPO - 6 - h * 0.55 + r), fill=rgba(G, al * min(forca, 1)))
def fumaca(d, t, a):
    if a <= 0.01: return
    u = cl((t - APAGA) / 4)
    pts = [(CX + 30 * math.sin(i / 6 + t * 1.5) * (i / 30), TOPO - 10 - i * 12 * (0.4 + u)) for i in range(31)]
    d.line(pts, fill=rgba(C, a * (1 - u * 0.7)), width=3, joint='curve')
F1, F2 = estilo.playfair(60), estilo.playfair(60, True)
FQ = estilo.playfair(54, True)
def txt(d, y, s, f, cor, a):
    if a > 0.01: d.text((W/2, y), s, font=f, fill=rgba(cor, a), anchor='mm')
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    img = Image.fromarray(fundo).convert('RGBA'); cam = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
    fim = 1 - ap(t, T - 0.8, 0.6)
    av = ap(t, 0.2, 0.8) * fim
    forca = ap(t, 2.0, 0.8) * (0.85 + 0.15 * sum(ap(t, t0 + 1.5, 0.6) for _, t0 in PERG)) * (1 - ap(t, APAGA, 1.0))
    halo(d, t, forca * fim)
    # vela: corpo, cera escorrida, pires
    d.rounded_rectangle((CX - 62, TOPO, CX + 62, BASE), 10, fill=(20, 19, 17, int(255 * av)), outline=rgba(B, av), width=4)
    d.line([(CX + 30, TOPO + 2), (CX + 34, TOPO + 60), (CX + 26, TOPO + 85)], fill=rgba(B, 0.7 * av), width=3, joint='curve')
    d.line([(CX, TOPO), (CX + 3, TOPO - 18)], fill=rgba(B, av), width=4)
    d.ellipse((CX - 170, BASE - 18, CX + 170, BASE + 30), outline=rgba(G, av), width=4)
    # a chama acende, firma a cada pergunta e se apaga no fim
    forca = ap(t, 2.0, 0.8) * (0.85 + 0.15 * sum(ap(t, t0 + 1.5, 0.6) for _, t0 in PERG)) * (1 - ap(t, APAGA, 1.0))
    chama(d, t, forca * fim)
    fumaca(d, t, ap(t, APAGA + 0.3, 0.5) * fim)
    txt(d, 380, 'Antes de dormir,', F1, B, jan(t, 0.3, 5.9)); txt(d, 460, 'Sêneca fazia três perguntas.', F2, G, jan(t, 0.8, 5.9))
    for i, (q, t0) in enumerate(PERG):
        txt(d, 300 + i * 95, q, FQ, B if i < 2 else G, ap(t, t0, 0.5) * (1 - ap(t, APAGA - 0.6, 0.5)))
    txt(d, 380, 'Revisar o dia', F1, B, jan(t, 18.2, 22.0)); txt(d, 460, 'também é descansar.', F2, G, jan(t, 18.6, 22.0))
    txt(d, 340, '“Examino o meu dia inteiro', estilo.playfair(48, True), G, ap(t, 22.1) * fim)
    txt(d, 405, 'e repasso o que fiz e disse.”', estilo.playfair(48, True), G, ap(t, 22.4) * fim)
    txt(d, 470, 'Sêneca, Sobre a ira, 3.36', estilo.playfair(30, True), C, ap(t, 22.9) * fim)
    if ap(t, 23.4) > 0:
        estilo.texto_espacado(d, (W/2, 1500), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(22, 500), rgba(C, ap(t, 23.4) * fim), 6)
    img = Image.alpha_composite(img, cam)
    ff.stdin.write(estilo.para_bytes(np.asarray(img.convert('RGB'), np.float32) * (1 - ap(t, T - 0.6, 0.6))))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); saida.with_suffix('.mudo.mp4').unlink(missing_ok=True)
print('ok')
