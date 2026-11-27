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
O = (230, 1000)
# alvo, rótulo, explicação, cor, quando entra
ramos = [((620, 790), 'Reviver o passado.', 'o que já não muda', VERM, 2.8),
         ((620, 1210), 'Temer o futuro.', 'o que ainda não aconteceu', VERM, 4.4),
         ((620, 1000), 'Viver o agora.', 'o único tempo que é seu', G, 6.4)]
T_APAGA = 8.4   # os caminhos vermelhos esmaecem e só o dourado fica
T = 16.0
def seta(d, a, b, p, cor, a8):
    x = a[0] + (b[0] - a[0]) * p; y = a[1] + (b[1] - a[1]) * p
    d.line((a[0], a[1], x, y), fill=cor + (a8,), width=4)
    if p > 0.98:
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        for s in (-1, 1):
            d.line((x, y, x - 22 * math.cos(ang + s * 0.45), y - 22 * math.sin(ang + s * 0.45)), fill=cor + (a8,), width=4)
def txt(d, xy, s, f, cor, a, anc='mm'):
    if a > 0.01: d.text(xy, s, font=f, fill=cor + (int(255 * min(a, 1)),), anchor=anc)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    img = Image.fromarray(fundo).convert('RGBA'); cam = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
    txt(d, (W/2, 540), 'Para onde vai', estilo.serifa(70, 600), B, ap(t, 0.2))
    txt(d, (W/2, 630), 'a sua energia?', estilo.serifa_italica(78, 600), G, ap(t, 0.9))
    a0 = ap(t, 2.0, 0.4)
    for alvo, rot, sub, cor, t0 in ramos:
        apaga = 1 - 0.75 * ap(t, T_APAGA, 0.8) if cor == VERM else 1
        p = min(1, max(0, (t - t0) / 0.7))
        if p > 0: seta(d, (O[0] + 20, O[1]), (alvo[0] - 20, alvo[1]), p, cor, int(230 * apaga))
        txt(d, (alvo[0] + 10, alvo[1] - 8), rot, estilo.serifa(52, 700), B, ap(t, t0 + 0.6) * apaga, 'ls')
        txt(d, (alvo[0] + 10, alvo[1] + 34), sub, estilo.serifa_italica(36, 500), C, ap(t, t0 + 0.8) * apaga, 'ls')
    if a0 > 0:
        d.ellipse((O[0] - 12, O[1] - 12, O[0] + 12, O[1] + 12), fill=B + (int(255 * a0),))
        txt(d, (O[0], O[1] - 48), 'Você', estilo.sem_serifa(34, 600), B, a0)
    txt(d, (W/2, 1400), '“Não recebemos uma vida curta.', estilo.serifa_italica(54, 700), G, ap(t, 9.6, 0.8))
    txt(d, (W/2, 1470), 'Nós a tornamos curta.”', estilo.serifa_italica(54, 700), G, ap(t, 10.4, 0.8))
    txt(d, (W/2, 1540), 'Sêneca, Sobre a brevidade da vida, 1', estilo.serifa_italica(32, 500), C, ap(t, 11.2))
    if ap(t, 12.0) > 0:
        estilo.texto_espacado(d, (W/2, 1620), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(24, 500), C + (int(255 * ap(t, 12.0)),), 6)
    img = Image.alpha_composite(img, cam)
    q = np.asarray(img.convert('RGB'), np.float32) * (1 - ap(t, T - 0.6, 0.6))
    ff.stdin.write(estilo.para_bytes(q))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); saida.with_suffix('.mudo.mp4').unlink(missing_ok=True)
print('ok')
