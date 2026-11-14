"""Reels de agradecimento (v3, roteiro da Simone): números concentrados na abertura, com recortes reais
dos prints de insights; depois a reflexão. Uso: python3 numeros_obrigada.py prints.jpg saida.mp4
(prints.jpg = print da lista de reels; os recortes ficam só na saída, não vão para o repositório.)
"""
import sys
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia, numpy as np
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, (150, 146, 140)
TX = (205, 200, 194)
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.5): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
def rgba(c, a): return c + (int(255 * max(0, min(1, a))),)
fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')

src = Image.open(sys.argv[1]).convert('RGB')
LIN = [(55, 250), (272, 467), (489, 684), (706, 901), (923, 1118)]
REC = []
for a, b in LIN:
    r = src.crop((30, a, 1179, b)).resize((960, int(960 * (b - a) / 1149)), Image.LANCZOS).convert('RGBA')
    m = Image.new('L', r.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, r.width - 1, r.height - 1), 22, fill=255)
    r.putalpha(m); REC.append(r)

# (início, fim, linhas, linha dourada opcional)
TEXTOS = [
    (0.3, 9.0, ['Um único vídeo,', 'quase 100 mil visualizações.'], None),
    (4.4, 9.0, ['Oito mil curtidas.', 'Mais de mil republicações.'], 'baixo'),
    (9.2, 20.4, ['E outros conteúdos também', 'chegando a milhares de pessoas…'], None),
    (20.6, 24.4, ['E sabe o que', 'me deixa feliz nisso?'], None),
    (24.6, 30.0, ['Ver tanta gente se interessando', 'por assuntos que nos fazem', 'olhar para a própria vida.'], None),
    (36.4, 41.0, ['Buscar a verdade,', 'inclusive quando ela exige', 'mudar de ideia.'], None),
    (41.2, 46.4, ['Talvez você encontre aqui palavras', 'para algo que está vivendo.', 'Ou uma pergunta', 'que ainda não tinha feito.'], None),
    (46.6, 53.0, ['É muito bom encontrar vocês', 'nesse caminho de reflexão,', 'conhecimento e mudança.'], None),
]
TRES = ['Enxergar o que antes passava despercebido.', 'Questionar o que parecia normal.', 'Reconhecer ciclos que não queremos mais repetir.']
PAL = ['Enxergar além das aparências', 'Reconhecer padrões', 'Romper ciclos', 'Rever certezas', 'Escolher com consciência']
T = 53.4
F = estilo.playfair(60); FI = estilo.playfair(60, True)

def rec(im, r, cx, cy, a):
    if a < 0.02: return
    r2 = r.copy(); r2.putalpha(r.getchannel('A').point(lambda v: int(v * a)))
    borda = Image.new('RGBA', (r2.width + 6, r2.height + 6), (0, 0, 0, 0))
    ImageDraw.Draw(borda).rounded_rectangle((0, 0, borda.width - 1, borda.height - 1), 24, outline=rgba(G, a), width=3)
    borda.alpha_composite(r2, (3, 3))
    im.alpha_composite(borda, (int(cx - borda.width / 2), int(cy - borda.height / 2)))

saida = Path(sys.argv[2]); ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    im = fundo.copy()
    # abertura: o print do vídeo de 99 mil
    rec(im, REC[0], W / 2, 900, jan(t, 0.8, 9.0))
    # os outros quatro, um por vez, cada um com uma palavra salpicada
    for i in range(4):
        t0 = 11.0 + i * 2.2
        rec(im, REC[i + 1], W / 2, 660 + i * 170, jan(t, t0, 20.4))
    d = ImageDraw.Draw(im, 'RGBA')
    for i, w in enumerate(PAL):
        t0 = 11.6 + i * 1.9
        a = jan(t, t0, 20.4)
        if a > 0.02:
            pos = [(310, 1360), (790, 1360), (310, 1440), (790, 1440), (W / 2, 1520)][i]
            d.text(pos, w, font=estilo.playfair(38, True), fill=rgba(G, a), anchor='mm')
    for t0, t1, linhas, extra in TEXTOS:
        a = jan(t, t0, t1)
        if a < 0.02: continue
        y0 = 1180 if extra == 'baixo' else (430 if t0 < 21 else 860 - len(linhas) * 40)
        if t0 < 1: y0 = 520
        for j, l in enumerate(linhas):
            d.text((W / 2, y0 + j * 78), l, font=F, fill=rgba(B, a), anchor='mm')
    for j, l in enumerate(TRES):
        a = jan(t, 30.2 + j * 1.6, 36.2)
        if a > 0.02:
            d.text((W / 2, 760 + j * 120), l, font=estilo.playfair(48, j == 2), fill=rgba(G if j == 2 else B, a), anchor='mm')
    a = ap(t, 48.6, 0.6)
    if a > 0.02: estilo.texto_espacado(d, (W / 2, 1180), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(26, 500), rgba(C, a * (1 - ap(t, 53.0, 0.4))), 6)
    ff.stdin.write(estilo.para_bytes(np.asarray(im.convert('RGB'), np.float32) * (1 - ap(t, T - 0.3, 0.3))))
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); print('ok')
