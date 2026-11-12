"""Reels teste (série Estoicos sem saber): Senna em 5 cenas, fotos livres do Commons com zoom lento.
Uso: python3 senna_reels.py saida.mp4   (sem áudio: a música entra no Instagram)
"""
import sys, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw, ImageOps
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
FOTOS = Path(__file__).parent.parent / 'posts' / 'fotos_terceiros'
saida = Path(sys.argv[1])
fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGB')

def ap(t, t0, d=0.6): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def carregar(nome):
    f = ImageOps.autocontrast(Image.open(FOTOS / nome).convert('L'), cutoff=1)
    return f.convert('RGB')
F1, F2 = carregar('senna_1993_martin_lee.jpg'), carregar('senna_instituto.jpg')
def foto_zoom(f, larg, alt, z, cy=0.3):
    esc = max(larg / f.width, alt / f.height) * z
    g = f.resize((round(f.width * esc), round(f.height * esc)), Image.LANCZOS)
    x = (g.width - larg) // 2; y = int((g.height - alt) * cy)
    return g.crop((x, y, x + larg, y + alt))
def texto(d, y, linhas, f, cor, a, alt):
    for i, l in enumerate(linhas):
        d.text((W/2, y + i * alt + 20 * (1 - a)), l, font=f, fill=cor + (int(255 * a),), anchor='mm')
def moldura(im, d, f, x, y, larg, alt, z, a):
    ph = foto_zoom(f, larg, alt, z)
    im.paste(Image.blend(Image.new('RGB', ph.size, (12, 12, 12)), ph, a), (x, y))
    d.rectangle((x - 14, y - 14, x + larg + 13, y + alt + 13), outline=G + (int(255 * a),), width=2)

# cenas: (início, duração)
CENAS = [(0, 6), (6, 5.5), (11.5, 5.5), (17, 5), (22, 6)]
T = 28.0
P = estilo.playfair
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    im = fundo.copy(); d = ImageDraw.Draw(im, 'RGBA')
    for n, (t0, dur) in enumerate(CENAS):
        if not (t0 <= t < t0 + dur): continue
        s = t - t0; sai = 1 - ap(s, dur - 0.5, 0.5); a = lambda x: ap(s, x) * sai
        if n == 0:
            d.line([(160, 330), (920, 330)], fill=G + (int(255 * a(0)),), width=2)
            texto(d, 395, ['AYRTON SENNA', 'VIVEU SÓ 34 ANOS.'], P(66), B, a(0.1), 80)
            d.line([(160, 520), (920, 520)], fill=G + (int(255 * a(0)),), width=2)
            moldura(im, d, F1, 220, 570, 640, 780, 1 + 0.06 * s / dur, a(0.4))
            texto(d, 1440, ['Mas não desperdiçou um dia.'], P(58, True), G, a(2.4), 0)
        elif n == 1:
            texto(d, 700, ['Treinava até a exaustão.', 'Conhecia cada curva', 'antes de correr.'], P(64), B, a(0.1), 86)
            texto(d, 1030, ['“Nenhuma grande coisa', 'nasce de repente.”'], P(60, True), G, a(2.2), 80)
            texto(d, 1210, ['Epicteto, Discursos, 1.15'], P(34, True), C, a(2.6), 0)
        elif n == 2:
            texto(d, 660, ['Dava tudo de si.', 'Mas o carro, a chuva', 'e a sorte', 'não dependiam dele.'], P(64), B, a(0.1), 86)
            texto(d, 1080, ['“Algumas coisas dependem', 'de nós; outras, não.”'], P(56, True), G, a(2.2), 78)
            texto(d, 1250, ['Epicteto, Encheirídion, 1'], P(34, True), C, a(2.6), 0)
        elif n == 3:
            texto(d, 820, ['“Não recebemos', 'uma vida curta.'], P(76), B, a(0.1), 98)
            texto(d, 1030, ['Nós a tornamos curta.”'], P(76, True), G, a(1.6), 0)
            texto(d, 1180, ['Sêneca, Sobre a brevidade da vida, 1.4'], P(34, True), C, a(2.2), 0)
        else:
            moldura(im, d, F2, 330, 360, 420, 500, 1 + 0.05 * s / dur, a(0))
            texto(d, 1010, ['Se a sua vida', 'fosse curta como a dele,'], P(62), B, a(0.6), 82)
            texto(d, 1200, ['em que você pararia', 'de desperdiçar tempo?'], P(62, True), G, a(1.8), 82)
            estilo.texto_espacado(d, (W/2, 1420), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(26, 500), C, 6)
    # crédito das fotos, discreto, nas cenas com foto
    if t < 6 or t >= 22:
        cred = 'Foto: Martin Lee, CC BY-SA 2.0, Wikimedia Commons' if t < 6 else 'Foto: Instituto Ayrton Senna, CC BY 2.0, Wikimedia Commons'
        d.text((W/2, 1560), cred + ' (recortada, P&B)', font=estilo.sem_serifa(18, 400), fill=C + (150,), anchor='mm')
    ff.stdin.write(estilo.para_bytes(np.asarray(im, np.float32) * (1 - ap(t, T - 0.8, 0.8))))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida)
print('ok', saida)
