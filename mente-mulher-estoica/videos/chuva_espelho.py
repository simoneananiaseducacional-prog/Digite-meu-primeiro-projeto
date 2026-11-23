"""Chuva no retrovisor, à noite: vídeo enviado pela Simone + Epicteto, Encheirídion, 10.
Gancho de pergunta, citação inteira e fecho ligando ao que depende de nós (mesma ideia do post do Senna).
Uso: python3 chuva_espelho.py entrada.mp4 saida.mp4 [lento, ex. 1.76 para ~40 s]
"""
import sys, subprocess, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo
from PIL import Image, ImageDraw, ImageFilter
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
ENT, SAI = sys.argv[1], sys.argv[2]
LENTO = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0   # câmera lenta (o original é 60 fps)
DUR = LENTO * float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', ENT]))
def cl(p): return max(0.0, min(1.0, p))
def jan(t, t0, t1, d=0.45): return cl(min((t - t0) / d, (t1 - t) / d))

# blocos: (início, fim, [(texto, fonte, cor)])
BLOCOS = [
    (0.0, 7.5, [('A chuva não pede licença.', estilo.playfair(66), B),
                ('O que você faz com ela?', estilo.playfair(66, True), G)]),
    (8.0, 23.5, [('“A cada imprevisto que lhe acontecer,', estilo.playfair(48, True), B),
                 ('lembre-se de voltar-se para si mesmo', estilo.playfair(48, True), B),
                 ('e perguntar qual capacidade você tem', estilo.playfair(48, True), B),
                 ('para tirar proveito dele.”', estilo.playfair(48, True), G),
                 ('', None, None),
                 ('Epicteto, Encheirídion, 10', estilo.playfair(32, True), C)]),
    (24.0, 32.0, [('Você não controla a chuva.', estilo.playfair(66), B),
                  ('Controla como segue o caminho.', estilo.playfair(62, True), G)]),
    (32.5, DUR - 0.1, [('E hoje, qual capacidade', estilo.playfair(66), B),
                       ('você vai usar?', estilo.playfair(66, True), G)]),
]
ALT = {2: 98, 6: 70}

def texto(im, xy, s, font, cor, a):
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((xy[0] + 3, xy[1] + 4), s, font=font, fill=(0, 0, 0, 255), anchor='mm')
    sh = lay.filter(ImageFilter.GaussianBlur(7)); sh.putalpha(sh.getchannel('A').point(lambda v: int(v * 0.9 * a)))
    l2 = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(l2).text(xy, s, font=font, fill=cor + (255,), anchor='mm')
    l2.putalpha(l2.getchannel('A').point(lambda v: int(v * a)))
    return Image.alpha_composite(Image.alpha_composite(im, sh), l2)

# sombra suave no topo para leitura
y = np.arange(H)[:, None, None].astype(np.float32)
esc = 1 - 0.72 * np.clip(1 - (y - 150) / 750, 0, 1) * np.clip(y / 150, 0, 1) - 0.55 * np.clip(1 - y / 150, 0, 1)

dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', ENT, '-vf', f'setpts={LENTO}*PTS,fps={FPS},scale={W}:{H}:flags=lanczos', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '18',
                        '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', '-movflags', '+faststart', SAI], stdin=subprocess.PIPE)
k = 0
while True:
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    t = k / FPS; k += 1
    a = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(np.float32) * esc
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA')
    for t0, t1, linhas in BLOCOS:
        q = jan(t, t0, t1)
        if q <= 0.02: continue
        n = len(linhas); passo = ALT[n]; yy = 360 - (n - 1) * passo / 2 + (60 if n == 2 else 0)
        for s, f, cor in linhas:
            if s: im = texto(im, (W / 2, yy), s, f, cor, q)
            yy += passo
    d = ImageDraw.Draw(im, 'RGBA')
    estilo.texto_espacado(d, (W / 2, 1800), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(26, 500), (235, 228, 215, 200), 6)
    fim = cl((DUR - t) / 0.4)
    enc.stdin.write((np.asarray(im.convert('RGB'), np.float32) * fim).astype(np.uint8).tobytes())
enc.stdin.close(); enc.wait(); print('ok', SAI, k)
