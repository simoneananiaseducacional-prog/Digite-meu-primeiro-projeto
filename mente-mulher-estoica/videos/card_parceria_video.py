"""Card "Como ser parceria, e não peso, para quem você ama" em vídeo 9:16: cabeçalho estilo tweet e título já no quadro zero,
itens entrando um por um (movimento desde o início), fecho com Epicteto, Manual 1. Mesmo texto de posts/card_tweet_lista.py.
Ideias inspiradas na lista de @maiconknoblauch, reescritas com palavras próprias.
Uso: python3 card_parceria_video.py foto_perfil.png saida.mp4   # a foto nunca vai para o repositório
"""
import sys, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/posts')
import estilo, midia
from PIL import Image, ImageDraw
from pathlib import Path

W, H, FPS, T = 1080, 1920, 30, 13.5
BR, CZ, G = (240, 240, 240), (140, 140, 140), estilo.DOURADO
_src = Path('/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/posts/card_tweet_lista.py').read_text()
_ns = {}; exec(_src[_src.index('TITULO ='):_src.index('foto = ')], _ns)   # mesmo texto do card
TITULO, LISTA, FECHO, FONTE = _ns['TITULO'], _ns['LISTA'], _ns['FECHO'], _ns['FONTE']
def cl(p): return max(0.0, min(1.0, p))
def sv(p): p = cl(p); return p * p * (3 - 2 * p)

foto = Image.open(sys.argv[1]).convert('RGB'); lado = min(foto.size)
foto = foto.crop(((foto.width - lado) // 2, (foto.height - lado) // 2, (foto.width + lado) // 2, (foto.height + lado) // 2))
av = foto.resize((130, 130), Image.LANCZOS)
m = Image.new('L', (520, 520), 0); ImageDraw.Draw(m).ellipse((0, 0, 519, 519), 255); m = m.resize((130, 130), Image.LANCZOS)
ft, fl, fi = estilo.sem_serifa(50, 600), estilo.sem_serifa(40, 400), estilo.playfair(42, italica=True)
X, Y0, PASSO = 80, 300, 56
T_ITEM, DT, T_FECHO = 0.1, 0.48, 7.4

base = Image.new('RGB', (W, H), (10, 10, 10)); d = ImageDraw.Draw(base)
base.paste(av, (X, Y0), m)
d.text((X + 158, Y0 + 46), 'Mente Mulher Estoica', font=estilo.sem_serifa(42, 700), fill=(245, 245, 245), anchor='lm')
d.text((X + 158, Y0 + 94), '@mente_mulher_estoica', font=estilo.sem_serifa(32, 400), fill=CZ, anchor='lm')
y = Y0 + 190
for l in TITULO:
    d.text((X, y), l, font=ft, fill=BR, anchor='ls'); y += 64
Y_LISTA = y + 26
Y_FECHO = Y_LISTA + len(LISTA) * PASSO + 34

def camada(desenho, a, dx=0):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); desenho(ImageDraw.Draw(lay));
    if dx: lay = lay.transform(lay.size, Image.AFFINE, (1, 0, -dx, 0, 1, 0))
    lay.putalpha(lay.getchannel('A').point(lambda v: int(v * cl(a))))
    return lay

def quadro(t):
    im = base.convert('RGBA')
    for k, item in enumerate(LISTA):
        p = sv((t - (T_ITEM + k * DT)) / 0.35)
        if p <= 0: continue
        yy = Y_LISTA + k * PASSO
        def des(dd, yy=yy, item=item):
            dd.ellipse((X + 2, yy - 21, X + 15, yy - 8), fill=G + (255,))
            dd.text((X + 36, yy), item, font=fl, fill=BR + (255,), anchor='ls')
        im = Image.alpha_composite(im, camada(des, p, dx=-40 * (1 - p)))
    pf = sv((t - T_FECHO) / 0.6)
    if pf > 0:
        def desf(dd):
            yy = Y_FECHO
            for l in FECHO:
                dd.text((X, yy), l, font=fi, fill=G + (255,), anchor='ls'); yy += 54
            dd.text((X, yy + 6), FONTE, font=estilo.sem_serifa(30, 400), fill=CZ + (255,), anchor='ls')
        im = Image.alpha_composite(im, camada(desf, pf))
    return im.convert('RGB')

if __name__ == '__main__':
    saida = Path(sys.argv[2])
    assert Y_FECHO + 2 * 54 + 6 < estilo.BASE_SEGURA + 120, Y_FECHO
    ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
    for k in range(int(T * FPS)):
        t = k / FPS
        ff.stdin.write(estilo.para_bytes(np.asarray(quadro(t), np.float32) * cl((T - t) / 0.4)))
    ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida)
    saida.with_suffix('.mudo.mp4').unlink(missing_ok=True); print('ok', saida)
