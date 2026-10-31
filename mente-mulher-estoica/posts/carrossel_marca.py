"""Carrossel de frases no PADRÃO DA MARCA: fundo preto com vinheta e granulado, serifa
off-white, destaque dourado em itálico e a assinatura MENTE MULHER ESTOICA no pé.

Use este para qualquer carrossel de frases. Posts de outros perfis servem só de referência
de ideia/estrutura, nunca de visual.

Cada linha do arquivo vira um card; "|" quebra a linha; um trecho entre *asteriscos*
sai dourado em itálico; um trecho começando com "_" vira o crédito pequeno.

    python3 carrossel_marca.py textos/sentir-marca.txt --saida saida/sentir
"""

import argparse
import sys
from pathlib import Path

from PIL import ImageDraw

from carrossel_lista import ALT, LARG, base, rodape

PASTA = Path(__file__).resolve().parent
sys.path.insert(0, str(PASTA.parent / "videos"))
import estilo  # noqa: E402

MX = 110


def card(texto, n, total):
    img = base()
    d = ImageDraw.Draw(img)
    partes = texto.split("|")
    credito = [p[1:] for p in partes if p.startswith("_")]
    linhas = [p for p in partes if not p.startswith("_")]
    tam = 100 if len(linhas) <= 3 else 84
    blocos = []
    for l in linhas:
        dourada = l.startswith("*") and l.endswith("*")
        f = estilo.serifa_italica(int(tam * 1.12), 600) if dourada else estilo.serifa(tam, 500)
        blocos.append((l.strip("*"), f, estilo.DOURADO if dourada else estilo.BRANCO))
    while max(f.getlength(s) for s, f, _ in blocos) > LARG - 2 * MX:
        blocos = [(s, f.font_variant(size=f.size - 4), c) for s, f, c in blocos]
    entre = blocos[0][1].size * 1.2
    y = ALT / 2 - entre * len(blocos) / 2 + entre * 0.75 - (30 if credito else 0)
    for s, f, c in blocos:
        d.text((LARG / 2, y), s, font=f, fill=c, anchor="ms", features=["lnum"])
        y += entre
    for c in credito:
        d.text((LARG / 2, y + 40), c, font=estilo.serifa_italica(46, 500), fill=estilo.CINZA, anchor="ms")
    rodape(d)
    d.text((LARG - 70, 90), f"{n}/{total}", font=estilo.sem_serifa(24, 500), fill=estilo.CINZA, anchor="rs")
    return img


def main():
    p = argparse.ArgumentParser(description="Carrossel de frases no padrão preto e dourado da marca")
    p.add_argument("texto")
    p.add_argument("--saida")
    a = p.parse_args()
    saida = Path(a.saida) if a.saida else PASTA / "saida" / Path(a.texto).stem
    saida.mkdir(parents=True, exist_ok=True)
    linhas = [l.strip() for l in Path(a.texto).read_text().splitlines() if l.strip()]
    for i, l in enumerate(linhas, 1):
        card(l, i, len(linhas)).save(saida / f"{i:02d}.jpg", quality=95)
    print(f"Pronto: {len(linhas)} cards em {saida}")


if __name__ == "__main__":
    sys.exit(main())
