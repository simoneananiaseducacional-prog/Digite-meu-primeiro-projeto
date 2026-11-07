"""Foto da Simone apontando para cima + frases que se revezam no topo, onde o dedo aponta.
Uso: python3 foto_frases.py foto.jpg saida.mp4   (a foto nunca entra no repositório)
"""
import sys, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw, ImageOps
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
VERM = (210, 90, 90)
foto, saida = Path(sys.argv[1]), Path(sys.argv[2])
def ap(t, t0, d=0.45): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1): return ap(t, t0) * (1 - ap(t, t1 - 0.35, 0.35))
FR = [  # (linha 1, cor 1, linha 2, cor 2, entra, sai)
    ('Quando alguém te machuca,', B, 'o primeiro impacto não é escolha.', B, 0.5, 4.0),
    ('O susto. O nó na garganta.', B, 'A lágrima que vem antes de pensar.', B, 4.2, 7.8),
    ('Mas o que vem depois', B, 'depende de você.', G, 8.0, 11.4),
    ('Que história você vai contar', B, 'sobre o que aconteceu?', G, 11.6, 15.0),
    ('Se não assume esse controle,', B, 'entrega suas emoções ao outro.', VERM, 15.2, 18.8),
    ('Você não escolhe o primeiro impacto.', B, 'Escolhe o que faz com ele.', G, 19.0, 23.0),
]
T = 29.0
img = ImageOps.exif_transpose(Image.open(foto)).convert('RGB')
esc = max(W / img.width, H / img.height) * 1.04
img = img.resize((int(img.width * esc), int(img.height * esc)), Image.LANCZOS)
x0 = (img.width - W) // 2; img = img.crop((x0, 0, x0 + W, H))
cinza = np.asarray(img.convert('L'), np.float32)
cor = np.asarray(img, np.float32)
base = cinza[..., None] * 0.75 + cor * 0.25            # quase preto e branco, com um resto de calor
yy = np.arange(H)[:, None, None]
sombra = np.clip(1 - 0.75 * np.clip((560 - yy) / 400, 0, 1), 0.25, 1)  # escurece o topo para ler
base = base * sombra * 0.9
F1, F2 = estilo.playfair(54), estilo.playfair(54, True)
def txt(d, xy, s, f, c, a):
    if a <= 0.01: return
    d.text((xy[0] + 2, xy[1] + 3), s, font=f, fill=(0, 0, 0, int(180 * a)), anchor='mm')
    d.text(xy, s, font=f, fill=c + (int(255 * a),), anchor='mm')
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    z = 1 + 0.05 * t / T
    cw, ch = W / z, H / z
    q = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).crop((int((W - cw) / 2), int((H - ch) * 0.35), int((W + cw) / 2), int((H - ch) * 0.35 + ch))).resize((W, H), Image.BILINEAR)
    escurece = 1 - 0.35 * ap(t, 23.2, 1.0)
    q = Image.fromarray((np.asarray(q, np.float32) * escurece).astype(np.uint8)).convert('RGBA')
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
    for l1, c1, l2, c2, t0, t1 in FR:
        a = jan(t, t0, t1)
        txt(d, (W/2, 215), l1, F1, c1, a); txt(d, (W/2, 295), l2, F2, c2, a)
    fim = 1 - ap(t, T - 0.8, 0.6)
    txt(d, (W/2, 215), '“Não são as coisas que nos perturbam,', estilo.playfair(48, True), G, ap(t, 23.3) * fim)
    txt(d, (W/2, 285), 'mas o juízo que fazemos delas.”', estilo.playfair(48, True), G, ap(t, 23.7) * fim)
    txt(d, (W/2, 350), 'Epicteto, Encheirídion, 5', estilo.playfair(30, True), (200, 200, 200), ap(t, 24.3) * fim)
    if ap(t, 25.0) > 0:
        estilo.texto_espacado(d, (W/2, 1440), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(22, 500), (220, 220, 220, int(255 * ap(t, 25.0) * fim)), 6)
    out = Image.alpha_composite(q, cam)
    fr = np.asarray(out.convert('RGB'), np.float32) * (1 - ap(t, T - 0.6, 0.6)) * ap(t, 0, 0.5)
    ff.stdin.write(estilo.para_bytes(np.clip(estilo.granulado(fr), 0, 255)))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); saida.with_suffix('.mudo.mp4').unlink(missing_ok=True)
print('ok')
