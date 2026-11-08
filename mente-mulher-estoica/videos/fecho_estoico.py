"""Acrescenta um fechamento estoico (tela preta com frases) ao fim de um vídeo da Simone.
Uso: python3 fecho_estoico.py video.mp4 saida.mp4   (o vídeo original não entra no repositório)
"""
import sys, subprocess, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
video, saida = sys.argv[1], Path(sys.argv[2])
fundo = np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def rgba(c, a): return c + (int(255 * min(max(a, 0), 1)),)
T = 7.0
card = saida.with_suffix('.card.mp4')
ff = midia.gravador(card, estatico=False)
F1, F2, F3 = estilo.playfair(60), estilo.playfair(60, True), estilo.playfair(48, True)
for k in range(int(T * FPS)):
    t = k / FPS
    img = Image.fromarray(fundo).convert('RGBA'); cam = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
    def tx(y, s, f, c, a): d.text((W/2, y), s, font=f, fill=rgba(c, a), anchor='mm')
    tx(640, 'O rótulo fala de quem rotula.', F1, B, ap(t, 0.2))
    tx(725, 'Sua firmeza fala de você.', F2, G, ap(t, 1.0))
    tx(960, '“Amamos mais a nós mesmos que aos outros,', F3, G, ap(t, 2.4))
    tx(1025, 'mas valorizamos mais a opinião deles', F3, G, ap(t, 2.7))
    tx(1090, 'do que a nossa.”', F3, G, ap(t, 3.0))
    tx(1165, 'Marco Aurélio, Meditações, 12.4', estilo.playfair(30, True), C, ap(t, 3.5))
    estilo.texto_espacado(d, (W/2, 1420), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(22, 500), rgba(C, ap(t, 4.0)), 6)
    img = Image.alpha_composite(img, cam)
    ff.stdin.write(estilo.para_bytes(np.asarray(img.convert('RGB'), np.float32) * (1 - ap(t, T - 0.6, 0.6))))
ff.stdin.close(); ff.wait()
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', video], capture_output=True, text=True).stdout)
off = dur - 0.5
fc = (f"[0:v]scale={W}:{H},fps={FPS},format=yuv420p,setsar=1[a];[1:v]fps={FPS},format=yuv420p,setsar=1[b];"
      f"[a][b]xfade=transition=fade:duration=0.5:offset={off}[v];[0:a]apad[au]")
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', video, '-i', str(card), '-filter_complex', fc,
                '-map', '[v]', '-map', '[au]', '-t', str(off + T), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20',
                '-c:a', 'aac', '-movflags', '+faststart', str(saida)], check=True)
card.unlink(missing_ok=True)
print('ok')
