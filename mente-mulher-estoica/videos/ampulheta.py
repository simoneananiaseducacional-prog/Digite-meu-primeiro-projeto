"""A ampulheta: a cada briga vem "Desculpa. Eu vou mudar." e ela vira a ampulheta de novo.
A areia que caiu são os anos (1, 3, 6, 10). Ela envelhece e apaga. Um dia, não vira mais: vai embora.
Base estoica na legenda: Marco Aurélio, Meditações 5.17; Epicteto, Encheirídion 1. Uso: python3 ampulheta.py saida.mp4
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia, personagens
from personagens import ela, ele
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
saida = Path(sys.argv[1])
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.4): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.3): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
def rgba(c, a): return c + (int(255 * cl(a)),)
def lerp(a, b, p): return a + (b - a) * p
def seg(t, t0, t1): return estilo.suavizar(cl((t - t0) / (t1 - t0)))
def mix(c1, c2, p): return tuple(int(lerp(c1[i], c2[i], p)) for i in range(3))

T = 28.0
CHAO = 1250
XE, XH, XA = 400, 720, 560          # ela, ele, ampulheta
HY = CHAO - 6 - 240
# ciclos: (grito, promessa, vira, anos ao fim do ciclo)
CICLOS = [(0.3, 2.4, 4.0, 1), (6.4, 7.6, 8.8, 3), (10.4, 11.4, 12.4, 6), (13.8, 14.6, 15.4, 10)]
FIM_CICLOS = 17.2
NAO_VIRA, VAI = 18.0, 20.2
FRASE = 22.4
OURO0, CAB0, CINZA0 = personagens.DOURADO, personagens.CABELO, personagens.CINZA

def anos(t):
    v = 0.0; prev = 0
    for g, p, vira, n in CICLOS:
        nxt = CICLOS[CICLOS.index((g, p, vira, n)) + 1][0] if (g, p, vira, n) != CICLOS[-1] else FIM_CICLOS
        if t >= vira: v = lerp(prev, n, seg(t, vira + 0.4, nxt))
        prev = n
    return v
def girando(t):
    for g, p, vira, n in CICLOS:
        if vira <= t <= vira + 0.6: return 180 * seg(t, vira, vira + 0.6)
    return 0.0
def areia_cima(t):
    """Fração de areia em cima no ciclo atual."""
    for i, (g, p, vira, n) in enumerate(CICLOS):
        nxt = CICLOS[i + 1][0] if i + 1 < len(CICLOS) else FIM_CICLOS
        if vira + 0.6 <= t < nxt + 1.0: return 1 - seg(t, vira + 0.6, nxt)
    return 0.0
def gritando(t): return max(jan(t, g, g + 1.6) for g, *_ in CICLOS)
def prometendo(t): return max(jan(t, p, p + (1.6 if i == 0 else 1.0)) for i, (g, p, *_) in enumerate(CICLOS))
def virando(t): return max(jan(t, v - 0.3, v + 0.9) for g, p, v, n in CICLOS)

def ampulheta(d, x, ybase, a, ang, cima, baixo):
    h, w = 150, 70
    cx, cy = x, ybase - h / 2 - 10
    r = math.radians(ang)
    def R(px, py): return (cx + px * math.cos(r) - py * math.sin(r), cy + px * math.sin(r) + py * math.cos(r))
    # mesinha
    d.line([(x - 70, ybase), (x + 70, ybase)], fill=rgba(C, a), width=4)
    for sx in (-55, 55): d.line([(x + sx, ybase), (x + sx, CHAO)], fill=rgba(C, a), width=4)
    if ang < 1:
        # areia de cima (triângulo que diminui) e de baixo (monte que cresce)
        if cima > 0.02:
            hh = 60 * cima
            d.polygon([R(-w / 2 * cima - 4, -8 - hh), R(w / 2 * cima + 4, -8 - hh), R(0, -6)], fill=rgba(G, a))
        if baixo > 0.02:
            hb = 62 * baixo
            d.polygon([R(-w / 2 + 6, h / 2 - 8), R(w / 2 - 6, h / 2 - 8), R(0, h / 2 - 8 - hb)], fill=rgba(G, a))
        if cima > 0.02: d.line([R(0, -6), R(0, h / 2 - 8)], fill=rgba(G, a * 0.8), width=2)
    vid = [R(-w / 2, -h / 2), R(w / 2, -h / 2), R(4, -4), R(w / 2, h / 2), R(-w / 2, h / 2), R(-4, -4)]
    d.line(vid + [vid[0]], fill=rgba(B, a), width=4, joint='curve')
    for yy in (-h / 2, h / 2): d.line([R(-w / 2 - 12, yy), R(w / 2 + 12, yy)], fill=rgba(B, a), width=7)

def balao(d, alvo, centro, linhas, a):
    if a <= 0.02: return
    f = estilo.sem_serifa(40, 700)
    larg = max(d.textlength(l, font=f) for l in linhas) + 70; alt = 54 * len(linhas) + 40
    x0, y0 = centro[0] - larg / 2, centro[1] - alt / 2
    d.rounded_rectangle((x0, y0, x0 + larg, y0 + alt), radius=30, fill=(16, 16, 16, int(240 * a)), outline=rgba(C, a), width=3)
    bx = max(x0 + 40, min(x0 + larg - 40, alvo[0])); base = y0 + alt
    d.polygon([(bx - 15, base - 2), (bx + 15, base - 2), alvo], fill=(16, 16, 16, int(240 * a)))
    d.line([(bx - 15, base), alvo, (bx + 15, base)], fill=rgba(C, a), width=3)
    for i, l in enumerate(linhas): d.text((centro[0], y0 + 46 + i * 54), l, font=f, fill=rgba(B, a), anchor='mm')

fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
FT = estilo.sem_serifa(54, 500); TXT = (205, 200, 194)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    a = ap(t, 0.05, 0.4)
    cena = a * (1 - 0.92 * ap(t, FRASE - 0.2, 0.6))
    cen = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(cen, 'RGBA')
    d.line([(0, CHAO), (W, CHAO)], fill=rgba(C, cena), width=4)
    # envelhecer e apagar; ao ir embora o dourado volta
    idade = cl(anos(t) / 10)
    volta = seg(t, VAI, VAI + 1.6)
    personagens.CABELO = mix(CAB0, (150, 150, 150), 0.75 * idade)
    personagens.DOURADO = mix(mix(OURO0, (95, 85, 65), 0.65 * idade), OURO0, volta)
    xe = lerp(XE, 290, seg(t, VAI + 0.2, VAI + 1.8))
    g_ = gritando(t); p_ = prometendo(t); v_ = virando(t)
    emo_ela = dict(triste=0.85 * max(g_, 0.5 * idade * (1 - volta)), sorriso=0.6 * p_ * (1 - 0.7 * idade) + 0.8 * volta, aberta=0.3 * g_)
    ela(d, xe, CHAO - 6, cena, braco=0.95 * v_, lado=1 if t < VAI else -1, cabeca_baixa=max(0.4 * idade * (1 - volta), 0.7 * jan(t, NAO_VIRA, VAI, 0.4)), t=t, emo=emo_ela)
    personagens.DOURADO = OURO0
    emo_ele = dict(raiva=g_, aberta=g_ * (0.6 + 0.4 * abs(math.sin(t * 9))), triste=0.6 * p_)
    ele(d, XH + 14 * g_, CHAO - 6, cena, braco=0.6 * g_, lado=-1, cabeca_baixa=0.3 * p_, t=t, emo=emo_ele)
    if g_ > 0.05:                                   # linhas do grito
        hx, hy = XH - 50, HY + 10
        for j in range(3):
            ang = math.radians(165 + j * 15)
            d.line([(hx + 20 * math.cos(ang), hy + 20 * math.sin(ang)), (hx + 55 * math.cos(ang), hy + 55 * math.sin(ang))], fill=rgba(B, cena * g_), width=4)
    personagens.CABELO = CAB0
    baixo = cl(anos(t) / 10) * 0.95 + 0.05 * (t > CICLOS[0][2] + 0.6)
    ampulheta(d, XA, CHAO - 110, cena, girando(t), areia_cima(t), baixo)
    # contador de anos
    n = anos(t)
    if n > 0.05:
        rotulo = f'{max(1, round(n))} ano' + ('s' if round(n) > 1 else '')
        d.text((XA, CHAO - 330), rotulo, font=estilo.sem_serifa(46, 700), fill=rgba(G, cena), anchor='mm')
    nao = jan(t, NAO_VIRA, VAI + 0.4)
    balao(d, (XH - 20, HY - 40), (XH - 30, HY - 180), ['Desculpa.', 'Eu vou mudar.'], cena * p_)
    # câmera: plano geral com close nela na hora de não virar
    K = lerp(1.5, 2.4, jan(t, NAO_VIRA - 0.3, VAI + 0.2, 0.5)); CX = lerp(560, XE + 60, jan(t, NAO_VIRA - 0.3, VAI + 0.2, 0.5)); CY = lerp(1110, HY + 40, jan(t, NAO_VIRA - 0.3, VAI + 0.2, 0.5))
    big = cen.resize((int(W * K), int(H * K)), Image.BICUBIC)
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.paste(big, (int(W / 2 - CX * K), int(H * 0.58 - CY * K)))
    im = Image.alpha_composite(fundo, cam); d2 = ImageDraw.Draw(im, 'RGBA')
    f1 = jan(t, FRASE, 26.4, 0.4); f2 = jan(t, FRASE + 1.2, 26.4, 0.4)
    if f1 > 0.02:
        d2.text((W/2, 640), 'Esperar alguém mudar', font=FT, fill=rgba(TXT, f1), anchor='mm')
        d2.text((W/2, 720), 'não é esperança.', font=FT, fill=rgba(TXT, f1), anchor='mm')
    if f2 > 0.02:
        d2.text((W/2, 850), 'É tempo que não volta.', font=estilo.playfair(64, True), fill=rgba(G, f2), anchor='mm')
    ia = ap(t, 26.4, 0.4)
    if ia > 0.02:
        s_ = 70; yy = 820
        d2.rounded_rectangle((W/2 - s_, yy - s_, W/2 + s_, yy + s_), radius=40, outline=rgba(B, ia), width=10)
        d2.ellipse((W/2 - 34, yy - 34, W/2 + 34, yy + 34), outline=rgba(B, ia), width=10)
        d2.ellipse((W/2 + 36, yy - 50, W/2 + 50, yy - 36), fill=rgba(B, ia))
        d2.text((W/2, yy + 140), '@mente_mulher_estoica', font=estilo.sem_serifa(46, 600), fill=rgba(B, ia), anchor='mm')
    ff.stdin.write(estilo.para_bytes(np.asarray(im.convert('RGB'), np.float32) * (1 - ap(t, T - 0.3, 0.3))))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida)
print('ok', saida)
