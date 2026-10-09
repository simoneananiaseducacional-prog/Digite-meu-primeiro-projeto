"""Post de citação no estilo "andorinha": cartão vinho de papel amassado sobre pedra bege.

Paleta:
    fundo (pedra)   #CFC6B4, manchas #B3A893
    cartão (vinho)  #6B1E2A, variando entre #5E1A24 e #7A2633 na textura
    texto           #EDE3CF (creme); créditos no mesmo creme, mais transparente
Fonte: Bebas Neue (condensada, caixa-alta).

Exemplo:
    python3 post_citacao.py "Sofremos mais na imaginação|do que na realidade." \\
        --credito "SÊNECA | CARTAS A LUCÍLIO, 13.4"
"""

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

PASTA = Path(__file__).resolve().parent
FONTE = PASTA.parent / "videos" / "fontes" / "BebasNeue-Regular.ttf"
LARG, ALT = 1080, 1350

PEDRA = np.array((207, 198, 180), np.float32)
PEDRA_ESCURA = np.array((179, 168, 147), np.float32)
VINHO = np.array((100, 27, 39), np.float32)
CREME = (237, 227, 207)
ASSINATURA = "MULHER ESTOICA  |  @mente_mulher_estoica"


def ruido(rng, h, w, escalas):
    """Ruído suave em várias escalas, normalizado para 0..1."""
    total = np.zeros((h, w), np.float32)
    for tam, peso in escalas:
        r = rng.random((max(2, h // tam), max(2, w // tam))).astype(np.float32)
        img = Image.fromarray((r * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        total += peso * np.asarray(img, np.float32) / 255
    total -= total.min()
    return total / (total.max() + 1e-6)


def fundo_pedra(rng):
    m = ruido(rng, ALT, LARG, [(180, 1.0), (60, 0.6), (15, 0.3), (3, 0.25)])
    m = np.clip((m - 0.35) * 1.6, 0, 1)[..., None]
    img = PEDRA * (1 - m * 0.75) + PEDRA_ESCURA * (m * 0.75)
    img += rng.normal(0, 3.5, (ALT, LARG, 1))
    return img


def vincos(rng, h, w, n=26):
    """Relevo de papel amassado: dobras retas em direções aleatórias."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    altura = np.zeros((h, w), np.float32)
    for _ in range(n):
        ang = rng.uniform(0, np.pi)
        cx, cy = rng.uniform(0, w), rng.uniform(0, h)
        d = (xx - cx) * np.cos(ang) + (yy - cy) * np.sin(ang)
        largura = rng.uniform(20, 90)
        altura += rng.uniform(-1, 1) * np.exp(-np.abs(d) / largura)
    altura += 0.6 * ruido(rng, h, w, [(40, 1.0), (8, 0.4)])
    # Luz vindo do alto à esquerda
    gy, gx = np.gradient(altura)
    luz = -(gx * 0.7 + gy * 0.7) * 22
    return np.clip(luz, -1, 1)


def cartao(rng, w, h):
    luz = vincos(rng, h, w)
    fibra = ruido(rng, h, w, [(4, 1.0), (1, 0.5)]) - 0.5
    img = VINHO[None, None] * (1 + 0.16 * luz[..., None] + 0.08 * fibra[..., None])
    # Bordas levemente mais escuras
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    borda = np.minimum.reduce([xx, w - xx, yy, h - yy])
    img *= (0.88 + 0.12 * np.clip(borda / 40, 0, 1))[..., None]
    return img


def escrever(img, linhas, credito, caixa):
    x0, y0, x1, y1 = caixa
    d = ImageDraw.Draw(img)
    util = (x1 - x0) * 0.86
    tam = 150
    while tam > 40:
        f = ImageFont.truetype(str(FONTE), tam)
        if max(f.getlength(l) for l in linhas) <= util:
            break
        tam -= 2
    entre = tam * 0.98
    fc = ImageFont.truetype(str(FONTE), 34)
    fa = ImageFont.truetype(str(FONTE), 26)
    bloco = entre * len(linhas) + 70 + 34
    y = (y0 + y1) / 2 - bloco / 2 - 30
    cx = (x0 + x1) / 2
    for l in linhas:
        d.text((cx, y + tam / 2), l, font=f, fill=CREME + (255,), anchor="mm")
        y += entre
    if credito:
        d.text((cx, y + 60), credito, font=fc, fill=CREME + (205,), anchor="mm")
    d.text((cx, y1 - 70), ASSINATURA, font=fa, fill=CREME + (175,), anchor="mm")


def gerar(frase, credito, saida, semente=7):
    rng = np.random.default_rng(semente)
    base = fundo_pedra(rng)
    mx, my = 105, 170
    w, h = LARG - 2 * mx, ALT - 2 * my
    # Sombra do cartão
    sombra = Image.new("L", (LARG, ALT), 0)
    ImageDraw.Draw(sombra).rectangle((mx + 6, my + 14, mx + w + 6, my + h + 14), fill=150)
    s = np.asarray(sombra.filter(ImageFilter.GaussianBlur(18)), np.float32)[..., None] / 255
    base *= 1 - 0.45 * s
    base[my:my + h, mx:mx + w] = cartao(rng, w, h)
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA")
    texto = Image.new("RGBA", img.size, (0, 0, 0, 0))
    linhas = [l.strip().upper() for l in frase.split("|")]
    escrever(texto, linhas, credito.upper(), (mx, my, mx + w, my + h))
    img = Image.alpha_composite(img, texto).convert("RGB")
    saida.parent.mkdir(parents=True, exist_ok=True)
    img.save(saida, quality=95)
    return saida


def main():
    p = argparse.ArgumentParser(description="Post de citação: cartão vinho sobre pedra bege")
    p.add_argument("frase", help="| quebra a linha")
    p.add_argument("--credito", default="", help='ex.: "SÊNECA | CARTAS A LUCÍLIO, 13.4"')
    p.add_argument("--semente", type=int, default=7, help="muda o desenho dos vincos do papel")
    p.add_argument("--saida")
    a = p.parse_args()
    saida = Path(a.saida) if a.saida else PASTA / "saida" / "post-citacao.jpg"
    print(f"Pronto: {gerar(a.frase, a.credito, saida, a.semente)}")


if __name__ == "__main__":
    sys.exit(main())
