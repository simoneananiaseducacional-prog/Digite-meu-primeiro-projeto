"""Pensamento, emoção, comportamento e significado: o mapa é desenhado no ritmo da explicação em áudio
de @intervalocriativo (áudio original, com crédito). Caminho vermelho (procrastinação, "não dou conta") e
caminho verde (faz e insiste, "sou capaz"). A posição da caneta dela (processo_caneta.json, 10 por segundo) guia um ponteiro dourado que aponta e circula
as mesmas palavras, como uma professora. Uso: python3 processo.py video_original.mp4 saida.mp4
"""
import sys, subprocess, json, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia, personagens
from personagens import ela
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
W, H, FPS = 1080, 1920, 30
T = 157.0
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
VERM, VERDE = (226, 96, 96), (120, 200, 130)
FONTES = Path('/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos/fontes')
MAO = ImageFont.truetype(str(FONTES / 'CaveatBrush-Regular.ttf'), 58)
EMO = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', 109)
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def rgba(c, a): return c + (int(255 * cl(a)),)

def camada_texto(s, font, cor):
    w = int(font.getlength(s)) + 20; h = int(font.size * 1.6)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ImageDraw.Draw(im).text((10, h / 2), s, font=font, fill=cor + (255,), anchor='lm')
    return im
def emoji(ch, alt=70):
    im = Image.new('RGBA', (140, 140), (0, 0, 0, 0)); ImageDraw.Draw(im).text((70, 70), ch, font=EMO, embedded_color=True, anchor='mm')
    im = im.crop(im.getbbox()); s = alt / im.height
    return im.resize((int(im.width * s), alt), Image.LANCZOS)

XN = 400
NOS = [('Pensamento', 520, 2.0), ('Emoção', 740, 6.0), ('Comportamento', 960, 9.0), ('Significado', 1190, 14.0)]
NOTAS = [  # (camada, x, y, início)
    (emoji('❌', 56), 770, 520, 24.0),
    (emoji('😰', 62), 770, 740, 30.0),
    (camada_texto('Procrastinação', MAO, VERM), 845, 935, 32.0),
    (camada_texto('Não dou conta', MAO, VERM), 845, 1150, 34.5),
    (emoji('✅', 56), 860, 520, 96.0),
    (emoji('💪', 62), 860, 740, 102.0),
    (camada_texto('Faz e insiste', MAO, VERDE), 845, 995, 110.0),
    (camada_texto('Sou capaz!!!', MAO, VERDE), 845, 1215, 112.0),
]
NO_LAY = [camada_texto(n, estilo.playfair(54), B) for n, _, _ in NOS]

def colar(im, lay, cx, cy, p, a=1.0):
    """Revela a camada da esquerda para a direita (efeito de escrita)."""
    if p <= 0.01 or a <= 0.01: return
    w = max(1, int(lay.width * cl(p))); part = lay.crop((0, 0, w, lay.height))
    if a < 1: part.putalpha(part.getchannel('A').point(lambda v: int(v * a)))
    im.alpha_composite(part, (int(cx - lay.width / 2), int(cy - lay.height / 2)))

# --- caneta: vídeo (512x910) -> nosso mapa ---
VY = [(230, 520), (386, 740), (586, 960), (780, 1190)]
def mapa(xv, yv):
    ys = [a for a, _ in VY]; ym = np.interp(yv, ys, [b for _, b in VY], left=None, right=None)
    if yv < ys[0]: ym = VY[0][1] + (yv - ys[0]) * 1.4
    if yv > ys[-1]: ym = VY[-1][1] + (yv - ys[-1]) * 1.2
    return float(np.clip(400 + (xv - 270) * 3.0, 120, 1010)), float(np.clip(ym, 420, 1330))
RAW = json.load(open(Path(__file__).with_name('processo_caneta.json')))
N = len(RAW); PX = np.full(N, np.nan); PY = np.full(N, np.nan)
for i, p in enumerate(RAW):
    if p: PX[i], PY[i] = mapa(*p)
def suaviza(v):
    ok = ~np.isnan(v); idx = np.arange(len(v)); out = np.interp(idx, idx[ok], v[ok])
    gap = np.zeros(len(v), bool); run = 0
    for i in range(len(v)):
        run = 0 if ok[i] else run + 1
        gap[i] = run > 8
    k = np.ones(3) / 3; out = np.convolve(np.pad(out, 1, mode='edge'), k, 'valid')
    return out, gap
PX, GAP = suaviza(PX); PY, _ = suaviza(PY)
def caneta(t):
    i = t * 10; j = min(int(i), N - 2); f = i - j
    if GAP[j] or GAP[j + 1]: return None
    return (PX[j] * (1 - f) + PX[j + 1] * f, PY[j] * (1 - f) + PY[j + 1] * f)
# elementos que podem ser destacados: (x, y, raio x, raio y, aparece)
ALVOS = [(XN, y, 190 if n == 'Comportamento' else 150, 64 if n == 'Significado' else 50, t0) for n, y, t0 in NOS]
ALVOS += [(x + lay.width / 2 - (lay.width / 2 if lay.width < 120 else 0), y, max(50, lay.width / 2 + 18), 44, t0) for lay, x, y, t0 in NOTAS]
FOCO = np.zeros(len(ALVOS))

fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
saida = Path(sys.argv[2]); ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    im = fundo.copy()
    verde = ap(t, 102.0, 1.5)
    if verde > 0.02:   # brilho atrás da personagem no caminho verde
        gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(gl).ellipse((540 - 230, 1500 - 230, 540 + 230, 1500 + 230), fill=G + (int(60 * verde),))
        im = Image.alpha_composite(im, gl.filter(ImageFilter.GaussianBlur(70)))
    d = ImageDraw.Draw(im, 'RGBA')
    q = 1 - ap(t, 7.0, 0.8)
    if q > 0.02:
        d.text((W / 2, 250), 'Como um pensamento vira', font=estilo.playfair(56), fill=rgba(B, q), anchor='mm')
        d.text((W / 2, 330), 'o que você acredita sobre si', font=estilo.playfair(56, True), fill=rgba(G, q), anchor='mm')
    for i, ((nome, y, t0), lay) in enumerate(zip(NOS, NO_LAY)):
        p = cl((t - t0) / 1.3)
        if p <= 0: continue
        rx, ry = (lay.width / 2 + 34, 64) if nome == 'Significado' else (lay.width / 2 + 24, 46)
        d.ellipse((XN - rx, y - ry, XN + rx, y + ry), outline=rgba(G, ap(t, t0 + 0.8, 0.6)), width=3)
        colar(im, lay, XN, y, p)
        if i < len(NOS) - 1:   # seta para o próximo
            ny = NOS[i + 1][1]; pa = ap(t, NOS[i + 1][2] - 0.6, 0.5)
            if pa > 0.02:
                y0, y1 = y + ry + 10, ny - 56
                d.line([(XN, y0), (XN, y0 + (y1 - y0) * pa)], fill=rgba(C, 0.9), width=3)
                if pa > 0.95: d.polygon([(XN - 10, y1 - 14), (XN + 10, y1 - 14), (XN, y1)], fill=rgba(C, 0.9))
    for lay, x, y, t0 in NOTAS:
        colar(im, lay, x, y, cl((t - t0) / 1.0))
    # ponteiro dourado seguindo a caneta dela + destaque da palavra apontada
    pc = caneta(t)
    alvo = -1
    if pc:
        dist = [((pc[0] - x) / rx) ** 2 + ((pc[1] - y) / ry) ** 2 if t >= t0 + 0.5 else 9 for x, y, rx, ry, t0 in ALVOS]
        if min(dist) < 2.2: alvo = int(np.argmin(dist))
    for i in range(len(ALVOS)):
        FOCO[i] = min(1, FOCO[i] + 1 / (0.35 * FPS)) if i == alvo else max(0, FOCO[i] - 1 / (1.2 * FPS))
    lay2 = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d3 = ImageDraw.Draw(lay2, 'RGBA')
    for i, (x, y, rx, ry, _) in enumerate(ALVOS):
        f = FOCO[i]
        if f < 0.02: continue
        rx2, ry2 = rx * 1.12, ry * 1.25
        d3.arc((x - rx2, y - ry2, x + rx2, y + ry2), -90, -90 + 360 * min(1, f * 1.15), fill=(240, 205, 130, int(255 * f)), width=6)
    if pc:
        tr = [caneta(t - k * 0.04) for k in range(12)]
        for k, q in enumerate(tr[1:], 1):
            if q: d3.ellipse((q[0] - 9 + k * 0.5, q[1] - 9 + k * 0.5, q[0] + 9 - k * 0.5, q[1] + 9 - k * 0.5), fill=(240, 205, 130, int(110 * (1 - k / 12))))
        g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse((pc[0] - 34, pc[1] - 34, pc[0] + 34, pc[1] + 34), fill=G + (150,))
        im.alpha_composite(g.filter(ImageFilter.GaussianBlur(14)))
        d3.ellipse((pc[0] - 11, pc[1] - 11, pc[0] + 11, pc[1] + 11), fill=(255, 236, 190, 255))
    im.alpha_composite(lay2)
    d = ImageDraw.Draw(im, 'RGBA')
    vermelho = ap(t, 30.0, 1.0) * (1 - verde)
    ela(d, 540, 1720, 1.0, lado=1, cabeca_baixa=0.5 * vermelho, t=t,
        emo=dict(triste=0.8 * vermelho, sorriso=0.8 * verde))
    d.text((W / 2, 1780), 'Áudio: @intervalocriativo', font=estilo.sem_serifa(24, 500), fill=(170, 165, 158, 230), anchor='mm')
    estilo.texto_espacado(d, (W / 2, 1830), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(22, 500), (150, 146, 140, 220), 6)
    ff.stdin.write(estilo.para_bytes(np.asarray(im.convert('RGB'), np.float32) * (1 - ap(t, T - 0.6, 0.6))))
ff.stdin.close(); ff.wait()
# áudio original da explicação, com fim suave
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(saida.with_suffix('.mudo.mp4')), '-i', sys.argv[1],
                '-filter_complex', f'[1:a]atrim=0:{T},asetpts=PTS-STARTPTS,afade=t=out:st={T - 1.5}:d=1.5[a]',
                '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', str(saida)], check=True)
print('ok', saida)
