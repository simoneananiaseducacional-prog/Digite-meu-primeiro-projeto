"""A ponte de um só: o chão racha entre duas pessoas; uma constrói a ponte, a outra não se move.
Inspirado na ideia de @stepbychalk, com desenho próprio. Ou ação, ou texto. Uso: python3 ponte.py saida.mp4
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from personagens import ela, ele
from PIL import Image, ImageDraw
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
C2 = (170, 170, 170)
saida = Path(sys.argv[1])
fundo = np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1): return ap(t, t0) * (1 - ap(t, t1 - 0.4, 0.4))
def cl(p): return max(0.0, min(1.0, p))
def rgba(c, a): return c + (int(255 * cl(a)),)
T = 30.0
CHAO = 1250
RACHA, ABRE = 4.0, 7.5            # o chão racha e o vão se abre
def vao(t):                        # meia-largura do vão
    return 6 + 150 * estilo.suavizar(cl((t - ABRE) / 2.5)) if t > RACHA else 0
def pessoa(d, x, y, cor, a, sentado=0.0, braco=0.0, cabeca_baixa=0.0, lado=1):
    """Figura em traço. sentado 0..1; braco 0..1 estende para o lado 'lado'."""
    if a <= 0.01: return
    w = 5
    hy = y - 230 + 90 * sentado + 18 * cabeca_baixa
    hx = x + lado * 10 * cabeca_baixa
    d.ellipse((hx - 34, hy - 34, hx + 34, hy + 34), outline=rgba(cor, a), width=w)
    ex = 10 if cabeca_baixa < 0.5 else 0
    for s in (-1, 1):
        d.ellipse((hx + s * 12 - 4 + lado * ex * 0, hy - 4 + 10 * cabeca_baixa - 4, hx + s * 12 + 4, hy + 4 + 10 * cabeca_baixa), fill=rgba(cor, a))
    ombro = (x, hy + 34); quadril = (x, y - 90 + 70 * sentado)
    d.line([ombro, quadril], fill=rgba(cor, a), width=w)
    if sentado < 0.5:
        for s in (-1, 1):
            d.line([quadril, (x + s * 30, y)], fill=rgba(cor, a), width=w)
    else:   # sentado, joelhos dobrados à frente
        jo = (x + lado * 55, quadril[1] - 30)
        d.line([quadril, jo, (x + lado * 70, y)], fill=rgba(cor, a), width=w, joint='curve')
        d.line([quadril, (jo[0] - lado * 10, jo[1] + 5), (x + lado * 55, y)], fill=rgba(cor, a), width=w, joint='curve')
    mao = (x + lado * (40 + 110 * braco), hy + 70 - 20 * braco)
    d.line([(x, hy + 55), mao], fill=rgba(cor, a), width=w)
    if sentado >= 0.5:   # braços abraçando os joelhos
        d.line([(x, hy + 55), (x + lado * 60, quadril[1] - 30)], fill=rgba(cor, a), width=w)
    else:
        d.line([(x, hy + 55), (x - lado * 40, hy + 140)], fill=rgba(cor, a), width=w)
PEDRAS = [3, 2, 1, 0]                       # ordem de colocação (da borda dela para a dele)
T_PEDRA = [12.6, 14.0, 15.4, 16.8]
CAI = 22.8
F1, F2 = estilo.playfair(58), estilo.playfair(58, True)
def txt(d, y, s, f, cor, a):
    if a > 0.01: d.text((W/2, y), s, font=f, fill=rgba(cor, a), anchor='mm')
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    img = Image.fromarray(fundo).convert('RGBA'); cam = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
    fim = 1 - ap(t, T - 0.8, 0.6)
    v = vao(t)
    # chão com o vão no meio
    d.line([(60, CHAO), (540 - v, CHAO)], fill=rgba(C, 0.9 * fim), width=4)
    d.line([(540 + v, CHAO), (1020, CHAO)], fill=rgba(C, 0.9 * fim), width=4)
    if t > RACHA:
        r = cl((t - RACHA) / 0.8)
        if v < 10:   # a rachadura desce em zigue-zague
            pts = [(540 + (12 if i % 2 else -12), CHAO + i * 40 * r) for i in range(8)]
            d.line(pts, fill=rgba(C, fim), width=3)
        else:
            for s in (-1, 1):
                d.line([(540 + s * v, CHAO), (540 + s * v * 0.85, CHAO + 380)], fill=rgba(C, 0.7 * fim), width=3)
    # quem se afasta junto com a borda
    xe, xd = 540 - v - 140 if v else 470, 540 + v + 140 if v else 610
    junto = 1 - ap(t, RACHA - 0.4, 0.4)
    if junto > 0.05:   # mãos dadas no começo
        d.line([(xe + 40, CHAO - 160), (xd - 40, CHAO - 160)], fill=rgba(B, junto * fim), width=5)
    senta = ap(t, 10.0, 1.2)
    ela(d, xe, CHAO, ap(t, 0.2, 0.8) * fim, braco=ap(t, 11.6, 0.6) * (1 - ap(t, 18.2, 0.6)), lado=1, t=t)
    ele(d, xd, CHAO, ap(t, 0.2, 0.8) * fim * (1 - ap(t, 26.5, 1.0)), sentado=senta, cabeca_baixa=ap(t, 9.4, 0.8), lado=-1, t=t)
    # pedras: ela coloca, e no fim caem no vão
    for i, tp in zip(PEDRAS, T_PEDRA):
        a = ap(t, tp, 0.4)
        if a <= 0: continue
        larg = (2 * v) / 4
        x0 = 540 - v + i * larg
        queda = 0
        if t > CAI + i * 0.25: queda = 900 * cl((t - CAI - i * 0.25) / 1.2) ** 2
        y = CHAO + 6 + queda
        d.rounded_rectangle((x0 + 6, y, x0 + larg - 6, y + 26), 8, outline=rgba(G, a * fim * (1 - cl(queda / 700))), width=4)
    # textos no topo, só com a cena parada
    txt(d, 420, 'A distância', F1, B, jan(t, 0.3, 4.0)); txt(d, 500, 'nem sempre começa com uma briga.', F2, G, jan(t, 0.7, 4.0))
    txt(d, 420, 'Às vezes, um continua', F1, B, jan(t, 18.6, 22.6)); txt(d, 500, 'construindo a ponte sozinho.', F2, G, jan(t, 19.0, 22.6))
    txt(d, 400, 'Uma ponte não se sustenta', F1, B, ap(t, 25.0) * fim); txt(d, 480, 'com o esforço de um só.', F2, G, ap(t, 25.4) * fim)
    txt(d, 580, '“Algumas coisas dependem de nós; outras, não.”', estilo.playfair(36, True), C, ap(t, 26.2) * fim)
    txt(d, 630, 'Epicteto, Encheirídion, 1', estilo.playfair(28, True), C, ap(t, 26.6) * fim)
    if ap(t, 27.0) > 0:
        estilo.texto_espacado(d, (W/2, 1500), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(22, 500), rgba(C, ap(t, 27.0) * fim), 6)
    img = Image.alpha_composite(img, cam)
    ff.stdin.write(estilo.para_bytes(np.asarray(img.convert('RGB'), np.float32) * (1 - ap(t, T - 0.6, 0.6))))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); saida.with_suffix('.mudo.mp4').unlink(missing_ok=True)
print('ok')
