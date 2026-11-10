"""Você acredita em destino? Reels curto, texto grande, uma linha dourada. Heráclito, B119.
Uso: python3 destino.py saida.mp4 (vídeo mudo)
"""
import sys, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
saida = Path(sys.argv[1])
fundo = np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)
def ap(t, t0, d=0.4): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1): return ap(t, t0) * (1 - ap(t, t1 - 0.35, 0.35))
T = 15.0
FG, FGI = estilo.playfair(92), estilo.playfair(92, True)
FM, FMI = estilo.playfair(70), estilo.playfair(70, True)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    img = Image.fromarray(fundo).convert('RGBA'); cam = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
    def tx(y, s, f, c, a, x=110):
        if a > 0.01: d.text((x, y), s, font=f, fill=c + (int(255 * min(a, 1)),), anchor='lm')
    fim = 1 - ap(t, T - 0.6, 0.5)
    # 1. a pergunta
    a1 = jan(t, 0.2, 3.4)
    tx(820, 'Você acredita', FG, B, a1); tx(930, 'em destino?', FGI, G, a1)
    # 2. a virada
    a2 = jan(t, 3.5, 10.3)
    tx(760, 'Os estoicos', FM, B, a2); tx(850, 'acreditavam.', FM, B, a2)
    a3 = jan(t, 6.0, 10.3)
    tx(990, 'Mas sabiam que', FM, B, a3); tx(1080, 'quem você se torna', FMI, G, a3); tx(1170, 'muda o seu.', FM, B, a3)
    # linha dourada que cresce sob a virada
    q = min(1, max(0, (t - 6.4) / 2.5)) * a3
    if q > 0: d.line([(110, 1250), (110 + 620 * q, 1250)], fill=G + (int(230 * a3),), width=3)
    # 3. Heráclito
    a4 = ap(t, 10.4) * fim
    tx(820, '“O caráter de uma pessoa', estilo.playfair(62, True), G, a4)
    tx(905, 'é o seu destino.”', estilo.playfair(62, True), G, ap(t, 10.7) * fim)
    tx(990, 'Heráclito, fragmento B119', estilo.playfair(34, True), C, ap(t, 11.2) * fim)
    if ap(t, 11.6) > 0:
        estilo.texto_espacado(d, (W/2, 1440), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(22, 500), C + (int(255 * ap(t, 11.6) * fim),), 6)
    img = Image.alpha_composite(img, cam)
    ff.stdin.write(estilo.para_bytes(np.asarray(img.convert('RGB'), np.float32) * (1 - ap(t, T - 0.4, 0.4))))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); saida.with_suffix('.mudo.mp4').unlink(missing_ok=True)
print('ok')
