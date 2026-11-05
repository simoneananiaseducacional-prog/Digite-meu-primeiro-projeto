"""Mapas da mente: as palavras convergem num ponto e seguem para "mente."
Desenho de convergência (as linhas se juntam), diferente do leque do vídeo da energia.
Uso: python3 diagrama_interpretacao.py saida.mp4  (vídeo mudo; a música entra no Instagram)
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
saida = Path(sys.argv[1])
fundo = np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def mix(a, b, p): return tuple(int(a[i] + (b[i] - a[i]) * p) for i in range(3))
PONTO = (600, 940)
PALAVRAS = ['A maioria', 'dos seus', 'problemas', 'pode ser', 'uma falsa', 'interpretação', 'da sua']
X_FIM = 380                       # onde termina cada palavra (alinhada à direita)
YS = [740 + i * 67 for i in range(7)]
T0, PASSO = 2.4, 0.6              # entra uma palavra a cada 0,6 s
T_SETA = T0 + 7 * PASSO + 0.3     # seta para "mente."
T_OURO = T_SETA + 1.0             # as linhas acendem em dourado
T = 17.0
def txt(d, xy, s, f, cor, a, anc='mm'):
    if a > 0.01: d.text(xy, s, font=f, fill=cor + (int(255 * min(a, 1)),), anchor=anc)
f_pal = estilo.serifa(44, 600)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    img = Image.fromarray(fundo).convert('RGBA'); cam = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
    if ap(t, 0.1) > 0:
        estilo.texto_espacado(d, (W/2, 400), 'MAPAS DA MENTE', estilo.sem_serifa(24, 500), C + (int(200 * ap(t, 0.1)),), 8)
    txt(d, (W/2, 480), 'De onde vêm', estilo.serifa(68, 600), B, ap(t, 0.3))
    txt(d, (W/2, 565), 'os seus problemas?', estilo.serifa_italica(74, 600), G, ap(t, 0.9))
    ouro = ap(t, T_OURO, 0.9)
    cor_linha = mix(C, G, ouro)
    for i, (p, y) in enumerate(zip(PALAVRAS, YS)):
        t0 = T0 + i * PASSO
        a = ap(t, t0, 0.35)
        txt(d, (X_FIM, y), p, f_pal, B, a, 'rm')
        q = min(1, max(0, (t - t0 - 0.15) / 0.45))
        if q > 0:
            x0, y0 = X_FIM + 18, y
            x1 = x0 + (PONTO[0] - x0) * q; y1 = y0 + (PONTO[1] - y0) * q
            d.line((x0, y0, x1, y1), fill=cor_linha + (int(220 * q),), width=3)
    a_p = ap(t, T0 + 0.3, 0.4)
    if a_p > 0:
        r = 11 + 5 * ouro
        d.ellipse((PONTO[0] - r, PONTO[1] - r, PONTO[0] + r, PONTO[1] + r), fill=mix(B, G, ouro) + (int(255 * a_p),))
    s = min(1, max(0, (t - T_SETA) / 0.5))
    if s > 0:
        xa, xb = PONTO[0] + 22, 790
        x = xa + (xb - xa) * s
        d.line((xa, PONTO[1], x, PONTO[1]), fill=B + (230,), width=3)
        if s > 0.98:
            for sg in (-1, 1):
                d.line((x, PONTO[1], x - 18, PONTO[1] + sg * 10), fill=B + (230,), width=3)
    txt(d, (810, PONTO[1]), 'mente.', estilo.serifa_italica(60, 700), G, ap(t, T_SETA + 0.5), 'lm')
    txt(d, (W/2, 1230), '“Não são as coisas que nos perturbam,', estilo.serifa_italica(46, 600), B, ap(t, 9.4, 0.7))
    txt(d, (W/2, 1292), 'mas o juízo que fazemos delas.”', estilo.serifa_italica(46, 600), B, ap(t, 10.0, 0.7))
    txt(d, (W/2, 1360), 'Epicteto, Encheirídion, 5', estilo.serifa_italica(32, 500), C, ap(t, 10.7))
    if ap(t, 11.4) > 0:
        estilo.texto_espacado(d, (W/2, 1430), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(22, 500), C + (int(255 * ap(t, 11.4)),), 6)
    img = Image.alpha_composite(img, cam)
    q = np.asarray(img.convert('RGB'), np.float32) * (1 - ap(t, T - 0.6, 0.6))
    ff.stdin.write(estilo.para_bytes(q))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); saida.with_suffix('.mudo.mp4').unlink(missing_ok=True)
print('ok')
