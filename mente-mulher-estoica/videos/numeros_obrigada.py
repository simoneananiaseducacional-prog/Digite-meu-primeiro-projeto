"""Reels de agradecimento (v2): abre com o vídeo de quase 100 mil e seus números reais, depois os outros,
depois palavras salpicadas do propósito da página, e o agradecimento. Uso: python3 numeros_obrigada.py saida.mp4
Números de 15/11/2026 (prints da Simone). Atualizar antes de postar se mudarem.
"""
import sys, math, random
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia, numpy as np
from PIL import Image, ImageDraw
from pathlib import Path
W, H, FPS, T = 1080, 1920, 30, 24.0
B, G, C = estilo.BRANCO, estilo.DOURADO, (150, 146, 140)
TX = (205, 200, 194)
def ap(t, t0, d=0.5): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.5): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
def rgba(c, a): return c + (int(255 * max(0, min(1, a))),)
fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')

VIEWS = 98684
STATS = [('8 mil', 'curtidas'), ('1,5 mil', 'salvamentos'), ('1,2 mil', 'envios'), ('1 mil', 'reposts'), ('506', 'novos seguidores')]
OUTROS = [('43 mil', 'para onde vai a sua energia', 300, 640), ('42,3 mil', 'o próximo passo', 790, 780),
          ('38,7 mil', 'a ponte', 280, 940), ('22,2 mil', 'a borracha', 780, 1080), ('10,2 mil', 'a coragem', 320, 1220)]
PALAVRAS = ['tirar o véu', 'quebrar ciclos', 'enxergar além da cortina', 'procurar a verdade', 'evoluir',
            'consciência', 'virar a chave', 'coragem', 'autoconhecimento', 'liberdade', 'clareza', 'recomeçar']
random.seed(3)
LUG = [(300, 520), (800, 600), (540, 760), (340, 900), (820, 980), (520, 1120), (280, 1270), (790, 1330),
       (540, 1460), (330, 660), (800, 1200), (540, 600)]

saida = Path(sys.argv[1]); ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    im = fundo.copy(); d = ImageDraw.Draw(im, 'RGBA')
    # 1) um único vídeo
    a = jan(t, 0.2, 7.6)
    if a > 0.02:
        d.text((W/2, 560), 'Um único vídeo.', font=estilo.playfair(64), fill=rgba(B, a * ap(t, 0.2)), anchor='mm')
        n = int(VIEWS * estilo.suavizar(min(1, max(0, (t - 1.2) / 2.2))))
        if t > 1.2:
            d.text((W/2, 720), f'{n:,}'.replace(',', '.'), font=estilo.playfair(130), fill=rgba(G, a), anchor='mm')
            d.text((W/2, 830), 'visualizações', font=estilo.sem_serifa(40, 500), fill=rgba(TX, a), anchor='mm')
        for i, (num, lab) in enumerate(STATS):
            sa = ap(t, 3.8 + i * 0.5, 0.4) * a
            if sa < 0.02: continue
            y = 990 + i * 92
            d.text((W/2 - 20, y), num, font=estilo.sem_serifa(50, 700), fill=rgba(B, sa), anchor='rm')
            d.text((W/2 + 10, y), lab, font=estilo.sem_serifa(42, 400), fill=rgba(TX, sa), anchor='lm')
    # 2) e não foi o único
    b = jan(t, 7.8, 12.8)
    if b > 0.02:
        d.text((W/2, 460), 'E não foi o único.', font=estilo.playfair(64, True), fill=rgba(B, b), anchor='mm')
        for i, (num, tema, x, y) in enumerate(OUTROS):
            p = ap(t, 8.5 + i * 0.55, 0.4) * b
            if p < 0.02: continue
            d.text((x, y), num, font=estilo.playfair(88), fill=rgba(G, p), anchor='mm')
            d.text((x, y + 66), tema, font=estilo.sem_serifa(30, 500), fill=rgba(TX, p), anchor='mm')
    # 3) palavras salpicadas
    for i, (w, (x, y)) in enumerate(zip(PALAVRAS, LUG)):
        t0 = 13.0 + i * 0.32
        p = jan(t, t0, 18.4, 0.35)
        if p < 0.02: continue
        dourada = i % 3 == 0
        f = estilo.playfair(60, True) if dourada else estilo.sem_serifa(44, 500)
        d.text((x, y - 10 * (1 - ap(t, t0, 0.4))), w, font=f, fill=rgba(G if dourada else B, p), anchor='mm')
    # 4) agradecimento
    c = jan(t, 18.6, 23.6)
    if c > 0.02:
        for i, l in enumerate(['Ainda existem pessoas', 'que procuram a verdade.']):
            d.text((W/2, 760 + i * 84), l, font=estilo.playfair(66), fill=rgba(B, c), anchor='mm')
        c2 = jan(t, 19.8, 23.6)
        d.text((W/2, 1010), 'Obrigada por ser uma delas.', font=estilo.playfair(62, True), fill=rgba(G, c2), anchor='mm')
        c3 = jan(t, 20.6, 23.6)
        if c3 > 0.02: estilo.texto_espacado(d, (W/2, 1200), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(26, 500), rgba(C, c3), 6)
    ff.stdin.write(estilo.para_bytes(np.asarray(im.convert('RGB'), np.float32) * (1 - ap(t, T - 0.3, 0.3))))
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); print('ok')
