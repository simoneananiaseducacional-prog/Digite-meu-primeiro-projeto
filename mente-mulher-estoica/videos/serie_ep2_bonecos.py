"""Série Amor & Limites, Ep. 2 com bonecos: Quantas decisões suas você já entregou?
Ação no quadro zero (aprendizado 038): ele já fala "Essa roupa não." e o cartão "A roupa" sai da mão dela.
A cada pedido, uma decisão passa para a pilha dele; o círculo do espaço dela encolhe e ela perde a cor.
Base: controle coercitivo (Evan Stark, 2007); Sêneca, Cartas a Lucílio, 1.1.
Uso: python3 serie_ep2_bonecos.py saida.mp4 [capa.png]
"""
import sys, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia, personagens
from personagens import ela, ele
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
W, H, FPS, T = 1080, 1920, 30, 27.0
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
FT = Path(__file__).with_name('fontes')
def ebg(nome, t): return ImageFont.truetype(str(FT / f'EBGaramond-{nome}.ttf'), t)
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.3): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.25): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
def mix(a, b, p): return tuple(int(a[i] + (b[i] - a[i]) * p) for i in range(3))
saida = Path(sys.argv[1]); capa = Path(sys.argv[2]) if len(sys.argv) > 2 else None

CHAO, K, CENTRO = 1250, 1.5, (540, 1080)
XE, XH = 380, 700
def tela(x, y): return (W / 2 + (x - CENTRO[0]) * K, 1060 + (y - CENTRO[1]) * K)
EX, HX = tela(XE, 0)[0], tela(XH, 0)[0]
Y_CHAO = tela(0, CHAO)[1]
OURO0, CINZA_ELA = personagens.DOURADO, (105, 105, 112)
PEDIDOS = [(-0.6, 'Essa roupa não.', 'A roupa'), (2.2, 'Sair com elas de novo?', 'Com quem sai'),
           (4.6, 'Deixa que eu cuido do dinheiro.', 'O dinheiro'), (7.0, 'Apaga essa foto.', 'O que posta'),
           (9.4, 'Sua família de novo?', 'A família')]
T_CENA = 12.0
FB, FC = estilo.sem_serifa(40, 600), estilo.sem_serifa(28, 600)
CW, CH = 200, 50

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
def quadro(t):
    cena = 1 - 0.85 * ap(t, T_CENA, 0.6)
    movidos = sum(ap(t, t0 + 0.9, 0.9) for t0, _, _ in PEDIDOS)
    perda = movidos / len(PEDIDOS)
    im = fundo.copy()
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    # o espaço dela encolhe
    r = 220 - 130 * perda; cy = Y_CHAO - 190
    d.ellipse((EX - r, cy - r, EX + r, cy + r), outline=G + (int(170 * cena),), width=3)
    d.text((EX, cy + r + 30), 'seu espaço', font=ebg('Italic', 34), fill=C + (int(220 * cena),), anchor='mm')
    im = Image.alpha_composite(im, lay)
    cen = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dc = ImageDraw.Draw(cen, 'RGBA')
    dc.line([(CENTRO[0] - 380, CHAO), (CENTRO[0] + 380, CHAO)], fill=C + (int(200 * cena),), width=4)
    ele(dc, XH, CHAO - 6, cena, braco=0.7, lado=-1, t=t, emo=dict(raiva=0.25))
    personagens.DOURADO = mix(OURO0, CINZA_ELA, perda)
    ela(dc, XE, CHAO - 6, cena, braco=0.6, lado=1, cabeca_baixa=0.5 * perda, t=t, emo=dict(triste=0.8 * perda, sorriso=0.4 * (1 - perda)))
    personagens.DOURADO = OURO0
    big = cen.resize((int(W * K), int(H * K)), Image.BICUBIC)
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.paste(big, (int(W / 2 - CENTRO[0] * K), int(1060 - CENTRO[1] * K)))
    im = Image.alpha_composite(im, cam)
    # cartões de decisão: saem da mão dela e vão para a pilha dele
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for i, (t0, _, rot) in enumerate(PEDIDOS):
        a = ap(t, t0 - 0.2, 0.3) * cena
        if a <= 0.01: continue
        p = estilo.suavizar(cl((t - t0 - 0.9) / 0.9))
        x0, y0 = EX + 130, Y_CHAO - 330
        x1, y1 = HX + 150, Y_CHAO - 40 - i * (CH + 8)
        x = x0 + (x1 - x0) * p; y = y0 + (y1 - y0) * p - 120 * p * (1 - p)
        cor = mix(G, (150, 70, 70), p)
        d.rounded_rectangle((x - CW / 2, y - CH / 2, x + CW / 2, y + CH / 2), radius=12, fill=(24, 22, 20, int(240 * a)), outline=cor + (int(255 * a),), width=3)
        d.text((x, y), rot, font=FC, fill=B + (int(255 * a),), anchor='mm')
    im = Image.alpha_composite(im, lay)
    for t0, s, _ in PEDIDOS: im = balao(im, HX - 20, 620, s, jan(t, t0, t0 + 2.2) * cena, (236, 214, 160), (40, 30, 20), 1)
    q = 1 - ap(t, T_CENA - 0.2, 0.4)
    estilo.texto_espacado(ImageDraw.Draw(im, 'RGBA'), (W / 2, 175), 'SÉRIE  ·  EP. 2', estilo.sem_serifa(32, 600), G + (int(235 * q),), 10)
    im = texto(im, (W / 2, 270), 'Quantas decisões suas', ebg('Regular', 74), B, q)
    im = texto(im, (W / 2, 360), 'você já entregou?', ebg('Italic', 78), G, q)
    f1 = jan(t, 12.4, 16.6)
    im = texto(im, (W / 2, 800), 'Ninguém tira tudo de uma vez.', ebg('Regular', 68), B, f1)
    im = texto(im, (W / 2, 895), 'Vai pedindo uma decisão por vez.', ebg('Italic', 66), G, f1 * ap(t, 13.1))
    im = texto(im, (W / 2, 985), 'Controle coercitivo, Evan Stark, 2007', ebg('Italic', 32), C, f1 * ap(t, 13.6))
    f2 = jan(t, 16.8, 20.8)
    im = texto(im, (W / 2, 830), '“Reivindique-se para si mesmo.”', ebg('Italic', 70), B, f2)
    im = texto(im, (W / 2, 915), 'Sêneca, Cartas a Lucílio, 1.1', ebg('Italic', 34), C, f2)
    f3 = ap(t, 21.0)
    im = texto(im, (W / 2, 780), 'Quando foi a última vez', ebg('Regular', 70), B, f3)
    im = texto(im, (W / 2, 870), 'que você decidiu algo', ebg('Regular', 70), B, f3)
    im = texto(im, (W / 2, 965), 'só por você?', ebg('Italic', 78), G, f3)
    im = texto(im, (W / 2, 1130), 'Manda para quem precisa ouvir isso.', ebg('Medium', 46), G, ap(t, 22.4))
    im = texto(im, (W / 2, 1540), 'Isto não é diagnóstico. Se dói, procure apoio profissional.', estilo.sem_serifa(28, 500), C, ap(t, 22.8))
    estilo.texto_espacado(ImageDraw.Draw(im, 'RGBA'), (W / 2, 1720), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(26, 500), (170, 165, 158, 210), 6)
    return im.convert('RGB')

if capa: quadro(0.3).save(capa)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    ff.stdin.write(estilo.para_bytes(np.asarray(quadro(t), np.float32) * cl((T - t) / 0.4)))
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida)
saida.with_suffix('.mudo.mp4').unlink(missing_ok=True); print('ok', saida)
