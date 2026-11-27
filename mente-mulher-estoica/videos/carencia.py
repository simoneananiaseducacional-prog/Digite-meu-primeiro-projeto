"""Frase única (sem desenho): a carência abre a porta antes de ver quem entra. Sêneca, Cartas a Lucílio, 3.2
("post amicitiam credendum est, ante amicitiam iudicandum"). Formato inspirado em card de frase com fundo texturizado.
Uso: python3 carencia.py saida.mp4 [vinho|preto]
"""
import sys, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
W, H, FPS, T = 1080, 1920, 30, 10.0
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.6): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.6): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
def rgba(c, a): return c + (int(255 * cl(a)),)

cor = sys.argv[2] if len(sys.argv) > 2 else 'vinho'
if cor == 'vinho':
    rng = np.random.default_rng(3)
    base = np.array([92, 22, 26], np.float32)
    ruido = Image.fromarray((rng.random((H // 8, W // 8)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(30))
    n = np.asarray(ruido, np.float32)[..., None] / 255
    yy, xx = np.mgrid[0:H, 0:W]; vin = 1 - 0.45 * (((xx - W / 2) / W) ** 2 + ((yy - H / 2) / H) ** 2) * 2.2
    arr = base * (0.75 + 0.5 * n) * vin[..., None]
    arr = arr + rng.normal(0, 5, arr.shape)
    fundo = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert('RGBA')
    DOUR = (236, 200, 140)
else:
    fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
    DOUR = G
F = estilo.playfair(70); FI = estilo.playfair(70, True)
saida = Path(sys.argv[1]); ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    im = fundo.copy(); d = ImageDraw.Draw(im, 'RGBA')
    a1 = 1 - ap(t, 3.9, 0.6)   # inteira desde o quadro zero
    if a1 > 0.02:
        d.text((W / 2, 860), 'A carência abre a porta', font=F, fill=rgba(B, a1), anchor='mm')
        d.text((W / 2, 960), 'antes de ver', font=FI, fill=rgba(DOUR, a1), anchor='mm')
        d.text((W / 2, 1050), 'quem está entrando.', font=FI, fill=rgba(DOUR, a1), anchor='mm')
    a2 = ap(t, 4.5, 0.7)
    if a2 > 0.02:
        d.text((W / 2, 860), 'Antes da amizade, avaliar.', font=F, fill=rgba(B, a2), anchor='mm')
        d.text((W / 2, 960), 'Depois da amizade, confiar.', font=FI, fill=rgba(DOUR, a2), anchor='mm')
        d.text((W / 2, 1090), 'Sêneca, Cartas a Lucílio, 3.2', font=estilo.playfair(34, True), fill=rgba((215, 205, 195), ap(t, 5.3, 0.7)), anchor='mm')
    estilo.texto_espacado(d, (W / 2, 1640), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(24, 500), (215, 205, 195, 190), 6)
    ff.stdin.write(estilo.para_bytes(np.asarray(im.convert('RGB'), np.float32) * (1 - ap(t, T - 0.4, 0.4))))
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); print('ok', saida)
