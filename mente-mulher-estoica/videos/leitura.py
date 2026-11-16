"""Cada um lê com a dor que carrega: a mesma frase ("Não encaixou.") chega a três pessoas;
cada uma ouve outra coisa. Epicteto, Encheirídion 5. Ideia nascida de um comentário na página (sem expor ninguém).
Uso: python3 leitura.py saida.mp4
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia, personagens
from personagens import ela, ele
from PIL import Image, ImageDraw
from pathlib import Path
W, H, FPS, T = 1080, 1920, 30, 19.0
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
TX = (215, 210, 202); CZ = (165, 168, 178)
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.5): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
def rgba(c, a): return c + (int(255 * cl(a)),)
def lerp(a, b, p): return a + (b - a) * p

CHAO, K = 1250, 1.5
def tela(x, y): return (W / 2 + (x - 540) * K, 1050 + (y - 1010) * K)
PESSOAS = [  # (x na cena, quem, o que ouviu, cor, quando)
    (300, 'ela_cinza', ['Fui', 'rejeitada.'], CZ, 3.4),
    (540, 'ele', ['Eu não sou', 'suficiente.'], CZ, 4.6),
    (780, 'ela', ['Tudo bem,', 'não era para ser.'], G, 5.8),
]
BAL = (540, 610)
FQ = estilo.playfair(64); FQ2 = estilo.playfair(64, True)
FB = estilo.sem_serifa(42, 600); FP = estilo.sem_serifa(32, 500)

def nuvem_pensamento(d, cx, cy, linhas, cor, a, cabeca):
    if a < 0.02: return
    w, h = 330, 130
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), radius=60, fill=(26, 25, 24, int(235 * a)), outline=rgba(cor, a), width=4)
    for i, (f, r) in enumerate([(0.45, 13), (0.75, 8)]):   # bolinhas até a cabeça
        bx, by = lerp(cx, cabeca[0], f), lerp(cy + h / 2, cabeca[1], f)
        d.ellipse((bx - r, by - r, bx + r, by + r), fill=(26, 25, 24, int(235 * a)), outline=rgba(cor, a), width=3)
    for i, l in enumerate(linhas):
        d.text((cx, cy - 22 + i * 44), l, font=FP, fill=rgba(cor if cor == G else TX, a), anchor='mm')

fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
OURO0, CAB0 = personagens.DOURADO, personagens.CABELO
saida = Path(sys.argv[1]); ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    cena_a = 1 - 0.8 * ap(t, 9.4, 0.7)
    cen = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(cen, 'RGBA')
    d.line([(160, CHAO), (920, CHAO)], fill=rgba(C, cena_a * 0.8), width=4)
    for x, quem, _, cor, tq in PESSOAS:
        ouviu = ap(t, tq, 0.6)
        if quem == 'ele':
            ele(d, x, CHAO - 6, cena_a, lado=1, cabeca_baixa=0.5 * ouviu, t=t, emo=dict(triste=0.8 * ouviu))
        elif quem == 'ela_cinza':
            personagens.DOURADO = (170, 172, 182)
            ela(d, x, CHAO - 6, cena_a, lado=1, cabeca_baixa=0.6 * ouviu, t=t + 1.3, emo=dict(triste=0.9 * ouviu))
            personagens.DOURADO = OURO0
        else:
            ela(d, x, CHAO - 6, cena_a, lado=-1, t=t, emo=dict(sorriso=0.8 * ouviu))
    big = cen.resize((int(W * K), int(H * K)), Image.BICUBIC)
    cam = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cam.paste(big, (int(W / 2 - 540 * K), int(1050 - 1010 * K)))
    im = Image.alpha_composite(fundo, cam); d2 = ImageDraw.Draw(im, 'RGBA')
    # pergunta inteira desde o quadro zero
    q = 1 - ap(t, 9.0, 0.5)
    if q > 0.02:
        d2.text((W / 2, 290), 'Por que a mesma frase', font=FQ, fill=rgba(B, q), anchor='mm')
        d2.text((W / 2, 380), 'fere uns e não outros?', font=FQ2, fill=rgba(G, q), anchor='mm')
    # o balão: aparece, se divide em três e cada cópia vai até uma cabeça
    ab = ap(t, 0.3, 0.5)
    viagem = estilo.suavizar(cl((t - 2.0) / 1.3))
    for i, (x, _, _, _, _) in enumerate(PESSOAS):
        if viagem <= 0 and i > 0: break
        alvo = tela(x, CHAO - 6 - 240)
        bx, by = lerp(BAL[0], alvo[0], viagem), lerp(BAL[1], alvo[1] - 40, viagem)
        esc = 1 - 0.6 * viagem; aa = ab * (1 - ap(t, 3.1, 0.3)) * cena_a
        if aa < 0.02: continue
        f = estilo.sem_serifa(int(42 * esc), 600)
        w2, h2 = 320 * esc, 96 * esc
        d2.rounded_rectangle((bx - w2 / 2, by - h2 / 2, bx + w2 / 2, by + h2 / 2), radius=int(40 * esc), fill=(236, 232, 224, int(245 * aa)))
        if viagem <= 0.02:
            d2.polygon([(bx - 20, by + h2 / 2 - 2), (bx + 20, by + h2 / 2 - 2), (bx, by + h2 / 2 + 26)], fill=(236, 232, 224, int(245 * aa)))
        d2.text((bx, by + 2), 'Não encaixou.', font=f, fill=(24, 22, 20, int(255 * aa)), anchor='mm')
    # o que cada um ouviu
    for x, _, linhas, cor, tq in PESSOAS:
        cab = tela(x, CHAO - 6 - 240 - 40)
        nuvem_pensamento(d2, cab[0], 790, linhas, cor, jan(t, tq, 9.6, 0.5), (cab[0], cab[1] - 20))
    f1 = jan(t, 9.8, 13.8); f2 = jan(t, 10.8, 13.8)
    if f1 > 0.02: d2.text((W / 2, 820), 'Cada um lê', font=estilo.playfair(74), fill=rgba(B, f1), anchor='mm')
    if f2 > 0.02: d2.text((W / 2, 920), 'com a dor que carrega.', font=estilo.playfair(74, True), fill=rgba(G, f2), anchor='mm')
    f3 = jan(t, 14.1, 18.6)
    if f3 > 0.02:
        for i, l in enumerate(['“O que perturba as pessoas', 'não são os fatos, mas as opiniões', 'que elas formam sobre os fatos.”']):
            d2.text((W / 2, 760 + i * 76), l, font=estilo.playfair(52, True), fill=rgba(G if i == 2 else B, f3), anchor='mm')
        d2.text((W / 2, 1040), 'Epicteto, Encheirídion, 5', font=estilo.playfair(32, True), fill=rgba(C, f3), anchor='mm')
    estilo.texto_espacado(d2, (W / 2, 1640), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(24, 500), rgba((170, 165, 158), 0.8), 6)
    ff.stdin.write(estilo.para_bytes(np.asarray(im.convert('RGB'), np.float32) * (1 - ap(t, T - 0.4, 0.4))))
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); print('ok', saida)
