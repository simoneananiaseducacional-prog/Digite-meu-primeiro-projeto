"""Carrossel de lista numerada em papel envelhecido: número em dourado envelhecido, regra em
serifa escura com um traço dourado embaixo e, depois, o porquê em itálico.

Mesmo arquivo de texto de carrossel_lista.py: 1ª linha é a capa; cada linha
"regra || porquê" vira um card numerado; a última linha é o fechamento. "|" quebra a linha.

    python3 carrossel_pergaminho_lista.py textos/praticas-estoicas.txt --saida saida/praticas
"""

import argparse
import sys
from pathlib import Path

from PIL import ImageDraw

from carrossel_pergaminho import CREDITO, TINTA, papel

PASTA = Path(__file__).resolve().parent
sys.path.insert(0, str(PASTA.parent / "videos"))
import estilo  # noqa: E402

LARG, ALT = 1080, 1350
MX = 120
OURO_VELHO = (150, 112, 52)
ARROBA = "@mente_mulher_estoica"


def bloco(d, blocos, y_meio):
    """Desenha blocos [(linhas, fonte, cor, entre, espaco_depois, traco)] centralizados na altura."""
    altura = sum(len(l) * e + esp for l, _, _, e, esp, _ in blocos)
    y = y_meio - altura / 2
    for linhas, f, cor, entre, esp, traco in blocos:
        for l in linhas:
            d.text((LARG / 2, y + entre * 0.8), l, font=f, fill=cor, anchor="ms", features=["lnum"])
            y += entre
        if traco:
            d.line((LARG / 2 - 50, y + 26, LARG / 2 + 50, y + 26), fill=OURO_VELHO, width=3)
        y += esp


def rodape(d):
    estilo.texto_espacado(d, (LARG / 2, ALT - 90), estilo.ASSINATURA, estilo.sem_serifa(22, 600), CREDITO, 6)


def quebrar(texto, f, largura):
    return estilo.quebrar_linhas(texto.replace("|", "\n"), f, largura)


def card_capa(fundo, texto):
    img = fundo.copy(); d = ImageDraw.Draw(img)
    f = estilo.serifa(96, 700)
    bloco(d, [(quebrar(texto, f, LARG - 2 * MX), f, TINTA, 108, 60, True),
              (["arraste →"], estilo.serifa_italica(46, 500), OURO_VELHO, 50, 0, False)], ALT / 2)
    rodape(d)
    return img


def card_item(fundo, n, regra, porque):
    img = fundo.copy(); d = ImageDraw.Draw(img)
    fr, fp = estilo.serifa(86, 700), estilo.serifa_italica(58, 500)
    bloco(d, [([f"{n:02d}"], estilo.serifa(104, 600), OURO_VELHO, 116, 30, False),
              (quebrar(regra, fr, LARG - 2 * MX), fr, TINTA, 98, 60, True),
              (quebrar(porque, fp, LARG - 2 * MX - 40), fp, CREDITO, 72, 0, False)], ALT / 2)
    rodape(d)
    return img


def card_final(fundo, texto):
    img = fundo.copy(); d = ImageDraw.Draw(img)
    l1, l2 = texto.split("|")
    bloco(d, [([l1], estilo.serifa(78, 600), TINTA, 92, 20, False),
              ([l2], estilo.serifa_italica(106, 600), OURO_VELHO, 112, 70, False),
              ([ARROBA], estilo.sem_serifa(28, 600), CREDITO, 40, 0, False)], ALT / 2)
    return img


def main():
    p = argparse.ArgumentParser(description="Carrossel de lista numerada em papel envelhecido")
    p.add_argument("texto")
    p.add_argument("--saida")
    a = p.parse_args()
    linhas = [l.strip() for l in Path(a.texto).read_text().splitlines() if l.strip()]
    saida = Path(a.saida) if a.saida else PASTA / "saida" / f"{Path(a.texto).stem}-pergaminho"
    saida.mkdir(parents=True, exist_ok=True)
    fundo = papel()
    cards = [card_capa(fundo, linhas[0])]
    for n, l in enumerate(linhas[1:-1], 1):
        regra, porque = (s.strip() for s in l.split("||"))
        cards.append(card_item(fundo, n, regra, porque))
    cards.append(card_final(fundo, linhas[-1]))
    for i, c in enumerate(cards, 1):
        c.save(saida / f"{i:02d}.jpg", quality=95)
    print(f"Pronto: {len(cards)} cards em {saida}")


if __name__ == "__main__":
    sys.exit(main())
