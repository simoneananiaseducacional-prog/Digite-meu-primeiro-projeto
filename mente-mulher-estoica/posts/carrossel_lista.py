"""Carrossel de lista numerada no padrão da marca: fundo preto, número dourado,
regra em serifa grande e, embaixo, uma linha em itálico com o porquê.

Arquivo de texto: 1ª linha é a capa; cada linha "regra || porquê" vira um card numerado;
a última linha é o fechamento ("|" quebra a linha).

    python3 carrossel_lista.py textos/se-respeita.txt --saida saida/se-respeita
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw

PASTA = Path(__file__).resolve().parent
sys.path.insert(0, str(PASTA.parent / "videos"))
import estilo  # noqa: E402

LARG, ALT = 1080, 1350
MX = 110
NOTA = (175, 168, 158)
ARROBA = "@mente_mulher_estoica"


_FUNDO = None


def base():
    """Fundo preto com vinheta e granulado da identidade, no formato 4:5 do feed."""
    global _FUNDO
    if _FUNDO is None:
        _FUNDO = Image.fromarray(estilo.granulado(estilo.fundo()).clip(0, 255).astype("uint8")).resize(
            (LARG, ALT)).convert("RGB")
    return _FUNDO.copy()


def centralizado(d, linhas_fontes, y_meio):
    """Desenha blocos [(linhas, fonte, cor, entre, espaco_depois)] centralizados na altura."""
    altura = sum(len(l) * e + esp for l, _, _, e, esp in linhas_fontes)
    y = y_meio - altura / 2
    for linhas, f, cor, entre, esp in linhas_fontes:
        for l in linhas:
            d.text((LARG / 2, y + entre * 0.8), l, font=f, fill=cor, anchor="ms", features=["lnum"])
            y += entre
        y += esp


def rodape(d):
    estilo.texto_espacado(d, (LARG / 2, ALT - 90), estilo.ASSINATURA, estilo.sem_serifa(22, 500), estilo.CINZA, 6)


def card_capa(texto):
    img = base(); d = ImageDraw.Draw(img)
    f = estilo.serifa(92, 600)
    centralizado(d, [(estilo.quebrar_linhas(texto, f, LARG - 2 * MX), f, estilo.BRANCO, 104, 50),
                     (["arraste →"], estilo.serifa_italica(44, 500), estilo.DOURADO, 50, 0)], ALT / 2)
    rodape(d)
    return img


def card_item(n, regra, porque):
    img = base(); d = ImageDraw.Draw(img)
    fr, fp = estilo.serifa(84, 700), estilo.serifa_italica(58, 500)
    centralizado(d, [([f"{n}."], estilo.serifa(110, 600), estilo.DOURADO, 120, 30),
                     (estilo.quebrar_linhas(regra, fr, LARG - 2 * MX), fr, estilo.BRANCO, 96, 50),
                     (estilo.quebrar_linhas(porque, fp, LARG - 2 * MX - 40), fp, NOTA, 70, 0)], ALT / 2)
    rodape(d)
    return img


def card_final(texto):
    img = base(); d = ImageDraw.Draw(img)
    l1, l2 = texto.split("|")
    centralizado(d, [([l1], estilo.serifa(76, 500), estilo.BRANCO, 90, 20),
                     ([l2], estilo.serifa_italica(104, 600), estilo.DOURADO, 110, 60),
                     ([ARROBA], estilo.sem_serifa(28, 500), estilo.CINZA, 40, 0)], ALT / 2)
    return img


def main():
    p = argparse.ArgumentParser(description="Carrossel de lista numerada, preto e dourado")
    p.add_argument("texto")
    p.add_argument("--saida")
    a = p.parse_args()
    linhas = [l.strip() for l in Path(a.texto).read_text().splitlines() if l.strip()]
    saida = Path(a.saida) if a.saida else PASTA / "saida" / Path(a.texto).stem
    saida.mkdir(parents=True, exist_ok=True)
    cards = [card_capa(linhas[0])]
    for n, l in enumerate(linhas[1:-1], 1):
        regra, porque = (s.strip() for s in l.split("||"))
        cards.append(card_item(n, regra, porque))
    cards.append(card_final(linhas[-1]))
    for i, c in enumerate(cards, 1):
        c.save(saida / f"{i:02d}.jpg", quality=95)
    print(f"Pronto: {len(cards)} cards em {saida}")


if __name__ == "__main__":
    sys.exit(main())
