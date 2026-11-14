"""O balão: ela quer subir com um balão dourado, mas está amarrada a pesos (o passado, a culpa,
o que vão pensar). Solta um por um e sobe para a luz. Texto só no fim (Epicteto, Encheirídion 1) e @.
Inspirado no ritmo de vídeos de metáfora única (sem copiar a cena de ninguém). Uso: python3 balao.py saida.mp4
"""
import sys, math, random, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from personagens import ela
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
saida = Path(sys.argv[1])
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.4): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.4): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
def rgba(c, a): return c + (int(255 * cl(a)),)
def lerp(a, b, p): return a + (b - a) * p
def seg(t, t0, t1): return estilo.suavizar(cl((t - t0) / (t1 - t0)))

class Cam:
    """Desenha em coordenadas do mundo; converte para a tela com foco (fx, fy) e escala S."""
    def __init__(self, d, fx, fy, S): self.d, self.fx, self.fy, self.S = d, fx, fy, S
    def p(self, x, y): return ((x - self.fx) * self.S + W / 2, (y - self.fy) * self.S + H * 0.58)
    def _xy(self, xy):
        if isinstance(xy[0], (tuple, list)): return [self.p(*q) for q in xy]
        out = []
        for i in range(0, len(xy), 2): out += list(self.p(xy[i], xy[i + 1]))
        return out
    def __getattr__(self, nome):
        orig = getattr(self.d, nome)
        def chama(xy, *args, **kw):
            for k in ('width', 'radius'):
                if k in kw: kw[k] = max(1, int(round(kw[k] * self.S)))
            return orig(self._xy(xy), *args, **kw)
        return chama

T = 24.0
CHAO = 1250
X = 540
SOLTA = [(7.6, 'o passado', -250), (9.8, 'a culpa', 0), (12.2, 'o que vão|pensar', 250)]
def soltou(t, i): return t >= SOLTA[i][0]
def lift(t):
    """Quanto ela já subiu (em px do mundo)."""
    if t < SOLTA[0][0]: return 26 * abs(math.sin(t * 3.2)) * ap(t, 1.6, 0.6)
    if t < SOLTA[1][0]: return lerp(20, 130, seg(t, SOLTA[0][0], SOLTA[0][0] + 0.9)) + 10 * abs(math.sin(t * 3.4))
    if t < SOLTA[2][0]: return lerp(130, 250, seg(t, SOLTA[1][0], SOLTA[1][0] + 0.9)) + 14 * abs(math.sin(t * 4.0)) * ap(t, 11.0, 0.4)
    u = t - SOLTA[2][0]
    return 250 + 60 * u + 120 * u * u
def camera(t):
    y_ela = CHAO - lift(t)
    S = 1.36
    fx, fy = X, CHAO - 260
    close = jan(t, 4.6, 6.6, 0.4)                       # close no rosto quando ela não consegue subir
    S = lerp(S, 3.0, close); fy = lerp(fy, y_ela - 230, close)
    sobe = seg(t, SOLTA[2][0] + 0.3, SOLTA[2][0] + 1.5)  # depois de livre, a câmera acompanha
    fy = lerp(fy, y_ela - 160, sobe)
    return fx, fy, S

