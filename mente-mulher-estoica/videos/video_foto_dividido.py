"""Tela dividida: vídeo de outro criador em cima (com a voz), foto da Simone embaixo; frases no fim.
Uso: python3 video_foto_dividido.py video.mp4 corte_s foto.jpg saida.mp4  (vídeo e foto não entram no repositório)
"""
import sys, subprocess, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw, ImageOps
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
video, CORTE, foto, saida = sys.argv[1], float(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
MEIO = 960
raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', video, '-t', str(CORTE), '-vf', f'scale={W}:{H},fps={FPS},crop={W}:{MEIO}:0:440', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
FR = np.frombuffer(raw, np.uint8).reshape(-1, MEIO, W, 3)
im = ImageOps.exif_transpose(Image.open(foto)).convert('RGB')
esc = W / im.width; im = im.resize((W, int(im.height * esc)), Image.LANCZOS)
im = im.crop((0, 380, W, 380 + MEIO))
f = np.asarray(im, np.float32); f = f * 0.6 + f.mean(2, keepdims=True) * 0.4
yy = np.arange(MEIO)[:, None, None]
f *= np.clip(1 - 0.85 * np.clip((yy - 400) / 300, 0, 1), 0.15, 1)        # base da foto escurece para o texto
FOTO = f * 0.95
def ap(t, t0, d=0.45): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
F1, F2, F3 = estilo.playfair(62), estilo.playfair(46, True), estilo.playfair(40, True)
def txt(d, y, s, f, cor, a):
    if a <= 0.01: return
    d.text((W/2 + 2, y + 3), s, font=f, fill=(0, 0, 0, int(170 * a)), anchor='mm')
    d.text((W/2, y), s, font=f, fill=cor + (int(255 * a),), anchor='mm')
T = CORTE + 8.0
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    topo = FR[min(k, len(FR) - 1)].astype(np.float32) * (1 - 0.55 * ap(t, CORTE, 0.6))
    z = 1 + 0.04 * t / T
    cw, ch = W / z, MEIO / z
    fr = Image.fromarray(np.clip(FOTO, 0, 255).astype(np.uint8)).crop((int((W - cw) * 0.7), int((MEIO - ch) * 0.3), int((W - cw) * 0.7 + cw), int((MEIO - ch) * 0.3 + ch))).resize((W, MEIO), Image.BILINEAR)
    baixo = np.asarray(fr, np.float32)
    quadro = np.concatenate([topo, baixo], 0) * ap(t, 0, 0.3) * (1 - ap(t, T - 0.6, 0.6))
    out = Image.fromarray(np.clip(estilo.granulado(quadro), 0, 255).astype(np.uint8)).convert('RGBA')
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
    d.line([(0, MEIO), (W, MEIO)], fill=G + (200,), width=3)
    fim = 1 - ap(t, T - 0.8, 0.6)
    txt(d, 1560, 'Não duvide de você.', F1, B, ap(t, CORTE + 0.4) * fim)
    txt(d, 1640, 'Mas não confunda autoconfiança com controlar tudo.', F3, G, ap(t, CORTE + 1.4) * fim)
    txt(d, 1720, 'Sua ação depende de você. O resultado, nem sempre.', F3, B, ap(t, CORTE + 3.0) * fim)
    txt(d, 1785, 'Epicteto, Encheirídion, 1 (paráfrase)', estilo.playfair(26, True), (205, 205, 205), ap(t, CORTE + 3.6) * fim)
    if ap(t, CORTE + 4.2) > 0:
        estilo.texto_espacado(d, (W/2, 1855), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(18, 500), (215, 215, 215, int(255 * ap(t, CORTE + 4.2) * fim)), 5)
    out = Image.alpha_composite(out, cam)
    ff.stdin.write(estilo.para_bytes(np.asarray(out.convert('RGB'), np.float32)))
ff.stdin.close(); ff.wait()
voz = saida.with_suffix('.voz.m4a')
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', video, '-t', str(CORTE), '-vn', '-af', f'afade=t=out:st={CORTE - 0.4}:d=0.4,apad', '-c:a', 'aac', '-t', str(T), str(voz)], check=True)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(saida.with_suffix('.mudo.mp4')), '-i', str(voz), '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-t', str(T), '-movflags', '+faststart', str(saida)], check=True)
saida.with_suffix('.mudo.mp4').unlink(missing_ok=True); voz.unlink(missing_ok=True)
print('ok')
