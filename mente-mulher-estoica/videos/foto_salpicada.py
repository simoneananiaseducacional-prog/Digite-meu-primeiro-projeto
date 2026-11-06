"""Foto com frases salpicadas (formato da base 018).
A foto fica em preto e branco, escurecida, com zoom lento; as frases aparecem
uma a uma em pontos diferentes da tela e ficam até o fim; a última entra em dourado.
Uso: python3 foto_salpicada.py foto.jpg saida.mp4
A foto nunca entra no repositório; a saída vai para posts/saida (ignorada pelo git).
"""
import sys, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
foto, saida = Path(sys.argv[1]), Path(sys.argv[2])
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0

TITULO = 'Ser estoico é:'
# (frase, x, y, alinhamento) espalhadas, fora do centro e dentro da área segura
FRASES = [('Aceitar o que acontece', 70, 700, 'lm'),
          ('Focar no que depende de você', 1010, 805, 'rm'),
          ('Desejar só o que depende de você', 70, 910, 'lm'),
          ('Governar o diálogo interno', 1010, 1015, 'rm'),
          ('Firmeza sem dureza', 70, 1120, 'lm'),
          ('Não temer a morte', 1010, 1225, 'rm'),
          ('Viver segundo a razão', 70, 1330, 'lm')]
FINAL = 'Ser senhor de si.'
T0, PASSO = 1.6, 1.7
T_FINAL = T0 + len(FRASES) * PASSO + 0.3
T = T_FINAL + 3.6

img = ImageOps.exif_transpose(Image.open(foto)).convert('L')
TOPO = 250                      # a foto entra inteira na largura, abaixo do título
esc = W / img.width
img = img.resize((W, int(img.height * esc)), Image.LANCZOS)
ph = np.asarray(img, np.float32)
m = np.ones(ph.shape[0], np.float32)
borda = 140
m[:borda] = np.linspace(0, 1, borda); m[-borda:] = np.linspace(1, 0, borda)
ph = ph * m[:, None]
base = np.zeros((H, W), np.float32)
alt = min(ph.shape[0], H - TOPO)
base[TOPO:TOPO + alt] = ph[:alt]
yy, xx = np.mgrid[0:H, 0:W]
vinheta = 1 - 0.55 * (((xx - W/2) / (W/2)) ** 2 + ((yy - H/2) / (H/2)) ** 2) / 2
f_tit = estilo.serifa_italica(60, 700)
f_fr = estilo.serifa(48, 700)
f_fim = estilo.serifa_italica(76, 700)

def escrever(d, xy, s, f, cor, a, anc):
    if a <= 0.01: return
    for dx, dy in ((2, 2), (0, 3), (3, 0)):
        d.text((xy[0] + dx, xy[1] + dy), s, font=f, fill=(0, 0, 0, int(170 * a)), anchor=anc)
    d.text(xy, s, font=f, fill=cor + (int(255 * a),), anchor=anc)

ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    z = 1 + 0.07 * t / T
    cw, ch = W / z, H / z
    x0 = (W - cw) / 2; y0 = (H - ch) / 2
    quadro = Image.fromarray(base.astype(np.uint8)).crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.BILINEAR)
    escuro = 0.62 - 0.14 * ap(t, T_FINAL, 1.0)
    q = np.asarray(quadro, np.float32) * escuro * vinheta
    q = np.clip(estilo.granulado(np.stack([q] * 3, -1)), 0, 255).astype(np.uint8)
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
    escrever(d, (W/2, 200), TITULO, f_tit, G, ap(t, 0.3), 'mm')
    for i, (s, x, y, anc) in enumerate(FRASES):
        t1 = T0 + i * PASSO
        a = ap(t, t1, 0.4)
        sobe = 14 * (1 - a)
        escrever(d, (x, y + sobe), s, f_fr, B, a, anc)
    escrever(d, (W/2, 1450), FINAL, f_fim, G, ap(t, T_FINAL, 0.7), 'mm')
    out = Image.alpha_composite(Image.fromarray(q).convert('RGBA'), cam)
    fr = np.asarray(out.convert('RGB'), np.float32) * (1 - ap(t, T - 0.6, 0.6))
    ff.stdin.write(estilo.para_bytes(fr))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); saida.with_suffix('.mudo.mp4').unlink(missing_ok=True)
print('ok', round(T, 1), 's')
