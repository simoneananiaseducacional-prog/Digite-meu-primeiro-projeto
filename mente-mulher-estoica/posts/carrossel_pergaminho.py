"""Carrossel de frases em papel envelhecido: serifa grande, centralizada, tinta quase preta.

Cada linha do arquivo vira um card; "|" quebra a linha e um trecho começando com "_"
vira a linha pequena de crédito no pé da frase.

    python3 carrossel_pergaminho.py textos/sentir.txt --saida saida/sentir
"""

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

PASTA = Path(__file__).resolve().parent
sys.path.insert(0, str(PASTA.parent / "videos"))
import estilo  # noqa: E402

LARG, ALT = 1080, 1350
TINTA = (28, 24, 20)
CREDITO = (110, 96, 78)


def papel(semente=3):
    """Papel bege com manchas suaves, bordas queimadas e fibras finas."""
    rng = np.random.default_rng(semente)
    base = np.array((236, 222, 196), np.float32)
    manchas = Image.fromarray((rng.random((27, 34)) * 255).astype(np.uint8)).resize((LARG, ALT), Image.BICUBIC)
    m = np.asarray(manchas.filter(ImageFilter.GaussianBlur(30)), np.float32)[..., None] / 255
    img = base * (0.93 + 0.08 * m)
    yy, xx = np.mgrid[0:ALT, 0:LARG].astype(np.float32)
    d = np.sqrt(((xx - LARG / 2) / (LARG * 0.62)) ** 2 + ((yy - ALT / 2) / (ALT * 0.62)) ** 2)
    img *= (1 - 0.22 * np.clip(d - 0.55, 0, 1) ** 1.5)[..., None]
    img += rng.normal(0, 3.0, (ALT, LARG, 1))
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))


def card(texto, fundo):
    img = fundo.copy()
    d = ImageDraw.Draw(img)
    partes = texto.split("|")
    credito = [p[1:] for p in partes if p.startswith("_")]
    linhas = [p for p in partes if not p.startswith("_")]
    tam = 124 if len(linhas) <= 3 else 98
    f = estilo.serifa(tam, 600)
    while max(f.getlength(l) for l in linhas) > LARG - 160:
        tam -= 4
        f = estilo.serifa(tam, 600)
    entre = tam * 1.18
    y = ALT / 2 - entre * len(linhas) / 2 + tam * 0.8 - (30 if credito else 0)
    for l in linhas:
        d.text((LARG / 2, y), l, font=f, fill=TINTA, anchor="ms")
        y += entre
    for c in credito:
        d.text((LARG / 2, y + 50), c, font=estilo.serifa_italica(48, 500), fill=CREDITO, anchor="ms")
    return img


def main():
    p = argparse.ArgumentParser(description="Carrossel de frases em papel envelhecido")
    p.add_argument("texto")
    p.add_argument("--saida")
    a = p.parse_args()
    saida = Path(a.saida) if a.saida else PASTA / "saida" / Path(a.texto).stem
    saida.mkdir(parents=True, exist_ok=True)
    fundo = papel()
    linhas = [l.strip() for l in Path(a.texto).read_text().splitlines() if l.strip()]
    for i, l in enumerate(linhas, 1):
        card(l, fundo).save(saida / f"{i:02d}.jpg", quality=95)
    print(f"Pronto: {len(linhas)} cards em {saida}")


if __name__ == "__main__":
    sys.exit(main())
