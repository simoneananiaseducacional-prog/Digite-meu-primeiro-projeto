"""Cards no estilo tweet: fundo preto, foto de perfil, nome com selo e frase grande (fim em dourado).

    python3 card_tweet.py caminho/da/foto.jpg   # gera tweet-1.jpg, tweet-2.jpg... na pasta atual
"""
import sys
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo
from PIL import Image, ImageDraw
W, H = 1080, 1350
foto = Image.open(sys.argv[1]).convert('RGB')  # foto de perfil: nunca vai para o repositório
fw, fh = foto.size
s = int(fw * 0.52); cx, cy = int(fw * 0.555), int(fh * 0.315)
av = foto.crop((cx - s//2, cy - s//2, cx + s//2, cy + s//2)).resize((150, 150), Image.LANCZOS)
m = Image.new('L', (600, 600), 0); ImageDraw.Draw(m).ellipse((0, 0, 599, 599), 255); m = m.resize((150, 150), Image.LANCZOS)
frases = [
 [("Quanto menos você espera dos outros,", (240,240,240)), ("menos poder eles têm sobre a sua paz.", estilo.DOURADO)],
 [("Decepção é a distância entre o que você esperava", (240,240,240)), ("e o que a pessoa podia dar.", estilo.DOURADO)],
 [("Coloque a sua energia no que depende de você.", (240,240,240)), ("O resto, deixe ir.", estilo.DOURADO)],
]
ft = estilo.sem_serifa(72, 500)
for i, partes in enumerate(frases, 1):
    img = Image.new('RGB', (W, H), (10, 10, 10)); d = ImageDraw.Draw(img)
    linhas = []
    for txt, cor in partes:
        linhas += [(l, cor) for l in estilo.quebrar_linhas(txt, ft, W - 200)]
    bloco = 150 + 70 + len(linhas) * 92
    y0 = (H - bloco) // 2
    img.paste(av, (100, y0), m)
    d.text((275, y0 + 52), "Mente Mulher Estoica", font=estilo.sem_serifa(40, 700), fill=(245,245,245), anchor="lm")
    nw = d.textlength("Mente Mulher Estoica", font=estilo.sem_serifa(40, 700))
    bx, by = 275 + nw + 26, y0 + 52
    d.ellipse((bx - 17, by - 17, bx + 17, by + 17), fill=(0, 149, 246))
    d.line((bx - 8, by, bx - 2, by + 7, bx + 9, by - 7), fill='white', width=4, joint='curve')
    d.text((275, y0 + 102), "@mente_mulher_estoica", font=estilo.sem_serifa(32, 400), fill=(140,140,140), anchor="lm")
    y = y0 + 150 + 70
    for l, cor in linhas:
        d.text((100, y + 70), l, font=ft, fill=cor, anchor="ls"); y += 92
    img.save(f"tweet-{i}.jpg", quality=95)
