"""Story "pensamento da Simone" (modelo do card com foto, nome e caixa com borda dourada), em fonte mais leve.
A foto NÃO vai para o repositório: passe o caminho de um arquivo fora dele (scratchpad).
Uso: python3 story_pensamento.py saida.png foto.png "parágrafo 1||parágrafo 2" "Fonte linha 1|Fonte linha 2" [garamond|cormorant|playfair]
"""
import sys
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
W, H = 1080, 1920
FT = Path('/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos/fontes')
CREME, OURO, CINZA = (240, 232, 218), (201, 168, 118), (170, 162, 150)
saida, foto, texto, fonte_ref = sys.argv[1:5]
estilo_f = sys.argv[5] if len(sys.argv) > 5 else 'garamond'

def cormorant(t, peso='Regular', italico=False):
    f = ImageFont.truetype(str(FT / ('CormorantGaramond-Italic.ttf' if italico else 'CormorantGaramond.ttf')), t)
    try: f.set_variation_by_name(peso)
    except Exception: pass
    return f
def ebg(t, nome): return ImageFont.truetype(str(FT / f'EBGaramond-{nome}.ttf'), t)
if estilo_f == 'garamond':
    F_TXT, F_NOME, F_ARROBA, F_REF = ebg(70, 'Regular'), ebg(56, 'Medium'), ebg(34, 'Regular'), ebg(40, 'Italic')
    ALT = 92
elif estilo_f == 'playfair':
    F_TXT, F_NOME, F_ARROBA, F_REF = estilo.playfair(66), estilo.playfair(54), estilo.playfair(34), estilo.playfair(38, True)
    ALT = 92
else:
    F_TXT, F_NOME, F_ARROBA, F_REF = cormorant(80, 'Medium'), cormorant(62, 'SemiBold'), cormorant(38, 'Medium'), cormorant(44, 'Medium', True)
    ALT = 96

im = Image.new('RGB', (W, H), (10, 10, 10)); d = ImageDraw.Draw(im)
# cabeçalho: foto redonda com aro dourado, traço e nome
R, cx, cy = 135, 225, 370
ft = Image.open(foto).convert('RGB').resize((2 * R, 2 * R), Image.LANCZOS)
m = Image.new('L', (2 * R, 2 * R), 0); ImageDraw.Draw(m).ellipse((0, 0, 2 * R - 1, 2 * R - 1), fill=255)
im.paste(ft, (cx - R, cy - R), m)
d.ellipse((cx - R - 3, cy - R - 3, cx + R + 3, cy + R + 3), outline=OURO, width=3)
d.line([(405, cy - 90), (405, cy + 90)], fill=OURO, width=2)
d.text((445, cy - 32), 'Mente Mulher Estoica', font=F_NOME, fill=CREME, anchor='lm')
d.text((445, cy + 40), '@mente_mulher_estoica', font=F_ARROBA, fill=CINZA, anchor='lm')
# caixa
x0, x1, LARG = 55, W - 55, W - 55 * 2 - 150
def quebra(s, f):
    out, cur = [], ''
    for p in s.split():
        t = (cur + ' ' + p).strip()
        if f.getlength(t) <= LARG: cur = t
        else: out.append(cur); cur = p
    return out + [cur]
blocos = [quebra(p, F_TXT) for p in texto.split('||')]
refs = fonte_ref.split('|')
alt_txt = sum(len(b) for b in blocos) * ALT + (len(blocos) - 1) * 50
alt = 110 + alt_txt + 70 + 40 + len(refs) * 62 + 90
y0 = max(600, (H - alt) // 2 + 120); y1 = y0 + alt
d.rounded_rectangle((x0, y0, x1, y1), radius=36, fill=(16, 15, 14), outline=OURO, width=3)
y = y0 + 110
for b in blocos:
    for l in b:
        d.text((x0 + 75, y), l, font=F_TXT, fill=CREME, anchor='lm'); y += ALT
    y += 50
y += 10
d.line([(x0 + 75, y), (x0 + 255, y)], fill=OURO, width=3); y += 75
for r in refs:
    d.text((x0 + 75, y), r, font=F_REF, fill=CREME, anchor='lm'); y += 62
im.save(saida); print('ok', saida)
