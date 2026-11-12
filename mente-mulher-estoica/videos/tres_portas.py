"""Três portas: ela gira em círculo (esperar) até ver as saídas: mudar, aceitar, sair. Epicteto, Discursos 1.25.
Frase clara já no primeiro quadro (registro da main de 10/11). Uso: python3 tres_portas.py saida.mp4
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from personagens import ela
from PIL import Image, ImageDraw
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
VERM = (190, 60, 60)
saida = Path(sys.argv[1])
fundo = np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1): return ap(t, t0) * (1 - ap(t, t1 - 0.4, 0.4))
def cl(p): return max(0.0, min(1.0, p))
def rgba(c, a): return c + (int(255 * cl(a)),)
T = 26.0
CX, CY, RX, RY = 540, 1400, 170, 46
PORTAS = [(250, 1010, 'Mudar', ['o que depende', 'de você'], 4.2),
          (540, 900, 'Aceitar', ['o que não', 'depende'], 5.6),
          (830, 1010, 'Sair', ['quando ficar', 'custa a sua paz'], 7.0)]
PARA = 14.0          # ela para de girar
def txt(d, xy, s, f, cor, a, anc='mm'):
    if a > 0.01: d.text(xy, s, font=f, fill=rgba(cor, a), anchor=anc)
F1, F2 = estilo.playfair(62), estilo.playfair(62, True)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    img = Image.fromarray(fundo).convert('RGBA'); cam = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
    fim = 1 - ap(t, T - 0.8, 0.6)
    # o círculo vermelho de esperar: tracejado que gira; some quando ela para
    anel = (1 - ap(t, PARA, 1.2)) * fim
    for i in range(36):
        a0 = i / 36 * 2 * math.pi + t * 0.6
        if i % 2 == 0:
            p0 = (CX + RX * math.cos(a0), CY + RY * math.sin(a0)); a1 = a0 + 2 * math.pi / 36
            d.line([p0, (CX + RX * math.cos(a1), CY + RY * math.sin(a1))], fill=rgba(VERM, 0.85 * anel), width=4)
    if anel > 0.05:   # ponta de seta mostrando o giro
        a0 = t * 0.6 + math.pi * 0.5
        px, py = CX + RX * math.cos(a0), CY + RY * math.sin(a0)
        d.polygon([(px, py - 10), (px, py + 10), (px - 18, py)], fill=rgba(VERM, anel))
    # ela anda em volta do círculo e depois para no centro
    ang = min(t, PARA) * 1.1
    q = ap(t, PARA, 1.0)
    x = (CX + RX * 0.85 * math.cos(ang)) * (1 - q) + CX * q
    y = (CY + RY * 0.85 * math.sin(ang)) * (1 - q) + (CY + 10) * q
    ela(d, x, y, fim, lado=1 if math.sin(ang) < 0 else -1, cabeca_baixa=0.6 * (1 - q), t=t)
    # as três portas acendem
    for px, py, nome, sub, t0 in PORTAS:
        a = ap(t, t0, 0.6) * fim
        if a <= 0: continue
        d.ellipse((px - 120, py - 260, px + 120, py + 40), fill=rgba(G, 0.08 * a))
        d.rectangle((px - 52, py - 190, px + 52, py), fill=rgba((235, 205, 140), a), outline=rgba(B, a), width=3)
        d.ellipse((px + 30, py - 100, px + 40, py - 90), fill=rgba((40, 32, 20), a))
        txt(d, (px, py + 50), nome, estilo.playfair(46, True), G, a)
        for j, l in enumerate(sub):
            txt(d, (px, py + 102 + j * 40), l, estilo.playfair(34, True), (190, 186, 178), ap(t, t0 + 0.4, 0.5) * fim)
    # textos no topo; a pergunta já aparece no primeiro quadro
    txt(d, (W/2, 330), 'Você está esperando', F1, B, 1 - ap(t, 3.6, 0.4))
    txt(d, (W/2, 410), 'que tudo mude sozinho?', F2, G, 1 - ap(t, 3.6, 0.4))
    txt(d, (W/2, 330), 'Girar em círculo', F1, B, jan(t, 9.2, 13.6)); txt(d, (W/2, 410), 'não te tira do lugar.', F2, VERM, jan(t, 9.6, 13.6))
    txt(d, (W/2, 330), 'Esperar', F1, B, jan(t, 15.4, 19.6)); txt(d, (W/2, 410), 'não é uma das portas.', F2, G, jan(t, 15.8, 19.6))
    txt(d, (W/2, 300), '“A casa está cheia de fumaça?', estilo.playfair(46, True), G, ap(t, 19.8) * fim)
    txt(d, (W/2, 365), 'A porta está aberta.”', estilo.playfair(46, True), G, ap(t, 20.1) * fim)
    txt(d, (W/2, 430), 'Epicteto, Discursos, 1.25 (paráfrase)', estilo.playfair(28, True), C, ap(t, 20.6) * fim)
    if ap(t, 21.2) > 0:
        estilo.texto_espacado(d, (W/2, 1620), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(22, 500), rgba(C, ap(t, 21.2) * fim), 6)
    img = Image.alpha_composite(img, cam)
    ff.stdin.write(estilo.para_bytes(np.asarray(img.convert('RGB'), np.float32) * (1 - ap(t, T - 0.6, 0.6))))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); saida.with_suffix('.mudo.mp4').unlink(missing_ok=True)
print('ok')
