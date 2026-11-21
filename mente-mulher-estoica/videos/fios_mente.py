"""Fios da mente: cabeça de perfil cheia de fios embaraçados (ansiedade, e se, culpa, pressa).
Ela separa: o que depende dela vira fio dourado e reto; o que não depende, ela solta e sai da cabeça.
No espaço livre nasce um lótus. Fecho: a vida é breve (Sêneca, Brevidade 3.4) + Epicteto, Encheirídion 1.
Ideia inspirada em @_dreamscapes_sajna (desenho próprio). Uso: python3 fios_mente.py saida.mp4
"""
import sys, math, random, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
W, H, FPS, T = 1080, 1920, 30, 26.0
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
TX = (205, 200, 194)
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.5): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
def rgba(c, a): return c + (int(255 * cl(a)),)
def lerp(a, b, p): return a + (b - a) * p
def seg(t, t0, t1): return estilo.suavizar(cl((t - t0) / (t1 - t0)))

# perfil da cabeça (olhando para a direita), centro aproximado (500, 900)
def perfil():
    pts = []
    for g in range(200, 380, 4):          # nuca e topo (arco grande)
        r = math.radians(g); pts.append((520 + 300 * math.cos(r), 880 + 330 * math.sin(r)))
    pts += [(800, 820), (840, 900), (880, 960), (850, 980), (860, 1020), (845, 1060), (850, 1095),
            (820, 1140), (760, 1170), (700, 1180), (690, 1300), (670, 1420)]
    pts += [(380, 1420), (370, 1250), (300, 1150), (240, 1000)]
    return pts
CAB = perfil()
CX, CY, R = 520, 880, 250
random.seed(9)
def ponto_dentro():
    while True:
        x, y = random.uniform(CX - R, CX + R), random.uniform(CY - R * 0.9, CY + R * 0.9)
        if (x - CX) ** 2 + ((y - CY) / 0.95) ** 2 < R * R: return x, y
FIOS = []
for i in range(26):
    pts = [ponto_dentro() for _ in range(5)]
    meu = i % 4 == 0
    FIOS.append((pts, meu, random.uniform(0, 6.28)))
PALAVRAS = [('ansiedade', 430, 760), ('e se…', 610, 820), ('culpa', 400, 960), ('pressa', 600, 1010), ('o que vão pensar', 500, 880)]

def curva(pts, n=40):
    out = []
    for k in range(n + 1):
        u = k / n * (len(pts) - 1); i = min(int(u), len(pts) - 2); f = u - i
        out.append((lerp(pts[i][0], pts[i + 1][0], f), lerp(pts[i][1], pts[i + 1][1], f)))
    return out

def lotus(d, x, y, s, a):
    if s < 0.02: return
    for ang, sc in [(-60, 0.8), (-30, 0.95), (0, 1.1), (30, 0.95), (60, 0.8)]:
        r = math.radians(ang - 90); L = 110 * s * sc; w = 34 * s * sc
        tip = (x + L * math.cos(r), y + L * math.sin(r))
        n = (math.cos(r + math.pi / 2), math.sin(r + math.pi / 2))
        mid = (x + 0.5 * L * math.cos(r), y + 0.5 * L * math.sin(r))
        d.polygon([(x, y), (mid[0] + w * n[0], mid[1] + w * n[1]), tip, (mid[0] - w * n[0], mid[1] - w * n[1])],
                  fill=G + (int(170 * a),), outline=rgba((240, 210, 150), a))
    d.line([(x - 90 * s, y + 6), (x + 90 * s, y + 6)], fill=rgba(G, a), width=3)

fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
FT = estilo.sem_serifa(54, 500)
T_SEP, T_SOLTA, T_LOTUS, T_FIM = 6.0, 8.5, 13.0, 17.0
saida = Path(sys.argv[1]); ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    a = ap(t, 0.05, 0.6)
    cena = a * (1 - 0.85 * ap(t, T_FIM, 0.8))
    im = fundo.copy()
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay, 'RGBA')
    d.line(CAB, fill=rgba(B, cena * 0.85), width=4, joint='curve')
    sep = seg(t, T_SEP, T_SEP + 2.0)
    for i, (pts, meu, fase) in enumerate(FIOS):
        trem = 8 * (1 - sep)
        pp = [(x + trem * math.sin(t * 3 + fase + j), y + trem * math.cos(t * 2.6 + fase + j)) for j, (x, y) in enumerate(pts)]
        if meu:   # vira fio dourado reto, empilhado embaixo
            yy = 1060 + (i // 4) * 18
            reto = [(380 + j * 70, yy) for j in range(5)]
            pp = [(lerp(p[0], q[0], sep), lerp(p[1], q[1], sep)) for p, q in zip(pp, reto)]
            cor = tuple(int(lerp(C[c], G[c], sep)) for c in range(3)); aa = cena
        else:     # solta: sobe e sai da cabeça
            sai = seg(t, T_SOLTA + (i % 7) * 0.25, T_SOLTA + 2.5 + (i % 7) * 0.25)
            pp = [(x + 380 * sai + 40 * math.sin(fase), y - 700 * sai) for x, y in pp]
            cor = C; aa = cena * (1 - sai) * 0.9
        if aa > 0.02: d.line(curva(pp), fill=rgba(cor, aa), width=3, joint='curve')
    for w, x, y in PALAVRAS:
        pa = jan(t, 1.4, T_SOLTA + 0.6) * cena
        if pa > 0.02:
            d.text((x + 4 * math.sin(t * 5 + x), y), w, font=estilo.sem_serifa(30, 600), fill=rgba((220, 210, 205), pa), anchor='mm')
    ls = seg(t, T_LOTUS, T_LOTUS + 2.0)
    if ls > 0.02:
        gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl)
        gd.ellipse((CX - 220 * ls, 900 - 200 * ls, CX + 220 * ls, 900 + 200 * ls), fill=G + (int(70 * ls * cena),))
        im = Image.alpha_composite(im, gl.filter(ImageFilter.GaussianBlur(50)))
        lotus(d, CX, 980, ls, cena)
    im = Image.alpha_composite(im, lay); d2 = ImageDraw.Draw(im, 'RGBA')
    for t0, t1, s in [(0.6, 5.8, 'Quantos fios embaraçados'), (0.6, 5.8, 'você carrega hoje?'),
                      (6.2, 12.6, 'Pergunte a cada um:'), (6.2, 12.6, '“Isso depende de mim?”'),
                      (13.2, 16.8, 'Solte o resto.')]:
        fa = jan(t, t0, t1)
        if fa > 0.02:
            y = 320 if s in ('Quantos fios embaraçados', 'Pergunte a cada um:', 'Solte o resto.') else 400
            d2.text((W / 2, y), s, font=FT if '“' not in s else estilo.playfair(56, True), fill=rgba(G if '“' in s else TX, fa), anchor='mm')
    f1 = jan(t, T_FIM + 0.4, 25.6); f2 = jan(t, T_FIM + 1.8, 25.6); f3 = jan(t, T_FIM + 3.2, 25.6)
    if f1 > 0.02: d2.text((W / 2, 760), 'A vida é breve demais', font=estilo.playfair(62), fill=rgba(B, f1), anchor='mm')
    if f2 > 0.02: d2.text((W / 2, 860), 'para gastá-la', font=estilo.playfair(62), fill=rgba(B, f2), anchor='mm')
    if f3 > 0.02:
        d2.text((W / 2, 960), 'no que não depende de você.', font=estilo.playfair(62, True), fill=rgba(G, f3), anchor='mm')
        d2.text((W / 2, 1080), 'Sêneca e Epicteto', font=estilo.playfair(30, True), fill=rgba(C, f3), anchor='mm')
    sa = 0.8 * a
    estilo.texto_espacado(d2, (W / 2, 1640), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(24, 500), rgba((170, 165, 158), sa), 6)
    ff.stdin.write(estilo.para_bytes(np.asarray(im.convert('RGB'), np.float32) * (1 - ap(t, T - 0.3, 0.3))))
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); print('ok', saida)
