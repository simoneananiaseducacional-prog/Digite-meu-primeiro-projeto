"""Card estilo tweet com lista: fundo preto, foto de perfil redonda, nome e @, título, lista e fecho estoico com fonte.
Ideias inspiradas na lista de @maiconknoblauch, reescritas com palavras próprias, com linguagem neutra e ligação ao estoicismo.

    python3 card_tweet_lista.py foto_perfil.png saida.jpg   # a foto nunca vai para o repositório
"""
import sys
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo
from PIL import Image, ImageDraw

W, H = 1080, 1350
BR, CZ, G = (240, 240, 240), (140, 140, 140), estilo.DOURADO
TITULO = ['Como ser parceria, e não peso,', 'para quem você ama']
LISTA = ['Comece sem precisar de convite', 'Não fique esperando instruções', 'Perceba o que falta e faça',
         'Carregue a sua parte do peso', 'Caminhe ao lado, não pendurado', 'Enfrente os assuntos difíceis',
         'Escolham juntos o rumo', 'Troque a queixa pela ação', 'A casa também é sua: cuide dela',
         'Sonhem e organizem a vida em dupla', 'Filho não é favor, é responsabilidade',
         'Faça surpresas sem data marcada', 'Deixe suas ações falarem por você', 'Assuma seus erros sem desculpas']
FECHO = ['“Algumas coisas dependem de nós;', 'outras não dependem.”']
FONTE = 'Epicteto, Manual, 1'

foto = Image.open(sys.argv[1]).convert('RGB'); lado = min(foto.size)
foto = foto.crop(((foto.width - lado) // 2, (foto.height - lado) // 2, (foto.width + lado) // 2, (foto.height + lado) // 2))
av = foto.resize((120, 120), Image.LANCZOS)
m = Image.new('L', (480, 480), 0); ImageDraw.Draw(m).ellipse((0, 0, 479, 479), 255); m = m.resize((120, 120), Image.LANCZOS)

img = Image.new('RGB', (W, H), (10, 10, 10)); d = ImageDraw.Draw(img)
x, y = 90, 110
img.paste(av, (x, y), m)
d.text((x + 145, y + 42), 'Mente Mulher Estoica', font=estilo.sem_serifa(38, 700), fill=(245, 245, 245), anchor='lm')
d.text((x + 145, y + 86), '@mente_mulher_estoica', font=estilo.sem_serifa(30, 400), fill=CZ, anchor='lm')
y += 165
ft, fl = estilo.sem_serifa(44, 600), estilo.sem_serifa(36, 400)
for l in TITULO:
    d.text((x, y), l, font=ft, fill=BR, anchor='ls'); y += 56
y += 22
for item in LISTA:
    d.ellipse((x + 2, y - 19, x + 14, y - 7), fill=G)
    d.text((x + 34, y), item, font=fl, fill=BR, anchor='ls'); y += 50
y += 30
fi = estilo.playfair(38, italica=True)
for l in FECHO:
    d.text((x, y), l, font=fi, fill=G, anchor='ls'); y += 50
d.text((x, y + 4), FONTE, font=estilo.sem_serifa(28, 400), fill=CZ, anchor='ls')
assert y + 4 < H - 60, y
img.save(sys.argv[2], quality=95); print('ok', sys.argv[2], 'fim do texto em y =', y + 4)
