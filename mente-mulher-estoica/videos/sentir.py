"""Estoicismo e CNV, parte 2: Sentimento. Ela diz "Tô bem.", mas há um nó no peito. Ao olhar para dentro,
o nó vira palavras (cansada, sozinha, com medo) e o peito fica dourado.
Rosenberg, Comunicação Não-Violenta, cap. 4; Marco Aurélio, Meditações, 4.3. Uso: python3 sentir.py saida.mp4
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia, personagens
from personagens import ela
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
W, H, FPS, T = 1080, 1920, 30, 19.0
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
TX = (215, 210, 202)
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.5): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
def rgba(c, a): return c + (int(255 * cl(a)),)
def lerp(a, b, p): return a + (b - a) * p
def mix(a, b, p): return tuple(int(lerp(a[i], b[i], p)) for i in range(3))

XE, CHAO, K = 540, 1250, 1.6
PEITO = (XE, 1090)
def tela(x, y): return (W / 2 + (x - PEITO[0]) * K, 1060 + (y - PEITO[1]) * K)
PALAVRAS = [('cansada', (215, 980), 5.5), ('sozinha', (865, 980), 7.3), ('com medo', (540, 735), 9.1)]

def no(d, s, t, a):
    """Nó embolado no peito; s = tamanho (1 cheio, 0 desfeito)."""
    if s < 0.03 or a < 0.02: return
    pts = []
    for k in range(260):
        u = k / 259 * 2 * math.pi * 3
        r = 26 * s * (0.7 + 0.3 * math.sin(3.1 * u + t * 2))
        pts.append((PEITO[0] + r * math.cos(u) + 9 * s * math.sin(2.3 * u + 1.7), PEITO[1] + r * math.sin(1.3 * u) + 9 * s * math.cos(1.7 * u)))
    d.line(pts, fill=rgba((150, 150, 158), a), width=3, joint='curve')

fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
FQ = estilo.playfair(64); FQ2 = estilo.playfair(64, True); FW = estilo.playfair(54, True)
saida = Path(sys.argv[1]); ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    cena_a = 1 - 0.8 * ap(t, 11.0, 0.7)
    nomeados = sum(ap(t, tw, 1.0) for _, _, tw in PALAVRAS) / 3
    surge = ap(t, 2.6, 0.9)
    olhar = ap(t, 4.4, 0.8)
    cen = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(cen, 'RGBA')
    d.line([(XE - 360, CHAO), (XE + 360, CHAO)], fill=rgba(C, cena_a * 0.8), width=4)
    pc = mix((110, 110, 116), G, nomeados)
    if nomeados > 0.02:
        r = 10 + 10 * nomeados
        d.ellipse((PEITO[0] - r, PEITO[1] - r, PEITO[0] + r, PEITO[1] + r), fill=rgba(pc, cena_a))
    no(d, surge * (1 - nomeados), t, cena_a)
    falso = 1 - ap(t, 2.4, 0.6)
    ela(d, XE, CHAO - 6, cena_a, lado=1, cabeca_baixa=0.7 * olhar * (1 - 0.6 * ap(t, 9.8, 1.0)), t=t,
        emo=dict(sorriso=0.7 * falso + 0.7 * ap(t, 10.0, 1.0), triste=0.6 * surge * (1 - nomeados)))
    big = cen.resize((int(W * K), int(H * K)), Image.BICUBIC)
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.paste(big, (int(W / 2 - PEITO[0] * K), int(1060 - PEITO[1] * K)))
    im = fundo.copy()
    if nomeados > 0.02:
        gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl)
        gd.ellipse((W / 2 - 320, 1060 - 320, W / 2 + 320, 1060 + 320), fill=G + (int(75 * nomeados * cena_a),))
        im = Image.alpha_composite(im, gl.filter(ImageFilter.GaussianBlur(90)))
    im = Image.alpha_composite(im, cam); d2 = ImageDraw.Draw(im, 'RGBA')
    q = 1 - ap(t, 5.0, 0.5)   # pergunta inteira desde o quadro zero
    if q > 0.02:
        d2.text((W / 2, 290), 'Quantas vezes você disse', font=FQ, fill=rgba(B, q), anchor='mm')
        d2.text((W / 2, 380), '“tô bem” hoje?', font=FQ2, fill=rgba(G, q), anchor='mm')
    ab = jan(t, 0.4, 2.6, 0.4)
    if ab > 0.02:   # balão da fala
        bx, by = 800, 760
        d2.rounded_rectangle((bx - 125, by - 50, bx + 125, by + 50), radius=46, fill=(236, 232, 224, int(245 * ab)))
        d2.polygon([(bx - 90, by + 30), (bx - 50, by + 44), (bx - 150, by + 110)], fill=(236, 232, 224, int(245 * ab)))
        d2.text((bx, by + 2), 'Tô bem.', font=estilo.sem_serifa(46, 600), fill=(24, 22, 20, int(255 * ab)), anchor='mm')
    for w, alvo, tw in PALAVRAS:   # cada sentimento sai do peito e ganha nome
        p = ap(t, tw, 1.0); aw = ap(t, tw, 0.4) * (1 - ap(t, 10.8, 0.6))
        if aw < 0.02: continue
        x, y = lerp(W / 2, alvo[0], p), lerp(1060, alvo[1], p)
        d2.text((x, y), w, font=FW, fill=rgba(mix(TX, G, ap(t, tw + 0.8, 0.8)), aw), anchor='mm')
    f1 = jan(t, 11.4, 14.6); f2 = jan(t, 12.4, 14.6)
    if f1 > 0.02: d2.text((W / 2, 820), 'Nomear o que você sente', font=estilo.playfair(66), fill=rgba(B, f1), anchor='mm')
    if f2 > 0.02: d2.text((W / 2, 915), 'já é começar a cuidar.', font=estilo.playfair(68, True), fill=rgba(G, f2), anchor='mm')
    f3 = jan(t, 15.0, 18.6)
    if f3 > 0.02:
        for i, l in enumerate(['“Em nenhum lugar a pessoa', 'encontra retiro mais tranquilo', 'do que na própria alma.”']):
            d2.text((W / 2, 770 + i * 76), l, font=estilo.playfair(54, True), fill=rgba(G if i == 2 else B, f3), anchor='mm')
        d2.text((W / 2, 1050), 'Marco Aurélio, Meditações, 4.3', font=estilo.playfair(32, True), fill=rgba(C, f3), anchor='mm')
    estilo.texto_espacado(d2, (W / 2, 1640), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(24, 500), rgba((170, 165, 158), 0.8), 6)
    ff.stdin.write(estilo.para_bytes(np.asarray(im.convert('RGB'), np.float32) * (1 - ap(t, T - 0.4, 0.4))))
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); print('ok', saida)
