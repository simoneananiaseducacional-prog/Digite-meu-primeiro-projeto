"""Razão e emoção: uma mensagem chega ("A gente precisa conversar."); a emoção se assusta, a razão não a cala,
escuta o medo, e a resposta muda. Versão no padrão da página (fundo preto, traço) do mapa feito em outra conversa.
Uso: python3 razao_emocao.py saida.mp4
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
W, H, FPS, T = 1080, 1920, 30, 25.0
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
TX = (215, 210, 202); PRATA = (175, 178, 188)
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.4): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
def rgba(c, a): return c + (int(255 * cl(a)),)
def lerp(a, b, p): return a + (b - a) * p
def mix(a, b, p): return tuple(int(lerp(a[i], b[i], p)) for i in range(3))

CY, R = 1080, 105
FALAS = [  # (quem, linhas, início, fim)
    ('E', ['Fiz algo errado…'], 4.4, 7.4),
    ('R', ['Calma. Isso é', 'suposição, não fato.'], 7.4, 10.6),
    ('E', ['Mas eu senti medo.'], 10.6, 13.2),
    ('R', ['Então vamos', 'entender esse medo.'], 13.2, 15.8),
]
FB = estilo.sem_serifa(40, 600)

def rosto(d, x, y, cor, a, medo=0.0, calma=0.0, sorriso=0.0):
    d.ellipse((x - R, y - R, x + R, y + R), fill=(26, 25, 24, int(255 * a)), outline=rgba(cor, a), width=6)
    for s in (-1, 1):
        ex = x + s * 36
        d.line([(ex - 20, y - 40 - 10 * medo - s * 8 * medo), (ex + 20, y - 40 - 10 * medo + s * 8 * medo)], fill=rgba(cor, a), width=5)
        if calma > 0.5:
            d.arc((ex - 17, y - 22, ex + 17, y + 6), 200, 340, fill=rgba(cor, a), width=5)
        else:
            r = 8 + 6 * medo
            d.ellipse((ex - r, y - 10 - r, ex + r, y - 10 + r), outline=rgba(cor, a), width=4)
            d.ellipse((ex - 5, y - 15, ex + 5, y - 5), fill=rgba(cor, a))
    if medo > 0.4 and calma < 0.5:
        d.ellipse((x - 14, y + 34, x + 14, y + 62), outline=rgba(cor, a), width=5)
    else:
        c = max(sorriso, calma) * 0.9
        pts = [(x + u, y + 46 + 16 * c * (1 - (u / 34) ** 2) - 6 * c) for u in range(-34, 35, 4)]
        d.line(pts, fill=rgba(cor, a), width=5, joint='curve')

def celular(d, a, linhas, enviada, t):
    if a < 0.02: return
    tremor = 6 * math.sin(t * 60) * (1 - ap(t, 1.6, 0.4)) if not enviada else 0
    x, y = W / 2 + tremor, CY
    d.rounded_rectangle((x - 170, y - 300, x + 170, y + 300), radius=36, fill=(22, 22, 24, int(255 * a)), outline=rgba(G, a), width=5)
    d.line([(x - 40, y - 272), (x + 40, y - 272)], fill=rgba(G, a * 0.7), width=5)
    d.text((x, y - 210), 'MENSAGENS', font=estilo.sem_serifa(24, 600), fill=rgba(C, a), anchor='mm')
    cor = (232, 214, 170) if enviada else (210, 210, 214)
    d.rounded_rectangle((x - 158, y - 70, x + 158, y + 70), radius=24, fill=rgba(cor, a))
    for i, l in enumerate(linhas):
        d.text((x, y - 18 + i * 40), l, font=estilo.sem_serifa(30, 600), fill=(24, 22, 20, int(255 * a)), anchor='mm')
    d.text((x, y + 110), 'Enviada' if enviada else 'agora', font=estilo.sem_serifa(24, 500), fill=rgba(C, a), anchor='mm')
    if not enviada:   # ondas de vibração
        for k in (1, 2):
            v = a * (1 - ap(t, 1.8, 0.5)) * (0.5 + 0.5 * math.sin(t * 9 + k))
            d.arc((x - 190 - 22 * k, y - 120, x - 150 - 22 * k, y + 120), 120, 240, fill=rgba(G, v), width=4)
            d.arc((x + 150 + 22 * k, y - 120, x + 190 + 22 * k, y + 120), 300, 60, fill=rgba(G, v), width=4)

def balao(d, x, y, linhas, a, lado):
    if a < 0.02: return
    w = max(FB.getlength(l) for l in linhas) + 60; h = 56 * len(linhas) + 34
    x0 = min(max(x - w / 2, 40), W - 40 - w)
    d.rounded_rectangle((x0, y - h, x0 + w, y), radius=34, fill=(236, 232, 224, int(245 * a)))
    d.polygon([(x - 18, y - 2), (x + 18, y - 2), (x + 6 * lado, y + 34)], fill=(236, 232, 224, int(245 * a)))
    for i, l in enumerate(linhas):
        d.text((x0 + w / 2, y - h + 45 + i * 56), l, font=FB, fill=(24, 22, 20, int(255 * a)), anchor='mm')

fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
FQ = estilo.playfair(60); FQ2 = estilo.playfair(60, True)
saida = Path(sys.argv[1]); ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    im = fundo.copy()
    cena = jan(t, 4.0, 15.9, 0.5)
    une = ap(t, 13.4, 1.6)
    if une > 0.02 and cena > 0.02:
        gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl)
        gd.ellipse((W / 2 - 360, CY - 260, W / 2 + 360, CY + 260), fill=G + (int(60 * une * cena),))
        im = Image.alpha_composite(im, gl.filter(ImageFilter.GaussianBlur(80)))
    d = ImageDraw.Draw(im, 'RGBA')
    # 1. a mensagem chega (visível desde o quadro zero)
    celular(d, 1 - ap(t, 3.6, 0.4), ['A gente precisa', 'conversar.'], False, t)
    # 2 a 4. emoção e razão
    if cena > 0.02:
        xe, xr = lerp(300, 370, une), lerp(780, 710, une)
        medo = ap(t, 4.4, 0.4) * (1 - ap(t, 13.6, 1.2))
        tremor = 5 * math.sin(t * 30) * medo
        # fio entre as duas: tenso e cinza, depois calmo e dourado
        pts = []
        for i in range(31):
            u = i / 30
            amp = (14 * (1 - une) + 2) * math.sin(u * math.pi)
            pts.append((lerp(xe + R + 8, xr - R - 8, u), CY + amp * math.sin(u * 14 + t * 8)))
        d.line(pts, fill=rgba(mix((120, 120, 128), G, une), cena), width=4, joint='curve')
        rosto(d, xe + tremor, CY, G, cena, medo=medo, calma=ap(t, 14.2, 0.8))
        rosto(d, xr, CY, PRATA, cena, sorriso=0.4 + 0.5 * une)
        f = estilo.sem_serifa(34, 600)
        estilo.texto_espacado(d, (xe, CY + R + 60), 'EMOÇÃO', f, rgba(G, cena), 5)
        estilo.texto_espacado(d, (xr, CY + R + 60), 'RAZÃO', f, rgba(PRATA, cena), 5)
        for quem, linhas, t0, t1 in FALAS:
            x = xe if quem == 'E' else xr
            balao(d, x, CY - R - 40, linhas, jan(t, t0, t1, 0.3) * cena, 1 if quem == 'E' else -1)
    # 5. a resposta muda
    celular(d, jan(t, 16.0, 18.9, 0.4), ['Podemos conversar.', 'Quero entender.'], True, t)
    # textos de cima
    q = 1 - ap(t, 3.6, 0.4)
    if q > 0.02:
        d.text((W / 2, 300), 'O que você sente quando lê', font=FQ, fill=rgba(B, q), anchor='mm')
        d.text((W / 2, 390), '“A gente precisa conversar”?', font=FQ2, fill=rgba(G, q), anchor='mm')
    a5 = jan(t, 16.0, 18.9, 0.4)
    if a5 > 0.02: d.text((W / 2, 340), 'E a resposta muda.', font=FQ, fill=rgba(B, a5), anchor='mm')
    f1 = jan(t, 19.2, 24.6); f2 = jan(t, 20.6, 24.6)
    if f1 > 0.02:
        d.text((W / 2, 780), 'Equilíbrio não é', font=estilo.playfair(72), fill=rgba(B, f1), anchor='mm')
        d.text((W / 2, 870), 'calar a emoção.', font=estilo.playfair(72), fill=rgba(B, f1), anchor='mm')
    if f2 > 0.02:
        d.text((W / 2, 1000), 'É escutá-la', font=estilo.playfair(74, True), fill=rgba(G, f2), anchor='mm')
        d.text((W / 2, 1090), 'sem deixar de pensar.', font=estilo.playfair(74, True), fill=rgba(G, f2), anchor='mm')
    estilo.texto_espacado(d, (W / 2, 1640), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(24, 500), rgba((170, 165, 158), 0.8), 6)
    ff.stdin.write(estilo.para_bytes(np.asarray(im.convert('RGB'), np.float32) * (1 - ap(t, T - 0.4, 0.4))))
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); print('ok', saida)
