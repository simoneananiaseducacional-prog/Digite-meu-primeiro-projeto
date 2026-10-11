"""Troca a frase escrita numa caneca (ou objeto cilíndrico claro) de uma foto.

1. Apaga a frase antiga: cada coluna da área é refeita interpolando a cor da
   superfície logo acima e logo abaixo dela (funciona em porcelana lisa).
2. Escreve a frase nova em letra cursiva, inclinada como a original e
   comprimida nas bordas, acompanhando a curva da caneca.

Exemplo (a foto de referência da série):
    python3 trocar_frase.py caneca.png --frase "Nem tudo merece|a minha resposta." \\
        --area 225,835,690,1085 --centro 452,940 --raio 300 --inclinacao 3.5 --tamanho 88 --entrelinha 84
"""

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import estilo

FONTE = estilo.FONTES / "Sacramento-Regular.ttf"
TINTA = (14, 13, 13)


def apagar(img, area, faixa=18):
    """Refaz a superfície dentro de `area` interpolando, coluna a coluna, as faixas
    de `faixa` pixels logo acima e logo abaixo dela."""
    x0, y0, x1, y1 = area
    a = np.asarray(img, np.float32).copy()
    cima = np.median(a[y0 - faixa:y0, x0:x1], axis=0)
    baixo = np.median(a[y1:y1 + faixa, x0:x1], axis=0)
    t = np.linspace(0, 1, y1 - y0, dtype=np.float32)[:, None, None]
    miolo = cima[None] * (1 - t) + baixo[None] * t
    # Suaviza na horizontal e devolve um pouco do grão da foto
    miolo_img = Image.fromarray(np.clip(miolo, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))
    miolo = np.asarray(miolo_img, np.float32)
    rng = np.random.default_rng(1)
    miolo += rng.normal(0, 1.6, miolo.shape[:2])[..., None]
    # Bordas da área em degradê, para não deixar emenda
    m = np.ones((y1 - y0, x1 - x0), np.float32)
    borda = 10
    rampa = np.linspace(0, 1, borda, dtype=np.float32)
    m[:, :borda] *= rampa[None]
    m[:, -borda:] *= rampa[::-1][None]
    m = m[..., None]
    a[y0:y1, x0:x1] = a[y0:y1, x0:x1] * (1 - m) + miolo * m
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def texto_plano(linhas, tamanho, entrelinha):
    """Frase em letra cursiva sobre fundo transparente (só o alfa importa)."""
    f = ImageFont.truetype(str(FONTE), tamanho)
    larg = int(max(f.getlength(l) for l in linhas)) + 80
    alt = int(entrelinha * len(linhas) + tamanho)
    img = Image.new("L", (larg, alt), 0)
    d = ImageDraw.Draw(img)
    for i, l in enumerate(linhas):
        d.text((larg / 2, tamanho * 0.6 + i * entrelinha), l, font=f, fill=255, anchor="mm")
    return img


def curvar(alfa, raio):
    """Envolve o texto num cilindro: comprime as bordas como numa caneca vista de frente."""
    a = np.asarray(alfa, np.float32)
    h, w = a.shape
    cx = w / 2
    xs = np.arange(w, dtype=np.float32) - cx
    # Largura na tela que o texto ocupa depois de envolvido
    meia = raio * np.sin(min(cx / raio, np.pi / 2 - 0.05))
    saida_w = int(2 * meia) + 2
    xo = np.arange(saida_w, dtype=np.float32) - saida_w / 2
    origem = raio * np.arcsin(np.clip(xo / raio, -1, 1)) + cx
    i0 = np.clip(np.floor(origem).astype(int), 0, w - 2)
    frac = origem - i0
    res = a[:, i0] * (1 - frac) + a[:, i0 + 1] * frac
    # Perto da borda o traço também fica mais fraco (luz rasante)
    queda = np.cos(np.arcsin(np.clip(xo / raio, -1, 1))) ** 0.3
    return Image.fromarray(np.clip(res * queda[None], 0, 255).astype(np.uint8)), xs


def escrever(img, linhas, centro, raio, inclinacao, tamanho, entrelinha):
    alfa = texto_plano(linhas, tamanho, entrelinha)
    alfa, _ = curvar(alfa, raio)
    alfa = alfa.rotate(inclinacao, resample=Image.BICUBIC, expand=True)
    alfa = alfa.filter(ImageFilter.GaussianBlur(0.5))
    tinta = Image.new("RGB", alfa.size, TINTA)
    pos = (int(centro[0] - alfa.width / 2), int(centro[1] - alfa.height / 2))
    saida = img.copy()
    saida.paste(tinta, pos, alfa.point(lambda v: min(255, int(v * 1.25))))
    return saida


def main():
    p = argparse.ArgumentParser(description="Troca a frase escrita numa caneca")
    p.add_argument("foto")
    p.add_argument("--frase", required=True, help="linhas separadas por |")
    p.add_argument("--area", required=True, help="x0,y0,x1,y1 da frase antiga, para apagar")
    p.add_argument("--centro", required=True, help="x,y do centro da frase nova")
    p.add_argument("--raio", type=float, default=300, help="raio da caneca em pixels")
    p.add_argument("--inclinacao", type=float, default=0, help="graus; positivo sobe para a direita")
    p.add_argument("--tamanho", type=int, default=88)
    p.add_argument("--entrelinha", type=int, default=86)
    p.add_argument("--saida")
    a = p.parse_args()

    img = Image.open(a.foto).convert("RGB")
    area = tuple(int(v) for v in a.area.split(","))
    centro = tuple(float(v) for v in a.centro.split(","))
    limpa = apagar(img, area)
    nova = escrever(limpa, [l.strip() for l in a.frase.split("|")], centro, a.raio,
                    a.inclinacao, a.tamanho, a.entrelinha)
    saida = Path(a.saida) if a.saida else estilo.PASTA / "saida" / f"{Path(a.foto).stem}-nova-frase.png"
    saida.parent.mkdir(parents=True, exist_ok=True)
    nova.save(saida)
    print(f"Pronto: {saida}")


if __name__ == "__main__":
    sys.exit(main())
