import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
VERM = (190, 60, 60)
saida = Path(sys.argv[1])
fundo = np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)
def ap(t, t0, d=0.6): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
O = (150, 1000)   # você
N = (440, 1000)   # alguém difícil
# alvo, rótulo, explicação, cor, quando entra
ramos = [((640, 850), 'Sem preparo.', 'surpresa, depois explosão', VERM, 4.6),
         ((640, 1150), 'Com preparo.', 'você já esperava', G, 7.0)]
T_APAGA = 9.6
T = 21.0
def seta(d, a, b, p, cor, a8):
    x = a[0] + (b[0] - a[0]) * p; y = a[1] + (b[1] - a[1]) * p
    d.line((a[0], a[1], x, y), fill=cor + (a8,), width=4)
    if p > 0.98:
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        for s in (-1, 1):
            d.line((x, y, x - 22 * math.cos(ang + s * 0.45), y - 22 * math.sin(ang + s * 0.45)), fill=cor + (a8,), width=4)
def txt(d, xy, s, f, cor, a, anc='mm'):
    if a > 0.01: d.text(xy, s, font=f, fill=cor + (int(255 * min(a, 1)),), anchor=anc)
def ponto(d, xy, cor, a):
    if a > 0: d.ellipse((xy[0] - 12, xy[1] - 12, xy[0] + 12, xy[1] + 12), fill=cor + (int(255 * a),))
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    img = Image.fromarray(fundo).convert('RGBA'); cam = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
    # gancho visível já no primeiro quadro
    txt(d, (W/2, 500), 'Você vai encontrar', estilo.serifa(70, 600), B, 1)
    txt(d, (W/2, 585), 'alguém difícil hoje.', estilo.serifa(70, 600), B, 1)
    txt(d, (W/2, 680), 'Já se prepare.', estilo.serifa_italica(78, 600), G, ap(t, 0.8))
    a0 = ap(t, 2.0, 0.4)
    ponto(d, O, B, a0); txt(d, (O[0], O[1] - 48), 'Você', estilo.sem_serifa(34, 600), B, a0)
    p = min(1, max(0, (t - 2.8) / 0.7))
    if p > 0: seta(d, (O[0] + 20, O[1]), (N[0] - 20, N[1]), p, C, 230)
    an = ap(t, 3.5, 0.4)
    ponto(d, N, VERM, an); txt(d, (N[0], N[1] - 48), 'Alguém difícil', estilo.sem_serifa(34, 600), B, an)
    for alvo, rot, sub, cor, t0 in ramos:
        apaga = 1 - 0.75 * ap(t, T_APAGA, 0.8) if cor == VERM else 1
        p = min(1, max(0, (t - t0) / 0.7))
        if p > 0: seta(d, (N[0] + 20, N[1]), (alvo[0] - 20, alvo[1]), p, cor, int(230 * apaga))
        txt(d, (alvo[0] + 10, alvo[1] - 8), rot, estilo.serifa(50, 700), B, ap(t, t0 + 0.6) * apaga, 'ls')
        txt(d, (alvo[0] + 10, alvo[1] + 34), sub, estilo.serifa_italica(34, 500), C, ap(t, t0 + 0.8) * apaga, 'ls')
    f_c = estilo.serifa_italica(48, 700)
    txt(d, (W/2, 1270), '“Ao amanhecer, diga a si mesmo:', f_c, G, ap(t, 10.6, 0.8))
    txt(d, (W/2, 1335), 'hoje vou encontrar gente ingrata,', f_c, G, ap(t, 11.2, 0.8))
    txt(d, (W/2, 1400), 'arrogante e invejosa.”', f_c, G, ap(t, 11.8, 0.8))
    txt(d, (W/2, 1462), 'Marco Aurélio, Meditações II, 1', estilo.serifa_italica(32, 500), C, ap(t, 12.5))
    txt(d, (W/2, 1550), 'Quem espera não se surpreende.', estilo.serifa(44, 600), B, ap(t, 14.6))
    txt(d, (W/2, 1610), 'Quem se prepara não precisa reagir no impulso.', estilo.serifa(40, 600), B, ap(t, 15.8))
    if ap(t, 17.4) > 0:
        estilo.texto_espacado(d, (W/2, 1690), 'SALVA PARA VER DE MANHÃ', estilo.sem_serifa(26, 600), G + (int(255 * ap(t, 17.4)),), 5)
        estilo.texto_espacado(d, (W/2, 1738), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(24, 500), C + (int(255 * ap(t, 17.4)),), 6)
    img = Image.alpha_composite(img, cam)
    q = np.asarray(img.convert('RGB'), np.float32) * (1 - ap(t, T - 0.6, 0.6))
    ff.stdin.write(estilo.para_bytes(q))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); saida.with_suffix('.mudo.mp4').unlink(missing_ok=True)
print('ok')
