"""Reels no modelo aspas douradas: linhas entram uma a uma; texto fora da área dos botões do Instagram.
Uso: python3 reels_aspas.py saida.mp4 "linha|*linha dourada*" "fonte 1|fonte 2" [segundos]
"""
import sys, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B = (240, 236, 228); G = (196, 160, 92); C = (150, 146, 140)
saida = Path(sys.argv[1]); linhas = sys.argv[2].split('|'); fonte = sys.argv[3].split('|') if len(sys.argv) > 3 else []
T = float(sys.argv[4]) if len(sys.argv) > 4 else 12.0
def ap(t, t0, d=0.4): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
X = 90; ALT = 88; f = estilo.sem_serifa(72, 800)
Y0 = 560
PASSO = 0.9
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    im = Image.new('RGB', (W, H), (10, 10, 10)); d = ImageDraw.Draw(im, 'RGBA')
    d.text((X - 8, Y0 - 230), '“', font=estilo.sem_serifa(260, 900), fill=G + (int(255 * ap(t, 0.1)),), anchor='lt')
    y = Y0
    for i, l in enumerate(linhas):
        a = ap(t, 0.5 + i * PASSO); dour = l.startswith('*')
        d.text((X, y + 18 * (1 - a)), l.strip('*'), font=f, fill=(G if dour else B) + (int(255 * a),), anchor='lm'); y += ALT
    t2 = 0.5 + len(linhas) * PASSO + 0.6
    for i, l in enumerate(fonte):
        d.text((X, y + 50 + i * 44), l, font=estilo.sem_serifa(30, 500 if i == 0 else 400), fill=(B if i == 0 else C) + (int(255 * ap(t, t2 + i * 0.3)),), anchor='lm')
    d.text((X, y + 200), '@mente_mulher_estoica', font=estilo.sem_serifa(26, 500), fill=C + (int(255 * ap(t, t2 + 0.8)),), anchor='lm')
    ff.stdin.write(estilo.para_bytes(np.asarray(im, np.float32) * (1 - ap(t, T - 0.5, 0.5))))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); saida.with_suffix('.mudo.mp4').unlink(missing_ok=True)
print('ok')
