"""Série de dezembro "O preço de dar conta de tudo", Ep. 1, versão com personagem (par da versão em esquema,
reel_dar_conta_de_tudo.py). Ela equilibra uma pilha sobre a cabeça: três caixas de DEMANDAS REAIS e, por cima,
três pedras de AUTOCOBRANÇA. A pilha balança e ela se curva; as pedras caem, uma caixa vai para o chão e ela
se endireita. Três orientações; reflexão autoral inspirada em Epicteto, Manual, § 1.
Uso: python3 reel_dar_conta_bonecos.py saida.mp4 [capa.png]
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from personagens import ela
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
W, H, FPS, T = 1080, 1920, 30, 30.0
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
VINHO = (110, 34, 38)
FT = Path(__file__).with_name('fontes')
def ebg(nome, t): return ImageFont.truetype(str(FT / f'EBGaramond-{nome}.ttf'), t)
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.6): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
saida = Path(sys.argv[1]); capa = Path(sys.argv[2]) if len(sys.argv) > 2 else None
fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')

# cena do personagem (coordenadas da cena, ampliadas K vezes)
CHAO, K, CX, CY_TELA = 1000, 1.5, 540, 1180
def tela(x, y): return (W / 2 + (x - CX) * K, CY_TELA + (y - 900) * K)
Y_CHAO = tela(0, CHAO)[1]
TOPO_CABECA = tela(0, CHAO - 6 - 240 - 36)[1]
BW, BH = 380, 64
CAIXAS = [(2.8, 'Trabalho'), (4.0, 'Família'), (5.2, 'Responsabilidades')]
PEDRAS = [(7.8, 'Não posso falhar.'), (9.0, 'Não posso descansar.'), (10.2, 'Tenho que ser forte.')]
T_SOLTA, T_DESCE = 12.2, 14.0
ORI = [(14.4, 'Priorize o necessário.'), (15.8, 'Questione suas exigências.'), (17.2, 'Respeite seus limites.')]
T_FECHO = 19.2
F_TIT1, F_TIT2 = ebg('Regular', 80), ebg('Italic', 84)
F_BOX, F_PED, F_ROT, F_ORI = ebg('Regular', 40), ebg('Italic', 38), ebg('Medium', 36), ebg('Italic', 54)
REFLEXAO = [('Ser estoico não é aprender', B, 0), ('a suportar tudo.', B, 0), (None, None, 0),
            ('É desenvolver sabedoria', G, 1), ('para reconhecer o que realmente', G, 1),
            ('precisa ser suportado', G, 1), ('e o que pode ser mudado.', G, 1)]

def txt(d, xy, s, f, cor, a, anc='mm'):
    if a > 0.01 and s: d.text(xy, s, font=f, fill=cor + (int(255 * cl(a)),), anchor=anc)

def quadro(t):
    img = fundo.copy()
    cena = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(cena)
    n_ped = sum(ap(t, t0, 0.5) for t0, _ in PEDRAS) * (1 - ap(t, T_SOLTA, 0.4))
    alivio = ap(t, T_SOLTA + 0.6, 1.0)
    # chão
    d.line([(150, Y_CHAO), (930, Y_CHAO)], fill=C + (150,), width=3)
    # personagem (ampliado)
    pers = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ela(ImageDraw.Draw(pers, 'RGBA'), CX, CHAO - 6, 1.0, braco=0.0, lado=1, cabeca_baixa=0.1 + 0.35 * n_ped / 3 * (1 - alivio), t=t,
        emo=dict(triste=0.7 * n_ped / 3 * (1 - alivio), sorriso=0.6 * alivio))
    big = pers.resize((int(W * K), int(H * K)), Image.BICUBIC)
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.paste(big, (int(W / 2 - CX * K), int(CY_TELA - 900 * K)))
    cena = Image.alpha_composite(cena, cam); d = ImageDraw.Draw(cena)
    # pilha sobre a cabeça: balança mais quanto mais pedras
    balanco = 6 + 10 * n_ped
    base_y = TOPO_CABECA - 2 + 10 * n_ped / 3 * (1 - alivio)
    for i, (t0, s) in enumerate(CAIXAS):
        a = ap(t, t0, 0.5)
        if a <= 0: continue
        cair = (1 - ap(t, t0, 0.5)) * 120
        x = W / 2 + i * balanco * math.sin(t * 2.4) * 0.5
        y = base_y - (i + 1) * BH - cair
        if i == 2:   # "Priorize": a última caixa desce para o chão ao lado dela
            p = estilo.suavizar(cl((t - T_DESCE) / 1.0))
            x = x + (W / 2 + 250 - x) * p; y = y + (Y_CHAO - BH - y) * p
        d.rectangle((x - BW / 2, y, x + BW / 2, y + BH - 6), fill=(24, 22, 20, int(255 * a)), outline=G + (int(255 * a),), width=3)
        txt(d, (x, y + BH / 2 - 3), s, F_BOX, B, a)
    for j, (t0, s) in enumerate(PEDRAS):
        a = ap(t, t0, 0.5)
        if a <= 0: continue
        nivel = 3 + j
        x = W / 2 + nivel * balanco * math.sin(t * 2.4) * 0.5
        y = base_y - (nivel + 1) * BH - (1 - a) * 120
        q = cl((t - T_SOLTA - 0.15 * j) / 1.0)   # caem para a direita e somem
        if q > 0:
            x += 420 * q; y += (Y_CHAO - y) * q * q; a *= 1 - cl((q - 0.6) / 0.4)
        if a <= 0.01: continue
        d.rounded_rectangle((x - BW / 2 + 10, y, x + BW / 2 - 10, y + BH - 6), radius=28, fill=VINHO + (int(255 * a),), outline=(150, 70, 70, int(255 * a)), width=2)
        txt(d, (x, y + BH / 2 - 3), s, F_PED, (240, 226, 220), a)
    # rótulos laterais com setas finas douradas
    def rotulo(xy, s, alvo, a):
        if a <= 0.01: return
        txt(d, xy, s, F_ROT, G, a)
        d.line([(xy[0], xy[1] + 28), alvo], fill=G + (int(220 * a),), width=2)
    ar = ap(t, 2.2, 0.5) * (1 - ap(t, T_SOLTA, 0.5))
    rotulo((165, base_y - 1.5 * BH - 60), 'DEMANDAS', (W / 2 - BW / 2 - 12, base_y - 1.5 * BH), ar)
    txt(d, (165, base_y - 1.5 * BH - 22), 'REAIS', F_ROT, G, ar)
    ap2 = ap(t, 7.2, 0.5) * (1 - ap(t, T_SOLTA, 0.5))
    rotulo((915, base_y - 4.5 * BH - 60), 'AUTO-', (W / 2 + BW / 2 + 12, base_y - 4.5 * BH), ap2)
    txt(d, (915, base_y - 4.5 * BH - 22), 'COBRANÇA', F_ROT, G, ap2)
    # orientações
    for k, (t0, s) in enumerate(ORI): txt(d, (W / 2, Y_CHAO + 85 + k * 72), s, F_ORI, B, ap(t, t0, 0.6))
    # título fixo desde o quadro zero
    txt(d, (W / 2, 220), 'Você precisa', F_TIT1, B, 1)
    txt(d, (W / 2, 312), 'dar conta de tudo?', F_TIT2, B, 1)
    rec = 1 - ap(t, T_FECHO, 0.7)
    if rec < 0.999: cena.putalpha(cena.getchannel('A').point(lambda v: int(v * rec)))
    img = Image.alpha_composite(img, cena)
    if t > T_FECHO:
        top = Image.new('RGBA', img.size, (0, 0, 0, 0)); dt = ImageDraw.Draw(top); y = 760
        for i, (s, cor, it) in enumerate(REFLEXAO):
            if s: txt(dt, (W / 2, y), s, ebg('Italic', 58) if it else ebg('Regular', 60), cor, ap(t, T_FECHO + 0.6 + (0 if i < 3 else 1.4), 0.7))
            y += 40 if s is None else 80
        txt(dt, (W / 2, y + 60), 'Reflexão autoral inspirada em', ebg('Italic', 36), C, ap(t, 23.0, 0.6))
        txt(dt, (W / 2, y + 108), 'Epicteto, Manual, § 1', ebg('Italic', 36), C, ap(t, 23.0, 0.6))
        img = Image.alpha_composite(img, top)
    dd = ImageDraw.Draw(img, 'RGBA')
    estilo.texto_espacado(dd, (W / 2, 1720), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(26, 500), (170, 165, 158, 210), 6)
    return img.convert('RGB')

if capa: quadro(11.4).save(capa)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    ff.stdin.write(estilo.para_bytes(np.asarray(quadro(t), np.float32) * cl((T - t) / 0.5)))
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida)
saida.with_suffix('.mudo.mp4').unlink(missing_ok=True); print('ok', saida)
