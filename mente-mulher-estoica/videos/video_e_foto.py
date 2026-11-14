"""Montagem: trecho de vídeo de outro criador (a pergunta) e foto da Simone (a resposta).
Uso: python3 video_e_foto.py video.mp4 foto.jpg saida.mp4  (vídeo e foto não entram no repositório)
"""
import sys, subprocess, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw, ImageOps
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
video, foto, saida = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
CORTE = 9.0                        # segundos do vídeo original usados
raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', video, '-t', str(CORTE), '-vf', f'scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
FR = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
im = ImageOps.exif_transpose(Image.open(foto)).convert('L')
esc = max(W / im.width, H / im.height) * 1.02
im = im.resize((int(im.width * esc), int(im.height * esc)), Image.LANCZOS)
x0 = (im.width - W) // 2; im = im.crop((x0, 0, x0 + W, H))
yy = np.arange(H)[:, None]
sombra = 1 - 0.78 * np.clip((760 - yy) / 520, 0, 1)            # topo escuro para o texto
FOTO = np.asarray(im, np.float32) * sombra
def ap(t, t0, d=0.45): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1): return ap(t, t0) * (1 - ap(t, t1 - 0.35, 0.35))
F1, F2, F3 = estilo.playfair(62), estilo.playfair(62, True), estilo.playfair(48, True)
def txt(d, y, s, f, cor, a):
    if a <= 0.01: return
    d.text((W/2 + 2, y + 3), s, font=f, fill=(0, 0, 0, int(170 * a)), anchor='mm')
    d.text((W/2, y), s, font=f, fill=cor + (int(255 * a),), anchor='mm')
A1, V0, V1, T = 7.0, 7.0, 16.0, 21.5     # foto + Sêneca | vídeo | foto + resposta
def foto_quadro(u, dur, desloc):
    z = 1 + 0.06 * u / dur
    cw, ch = W / z, H / z
    f = Image.fromarray(np.clip(FOTO, 0, 255).astype(np.uint8)).crop((int((W - cw) * desloc), int((H - ch) * 0.5), int((W - cw) * desloc + cw), int((H - ch) * 0.5 + ch))).resize((W, H), Image.BILINEAR)
    return np.asarray(f, np.float32)[..., None].repeat(3, 2)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    if t < A1:
        g = foto_quadro(t, A1, 0.45) * ap(t, 0, 0.5) * (1 - ap(t, A1 - 0.4, 0.4))
        out = Image.fromarray(np.clip(estilo.granulado(g), 0, 255).astype(np.uint8)).convert('RGBA')
    elif t < V1:
        src = int((t - V0) * FPS)
        q = FR[min(src, len(FR) - 1)].astype(np.float32) * ap(t, V0, 0.3) * (1 - ap(t, V1 - 0.4, 0.4))
        out = Image.fromarray(q.astype(np.uint8)).convert('RGBA')
    else:
        u = t - V1
        g = foto_quadro(u, T - V1, 0.55)
        flash = max(0.0, 1 - u / 0.35)
        g = (g * (1 - flash) + 255 * flash) * (1 - ap(t, T - 0.6, 0.6))
        out = Image.fromarray(np.clip(estilo.granulado(g), 0, 255).astype(np.uint8)).convert('RGBA')
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
    fim = 1 - ap(t, T - 0.8, 0.6)
    sai = 1 - ap(t, A1 - 0.5, 0.4)
    txt(d, 250, '“Quem disse que a natureza', F3, G, ap(t, 0.5) * sai)
    txt(d, 315, 'foi avara com as mulheres?', F3, G, ap(t, 0.8) * sai)
    txt(d, 400, 'Elas têm o mesmo vigor', F3, B, ap(t, 2.4) * sai)
    txt(d, 465, 'e a mesma capacidade para o bem.”', F3, B, ap(t, 2.7) * sai)
    txt(d, 540, 'Sêneca, Consolação a Márcia, 16', estilo.playfair(30, True), (215, 215, 215), ap(t, 3.3) * sai)
    txt(d, 300, 'Ela existe.', F1, B, ap(t, V1 + 0.5) * fim)
    txt(d, 390, 'E não fica calada.', F2, G, ap(t, V1 + 1.1) * fim)
    if ap(t, V1 + 1.8) > 0:
        estilo.texto_espacado(d, (W/2, 1450), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(22, 500), (225, 225, 225, int(255 * ap(t, V1 + 1.8) * fim)), 6)
    out = Image.alpha_composite(out, cam)
    ff.stdin.write(estilo.para_bytes(np.asarray(out.convert('RGB'), np.float32)))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); saida.with_suffix('.mudo.mp4').unlink(missing_ok=True)
print('ok')
