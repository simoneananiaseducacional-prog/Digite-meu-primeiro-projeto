"""Carrossel de frases no estilo "destaque" que a Simone aprovou: aspas grandes, letra
Montserrat bem grossa alinhada à esquerda, trechos em dourado e, no pé, a foto dela com
"Mente Mulher Estoica" e o @. Três cores: claro, preto e vinho.

Mesmo formato de texto de carrossel_marca.py: "|" quebra a linha, *asteriscos* deixam a
linha dourada e "_" vira o crédito pequeno.

    python3 carrossel_destaque.py textos/sentir-marca.txt --tema vinho --foto foto.jpg \
        --rosto 545,480,250 --saida saida/sentir-vinho
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw

from post_frase import avatar

PASTA = Path(__file__).resolve().parent
sys.path.insert(0, str(PASTA.parent / "videos"))
import estilo  # noqa: E402

LARG, ALT = 1080, 1350
MX = 90
TEMAS = {
    "claro": dict(fundo=(250, 246, 240), texto=(92, 26, 40), aspas=(92, 26, 40), suave=(140, 110, 115)),
    "preto": dict(fundo=(11, 11, 11), texto=(242, 238, 230), aspas=estilo.DOURADO, suave=(150, 144, 136)),
    "vinho": dict(fundo=(88, 24, 36), texto=(240, 230, 212), aspas=estilo.DOURADO, suave=(200, 170, 160)),
}


def card(texto, tema, foto, rosto):
    t = TEMAS[tema]
    img = Image.new("RGB", (LARG, ALT), t["fundo"])
    d = ImageDraw.Draw(img)
    partes = texto.split("|")
    credito = [p[1:] for p in partes if p.startswith("_")]
    linhas = [p for p in partes if not p.startswith("_")]
    tam = 84
    f = estilo.sem_serifa(tam, 800)
    while max(f.getlength(l.strip("*")) for l in linhas) > LARG - 2 * MX:
        tam -= 2
        f = estilo.sem_serifa(tam, 800)
    entre = tam * 1.22
    # Aspas + frase centralizadas no espaço acima da assinatura
    bloco = 230 + entre * len(linhas) + (50 if credito else 0)
    topo = 120 + (1100 - 120 - bloco) / 2
    d.text((MX - 10, topo + 200), "“", font=estilo.sem_serifa(300, 900), fill=t["aspas"], anchor="ls")
    y = topo + 230 + tam
    for l in linhas:
        dourada = l.startswith("*") and l.endswith("*")
        d.text((MX, y), l.strip("*"), font=f, fill=estilo.DOURADO if dourada else t["texto"], anchor="ls")
        y += entre
    for c in credito:
        d.text((MX, y + 20), c, font=estilo.sem_serifa(30, 500), fill=t["suave"], anchor="ls")
    # Assinatura com a foto
    av = avatar(100, foto, rosto)
    img.paste(av, (MX, 1130), av)
    d.text((MX + 124, 1176), "Mente Mulher Estoica", font=estilo.sem_serifa(32, 600), fill=t["texto"], anchor="ls")
    d.text((MX + 124, 1186), "@mente_mulher_estoica", font=estilo.sem_serifa(26, 400), fill=t["suave"], anchor="lt")
    return img


def main():
    p = argparse.ArgumentParser(description="Carrossel estilo destaque (claro, preto ou vinho)")
    p.add_argument("texto")
    p.add_argument("--tema", choices=TEMAS, default="vinho")
    p.add_argument("--foto", required=True)
    p.add_argument("--rosto", required=True, help="x,y,raio do rosto na foto")
    p.add_argument("--saida")
    a = p.parse_args()
    rosto = tuple(int(v) for v in a.rosto.split(","))
    saida = Path(a.saida) if a.saida else PASTA / "saida" / f"{Path(a.texto).stem}-{a.tema}"
    saida.mkdir(parents=True, exist_ok=True)
    linhas = [l.strip() for l in Path(a.texto).read_text().splitlines() if l.strip()]
    for i, l in enumerate(linhas, 1):
        card(l, a.tema, a.foto, rosto).save(saida / f"{i:02d}.jpg", quality=95)
    print(f"Pronto: {len(linhas)} cards em {saida}")


if __name__ == "__main__":
    sys.exit(main())
