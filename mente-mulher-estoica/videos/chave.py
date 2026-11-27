"""A chave: interruptor REAGIR / RESPONDER. Bolinha tensa com nuvem; um dedo dourado arrasta para RESPONDER,
a carinha fica serena e a nuvem some. Epicteto, Encheirídion 5. Formato inspirado em @mentesquemarcam (desenho próprio).
Uso: python3 chave.py saida.mp4
"""
import sys, math, random, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
W, H, FPS, T = 1080, 1920, 30, 17.0
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
TX = (215, 210, 202)
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.5): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
def rgba(c, a): return c + (int(255 * cl(a)),)
def lerp(a, b, p): return a + (b - a) * p
def mix(a, b, p): return tuple(int(lerp(a[i], b[i], p)) for i in range(3))
def ease(p): p = cl(p); return p * p * (3 - 2 * p)

CY = 1000; X0, X1 = 330, 750; R = 120          # trilho e bolinha
T_DEDO, T_EMP, T_FIM_EMP = 3.8, 5.0, 7.0
random.seed(4)
GOTAS = [(random.uniform(-90, 90), random.uniform(0, 1)) for _ in range(14)]

def rosto(d, x, y, r, sereno, a):
    cor = mix((150, 150, 158), G, sereno)
    d.ellipse((x - r, y - r, x + r, y + r), fill=(28, 27, 26, int(255 * a)), outline=rgba(cor, a), width=6)
    for s in (-1, 1):   # sobrancelhas: franzidas -> relaxadas
        ix, ox = x + s * 18, x + s * 58
        d.line([(ix, y - 38 + 14 * (1 - sereno)), (ox, y - 46 - 2 * (1 - sereno))], fill=rgba(cor, a), width=6)
        if sereno > 0.6:  # olhos fechados em arco
            d.arc((x + s * 38 - 18, y - 22, x + s * 38 + 18, y + 6), 200, 340, fill=rgba(cor, a), width=6)
        else:
            d.ellipse((x + s * 38 - 8, y - 16, x + s * 38 + 8, y), fill=rgba(cor, a))
    c = sereno * 2 - 1   # boca: -1 triste, +1 sorriso
    pts = [(x + u, y + 45 + 18 * c * (1 - (u / 40) ** 2) - 8 * c) for u in range(-40, 41, 5)]
    d.line(pts, fill=rgba(cor, a), width=6, joint='curve')

def nuvem(d, x, y, a, t):
    if a < 0.02: return
    for dx, dy, r in [(-60, 10, 48), (-15, -18, 60), (40, -2, 52), (80, 16, 38), (0, 22, 46)]:
        d.ellipse((x + dx - r, y + dy - r, x + dx + r, y + dy + r), fill=(48, 48, 54, int(255 * a)), outline=rgba((120, 120, 128), a), width=3)
    for gx, f in GOTAS:
        yy = y + 60 + ((t * 1.6 + f) % 1) * 110
        d.line([(x + gx, yy), (x + gx - 4, yy + 18)], fill=(140, 160, 190, int(200 * a)), width=3)

def dedo(d, tipx, tipy, a):
    """Dedo indicador em traço dourado, vindo do canto de cima à direita."""
    if a < 0.02: return
    ang = math.radians(-40); L = 520; w = 34
    ux, uy = math.cos(ang), -math.sin(ang)       # direção do dedo (para cima e direita a partir da ponta)
    nx, ny = -uy, ux
    base = (tipx + ux * L, tipy + uy * L)
    pts = [(tipx + nx * w, tipy + ny * w), (base[0] + nx * w * 1.15, base[1] + ny * w * 1.15),
           (base[0] - nx * w * 1.15, base[1] - ny * w * 1.15), (tipx - nx * w, tipy - ny * w)]
    d.polygon(pts, fill=(30, 28, 24, int(250 * a)))
    d.line(pts[:2], fill=rgba(G, a), width=5); d.line(pts[2:], fill=rgba(G, a), width=5)
    d.chord((tipx - w, tipy - w, tipx + w, tipy + w), math.degrees(ang) + 90, math.degrees(ang) + 270, fill=(30, 28, 24, int(250 * a)), outline=rgba(G, a), width=5)
    for k in (0.32, 0.62):   # dobras
        cx_, cy_ = tipx + ux * L * k, tipy + uy * L * k
        d.arc((cx_ - w * 0.8, cy_ - 10, cx_ + w * 0.8, cy_ + 10), 0, 180, fill=rgba(G, a * 0.7), width=3)
    ux2 = tipx + ux * 34 + nx * 6; uy2 = tipy + uy * 34 + ny * 6   # unha
    d.ellipse((ux2 - 14, uy2 - 12, ux2 + 14, uy2 + 12), outline=rgba(G, a * 0.8), width=3)

fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
saida = Path(sys.argv[1]); ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    a = ap(t, 0.05, 0.5)
    p = ease((t - T_EMP) / (T_FIM_EMP - T_EMP))
    kx = lerp(X0, X1, p)
    sereno = ap(t, T_FIM_EMP - 0.6, 1.0)
    im = fundo.copy()
    if sereno > 0.02:
        gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl)
        gd.ellipse((kx - 300, CY - 300, kx + 300, CY + 300), fill=G + (int(70 * sereno * a),))
        im = Image.alpha_composite(im, gl.filter(ImageFilter.GaussianBlur(80)))
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay, 'RGBA')
    trilho = mix((110, 110, 116), G, sereno)
    d.rounded_rectangle((X0 - R - 26, CY - R - 26, X1 + R + 26, CY + R + 26), radius=R + 26, fill=(20, 20, 20, int(255 * a)), outline=rgba(trilho, a), width=5)
    if p > 0.01:   # rastro dourado
        d.rounded_rectangle((X0 - R, CY - R + 30, kx, CY + R - 30), radius=R - 30, fill=G + (int(55 * p * a),))
    f = estilo.sem_serifa(40, 600)
    d.text((X0, CY + R + 90), 'REAGIR', font=f, fill=rgba(mix((150, 150, 158), (90, 90, 96), sereno), a), anchor='mm')
    d.text((X1, CY + R + 90), 'RESPONDER', font=f, fill=rgba(mix((90, 90, 96), G, sereno), a), anchor='mm')
    nuvem(d, kx, CY - R - 170, a * (1 - ap(t, T_FIM_EMP - 0.4, 1.2)), t)
    tremor = 3 * math.sin(t * 34) * (1 - sereno) * ap(t, 0.5, 0.5)
    rosto(d, kx + tremor, CY, R - 8, sereno, a)
    # dedo: entra, empurra, sai
    entra = ap(t, T_DEDO, 1.0); sai = ap(t, T_FIM_EMP + 0.4, 1.0)
    tip = (kx + R * 0.55, CY - R * 0.55)
    off = (1 - entra) * 700 + sai * 700
    dedo(d, tip[0] + off * 0.77, tip[1] - off * 0.64, a * entra * (1 - sai))
    im = Image.alpha_composite(im, lay); d2 = ImageDraw.Draw(im, 'RGBA')
    a1 = jan(t, 0.5, 8.6)
    if a1 > 0.02:
        d2.text((W / 2, 440), 'Entre o que acontece', font=estilo.playfair(60), fill=rgba(B, a1), anchor='mm')
        d2.text((W / 2, 520), 'e o que você faz,', font=estilo.playfair(60), fill=rgba(B, a1), anchor='mm')
        d2.text((W / 2, 620), 'existe uma chave.', font=estilo.playfair(64, True), fill=rgba(G, ap(t, 1.6) * a1), anchor='mm')
    a2 = jan(t, 9.0, 16.6)
    if a2 > 0.02:
        d2.text((W / 2, 480), 'Ela sempre esteve', font=estilo.playfair(66), fill=rgba(B, a2), anchor='mm')
        d2.text((W / 2, 570), 'na sua mão.', font=estilo.playfair(70, True), fill=rgba(G, a2), anchor='mm')
        d2.text((W / 2, 1420), 'Epicteto, Encheirídion, 5', font=estilo.playfair(32, True), fill=rgba(C, jan(t, 10.0, 16.6)), anchor='mm')
    estilo.texto_espacado(d2, (W / 2, 1640), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(24, 500), rgba((170, 165, 158), 0.8 * a), 6)
    ff.stdin.write(estilo.para_bytes(np.asarray(im.convert('RGB'), np.float32) * (1 - ap(t, T - 0.4, 0.4))))
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); print('ok', saida)
