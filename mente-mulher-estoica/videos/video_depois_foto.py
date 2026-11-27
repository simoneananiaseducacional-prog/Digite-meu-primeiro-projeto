"""Trecho de vídeo de outro criador (com a voz) e, em seguida, foto da Simone com a resposta estoica.
Uso: python3 video_depois_foto.py video.mp4 corte_s foto.jpg saida.mp4   (vídeo e foto não entram no repositório)
"""
import sys, subprocess, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw, ImageOps
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
video, CORTE, foto, saida = sys.argv[1], float(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', video, '-t', str(CORTE), '-vf', f'scale={W}:{H},fps={FPS}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
FR = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
im = ImageOps.exif_transpose(Image.open(foto)).convert('RGB')
esc = max(W / im.width, H / im.height); im = im.resize((int(im.width * esc) + 1, int(im.height * esc) + 1), Image.LANCZOS)
im = im.crop(((im.width - W) // 2, 0, (im.width - W) // 2 + W, H))
f = np.asarray(im, np.float32)
cinza = f.mean(2, keepdims=True); f = f * 0.55 + cinza * 0.45          # cor mais contida, combina com a página
yy = np.arange(H)[:, None, None]
f *= np.clip(1 - 0.8 * np.clip((900 - yy) / 700, 0, 1), 0.2, 1)          # topo escuro para o texto
f *= np.clip(1 - 0.75 * np.clip((yy - 1450) / 400, 0, 1), 0.25, 1)       # base escura para a fonte
FOTO = f * 0.92
def ap(t, t0, d=0.45): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
F1, F2, F3 = estilo.playfair(70), estilo.playfair(54, True), estilo.playfair(44, True)
def txt(d, y, s, f, cor, a):
    if a <= 0.01: return
    d.text((W/2 + 2, y + 3), s, font=f, fill=(0, 0, 0, int(160 * a)), anchor='mm')
    d.text((W/2, y), s, font=f, fill=cor + (int(255 * a),), anchor='mm')
DF = 10.0; T = CORTE + DF
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    if t < CORTE:
        q = FR[min(k, len(FR) - 1)].astype(np.float32) * (1 - ap(t, CORTE - 0.4, 0.4))
        out = Image.fromarray(q.astype(np.uint8)).convert('RGBA')
    else:
        u = t - CORTE; z = 1 + 0.05 * u / DF
        cw, ch = W / z, H / z
        fr = Image.fromarray(np.clip(FOTO, 0, 255).astype(np.uint8)).crop((int((W - cw) * 0.6), int((H - ch) * 0.4), int((W - cw) * 0.6 + cw), int((H - ch) * 0.4 + ch))).resize((W, H), Image.BILINEAR)
        g = np.asarray(fr, np.float32) * ap(t, CORTE, 0.5) * (1 - ap(t, T - 0.6, 0.6))
        out = Image.fromarray(np.clip(estilo.granulado(g), 0, 255).astype(np.uint8)).convert('RGBA')
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
    fim = 1 - ap(t, T - 0.8, 0.6); c0 = CORTE
    txt(d, 250, 'Não duvide de você.', F1, B, ap(t, c0 + 0.5) * fim)
    txt(d, 345, 'Mas não confunda autoconfiança', F2, G, ap(t, c0 + 1.6) * fim)
    txt(d, 412, 'com controlar tudo.', F2, G, ap(t, c0 + 1.9) * fim)
    txt(d, 1600, 'Sua ação depende de você.', F3, B, ap(t, c0 + 3.6) * fim)
    txt(d, 1660, 'O resultado, nem sempre.', F3, B, ap(t, c0 + 4.0) * fim)
    txt(d, 1725, 'Epicteto, Encheirídion, 1 (paráfrase)', estilo.playfair(28, True), (210, 210, 210), ap(t, c0 + 4.6) * fim)
    if ap(t, c0 + 5.2) > 0:
        estilo.texto_espacado(d, (W/2, 1800), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(20, 500), (220, 220, 220, int(255 * ap(t, c0 + 5.2) * fim)), 6)
    out = Image.alpha_composite(out, cam)
    ff.stdin.write(estilo.para_bytes(np.asarray(out.convert('RGB'), np.float32)))
ff.stdin.close(); ff.wait()
voz = saida.with_suffix('.voz.m4a')
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', video, '-t', str(CORTE), '-vn', '-af', f'afade=t=out:st={CORTE - 0.4}:d=0.4,apad', '-c:a', 'aac', str(voz)], check=True)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(saida.with_suffix('.mudo.mp4')), '-i', str(voz), '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-t', str(T), '-movflags', '+faststart', str(saida)], check=True)
saida.with_suffix('.mudo.mp4').unlink(missing_ok=True); voz.unlink(missing_ok=True)
print('ok')
