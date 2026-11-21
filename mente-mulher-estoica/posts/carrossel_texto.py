"""Carrossel só de texto: fundo claro, serifa, texto alinhado à esquerda e centralizado na altura.

O arquivo de texto separa os cards com uma linha "---" e os parágrafos com linha em branco.
Parágrafo que começa com "**" sai em negrito.

    python3 carrossel_texto.py textos/limites.txt --saida saida/limites
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw

PASTA = Path(__file__).resolve().parent
sys.path.insert(0, str(PASTA.parent / "videos"))
import estilo  # noqa: E402

LARG, ALT = 1080, 1350
MX = 100
FUNDO = (244, 243, 241)
TEXTO = (22, 20, 18)
SUAVE = (150, 146, 140)
ARROBA = "@mente_mulher_estoica"


def cards(caminho):
    for bloco in Path(caminho).read_text().split("\n---\n"):
        yield [p.strip() for p in bloco.strip().split("\n\n") if p.strip()]


def desenhar(paragrafos, n, total):
    img = Image.new("RGB", (LARG, ALT), FUNDO)
    d = ImageDraw.Draw(img)
    # Card com uma frase só (capa) usa letra maior
    tam = 76 if len(paragrafos) == 1 and len(paragrafos[0]) < 90 else 58
    entre, espaco = tam * 1.22, tam * 0.9
    blocos = []
    for p in paragrafos:
        negrito = p.startswith("**")
        f = estilo.serifa(tam, 700 if negrito else 500)
        linhas = []
        for parte in p.lstrip("*").split("\n"):
            linhas += estilo.quebrar_linhas(parte, f, LARG - 2 * MX)
        blocos.append((f, linhas))
    altura = sum(len(l) * entre for _, l in blocos) + espaco * (len(blocos) - 1)
    y = (ALT - altura) / 2 + tam * 0.9  # linha de base da primeira linha
    for f, linhas in blocos:
        for l in linhas:
            d.text((MX, y), l, font=f, fill=TEXTO, anchor="ls")
            y += entre
        y += espaco
    d.text((MX, ALT - 80), ARROBA, font=estilo.sem_serifa(24, 500), fill=SUAVE, anchor="ls")
    d.text((LARG - MX, ALT - 80), f"{n}/{total}", font=estilo.sem_serifa(24, 500), fill=SUAVE, anchor="rs")
    return img


def main():
    p = argparse.ArgumentParser(description="Carrossel só de texto, fundo claro")
    p.add_argument("texto")
    p.add_argument("--saida")
    a = p.parse_args()
    saida = Path(a.saida) if a.saida else PASTA / "saida" / Path(a.texto).stem
    saida.mkdir(parents=True, exist_ok=True)
    todos = list(cards(a.texto))
    for i, c in enumerate(todos, 1):
        desenhar(c, i, len(todos)).save(saida / f"{i:02d}.jpg", quality=95)
    print(f"Pronto: {len(todos)} cards em {saida}")


if __name__ == "__main__":
    sys.exit(main())
