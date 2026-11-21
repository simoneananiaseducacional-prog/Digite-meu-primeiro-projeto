"""Fábula: a navegadora e a bússola (metáfora do curso de psicanálise da Simone).
Desenho: mar em movimento, dois barcos, bússola, rotas que se separam. Ou ação, ou texto (base 017).
Uso: python3 navegadora.py saida.mp4 (vídeo mudo)
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
C2 = (175, 175, 175)
saida = Path(sys.argv[1])
fundo = np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)
def ap(t, t0, d=0.4): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1): return ap(t, t0) * (1 - ap(t, t1 - 0.3, 0.3))
def cl(p): return max(0.0, min(1.0, p))
def lerp(a, b, p): return a + (b - a) * p
def rgba(c, a): return c + (int(255 * cl(a)),)
T = 32.6

def barco(d, x, y, cor, a):
    if a <= 0.01: return
    casco = [(x - 110, y - 10), (x + 120, y - 10), (x + 85, y + 34), (x - 80, y + 34)]
    d.polygon(casco, fill=(22, 22, 22, int(255 * a)))
    d.line(casco + [casco[0]], fill=rgba(cor, a), width=5, joint='curve')
    d.line([(x, y - 10), (x, y - 190)], fill=rgba(cor, a), width=5)
    vela = [(x + 6, y - 185), (x + 6, y - 30), (x + 105, y - 30)]
    d.polygon(vela, fill=(22, 22, 22, int(255 * a)))
    d.line(vela + [vela[0]], fill=rgba(cor, a), width=4, joint='curve')
    d.line([(x - 6, y - 165), (x - 6, y - 40), (x - 80, y - 40), (x - 6, y - 165)], fill=rgba(cor, a), width=4, joint='curve')
    d.line([(x - 110, y + 2), (x - 132, y + 26)], fill=rgba(cor, a), width=5)   # leme

def bussola(d, x, y, a, t):
    if a <= 0.01: return
    d.ellipse((x - 34, y - 34, x + 34, y + 34), outline=rgba(G, a), width=4)
    ang = -math.pi / 2 + 0.25 * math.sin(t * 1.5)
    p = (x + 26 * math.cos(ang), y + 26 * math.sin(ang)); q = (x - 18 * math.cos(ang), y - 18 * math.sin(ang))
    d.polygon([p, (x + 7 * math.cos(ang + math.pi / 2), y + 7 * math.sin(ang + math.pi / 2)), q,
               (x + 7 * math.cos(ang - math.pi / 2), y + 7 * math.sin(ang - math.pi / 2))], fill=rgba(G, a))

def farol(d, x, y, cor, a):
    if a <= 0.01: return
    d.polygon([(x - 16, y), (x + 16, y), (x + 9, y - 70), (x - 9, y - 70)], outline=rgba(cor, a))
    d.line([(x - 16, y), (x + 16, y), (x + 9, y - 70), (x - 9, y - 70), (x - 16, y)], fill=rgba(cor, a), width=4)
    d.ellipse((x - 9, y - 92, x + 9, y - 74), fill=rgba(cor, a))

# linha do tempo das ações
ENTRA1, JUNTA, SEPARA, TENTA, AFASTA = 4.3, 9.7, 11.0, 16.4, 22.0
def posicoes(t):
    x1 = lerp(-160, 300, estilo.suavizar(cl((t - ENTRA1) / 1.0))); y1 = 1040
    x2 = lerp(-160, 300, estilo.suavizar(cl((t - JUNTA) / 1.0))); y2 = 1290
    s = estilo.suavizar(cl((t - SEPARA) / 1.2)); f = estilo.suavizar(cl((t - AFASTA) / 1.0))
    x1 += 120 * s + 100 * f; y1 -= 50 * s + 40 * f
    x2 += 120 * s + 100 * f; y2 += 50 * s + 50 * f
    return (x1, y1), (x2, y2)

def txt(d, y, s, f, cor, a):
    if a > 0.01: d.text((W/2, y), s, font=f, fill=rgba(cor, a), anchor='mm')
F1, F2 = estilo.playfair(56), estilo.playfair(56, True)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    img = Image.fromarray(fundo).convert('RGBA'); cam = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
    fim = 1 - ap(t, T - 0.8, 0.6)
    am = ap(t, 0.2, 1.0) * fim
    for i, y0 in enumerate(range(1000, 1420, 60)):          # o mar sempre se mexe
        pts = [(x, y0 + 7 * math.sin(x / 70 + t * 1.6 + i)) for x in range(60, 1021, 15)]
        d.line(pts, fill=rgba(C, 0.28 * am), width=2)
    (x1, y1), (x2, y2) = posicoes(t)
    bob1, bob2 = 6 * math.sin(t * 2), 6 * math.sin(t * 2 + 1.4)
    # rotas: no começo paralelas, depois cada uma para o seu porto
    sep = estilo.suavizar(cl((t - SEPARA) / 1.2))
    a_r = ap(t, JUNTA + 1.0, 0.6) * fim
    portoA, portoB = (1000, lerp(1170, 960, sep)), (1000, lerp(1170, 1400, sep))
    farol(d, *portoA, G, a_r); farol(d, portoB[0], portoB[1], C2, a_r * sep)
    for (bx, by), (px, py), cor in (((x1 + 120, y1 + bob1), portoA, G), ((x2 + 120, y2 + bob2), portoB, C2)):
        if a_r > 0:
            n = 24
            for j in range(0, n, 2):
                u0, u1 = j / n, (j + 1) / n
                d.line([(lerp(bx, px - 20, u0), lerp(by, py, u0)), (lerp(bx, px - 20, u1), lerp(by, py, u1))], fill=rgba(cor, 0.6 * a_r), width=3)
    # corda entre os barcos: estica e se desfaz no fim
    a_c = ap(t, JUNTA + 0.8, 0.5) * (1 - ap(t, AFASTA + 0.3, 0.7)) * fim
    if a_c > 0:
        tensao = cl((t - SEPARA) / 6)
        meio = ((x1 + x2) / 2 - 60 * (1 - tensao), (y1 + y2) / 2)
        d.line([(x1 - 40, y1 + 10 + bob1), meio, (x2 - 40, y2 - 160 + bob2)], fill=rgba(C2, a_c), width=3, joint='curve')
    # ela tenta assumir o leme do outro: a linha dourada não alcança e se apaga
    q = cl((t - TENTA) / 0.7); some = 1 - ap(t, TENTA + 0.7, 0.4)
    if TENTA < t < TENTA + 1.2:
        ini = (x1 - 110, y1 + 20 + bob1); alvo = (x2 - 132, y2 + 26 + bob2)
        n = 20
        for j in range(0, int(n * q), 2):
            u0, u1 = j / n, (j + 1) / n
            p0 = (lerp(ini[0], alvo[0], u0) - 90 * math.sin(math.pi * u0), lerp(ini[1], alvo[1], u0))
            p1 = (lerp(ini[0], alvo[0], u1) - 90 * math.sin(math.pi * u1), lerp(ini[1], alvo[1], u1))
            d.line([p0, p1], fill=rgba(G, some), width=4)
    barco(d, x1, y1 + bob1, G, ap(t, ENTRA1, 0.3) * fim)
    barco(d, x2, y2 + bob2, C2, ap(t, JUNTA, 0.3) * fim)
    bussola(d, x1 + 55, y1 - 250 + bob1, ap(t, 5.4, 0.6) * fim, t)
    # textos no topo (só quando a cena está parada)
    txt(d, 470, 'Dá para navegar juntos', F1, B, jan(t, 0.3, 4.3)); txt(d, 550, 'rumo a portos diferentes?', F2, G, jan(t, 0.6, 4.3))
    txt(d, 470, 'Ela navegava guiada', F1, B, jan(t, 5.4, 9.6)); txt(d, 550, 'pela bússola dos seus valores.', F2, G, jan(t, 5.7, 9.6))
    txt(d, 470, 'Mas nem sempre olhavam', F1, B, jan(t, 12.3, 16.3)); txt(d, 550, 'para o mesmo horizonte.', F2, C2, jan(t, 12.6, 16.3))
    txt(d, 470, 'Ela podia conduzir o próprio barco.', F1, B, jan(t, 17.7, 21.9)); txt(d, 550, 'Não o leme do outro.', F2, G, jan(t, 18.0, 21.9))
    txt(d, 470, 'Dois barcos só navegam juntos', F1, B, jan(t, 23.1, 27.1)); txt(d, 550, 'quando os dois escolhem o porto.', F2, G, jan(t, 23.4, 27.1))
    txt(d, 470, '“Se não sabes para que porto navegas,', estilo.playfair(48, True), G, ap(t, 27.2) * fim)
    txt(d, 540, 'nenhum vento é favorável.”', estilo.playfair(48, True), G, ap(t, 27.5) * fim)
    txt(d, 605, 'Sêneca, Cartas a Lucílio, 71', estilo.playfair(30, True), C, ap(t, 27.9) * fim)
    if ap(t, 28.2) > 0:
        estilo.texto_espacado(d, (W/2, 1450), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(22, 500), rgba(C, ap(t, 28.2) * fim), 6)
    img = Image.alpha_composite(img, cam)
    q2 = np.asarray(img.convert('RGB'), np.float32) * (1 - ap(t, T - 0.6, 0.6))
    ff.stdin.write(estilo.para_bytes(q2))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida); saida.with_suffix('.mudo.mp4').unlink(missing_ok=True)
print('ok')
