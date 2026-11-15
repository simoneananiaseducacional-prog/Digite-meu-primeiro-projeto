"""O encaixe: ela tenta encaixar a sua peça com a de um homem, não encaixa; tenta com outro, também não.
Pensa "O problema sou eu?", olha a própria peça, entende que foi constatação e não fracasso, e segue.
Uso: python3 encaixe.py saida.mp4
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
def jan(t, t0, t1, d=0.4): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
def rgba(c, a): return c + (int(255 * cl(a)),)
def lerp(a, b, p): return a + (b - a) * p
def seg(t, t0, t1): return estilo.suavizar(cl((t - t0) / (t1 - t0)))

T = 28.0
CHAO = 1250
HY = CHAO - 6 - 240
XE = 380
PY = HY + 70                       # altura das peças
CINZA0 = personagens.CINZA
# homens: (entra, tenta, sai, cor)
HOMENS = [(0.6, 2.6, 5.4, (175, 175, 175)), (7.0, 8.8, 11.2, (140, 150, 165))]

def peca(d, x, y, a, lado, tipo, cor, s=1.0):
    """Peça quadrada (90 px). lado=+1: encaixe à direita; -1: à esquerda. tipo: 'redondo', 'triangulo', 'quadrado'."""
    if a < 0.02: return
    h = 45 * s
    if lado > 0:   # peça dela: aba redonda saindo para a direita
        d.rectangle((x - h, y - h, x + h, y + h), fill=rgba(cor, a))
        r = 20 * s; d.ellipse((x + h - 6 * s, y - r, x + h - 6 * s + 2 * r, y + r), fill=rgba(cor, a))
    else:          # peça dele: recorte à esquerda, de outro formato
        pts = [(x - h, y - h), (x + h, y - h), (x + h, y + h), (x - h, y + h)]
        d.polygon(pts, fill=rgba(cor, a))
        if tipo == 'triangulo':
            d.polygon([(x - h - 1, y - 24 * s), (x - h + 30 * s, y), (x - h - 1, y + 24 * s)], fill=(12, 12, 12, int(255 * a)))
        else:
            d.rectangle((x - h - 1, y - 16 * s, x - h + 30 * s, y + 16 * s), fill=(12, 12, 12, int(255 * a)))

def tentativa(t, ent, ten, sai):
    """x da peça dela e da dele durante uma tentativa."""
    junta = seg(t, ten, ten + 0.6) * (1 - seg(t, ten + 1.6, ten + 2.2))
    bate = math.sin(min(1, max(0, (t - ten - 0.6) / 0.5)) * math.pi) * (t > ten + 0.6) * (t < ten + 1.1)
    return junta, bate

fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
FT = estilo.sem_serifa(54, 500); TXT = (205, 200, 194)
TEXTOS = [(0.4, 5.6, ['Ela tentou.']), (6.8, 11.4, ['Tentou de novo.']), (11.4, 13.4, ['E de novo', 'não encaixou.']), (13.4, 16.0, ['“O problema sou eu?”'])]
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    a = ap(t, 0.05, 0.4)
    cena = a * (1 - 0.92 * ap(t, 17.2, 0.8))
    cen = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(cen, 'RGBA')
    d.line([(0, CHAO), (W, CHAO)], fill=rgba(C, cena), width=4)
    segue = seg(t, 17.6, 22.0)
    xe = XE + 300 * segue
    # peça dela: na mão; vai até o meio nas tentativas
    xp = xe + 120; tristeza = 0.0; aberta = 0.0
    for ent, ten, sai, cor in HOMENS:
        junta, bate = tentativa(t, ent, ten, sai)
        xp += 60 * junta - 6 * bate
        tristeza = max(tristeza, jan(t, ten + 0.9, sai + 0.8, 0.4))
        xh = lerp(1250, 740, seg(t, ent, ent + 1.4)) + (510) * seg(t, sai, sai + 1.4)
        if xh < 1180:
            personagens.CINZA = cor
            ele(d, xh, CHAO - 6, cena, braco=0.55, lado=-1, t=t, emo=None)
            personagens.CINZA = CINZA0
            tipo = 'triangulo' if cor == HOMENS[0][3] else 'quadrado'
            xph = xh - 130 - 60 * junta
            peca(d, xph, PY, cena, -1, tipo, cor)
    duvida = jan(t, 13.2, 15.8, 0.4)
    percebe = seg(t, 15.2, 16.4)
    emo = dict(sorriso=0.5 * (t < 2.8) + 0.3 * jan(t, 5.8, 8.8) + 0.9 * percebe,
               triste=0.8 * max(tristeza, duvida * (1 - percebe)))
    ela(d, xe, CHAO - 6, cena, braco=0.55, lado=1, cabeca_baixa=0.5 * max(tristeza, duvida) * (1 - percebe), t=t, emo=emo)
    # brilho da peça dela quando ela entende
    if percebe > 0.02:
        gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl)
        r = 110 * percebe; gd.ellipse((xp - r, PY - r, xp + r, PY + r), fill=G + (int(80 * percebe * cena),))
        cen = Image.alpha_composite(gl.filter(ImageFilter.GaussianBlur(28)), cen); d = ImageDraw.Draw(cen, 'RGBA')
    peca(d, xp, PY, cena, 1, 'redondo', G, 1.0 + 0.15 * percebe)
    # câmera
    close = jan(t, 12.2, 16.8, 0.6)
    K = lerp(1.55, 2.2, close); CX = lerp(560, XE + 60, close); CY = lerp(1100, HY + 20, close)
    big = cen.resize((int(W * K), int(H * K)), Image.BICUBIC)
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.paste(big, (int(W / 2 - CX * K), int(H * 0.58 - CY * K)))
    im = Image.alpha_composite(fundo, cam); d2 = ImageDraw.Draw(im, 'RGBA')
    for t0, t1, linhas in TEXTOS:
        fa = jan(t, t0, t1)
        for j, l in enumerate(linhas):
            if fa > 0.02: d2.text((W / 2, 440 + j * 76), l, font=FT, fill=rgba(TXT, fa), anchor='mm')
    fim = 27.6
    f1 = jan(t, 17.4, fim); f2 = jan(t, 19.0, fim); f3 = jan(t, 20.8, fim); f4 = jan(t, 22.8, fim)
    if f1 > 0.02: d2.text((W / 2, 360), 'Às vezes, não era para ser.', font=estilo.playfair(56), fill=rgba(B, f1), anchor='mm')
    if f2 > 0.02:
        d2.text((W / 2, 460), 'Às vezes, é algo em nós', font=estilo.playfair(56), fill=rgba(B, f2), anchor='mm')
        d2.text((W / 2, 528), 'que precisa mudar.', font=estilo.playfair(56), fill=rgba(B, f2), anchor='mm')
    if f3 > 0.02:
        d2.text((W / 2, 628), 'Às vezes, é quem a gente escolhe,', font=estilo.playfair(56), fill=rgba(B, f3), anchor='mm')
        d2.text((W / 2, 696), 'de novo e de novo.', font=estilo.playfair(56), fill=rgba(B, f3), anchor='mm')
    if f4 > 0.02: d2.text((W / 2, 810), 'Olhar para dentro é o começo.', font=estilo.playfair(58, True), fill=rgba(G, f4), anchor='mm')
    ia = jan(t, 25.0, 27.8)
    if ia > 0.02: estilo.texto_espacado(d2, (W / 2, 1560), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(26, 500), rgba((150, 146, 140), ia), 6)
    ff.stdin.write(estilo.para_bytes(np.asarray(im.convert('RGB'), np.float32) * (1 - ap(t, T - 0.3, 0.3))))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida)
print('ok', saida)
