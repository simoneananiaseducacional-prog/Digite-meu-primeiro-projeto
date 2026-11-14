"""Reels curto de pergunta convite: só a pergunta, centralizada, serifa clara em fundo escuro.
Uso: python3 pergunta_convite.py saida.mp4 "linha 1|linha 2|*linha em dourado*" [segundos]
"""
import sys, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
saida = Path(sys.argv[1]); linhas = sys.argv[2].split('|'); T = float(sys.argv[3]) if len(sys.argv) > 3 else 8.0
fundo = np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
ALT = 92
y0 = H / 2 - (len(linhas) - 1) * ALT / 2 - 40
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    img = Image.fromarray(fundo).convert('RGBA'); cam = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
    for i, l in enumerate(linhas):
        dour = l.startswith('*')
        f = estilo.playfair(66, dour)
        a = ap(t, 0.2 + i * 0.35)
        d.text((W/2, y0 + i * ALT), l.strip('*'), font=f, fill=(G if dour else B) + (int(255 * a),), anchor='mm')
    estilo.texto_espacado(d, (W/2, 1440), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(22, 500), C + (int(255 * ap(t, 1.5)),), 6)
    img = Image.alpha_composite(img, cam)
    ff.stdin.write(estilo.para_bytes(np.asarray(img.convert('RGB'), np.float32) * (1 - ap(t, T - 0.4, 0.4))))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); saida.with_suffix('.mudo.mp4').unlink(missing_ok=True)
print('ok')
