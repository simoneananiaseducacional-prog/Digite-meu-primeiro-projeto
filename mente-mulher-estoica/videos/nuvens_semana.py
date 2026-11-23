"""Nuvens (vídeo de @itwlu, sem texto e sem marca) + Sêneca, Cartas a Lucílio, 13.4. Reels de segunda-feira.
Gancho do banco (pergunta): "Você está sofrendo pelo que aconteceu ou pelo que imaginou?"
Uso: python3 nuvens_semana.py nuvens_limpo.mp4 saida.mp4 [lento]
"""
import sys, subprocess, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo
from PIL import Image, ImageDraw, ImageFilter
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, (215, 210, 200)
ENT, SAI = sys.argv[1], sys.argv[2]
LENTO = float(sys.argv[3]) if len(sys.argv) > 3 else 1.85
DUR = LENTO * float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', ENT]))
def cl(p): return max(0.0, min(1.0, p))
def jan(t, t0, t1, d=0.2): return cl(min((t - t0) / d, (t1 - t) / d))
P = estilo.playfair
BLOCOS = [
    (0.0, 5.2, 96, [('Você está sofrendo', P(78), B), ('pelo que aconteceu', P(78), B), ('ou pelo que imaginou?', P(78, True), G)]),
    (5.4, 11.0, 100, [('A maioria das nuvens', P(80), B), ('passa sem chover.', P(80, True), G)]),
    (11.2, 18.8, 80, [('“Há mais coisas que nos assustam', P(54, True), B), ('do que coisas que nos esmagam.', P(54, True), B),
                      ('Sofremos mais na imaginação', P(54, True), G), ('do que na realidade.”', P(54, True), G),
                      ('', None, None), ('Sêneca, Cartas a Lucílio, 13.4', P(34, True), C)]),
    (19.0, 23.0, 100, [('Nesta semana,', P(80), B), ('viva o que é real.', P(80, True), G)]),
    (23.2, DUR - 0.1, 90, [('Manda para quem', P(70), B), ('precisa ouvir isso hoje.', P(70, True), G)]),
]
def texto(im, xy, s, font, cor, a):
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).text((xy[0] + 3, xy[1] + 4), s, font=font, fill=(0, 0, 0, 255), anchor='mm')
    sh = lay.filter(ImageFilter.GaussianBlur(9)); sh.putalpha(sh.getchannel('A').point(lambda v: int(v * 0.95 * a)))
    l2 = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(l2).text(xy, s, font=font, fill=cor + (255,), anchor='mm')
    l2.putalpha(l2.getchannel('A').point(lambda v: int(v * a)))
    return Image.alpha_composite(Image.alpha_composite(im, sh), l2)
# escurecer: as nuvens são claras; mais escuro no centro (texto) e nas bordas
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
vin = 1 - 0.35 * np.clip(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2, 0, 1)
faixa = 1 - 0.25 * np.exp(-((yy - 900) / 420) ** 2)
ESC = (0.62 * vin * faixa)[..., None]
dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', ENT, '-vf',
                        f'setpts={LENTO}*PTS,minterpolate=fps={FPS}:mi_mode=blend,scale={W}:{H}:flags=lanczos', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '18',
                        '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', '-movflags', '+faststart', SAI], stdin=subprocess.PIPE)
k = 0
while True:
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    t = k / FPS; k += 1
    a = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(np.float32)
    g = a.mean(axis=2, keepdims=True); a = (0.8 * a + 0.2 * g) * ESC   # um pouco menos de cor, mais sóbrio
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA')
    d = ImageDraw.Draw(im, 'RGBA')
    estilo.texto_espacado(d, (W / 2, 250), 'COMEÇO DE SEMANA', estilo.sem_serifa(32, 600), G + (235,), 10)
    for t0, t1, passo, linhas in BLOCOS:
        q = jan(t, t0, t1)
        if q <= 0.02: continue
        y0 = 920 - (len(linhas) - 1) * passo / 2
        for i, (s, f, cor) in enumerate(linhas):
            if s: im = texto(im, (W / 2, y0 + i * passo), s, f, cor, q)
    d = ImageDraw.Draw(im, 'RGBA')
    d.text((W / 2, 1745), 'Vídeo: @itwlu', font=estilo.sem_serifa(24, 500), fill=(220, 214, 205, 210), anchor='mm')
    estilo.texto_espacado(d, (W / 2, 1795), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(26, 500), (235, 228, 215, 210), 6)
    enc.stdin.write((np.asarray(im.convert('RGB'), np.float32) * cl((DUR - t) / 0.5)).astype(np.uint8).tobytes())
enc.stdin.close(); enc.wait(); print('ok', SAI, k)
