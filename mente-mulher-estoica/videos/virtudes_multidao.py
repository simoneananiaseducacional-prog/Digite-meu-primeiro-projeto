"""Vídeo de outro criador + mapa das quatro virtudes (sair da multidão).
Usa só a faixa da cena (sem o texto e o logo finais do original). Crédito do vídeo na legenda.
Ou ação, ou texto (base 017): o vídeo congela quando o mapa aparece.
Uso: python3 virtudes_multidao.py video_original.mp4 saida.mp4   (o vídeo original não entra no repositório)
"""
import sys, math, subprocess, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
orig, saida = sys.argv[1], Path(sys.argv[2])
SW, SH, SY = 1080, 615, 330            # faixa da cena na tela
def ap(t, t0, d=0.4): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1): return ap(t, t0) * (1 - ap(t, t1 - 0.3, 0.3))
def cl(p): return max(0.0, min(1.0, p))
def rgba(c, a): return c + (int(255 * cl(a)),)

# lê todos os quadros da faixa, já cortados, em preto e branco suave
cmd = ['ffmpeg', '-loglevel', 'error', '-i', orig, '-t', '20', '-vf',
       f'crop=720:410:0:440,scale={SW}:{SH},hue=s=0.2,eq=brightness=-0.04:contrast=1.05', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
raw = subprocess.run(cmd, capture_output=True).stdout
FR = np.frombuffer(raw, np.uint8).reshape(-1, SH, SW, 3)
def quadro(src_t): return FR[min(len(FR) - 1, int(src_t * FPS))]

# linha do tempo: (início, fim, função tempo de saída -> tempo na fonte)
CONGELA1 = 8.0                         # a figura no meio da multidão
def fonte(t):
    if t < 8.0: return t                              # multidão e a figura saindo
    if t < 18.0: return CONGELA1 + (t - 8.0) * 0.2    # mapa das virtudes, em câmera lenta
    if t < 23.0: return 10.0 + (t - 18.0)             # beira da ponte, salto, floresta
    return 15.0 + min(t - 23.0, 4.5)                  # ela caminha na mata
T = 29.6
VIRTUDES = [('Sabedoria', 'ver a mentira', 8.6), ('Coragem', 'sair da fila', 10.9),
            ('Justiça', 'não desprezar quem ficou', 13.2), ('Temperança', 'não virar a única que enxerga', 15.5)]
LUZ = (628, SY + SH - 6)               # a linha dourada nasce embaixo da figura
F_TOP, F_TOPI = estilo.playfair(56), estilo.playfair(56, True)
F_V, F_S = estilo.playfair(44), estilo.playfair(38, True)
def txt(d, xy, s, f, cor, a, anc='mm'):
    if a > 0.01: d.text(xy, s, font=f, fill=rgba(cor, a), anchor=anc)
fundo = np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    base = fundo.copy()
    mapa = ap(t, 8.0, 0.5) * (1 - ap(t, 17.7, 0.4))
    cena = quadro(fonte(t)).astype(np.float32) * (1 - 0.2 * mapa)
    base[SY:SY + SH] = cena.astype(np.uint8)
    img = Image.fromarray(base).convert('RGBA'); cam = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
    d.rectangle((0, SY, W - 1, SY + SH), outline=rgba(G, 0.25), width=1)
    # mapa: a luz dela vira uma linha dourada que desce até as virtudes
    if mapa > 0:
        pulso = 1 + 0.25 * math.sin(t * 4)
        d.ellipse((LUZ[0] - 9 * pulso, LUZ[1] - 9 * pulso, LUZ[0] + 9 * pulso, LUZ[1] + 9 * pulso), fill=rgba(G, mapa))
        q = cl((t - 8.2) / 0.8)
        pts = []
        for i in range(31):
            u = i / 30
            x = (1 - u) ** 2 * LUZ[0] + 2 * (1 - u) * u * 520 + u * u * 150
            y = (1 - u) ** 2 * LUZ[1] + 2 * (1 - u) * u * 1010 + u * u * 1000
            pts.append((x, y))
        n = max(2, int(31 * q))
        d.line(pts[:n], fill=rgba(G, mapa), width=4, joint='curve')
        if q >= 1:
            fim_y = 1040 + 112 * (sum(1 for *_, t0 in VIRTUDES if t > t0) - 1)
            d.line([(150, 1000), (150, max(1000, fim_y))], fill=rgba(G, mapa), width=4)
        for i, (v, s, t0) in enumerate(VIRTUDES):
            a = ap(t, t0) * mapa
            y = 1040 + i * 112
            if a > 0:
                d.ellipse((150 - 9, y - 9, 150 + 9, y + 9), fill=rgba(G, a))
                txt(d, (190, y - 4), v, F_V, G, a, 'lm')
                txt(d, (190, y + 42), s, F_S, B, a, 'lm')
    # textos fora da cena
    txt(d, (W/2, 200), 'Por que é tão difícil', F_TOP, B, jan(t, 0.3, 18.0))
    txt(d, (W/2, 272), 'sair da multidão?', F_TOPI, G, jan(t, 0.8, 18.0))
    txt(d, (W/2, 1090), 'Todos seguem na mesma direção.', F_TOP, B, jan(t, 0.8, 7.9))
    txt(d, (W/2, 1175), 'Até que alguém decide sair.', F_TOPI, G, jan(t, 3.8, 7.9))
    txt(d, (W/2, 1120), 'Ela não saiu das pessoas.', F_TOP, B, jan(t, 18.6, 22.8))
    txt(d, (W/2, 1200), 'Saiu da mentira.', F_TOPI, G, jan(t, 19.1, 22.8))
    fim = 1 - ap(t, T - 0.8, 0.6)
    txt(d, (W/2, 1110), '“Justiça, verdade,', F_TOPI, G, ap(t, 23.2) * fim)
    txt(d, (W/2, 1185), 'temperança, coragem.”', F_TOPI, G, ap(t, 23.6) * fim)
    txt(d, (W/2, 1255), 'Marco Aurélio, Meditações, 3.6', estilo.playfair(30, True), C, ap(t, 24.2) * fim)
    if ap(t, 25.0) > 0:
        estilo.texto_espacado(d, (W/2, 1420), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(22, 500), rgba(C, ap(t, 25.0) * fim), 6)
    img = Image.alpha_composite(img, cam)
    out = np.asarray(img.convert('RGB'), np.float32) * (1 - ap(t, T - 0.6, 0.6)) * ap(t, 0, 0.4)
    ff.stdin.write(estilo.para_bytes(out))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); saida.with_suffix('.mudo.mp4').unlink(missing_ok=True)
print('ok')
