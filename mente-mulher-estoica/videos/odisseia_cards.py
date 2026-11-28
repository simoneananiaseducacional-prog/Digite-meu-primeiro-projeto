"""Reel da Odisseia a partir dos 9 cartões verticais refeitos (ChatGPT, imagens da Simone) + cartão 10 montado aqui
no mesmo estilo (fundo: mar e barco do cartão 1). Zoom lento e transição suave; tempo de leitura por cartão.
Uso: python3 odisseia_cards.py pasta_dos_cartoes saida.mp4   (cartões nomeados 01.png a 09.png)
"""
import sys, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pathlib import Path
W, H, FPS = 1080, 1920, 30
FT = Path(__file__).with_name('fontes')
def ebg(n, t): return ImageFont.truetype(str(FT / f'EBGaramond-{n}.ttf'), t)
PASTA, OUT = Path(sys.argv[1]), Path(sys.argv[2])
CARDS = [Image.open(PASTA / f'{i:02d}.png').convert('RGB').resize((W, H), Image.LANCZOS) for i in range(1, 10)]
# cartão 10: mar e barco do cartão 1 (metade de baixo), ampliados, com texto no mesmo estilo
c1 = CARDS[0]; mar = c1.crop((380, 900, 1080, 1700)).resize((W, int(800 * W / 700)), Image.LANCZOS)
c10 = Image.new('RGB', (W, H), (8, 7, 6)); c10.paste(mar, (0, H - mar.height - 120))
a = np.asarray(c10, np.float32); y = np.linspace(0, 1, H)[:, None, None]
a *= np.clip(0.25 + 0.75 * (y - 0.35) / 0.3, 0.2, 1.0); a *= 1 - 0.6 * np.clip((y - 0.9) / 0.1, 0, 1)
c10 = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(c10)
BR, OU = (239, 232, 220), (201, 168, 106)
X = 90; yy = 270
d.text((X, yy), '10', font=ebg('Regular', 38), fill=OU); yy += 80
for l in ['A ODISSEIA não é apenas', 'sobre voltar para casa.']:
    d.text((X, yy), l, font=ebg('Regular', 66), fill=BR); yy += 84
d.text((X, yy + 10), 'É sobre voltar para si.', font=ebg('Regular', 72), fill=OU); yy += 130
d.line([(X, yy), (X + 160, yy)], fill=OU, width=3); yy += 60
for l in ['Talvez o maior inimigo de Odisseu', 'nunca tenha sido Poseidon.', 'Foi esquecer aquilo que orientava', 'sua jornada. Talvez o nosso', 'também não seja.']:
    d.text((X, yy), l, font=ebg('Italic', 48), fill=BR); yy += 64
estilo.texto_espacado(d, (W / 2, 1810), '@mente_mulher_estoica', estilo.sem_serifa(28, 400), (205, 198, 188), 6)
CARDS.append(c10)
DUR = [7.5, 5.0, 5.5, 5.5, 6.0, 6.0, 5.5, 6.0, 6.0, 9.0]; CF = 0.6
def render(i, t):
    z = 1 + 0.035 * t / DUR[i]; im = CARDS[i]
    g = im.resize((int(W * z), int(H * z)), Image.BICUBIC); ox = (g.width - W) // 2; oy = (g.height - H) // 2
    return g.crop((ox, oy, ox + W, oy + H))
ff = midia.gravador(OUT.with_suffix('.mudo.mp4'), estatico=False)
T = sum(DUR); ini = np.cumsum([0] + DUR[:-1])
for k in range(int(T * FPS)):
    t = k / FPS; i = int(np.searchsorted(ini, t, side='right') - 1); tl = t - ini[i]
    fr = render(i, tl)
    if i + 1 < len(CARDS) and tl > DUR[i] - CF: fr = Image.blend(fr, render(i + 1, 0), (tl - (DUR[i] - CF)) / CF)
    ff.stdin.write((np.asarray(fr, np.float32) * min(1, (T - t) / 0.6)).astype(np.uint8).tobytes())
ff.stdin.close(); ff.wait(); midia.juntar_audio(OUT.with_suffix('.mudo.mp4'), OUT); OUT.with_suffix('.mudo.mp4').unlink(missing_ok=True)
c10.save(OUT.with_name('odisseia_cartao10.png')); CARDS[0].save(OUT.with_name('odisseia_capa.png')); print('ok', T)
