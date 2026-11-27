"""Pôr do sol com a letra da música (vídeo enviado pela Simone, legenda antiga queimada pelo ChatGPT).
Cobre a faixa da legenda antiga com um desfoque escuro e suave e escreve a letra no estilo do mar.mp4:
Playfair branco, segunda linha em itálico dourado, sombra, @ discreto embaixo. Áudio original.
Uso: python3 paisagem_letra.py entrada.mov saida.mp4
"""
import sys, subprocess, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo
from PIL import Image, ImageDraw, ImageFilter
W, H, FPS = 1080, 1920, 30
B, G = estilo.BRANCO, estilo.DOURADO
ENT, SAI = sys.argv[1], sys.argv[2]
DUR = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', ENT]))
# (início, fim, linha branca, linha dourada em itálico)
LETRA = [
    (1.0, 4.6, 'E se eu quisesse', 'desabar?'),
    (5.3, 9.0, 'Rir de tudo', 'na sua cara'),
    (9.3, 12.6, '', 'O que você faria?'),
    (17.3, 20.9, 'E se eu caísse', 'no chão'),
    (20.9, 24.8, 'Não pudesse mais', 'aguentar isso'),
    (24.8, 29.4, '', 'O que você faria?'),
    (30.8, 37.9, 'Venha', 'me destruir'),
    (37.9, 39.9, 'Me enterre,', 'me enterre'),
    (39.9, DUR - 0.2, 'Eu não quero', 'mais nada com você'),
]
# faixa da legenda antiga (escala 1080x1920)
Y0, Y1, F = 1155, 1478, 105
y = np.arange(H)[:, None].astype(np.float32)
m = np.clip(np.minimum((y - (Y0 - F)) / F, ((Y1 + F) - y) / F), 0, 1); m = (m * m * (3 - 2 * m))[..., None]
CY0, CY1 = Y0 - F - 60, Y1 + F + 60
mc = m[CY0:CY1]
YC = (Y0 + Y1) / 2
F1, F2 = estilo.playfair(70), estilo.playfair(70, True)

def alpha(t, t0, t1, d=0.35):
    return max(0.0, min(1.0, (t - t0) / d, (t1 - t) / d))

def texto(im, xy, s, font, cor, a):
    if a < 0.02 or not s: return im
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((xy[0] + 3, xy[1] + 4), s, font=font, fill=(0, 0, 0, 255), anchor='mm')
    sh = lay.filter(ImageFilter.GaussianBlur(6)); sh.putalpha(sh.getchannel('A').point(lambda v: int(v * 0.85 * a)))
    lay2 = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(lay2).text(xy, s, font=font, fill=cor + (255,), anchor='mm')
    lay2.putalpha(lay2.getchannel('A').point(lambda v: int(v * a)))
    return Image.alpha_composite(Image.alpha_composite(im, sh), lay2)

dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', ENT, '-vf', f'scale={W}:{H}:flags=lanczos', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-i', ENT, '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p',
                        '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', SAI], stdin=subprocess.PIPE)
k = 0
while True:
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    t = k / FPS; k += 1
    a = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(np.float32)
    faixa = Image.fromarray(a[CY0:CY1].astype(np.uint8))
    b = np.asarray(faixa.filter(ImageFilter.GaussianBlur(42)), np.float32) * 0.5
    a[CY0:CY1] = a[CY0:CY1] * (1 - mc) + b * mc
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA')
    for t0, t1, l1, l2 in LETRA:
        q = alpha(t, t0, t1)
        if q <= 0: continue
        if l1:
            im = texto(im, (W / 2, YC - 48), l1, F1, B, q)
            im = texto(im, (W / 2, YC + 48), l2, F2, G, q)
        else:
            im = texto(im, (W / 2, YC), l2, F2, G, q)
    d = ImageDraw.Draw(im, 'RGBA')
    estilo.texto_espacado(d, (W / 2, 1790), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(26, 500), (235, 228, 215, 200), 6)
    enc.stdin.write(np.asarray(im.convert('RGB')).tobytes())
enc.stdin.close(); enc.wait(); print('ok', SAI, k)
