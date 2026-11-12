"""Carrossel 5 telas: Senna e o estoicismo.
Capa com foto livre do Wikimedia Commons (Martin Lee, CC BY-SA 2.0), moldura no estilo da página.
Tela 5 com foto do Instituto Ayrton Senna (CC BY 2.0).
Uso: python3 carrossel_senna.py pasta_saida
"""
import sys
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, numpy as np
from PIL import Image, ImageDraw
from pathlib import Path
W, H = 1080, 1350
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
fundo = np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)[285:285 + H]
def tela(n):
    im = Image.fromarray(fundo).convert('RGB'); d = ImageDraw.Draw(im)
    d.text((W/2, H - 70), f'{n}/5', font=estilo.playfair(26), fill=C, anchor='mm')
    return im, d
def bloco(d, y, linhas, f, cor, alt):
    for i, l in enumerate(linhas): d.text((W/2, y + i * alt), l, font=f, fill=cor, anchor='mm')
FOTOS = Path(__file__).parent / 'fotos_terceiros'
def foto(nome, larg, alt, cy=0.35):
    f = Image.open(FOTOS / nome).convert('L')
    esc = max(larg / f.width, alt / f.height); f = f.resize((round(f.width * esc), round(f.height * esc)), Image.LANCZOS)
    x = (f.width - larg) // 2; y = int((f.height - alt) * cy)
    f = f.crop((x, y, x + larg, y + alt))
    from PIL import ImageOps
    return ImageOps.autocontrast(f, cutoff=1).convert('RGB')
def linhas_douradas(d, y, larg):
    d.line([(W/2 - larg/2, y), (W/2 + larg/2, y)], fill=G, width=2)
def moldura(im, d, img, x, y):
    im.paste(img, (x, y))
    d.rectangle((x - 14, y - 14, x + img.width + 13, y + img.height + 13), outline=G, width=2)

im, d = tela(1)
linhas_douradas(d, 80, 760)
bloco(d, 140, ['AYRTON SENNA', 'VIVEU SÓ 34 ANOS.'], estilo.playfair(62), B, 76)
linhas_douradas(d, 275, 760)
moldura(im, d, foto('senna_1993_martin_lee.jpg', 640, 740, 0.25), (W - 640) // 2, 315)
d.text((W/2, 1125), 'Mas não desperdiçou um dia.', font=estilo.playfair(56, True), fill=G, anchor='mm')
linhas_douradas(d, 1175, 420)
estilo.texto_espacado(d, (W/2, 1208), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(24, 500), C, 6)
linhas_douradas(d, 1241, 420)
d.text((W - 40, 1325), 'Foto: Martin Lee (recortada, P&B), CC BY-SA 2.0, via Wikimedia Commons', font=estilo.sem_serifa(16, 400), fill=C, anchor='rm')
im.save(out / '1.png')

im, d = tela(2)
bloco(d, 430, ['Treinava até a exaustão.', 'Conhecia cada curva', 'antes de correr.'], estilo.playfair(62), B, 82)
d.line([(W/2 - 50, 680), (W/2 + 50, 680)], fill=G, width=2)
bloco(d, 790, ['“Nenhuma grande coisa', 'nasce de repente.”'], estilo.playfair(58, True), G, 78)
d.text((W/2, 960), 'Epicteto, Discursos, 1.15', font=estilo.playfair(32, True), fill=C, anchor='mm')
im.save(out / '2.png')

im, d = tela(3)
bloco(d, 400, ['Dava tudo de si.', 'Mas o carro, a chuva', 'e a sorte', 'não dependiam dele.'], estilo.playfair(62), B, 82)
d.line([(W/2 - 50, 720), (W/2 + 50, 720)], fill=G, width=2)
bloco(d, 830, ['“Algumas coisas dependem', 'de nós; outras, não.”'], estilo.playfair(56, True), G, 76)
d.text((W/2, 1000), 'Epicteto, Encheirídion, 1', font=estilo.playfair(32, True), fill=C, anchor='mm')
im.save(out / '3.png')

im, d = tela(4)
bloco(d, 540, ['“Agarre o dia de hoje', 'e você dependerá menos'], estilo.playfair(66), B, 88)
d.text((W/2, 740), 'do amanhã.”', font=estilo.playfair(72, True), fill=G, anchor='mm')
d.text((W/2, 890), 'Sêneca, Cartas a Lucílio, 1.2 (tradução livre)', font=estilo.playfair(32, True), fill=C, anchor='mm')
im.save(out / '4.png')

im, d = tela(5)
moldura(im, d, foto('senna_instituto.jpg', 380, 440, 0.2), (W - 380) // 2, 150)
bloco(d, 720, ['Se a sua vida', 'fosse curta como a dele,'], estilo.playfair(58), B, 76)
bloco(d, 900, ['em que você pararia', 'de desperdiçar tempo?'], estilo.playfair(58, True), G, 76)
d.text((W - 40, 1325), 'Foto: Instituto Ayrton Senna (recortada, P&B), CC BY 2.0, via Wikimedia Commons', font=estilo.sem_serifa(16, 400), fill=C, anchor='rm')
estilo.texto_espacado(d, (W/2, 1120), '@MENTE_MULHER_ESTOICA', estilo.sem_serifa(26, 500), C, 6)
im.save(out / '5.png')
print('ok')
