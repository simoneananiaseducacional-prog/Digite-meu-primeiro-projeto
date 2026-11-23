"""Senna, GP do Brasil de 1991: "vai ter que dar". Trecho da entrevista (montagem de @chagaas_07, com as legendas dela)
+ gancho no topo + fecho em tela própria com Marco Aurélio, Meditações, 6.19. Áudio original.
Ideia da Simone: confiança com lastro (preparo, treino, autoconhecimento). Autoeficácia: Bandura, 1977 (na legenda).
Uso: python3 senna_vai_dar.py entrada.mp4 saida.mp4
"""
import sys, subprocess, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo
from PIL import Image, ImageDraw, ImageFilter
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, (205, 198, 188)
ENT, SAI = sys.argv[1], sys.argv[2]
CORTE, T = 21.8, 30.0
P = estilo.playfair
def cl(p): return max(0.0, min(1.0, p))
def jan(t, t0, t1, d=0.25): return cl(min((t - t0) / d, (t1 - t) / d))
TOPO = [  # textos sobre o vídeo (topo)
    (0.0, 5.0, [('De onde vem a certeza', P(64), B), ('de quem diz: “vai ter que dar”?', P(62, True), G)]),
    (12.6, CORTE - 0.1, [('Não é otimismo cego.', P(64), B), ('É treino, preparo e autoconhecimento.', P(52, True), G)]),
]
FECHO = [  # tela final
    (CORTE + 0.3, 27.0, 880, 84, [('“Se algo é possível', P(70, True), B), ('ao ser humano, considera', P(70, True), B),
                                  ('que também está', P(70, True), G), ('ao teu alcance.”', P(70, True), G), ('', None, None),
                                  ('Marco Aurélio, Meditações, 6.19', P(36, True), C)]),
    (27.2, T - 0.05, 900, 96, [('Manda para quem', P(76), B), ('está quase desistindo.', P(76, True), G)]),
]
def texto(im, xy, s, font, cor, a):
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).text((xy[0] + 3, xy[1] + 4), s, font=font, fill=(0, 0, 0, 255), anchor='mm')
    sh = lay.filter(ImageFilter.GaussianBlur(8)); sh.putalpha(sh.getchannel('A').point(lambda v: int(v * 0.95 * a)))
    l2 = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(l2).text(xy, s, font=font, fill=cor + (255,), anchor='mm')
    l2.putalpha(l2.getchannel('A').point(lambda v: int(v * a)))
    return Image.alpha_composite(Image.alpha_composite(im, sh), l2)
# vídeo recortado no centro (y 230..1580 da escala 1080x1920) e colado entre faixas escuras para os textos
Y_SRC, ALT_V, Y_DST = 230, 1350, 330
yv = np.arange(ALT_V)[:, None, None].astype(np.float32)
PENA = np.clip(yv / 90, 0, 1) * np.clip((ALT_V - yv) / 90, 0, 1)
FUNDO = np.full((H, W, 3), 8, np.float32)
def montar(a):
    out = FUNDO.copy(); seg = a[Y_SRC:Y_SRC + ALT_V]
    out[Y_DST:Y_DST + ALT_V] = seg * PENA + 8 * (1 - PENA)
    return out
dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-t', str(CORTE), '-i', ENT, '-vf', f'fps={FPS},scale={W}:{H}:flags=lanczos',
                        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-i', ENT, '-filter_complex', f'[1:a]atrim=0:{T},asetpts=PTS-STARTPTS,afade=t=out:st={T - 1.8}:d=1.8[a]',
                        '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
                        '-shortest', '-movflags', '+faststart', SAI], stdin=subprocess.PIPE)
def rodape(im):
    d = ImageDraw.Draw(im, 'RGBA')
    d.text((W / 2, 1755), 'Vídeo: @chagaas_07', font=estilo.sem_serifa(24, 500), fill=(225, 218, 208, 215), anchor='mm')
    estilo.texto_espacado(d, (W / 2, 1820), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(26, 500), (240, 232, 220, 220), 6)
    return im
k, ultimo = 0, None
while True:
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    t = k / FPS; k += 1
    a = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(np.float32); ultimo = a.copy()
    im = Image.fromarray(np.clip(montar(a), 0, 255).astype(np.uint8)).convert('RGBA')
    d = ImageDraw.Draw(im, 'RGBA')
    if not any(jan(t, t0, t1) > 0.02 for t0, t1, _ in TOPO):
        estilo.texto_espacado(d, (W / 2, 190), 'CONFIANÇA COM LASTRO', estilo.sem_serifa(32, 600), G + (235,), 10)
    for t0, t1, linhas in TOPO:
        q = jan(t, t0, t1)
        if q > 0.02:
            for i, (s, f, cor) in enumerate(linhas): im = texto(im, (W / 2, 145 + i * 92), s, f, cor, q)
    enc.stdin.write(np.asarray(rodape(im).convert('RGB')).tobytes())
# tela final: último quadro desfocado e escuro
base = Image.fromarray(ultimo.astype(np.uint8)).filter(ImageFilter.GaussianBlur(28))
base = Image.fromarray((np.asarray(base, np.float32) * 0.28).astype(np.uint8)).convert('RGBA')
while k < int(T * FPS):
    t = k / FPS; k += 1
    entra = cl((t - CORTE) / 0.5)
    im = Image.blend(Image.fromarray(np.clip(montar(ultimo), 0, 255).astype(np.uint8)).convert('RGBA'), base, entra)
    for t0, t1, yc, passo, linhas in FECHO:
        q = jan(t, t0, t1)
        if q > 0.02:
            y0 = yc - (len(linhas) - 1) * passo / 2
            for i, (s, f, cor) in enumerate(linhas):
                if s: im = texto(im, (W / 2, y0 + i * passo), s, f, cor, q)
    fim = cl((T - t) / 0.5)
    enc.stdin.write((np.asarray(rodape(im).convert('RGB'), np.float32) * fim).astype(np.uint8).tobytes())
enc.stdin.close(); enc.wait(); print('ok', SAI, k)
