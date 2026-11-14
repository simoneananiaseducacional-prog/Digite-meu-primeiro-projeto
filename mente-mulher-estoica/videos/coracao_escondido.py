"""O coração escondido: o amor existe, mas ele o esconde sempre que chegam sombras (gente que atrapalha).
Ela estende a mão; dessa vez ele tem coragem: segura o coração à vista de todos e as sombras somem.
Sem texto até o fim (molde visual com rostos e cortes). Base estoica: coragem como virtude; Sêneca, Cartas 104.26 (legenda).
História inspirada num relato pessoal, anonimizada. Uso: python3 coracao_escondido.py saida.mp4
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from personagens import ela, ele
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
F = 2.4
saida = Path(sys.argv[1])
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.4): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.4): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
def rgba(c, a): return c + (int(255 * cl(a)),)
def lerp(a, b, p): return a + (b - a) * p
def seg(t, t0, t1): return estilo.suavizar(cl((t - t0) / (t1 - t0)))

class Esc:
    def __init__(self, d, f): self.d, self.f = d, f
    def _xy(self, xy):
        if isinstance(xy[0], (tuple, list)): return [(p[0] * self.f, p[1] * self.f) for p in xy]
        return [v * self.f for v in xy]
    def __getattr__(self, nome):
        orig = getattr(self.d, nome)
        def chama(xy, *args, **kw):
            for k in ('width', 'radius'):
                if k in kw: kw[k] = max(1, int(round(kw[k] * self.f)))
            return orig(self._xy(xy), *args, **kw)
        return chama

T = 26.0
CHAO = 1250
XE, XH = 420, 660
HY = CHAO - 6 - 240
# sombras que chegam: (início, fim, lado de onde vêm)
VISITAS = [(3.0, 6.2, 1), (7.4, 10.4, -1), (11.4, 14.6, 1)]
T_MAO, T_HESITA, T_CORAGEM, T_FIM = 14.8, 16.0, 17.6, 21.0
PLANOS = [(0.0, 1.3, 540, 1060), (4.4, 3.0, XE, 980),     # close nela triste
          (5.6, 1.3, 540, 1060), (12.6, 3.0, XH, 980),    # close nele hesitando
          (13.4, 1.3, 540, 1060), (16.0, 3.0, XH, 980),   # close: a decisão
          (17.4, 1.3, 540, 1060), (T_FIM, 1.3, 540, 1060)]
def plano(t):
    p = PLANOS[0]
    for q in PLANOS:
        if t >= q[0]: p = q
    return p[1] * (1 + 0.025 * (t - p[0])), p[2], p[3]

def escondido(t):
    """1 = coração atrás das costas dele."""
    v = 0.0
    for a0, a1, _ in VISITAS: v = max(v, seg(t, a0 + 0.6, a0 + 1.1) * (1 - seg(t, a1 - 0.4, a1 + 0.1)))
    return v
def sombras(t):
    """Lista de (x, alfa) das sombras visíveis."""
    out = []
    for a0, a1, lado in VISITAS:
        if a0 <= t <= a1 + 0.6:
            chega = seg(t, a0, a0 + 1.0); vai = seg(t, a1 - 0.6, a1 + 0.4)
            base = 1080 + 120 if lado > 0 else -120
            alvo = 840 if lado > 0 else 240
            x = lerp(base, alvo, chega) + (base - alvo) * vai * 0.5
            out.append((x, chega * (1 - vai), lado))
    # no fim, todas aparecem juntas e depois somem diante da coragem
    fa = seg(t, T_HESITA - 0.4, T_HESITA + 0.6) * (1 - seg(t, T_CORAGEM + 0.6, T_CORAGEM + 2.0))
    if fa > 0.01:
        for x, l in ((230, -1), (850, 1), (160, -1)): out.append((x, fa, l))
    return out
def sombra(d, x, a, lado, t):
    if a < 0.02: return
    cor = (125, 125, 132)
    hy = HY + 6
    d.ellipse((x - 34, hy - 34, x + 34, hy + 34), fill=(45, 45, 50, int(235 * a)), outline=rgba(cor, a), width=4)
    d.line([(x, hy + 34), (x, CHAO - 96)], fill=rgba(cor, a), width=5)
    for s_ in (-1, 1): d.line([(x, CHAO - 96), (x + s_ * 28, CHAO - 6)], fill=rgba(cor, a), width=5)
    # braço apontando para o casal
    alvo = 540
    d.line([(x, hy + 60), (x + (alvo - x) * 0.22, hy + 46 + 4 * math.sin(t * 9))], fill=rgba(cor, a), width=5)
    for s_ in (-1, 1): d.line([(x + s_ * 12 - 5, hy - 3), (x + s_ * 12 + 5, hy - 3)], fill=rgba(cor, a), width=4)

def coracao(d, cx, cy, s, a, brilho=1.0):
    if a < 0.02: return
    r = 18 * s
    for k in (-1, 1): d.ellipse((cx + k * r - r, cy - r, cx + k * r + r, cy + r), fill=rgba(G, a))
    d.polygon([(cx - 2 * r + 1, cy + 4), (cx + 2 * r - 1, cy + 4), (cx, cy + 2.6 * r)], fill=rgba(G, a))

GLOW = None
fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
FT = estilo.sem_serifa(54, 500); TXT = (200, 196, 190)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    a = ap(t, 0.1, 0.5)
    cena = a * (1 - 0.8 * ap(t, T_FIM, 0.8))
    big = Image.new('RGBA', (int(W * F), int(H * F)), (0, 0, 0, 0)); d = Esc(ImageDraw.Draw(big, 'RGBA'), F)
    d.line([(0, CHAO), (W, CHAO)], fill=rgba(C, cena), width=4)
    for x, sa, lado in sombras(t): sombra(d, x, sa * cena, lado, t)
    esc = escondido(t)
    coragem = seg(t, T_CORAGEM, T_CORAGEM + 1.0)
    xh = lerp(XH, 600, coragem)
    # posição do coração: entre os dois / atrás das costas dele / erguido na mão dele
    meio = ((XE + XH) / 2, HY + 40)
    costas = (XH + 40, HY + 120)
    erguido = (xh - 70, HY - 40)
    cx, cy = lerp(meio[0], costas[0], esc), lerp(meio[1], costas[1], esc)
    cx, cy = lerp(cx, erguido[0], coragem), lerp(cy, erguido[1], coragem)
    s = 1.0 + 0.25 * coragem + 0.05 * math.sin(t * 4)
    vis = 1 - 0.55 * esc
    # emoções
    vis_som = max([sa for _, sa, _ in sombras(t)] + [0])
    emo_ela = dict(sorriso=0.8 * (1 - esc) * (1 - seg(t, T_HESITA, T_HESITA + 0.3)) + 0.9 * coragem,
                   triste=0.8 * max(esc, seg(t, T_HESITA, T_HESITA + 0.5) * (1 - coragem)))
    emo_ele = dict(sorriso=0.8 * (1 - esc) * (1 - seg(t, T_HESITA - 0.4, T_HESITA)) + 0.9 * coragem,
                   triste=0.6 * max(esc * 0.5, seg(t, T_HESITA, T_HESITA + 0.5) * (1 - coragem)),
                   raiva=0.0)
    mao_ela = seg(t, T_MAO, T_MAO + 0.6) * (1 - 0.3 * coragem)
    ela(d, XE, CHAO - 6, cena, braco=max(0.2, mao_ela), lado=1, cabeca_baixa=0.4 * esc * (1 - coragem), t=t, emo=emo_ela)
    olha_lado = math.sin(t * 6) * 0.4 * seg(t, T_HESITA, T_HESITA + 0.4) * (1 - seg(t, T_CORAGEM - 0.4, T_CORAGEM))
    ele(d, xh + 6 * olha_lado * 4, CHAO - 6, cena, braco=0.25 + 0.75 * coragem, lado=-1,
        cabeca_baixa=0.5 * esc * (1 - coragem), t=t, emo=emo_ele)
    coracao(d, cx, cy, s, cena * vis)
    # brilho do coração (mais forte quando à vista)
    K, ccx, ccy = plano(t)
    w, h = W / K * F, H / K * F
    x0 = max(0, min(big.width - w, ccx * F - w / 2)); y0 = max(0, min(big.height - h, ccy * F - h / 2))
    glow = Image.new('RGBA', big.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    gr = (90 + 120 * coragem) * F
    gd.ellipse((cx * F - gr, cy * F - gr, cx * F + gr, cy * F + gr), fill=G + (int(70 * cena * vis * (0.5 + 0.5 * coragem)),))
    region = (int(x0), int(y0), int(x0 + w), int(y0 + h))
    glow_c = glow.crop(region).resize((W, H), Image.BILINEAR).filter(ImageFilter.GaussianBlur(40))
    cam = big.crop(region).resize((W, H), Image.LANCZOS)
    im = Image.alpha_composite(fundo, glow_c); im = Image.alpha_composite(im, cam)
    d2 = ImageDraw.Draw(im, 'RGBA')
    f1 = jan(t, T_FIM + 0.3, 24.4); f2 = jan(t, T_FIM + 1.6, 24.4)
    if f1 > 0.02:
        for i, l in enumerate(['Não foi falta de amor.', 'Foi falta de coragem']):
            d2.text((W/2, 560 + i * 76), l, font=FT, fill=rgba(TXT, f1), anchor='mm')
        d2.text((W/2, 712), 'para viver esse amor.', font=FT, fill=rgba(TXT, f1), anchor='mm')
    if f2 > 0.02:
        d2.text((W/2, 860), 'Dessa vez, ele escolheu ter coragem.', font=estilo.playfair(50, True), fill=rgba(G, f2), anchor='mm')
    ia = ap(t, 24.4, 0.5)
    if ia > 0.02:
        s_ = 70; yy = 860
        d2.rounded_rectangle((W/2 - s_, yy - s_, W/2 + s_, yy + s_), radius=40, outline=rgba(B, ia), width=10)
        d2.ellipse((W/2 - 34, yy - 34, W/2 + 34, yy + 34), outline=rgba(B, ia), width=10)
        d2.ellipse((W/2 + 36, yy - 50, W/2 + 50, yy - 36), fill=rgba(B, ia))
        d2.text((W/2, yy + 140), '@mente_mulher_estoica', font=estilo.sem_serifa(46, 600), fill=rgba(B, ia), anchor='mm')
    ff.stdin.write(estilo.para_bytes(np.asarray(im.convert('RGB'), np.float32) * (1 - ap(t, T - 0.4, 0.4))))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida)
print('ok', saida)
