"""Quem some e volta: ele aparece com carinho, some, volta de novo; ela acende quando ele chega e apaga quando
ele some. Primeiro quadro já em ação (balão + personagens), título visível desde o quadro zero.
Base: reforço intermitente (Ferster e Skinner, Schedules of Reinforcement, 1957); vínculo traumático (Dutton e
Painter, Victimology, 1981); Sêneca, Cartas a Lucílio, 3.2. Uso: python3 some_e_volta.py saida.mp4 [capa.png]
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia, personagens
from personagens import ela, ele
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pathlib import Path
W, H, FPS, T = 1080, 1920, 30, 26.0
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
FT = Path(__file__).with_name('fontes')
def ebg(nome, t): return ImageFont.truetype(str(FT / f'EBGaramond-{nome}.ttf'), t)
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.3): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.25): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
def mix(a, b, p): return tuple(int(a[i] + (b[i] - a[i]) * p) for i in range(3))
saida = Path(sys.argv[1]); capa = Path(sys.argv[2]) if len(sys.argv) > 2 else None

CHAO, K, CENTRO = 1250, 1.5, (540, 1080)
XE, XH = 390, 690
OURO0, CINZA_ELA = personagens.DOURADO, (105, 105, 112)
# presença dele: (chega, sai). No quadro zero ele já está lá.
VISITAS = [(-1.0, 1.6), (5.0, 7.2), (8.8, 10.6)]
FALAS_ELE = [(-1.0, 1.5, 'Saudade de você.'), (5.2, 7.0, 'Desculpa, tava corrido.'), (9.0, 10.5, 'Você é especial.')]
FALAS_ELA = [(2.4, 3.6, 'Oi?'), (3.6, 4.9, 'Tá tudo bem?'), (7.8, 8.7, '...')]
FB = estilo.sem_serifa(40, 600)
def presenca(t):
    return max(cl(min((t - a) / 0.4, (b - t) / 0.4)) for a, b in VISITAS)
def brilho_dela(t):   # cada volta acende um pouco mais (a incerteza aumenta a recompensa)
    v = 0.0
    for i, (a, b) in enumerate(VISITAS): v = max(v, (0.7 + 0.3 * i / 2) * cl(min((t - a) / 0.4, (b + 0.8 - t) / 0.8)))
    return v

def balao(im, cx, cy, s, a, fundo, cor, ponta):
    if a < 0.02: return im
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    w = FB.getlength(s) + 70; h = 92; x0 = min(max(cx - w / 2, 40), W - 40 - w)
    d.rounded_rectangle((x0, cy - h / 2, x0 + w, cy + h / 2), radius=40, fill=fundo + (245,))
    d.polygon([(cx - 18, cy + h / 2 - 2), (cx + 18, cy + h / 2 - 2), (cx + 14 * ponta, cy + h / 2 + 34)], fill=fundo + (245,))
    d.text((x0 + w / 2, cy + 2), s, font=FB, fill=cor + (255,), anchor='mm')
    lay.putalpha(lay.getchannel('A').point(lambda v: int(v * cl(a))))
    return Image.alpha_composite(im, lay)
def texto(im, xy, s, font, cor, a):
    if a < 0.02: return im
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).text(xy, s, font=font, fill=cor + (255,), anchor='mm')
    lay.putalpha(lay.getchannel('A').point(lambda v: int(v * cl(a))))
    return Image.alpha_composite(im, lay)

fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
T_CENA = 11.4
def quadro(t):
    cena = 1 - 0.85 * ap(t, T_CENA, 0.6)
    p = presenca(t); br = brilho_dela(t); cinza = (1 - br) * ap(t, 1.4, 0.6)
    cen = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(cen, 'RGBA')
    d.line([(CENTRO[0] - 380, CHAO), (CENTRO[0] + 380, CHAO)], fill=C + (int(200 * cena),), width=4)
    if p > 0.02:
        ele(d, XH + 260 * (1 - p), CHAO - 6, cena * p, braco=0.5 * p, lado=-1, t=t, emo=dict(sorriso=0.8))
    personagens.DOURADO = mix(OURO0, CINZA_ELA, cinza)
    cel = cinza
    ela(d, XE, CHAO - 6, cena, braco=0.45 * cel, lado=1, cabeca_baixa=0.5 * cel, t=t, emo=dict(sorriso=0.9 * br, triste=0.7 * cinza))
    personagens.DOURADO = OURO0
    if cel > 0.05:   # celular na mão dela, esperando
        hy = CHAO - 6 - 240 + 8 * cel; px, py = XE + 74, hy + 64
        d.rounded_rectangle((px - 11, py - 19, px + 11, py + 19), radius=3, fill=(30, 30, 32, int(255 * cena * cel)), outline=(200, 200, 206, int(255 * cena * cel)), width=2)
    big = cen.resize((int(W * K), int(H * K)), Image.BICUBIC)
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.paste(big, (int(W / 2 - CENTRO[0] * K), int(1060 - CENTRO[1] * K)))
    im = fundo.copy()
    if br > 0.02:
        gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); px = W / 2 + (XE - CENTRO[0]) * K
        ImageDraw.Draw(gl).ellipse((px - 260, 1000 - 330, px + 260, 1000 + 330), fill=G + (int(70 * br * cena),))
        im = Image.alpha_composite(im, gl.filter(ImageFilter.GaussianBlur(80)))
    im = Image.alpha_composite(im, cam)
    hx = W / 2 + (XH - CENTRO[0]) * K; ex = W / 2 + (XE - CENTRO[0]) * K
    for t0, t1, s in FALAS_ELE: im = balao(im, hx - 30, 640, s, jan(t, t0, t1) * cena, (236, 214, 160), (40, 30, 20), 1)
    for t0, t1, s in FALAS_ELA: im = balao(im, ex + 30, 690, s, jan(t, t0, t1) * cena, (60, 58, 62), (236, 232, 224), -1)
    q = 1 - ap(t, T_CENA - 0.2, 0.4)
    im = texto(im, (W / 2, 250), 'Some. Volta. Some de novo.', ebg('Regular', 74), B, q)
    im = texto(im, (W / 2, 345), 'Por que é tão difícil largar?', ebg('Italic', 74), G, q)
    f1 = jan(t, 11.8, 15.6)
    im = texto(im, (W / 2, 820), 'Não é só o amor que prende.', ebg('Regular', 70), B, f1)
    im = texto(im, (W / 2, 920), 'É a incerteza.', ebg('Italic', 84), G, f1 * ap(t, 12.6))
    f2 = jan(t, 15.8, 20.0)
    im = texto(im, (W / 2, 740), 'O carinho que vem e vai', ebg('Regular', 62), B, f2)
    im = texto(im, (W / 2, 820), 'prende mais do que o constante.', ebg('Regular', 62), B, f2)
    im = texto(im, (W / 2, 900), 'Reforço intermitente, Ferster e Skinner, 1957', ebg('Italic', 32), C, f2 * ap(t, 16.4))
    im = texto(im, (W / 2, 1010), 'Na relação, isso tem nome:', ebg('Regular', 58), B, f2 * ap(t, 17.4))
    im = texto(im, (W / 2, 1090), 'vínculo traumático.', ebg('Italic', 66), G, f2 * ap(t, 17.8))
    im = texto(im, (W / 2, 1160), 'Dutton e Painter, 1981', ebg('Italic', 32), C, f2 * ap(t, 18.2))
    f3 = ap(t, 20.2)
    im = texto(im, (W / 2, 760), 'Observe o padrão,', ebg('Regular', 76), B, f3)
    im = texto(im, (W / 2, 860), 'não a promessa.', ebg('Italic', 80), G, f3)
    im = texto(im, (W / 2, 970), '“Antes da amizade, avaliar. Depois, confiar.”', ebg('Italic', 40), B, f3 * ap(t, 20.8))
    im = texto(im, (W / 2, 1025), 'Sêneca, Cartas a Lucílio, 3.2', ebg('Italic', 32), C, f3 * ap(t, 20.8))
    im = texto(im, (W / 2, 1190), 'Manda para quem vive esse vai e volta.', ebg('Medium', 46), G, ap(t, 22.0))
    im = texto(im, (W / 2, 1540), 'Isto não é diagnóstico. Se dói, procure apoio profissional.', estilo.sem_serifa(28, 500), C, ap(t, 22.4))
    d2 = ImageDraw.Draw(im, 'RGBA')
    estilo.texto_espacado(d2, (W / 2, 1720), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(26, 500), (170, 165, 158, 210), 6)
    return im.convert('RGB')

if capa: quadro(0.0).save(capa)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    ff.stdin.write(estilo.para_bytes(np.asarray(quadro(t), np.float32) * cl((T - t) / 0.4)))
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida)
saida.with_suffix('.mudo.mp4').unlink(missing_ok=True); print('ok', saida)
