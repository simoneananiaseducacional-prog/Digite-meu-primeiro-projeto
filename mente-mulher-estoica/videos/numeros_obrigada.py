import sys, math
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia, numpy as np
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
W, H, FPS, T = 1080, 1920, 30, 17.0
B, G, C = estilo.BRANCO, estilo.DOURADO, (150, 146, 140)
U = '/root/.claude/uploads/fe1db7e1-a242-55eb-8116-11f11488b586/'
g = Image.open(U + '4fed8218-image.png').convert('RGB'); r = Image.open(U + 'e827143c-image.jpg').convert('RGB')
TH = [g.crop((617, 490, 923, 1033)), r.crop((0, 0, 390, 680)), g.crop((0, 1037, 305, 1580)), r.crop((395, 0, 785, 680)), g.crop((0, 490, 305, 1033))]
TH = [t.resize((330, int(330 * t.height / t.width)), Image.LANCZOS) for t in TH]
POS = [(540, 820, -4), (250, 640, 6), (820, 600, -7), (270, 1080, -5), (810, 1060, 5)]   # centro x, y, rotação
INI = [3.0, 4.0, 4.8, 5.6, 6.4]
NUMS = [('98,7 mil', 'duas pessoas, dois caminhos', 540, 560), ('43 mil', 'para onde vai a sua energia', 300, 760),
        ('42,3 mil', 'o próximo passo', 790, 900), ('38,7 mil', 'a ponte', 280, 1060),
        ('22,2 mil', 'a borracha', 770, 1200), ('10,2 mil', 'a coragem', 330, 1330)]
INI2 = [3.0, 3.7, 4.4, 5.1, 5.8, 6.5]
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.5): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
saida = Path(sys.argv[1]); ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
F1 = estilo.playfair(66); F2 = estilo.playfair(66, True)
for k in range(int(T * FPS)):
    t = k / FPS
    im = fundo.copy(); d = ImageDraw.Draw(im, 'RGBA')
    a = jan(t, 0.2, 3.2)
    if a > 0.02:
        d.text((W/2, 860), 'Não é dancinha.', font=F1, fill=B + (int(255 * a),), anchor='mm')
        d.text((W/2, 960), 'Não é piada.', font=F1, fill=B + (int(255 * a),), anchor='mm')
        d.text((W/2, 1080), 'É reflexão.', font=F2, fill=G + (int(255 * ap(t, 1.2) * a / max(a, 1e-3) * a),), anchor='mm')
    some = 1 - ap(t, 10.6, 0.6)
    for (num, tema, x, y), t0 in zip(NUMS, INI2):
        p = ap(t, t0, 0.4) * some
        if p < 0.02: continue
        sc = 0.8 + 0.2 * ap(t, t0, 0.4)
        d.text((x, y), num, font=estilo.playfair(int(92 * sc)), fill=G + (int(255 * p),), anchor='mm')
        d.text((x, y + 72), tema, font=estilo.sem_serifa(30, 500), fill=(205, 200, 194, int(255 * p)), anchor='mm')
    d = ImageDraw.Draw(im, 'RGBA')
    tt = jan(t, 7.4, 10.8)
    if tt > 0.02:
        d.text((W/2, 1530), 'Mais de 250 mil visualizações', font=estilo.sem_serifa(46, 600), fill=B + (int(255 * tt),), anchor='mm')
        d.text((W/2, 1600), 'em vídeos sobre a vida real.', font=estilo.sem_serifa(46, 400), fill=(205, 200, 194, int(255 * tt)), anchor='mm')
    f = jan(t, 11.0, 16.6)
    if f > 0.02:
        for i, l in enumerate(['Ainda existem pessoas', 'que procuram a verdade,', 'que querem quebrar ciclos', 'e virar a chave da vida.']):
            d.text((W/2, 720 + i * 82), l, font=F1, fill=B + (int(255 * f),), anchor='mm')
        f2 = jan(t, 12.6, 16.6)
        d.text((W/2, 1110), 'Obrigada por ser uma delas.', font=F2, fill=G + (int(255 * f2),), anchor='mm')
        f3 = jan(t, 13.6, 16.6)
        if f3 > 0.02: estilo.texto_espacado(d, (W/2, 1300), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(26, 500), C + (int(255 * f3),), 6)
    ff.stdin.write(estilo.para_bytes(np.asarray(im.convert('RGB'), np.float32) * (1 - ap(t, T - 0.4, 0.4))))
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); print('ok')
