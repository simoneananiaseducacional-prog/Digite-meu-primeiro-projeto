"""Post de frase autoral no formato "citação de perfil": aspas grandes, frase em serifa,
linha fina e, embaixo, o avatar da Soberana com o nome do perfil.

Fundo preto com aspas douradas (padrão da marca) ou, com --claro, fundo off-white.

    python3 post_frase.py "Se a sua paz depende do humor de alguém, ela não é paz. É aluguel."
    python3 post_frase.py "..." --claro --saida saida/frase-clara.jpg
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw

PASTA = Path(__file__).resolve().parent
sys.path.insert(0, str(PASTA.parent / "videos"))
import estilo  # noqa: E402

LARG, ALT = 1080, 1350
MX = 90
AVATAR = PASTA.parent / "personagem" / "soberana-busto.png"
ROSTO = (530, 400, 230)  # centro x, centro y e raio do rosto em soberana-busto.png
NOME = "Mente Mulher Estoica"
ARROBA = "@mente_mulher_estoica"


def avatar(tam, foto=AVATAR, rosto_xyr=ROSTO):
    """Recorta o rosto (centro x, centro y, raio) da foto em um círculo."""
    cx, cy, r = rosto_xyr
    rosto = Image.open(foto).convert("RGB").crop((cx - r, cy - r, cx + r, cy + r)).resize((tam, tam), Image.LANCZOS)
    mascara = Image.new("L", (tam * 4, tam * 4), 0)
    ImageDraw.Draw(mascara).ellipse((0, 0, tam * 4, tam * 4), fill=255)
    rosto.putalpha(mascara.resize((tam, tam), Image.LANCZOS))
    return rosto


def gerar(frase, saida, claro=False):
    fundo, texto, suave, linha = ((242, 238, 230), (22, 20, 18), (110, 104, 96), (190, 182, 170)) if claro else \
        (estilo.PRETO, estilo.BRANCO, estilo.CINZA, (60, 56, 50))
    img = Image.new("RGB", (LARG, ALT), fundo)
    d = ImageDraw.Draw(img)

    # Frase: o maior tamanho que caiba em até 7 linhas
    for tam in range(92, 50, -2):
        f = estilo.serifa(tam, 500)
        linhas = estilo.quebrar_linhas(frase, f, LARG - 2 * MX)
        if len(linhas) <= 7:
            break
    entre = tam * 1.12
    y_linha = 1030
    # Aspas + frase centralizadas no espaço acima da linha
    bloco = 130 + entre * len(linhas)
    aspas_y = (y_linha - bloco) / 2 + 150
    d.text((MX - 12, aspas_y), "“", font=estilo.serifa(440, 600), fill=estilo.DOURADO, anchor="ls")
    y = aspas_y + 20
    for l in linhas:
        d.text((MX, y), l, font=f, fill=texto, anchor="lt")
        y += entre

    # Linha e assinatura do perfil
    d.line((MX, y_linha, LARG - MX, y_linha), fill=linha, width=2)
    tam_av = 110
    img.paste(av := avatar(tam_av), (MX, y_linha + 50), av)
    tx = MX + tam_av + 26
    d.text((tx, y_linha + 50 + tam_av / 2 - 4), NOME, font=estilo.sem_serifa(34, 600), fill=texto, anchor="ls")
    d.text((tx, y_linha + 50 + tam_av / 2 + 6), ARROBA, font=estilo.sem_serifa(28, 400), fill=suave, anchor="lt")

    saida.parent.mkdir(parents=True, exist_ok=True)
    img.save(saida, quality=95)
    return saida


def main():
    p = argparse.ArgumentParser(description="Post de frase autoral com avatar do perfil")
    p.add_argument("frase")
    p.add_argument("--claro", action="store_true", help="fundo off-white em vez de preto")
    p.add_argument("--saida")
    a = p.parse_args()
    saida = Path(a.saida) if a.saida else PASTA / "saida" / "post-frase.jpg"
    print(f"Pronto: {gerar(a.frase, saida, a.claro)}")


if __name__ == "__main__":
    sys.exit(main())