random.seed(7)
ESTRELAS = [(random.uniform(-200, 1280), random.uniform(-3000, 1150), random.uniform(1, 2.6)) for _ in range(220)]
fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
FT = estilo.sem_serifa(52, 500); TXT = (205, 200, 194)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    a = ap(t, 0.1, 0.5)
    cena = a * (1 - 0.85 * ap(t, 17.6, 0.8))
    fx, fy, S = camera(t)
    im = fundo.copy()
    # luz dourada que nasce no alto quando ela fica livre
    luz = seg(t, SOLTA[2][0] + 0.4, SOLTA[2][0] + 4.0)
    if luz > 0.01:
        gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl)
        gd.ellipse((-300, -900, W + 300, 700 + 500 * luz), fill=G + (int(120 * luz * cena),))
        im = Image.alpha_composite(im, gl.filter(ImageFilter.GaussianBlur(120)))
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d0 = ImageDraw.Draw(lay, 'RGBA'); d = Cam(d0, fx, fy, S)
    for sx, sy, r in ESTRELAS:
        px, py = d.p(sx, sy)
        if -5 < px < W + 5 and -5 < py < H + 5:
            tw = 0.5 + 0.5 * math.sin(t * 2 + sx)
            d0.ellipse((px - r, py - r, px + r, py + r), fill=(220, 215, 205, int(140 * tw * cena)))
    d.line([(-400, CHAO), (1480, CHAO)], fill=rgba(C, cena), width=4)
    ly = lift(t); pe = CHAO - 6 - ly
    hy = pe - 240
    quadril = (X, pe - 95)
    # emoções e olhar
    livre = seg(t, SOLTA[2][0], SOLTA[2][0] + 1.0)
    esforco = ap(t, 1.8, 0.6) * (1 - livre)
    olhar_baixo = max(jan(t, SOLTA[i][0] - 1.0, SOLTA[i][0] + 0.2, 0.3) for i in range(3))
    emo = dict(sorriso=0.6 * (t < 1.8) + 0.4 * max(jan(t, SOLTA[0][0] + 0.2, SOLTA[1][0] - 1.0), jan(t, SOLTA[1][0] + 0.2, SOLTA[2][0] - 1.4)) + 1.0 * livre,
               triste=0.8 * esforco * (1 - 0.6 * olhar_baixo), aberta=0.0)
    ela(d, X, pe, cena, braco=0.9, lado=1, cabeca_baixa=0.6 * olhar_baixo, t=t, emo=emo)
    # pesos e cordas
    for i, (ts, nome, dx) in enumerate(SOLTA):
        px, py = X + dx, CHAO - 34
        rot = 1 - seg(t, ts, ts + 0.5)
        d.ellipse((px - 100, py - 40, px + 100, py + 34), fill=(40, 40, 46, int(240 * cena)), outline=rgba((140, 140, 148), cena), width=4)
        tx_, ty_ = d.p(px, py)
        fs = estilo.sem_serifa(int(21 * S), 600)
        ls = nome.split('|')
        for j, l in enumerate(ls):
            d0.text((tx_, ty_ - 4 * S + (j - (len(ls) - 1) / 2) * 24 * S), l, font=fs, fill=rgba((215, 210, 200), cena), anchor='mm')
        if rot > 0.02:
            tensa = 1.0 if t < ts else rot
            meio = ((quadril[0] + px) / 2, (quadril[1] + py - 34) / 2 + 20 * (1 - tensa))
            d.line([quadril, meio, (px, py - 40)], fill=rgba((170, 160, 140), cena * rot), width=4, joint='curve')
        if ts <= t < ts + 0.6:                       # faísca dourada ao soltar
            q = (t - ts) / 0.6
            for j in range(8):
                ang = j * math.pi / 4
                r0, r1 = 20 + 60 * q, 40 + 80 * q
                cx, cy = (quadril[0] + px) / 2, (quadril[1] + py) / 2
                d.line([(cx + r0 * math.cos(ang), cy + r0 * math.sin(ang)), (cx + r1 * math.cos(ang), cy + r1 * math.sin(ang))],
                       fill=rgba(G, cena * (1 - q)), width=3)
    # balão
    mao = (X + 40 + 99, hy + 72 - 20)
    bx, by = mao[0] + 30 + 8 * math.sin(t * 1.3), mao[1] - 300
    d.line([mao, (bx - 6, by + 74), (bx, by + 66)], fill=rgba((200, 190, 170), cena), width=3, joint='curve')
    gl2 = Image.new('RGBA', (W, H), (0, 0, 0, 0)); g2 = ImageDraw.Draw(gl2)
    gx, gy = d.p(bx, by); gr = 120 * S
    g2.ellipse((gx - gr, gy - gr, gx + gr, gy + gr), fill=G + (int(70 * cena),))
    im = Image.alpha_composite(im, gl2.filter(ImageFilter.GaussianBlur(40)))
    d.ellipse((bx - 58, by - 70, bx + 58, by + 66), fill=rgba(G, cena))
    d.ellipse((bx - 30, by - 46, bx - 10, by - 18), fill=(255, 240, 210, int(160 * cena)))
    d.polygon([(bx - 8, by + 64), (bx + 8, by + 64), (bx, by + 76)], fill=rgba(G, cena))
    im = Image.alpha_composite(im, lay)
    d2 = ImageDraw.Draw(im, 'RGBA')
    f1 = jan(t, 18.0, 22.2)
    if f1 > 0.02:
        d2.text((W/2, 640), 'Solte o que', font=estilo.playfair(66), fill=rgba(B, f1), anchor='mm')
        d2.text((W/2, 730), 'não depende de você.', font=estilo.playfair(66, True), fill=rgba(G, f1), anchor='mm')
        d2.text((W/2, 850), 'Epicteto, Encheirídion, 1', font=estilo.playfair(32, True), fill=rgba(C, f1), anchor='mm')
    ia = ap(t, 22.2, 0.4)
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
