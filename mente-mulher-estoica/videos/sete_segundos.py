"""Reels de 7 s (formato de teste, registro 2026-11-09 da main): uma frase na tela, desenvolvimento na legenda.
Uso: python3 sete_segundos.py saida.mp4
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
def ap(t, t0, d=0.4): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
T = 7.0
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    img = Image.fromarray(fundo).convert('RGBA'); cam = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
    def tx(y, s, f, c, a): d.text((W/2, y), s, font=f, fill=c + (int(255 * min(a, 1)),), anchor='mm')
    tx(760, 'Você não precisa', estilo.playfair(72), B, ap(t, 0.2))
    tx(850, 'carregar a semana inteira', estilo.playfair(72), B, ap(t, 0.5))
    tx(950, 'nesta segunda-feira.', estilo.playfair(76, True), G, ap(t, 1.0))
    # uma linha dourada que se desenha devagar: um dia de cada vez
    q = min(1, max(0, (t - 1.6) / 4.5)); x0 = 300
    d.line([(x0, 1080), (x0 + 480 * q, 1080)], fill=G + (220,), width=3)
    for i in range(7):
        xi = x0 + i * 80
        if xi <= x0 + 480 * q + 1:
            r = 9 if i == 0 else 6
            d.ellipse((xi - r, 1080 - r, xi + r, 1080 + r), fill=(G if i == 0 else C) + (255,))
    tx(1150, 'Só o dia de hoje.', estilo.playfair(48, True), C, ap(t, 2.4))
    estilo.texto_espacado(d, (W/2, 1420), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(22, 500), C + (int(255 * ap(t, 0.4)),), 6)
    img = Image.alpha_composite(img, cam)
    ff.stdin.write(estilo.para_bytes(np.asarray(img.convert('RGB'), np.float32) * (1 - ap(t, T - 0.4, 0.4))))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); saida.with_suffix('.mudo.mp4').unlink(missing_ok=True)
print('ok')
