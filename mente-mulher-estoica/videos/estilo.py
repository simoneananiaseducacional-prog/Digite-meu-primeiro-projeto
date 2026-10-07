"""Identidade visual dos vídeos da @mente.mulher.estoica.

Preto e branco editorial, dourado como acento, serifa elegante e muito respiro.
Tudo que define a aparência dos vídeos fica aqui, para os dois geradores
(reel de frases e legendas) falarem a mesma língua visual.
"""

import re
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

PASTA = Path(__file__).resolve().parent
FONTES = PASTA / "fontes"

# Formato Reels / Stories
LARGURA, ALTURA, FPS = 1080, 1920, 30

# Paleta
PRETO = (11, 11, 11)
BRANCO = (242, 238, 230)  # off-white, menos agressivo que o branco puro
DOURADO = (196, 160, 98)
CINZA = (130, 126, 120)

ARROBA = "@mente.mulher.estoica"
ASSINATURA = "MENTE MULHER ESTOICA"

# Área segura do Reels: o topo e a base ficam cobertos pela interface do app
MARGEM_X = 110
TOPO_SEGURO = 260
BASE_SEGURA = ALTURA - 420


def fonte(nome, tamanho, peso=400):
    """Carrega uma fonte variável da pasta fontes/ no peso pedido."""
    f = ImageFont.truetype(str(FONTES / nome), tamanho)
    try:
        f.set_variation_by_axes([peso])
    except OSError:
        pass
    return f


def serifa(tamanho, peso=400):
    return fonte("CormorantGaramond.ttf", tamanho, peso)


def serifa_italica(tamanho, peso=500):
    return fonte("CormorantGaramond-Italic.ttf", tamanho, peso)


def sem_serifa(tamanho, peso=500):
    return fonte("Montserrat.ttf", tamanho, peso)


def quebrar_linhas(texto, f, largura_max):
    """Quebra o texto em linhas que caibam na largura, palavra por palavra."""
    linhas = []
    for paragrafo in texto.split("\n"):
        atual = ""
        for palavra in paragrafo.split():
            teste = f"{atual} {palavra}".strip()
            if f.getlength(teste) <= largura_max or not atual:
                atual = teste
            else:
                linhas.append(atual)
                atual = palavra
        linhas.append(atual)
    return linhas


def texto_espacado(draw, xy_centro, texto, f, cor, espaco):
    """Escreve em caixa alta com espaçamento entre letras, centralizado."""
    larguras = [f.getlength(c) for c in texto]
    total = sum(larguras) + espaco * (len(texto) - 1)
    x = xy_centro[0] - total / 2
    for c, w in zip(texto, larguras):
        draw.text((x, xy_centro[1]), c, font=f, fill=cor, anchor="lm")
        x += w + espaco


def fundo():
    """Fundo preto com vinheta suave, como array float32 (A, L, 3)."""
    y, x = np.mgrid[0:ALTURA, 0:LARGURA].astype(np.float32)
    dx = (x - LARGURA / 2) / (LARGURA * 0.75)
    dy = (y - ALTURA * 0.47) / (ALTURA * 0.6)
    luz = np.clip(1.0 - (dx**2 + dy**2), 0, 1) ** 1.6
    base = np.array(PRETO, np.float32)
    claro = np.array((30, 28, 26), np.float32)
    return base + (claro - base) * luz[..., None]


def moldura():
    """Elementos fixos de todas as telas: assinatura no topo e arroba na base."""
    img = Image.new("RGBA", (LARGURA, ALTURA), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    texto_espacado(d, (LARGURA / 2, TOPO_SEGURO), ASSINATURA,
                   sem_serifa(22, 500), DOURADO + (255,), 9)
    d.line([(LARGURA / 2 - 28, TOPO_SEGURO + 38), (LARGURA / 2 + 28, TOPO_SEGURO + 38)],
           fill=DOURADO + (200,), width=2)
    d.text((LARGURA / 2, BASE_SEGURA + 40), ARROBA, font=sem_serifa(24, 400),
           fill=CINZA + (255,), anchor="mm")
    return img


def granulado(quadro, intensidade=4.0, semente=7):
    """Textura de papel fixa sobre o preto chapado.

    É estática de propósito: ruído mudando a cada quadro multiplica o tamanho
    do arquivo sem ganho visível depois da compressão do Instagram.
    """
    rng = np.random.default_rng(semente)
    return quadro + rng.normal(0, intensidade, (ALTURA, LARGURA, 1)).astype(np.float32)


class Camada:
    """Imagem RGBA recortada e pré-multiplicada, pronta para compor quadro a quadro."""

    def __init__(self, img):
        caixa = img.getbbox() or (0, 0, 1, 1)
        self.x0, self.y0 = caixa[0], caixa[1]
        arr = np.asarray(img.crop(caixa), np.float32) / 255.0
        self.alfa = arr[..., 3:4]
        self.cor = arr[..., :3] * 255.0 * self.alfa

    def compor(self, quadro, opacidade=1.0, deslocamento_y=0):
        """Aplica a camada sobre o quadro (alterando-o) e devolve o quadro."""
        if opacidade <= 0:
            return quadro
        h, w = self.alfa.shape[:2]
        y0 = min(max(self.y0 + deslocamento_y, 0), ALTURA - h)
        regiao = quadro[y0:y0 + h, self.x0:self.x0 + w]
        regiao *= 1 - self.alfa * opacidade
        regiao += self.cor * opacidade
        return quadro


def _altura_bloco(blocos):
    total = 0
    for i, (linhas, f, _, entrelinha) in enumerate(blocos):
        total += len(linhas) * entrelinha + (44 if i else 0)
    return total


def tela_de_texto(linhas, largura_max=LARGURA - 2 * MARGEM_X):
    """Desenha uma tela do reel: destaques em itálico dourado, texto em serifa clara.

    `linhas` é uma lista de (texto, destaque). A fonte diminui até o texto caber
    na área segura.
    """
    escala = 1.0
    limite = BASE_SEGURA - TOPO_SEGURO - 220
    while True:
        blocos = []
        for texto, destaque in linhas:
            if destaque:
                f = serifa_italica(int(88 * escala), 600)
                cor, entre = DOURADO, int(100 * escala)
            else:
                f = serifa(int(64 * escala), 500)
                cor, entre = BRANCO, int(80 * escala)
            blocos.append((quebrar_linhas(texto, f, largura_max), f, cor, entre))
        if _altura_bloco(blocos) <= limite or escala < 0.6:
            break
        escala -= 0.06

    img = Image.new("RGBA", (LARGURA, ALTURA), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    centro = (TOPO_SEGURO + BASE_SEGURA) / 2
    y = centro - _altura_bloco(blocos) / 2
    for i, (ls, f, cor, entre) in enumerate(blocos):
        if i:
            y += 44
        for linha in ls:
            d.text((LARGURA / 2, y + entre / 2), linha, font=f, fill=cor + (255,), anchor="mm")
            y += entre
    return img


def tela_final(frase):
    """Tela de fechamento: frases empilhadas entre dois filetes dourados.

    A última frase ganha o itálico dourado, como a assinatura do vídeo.
    """
    frases = [f for f in re.split(r"(?<=[.!?…])\s+", frase.strip()) if f] or [frase]
    linhas = [(f, i == len(frases) - 1 and len(frases) > 1) for i, f in enumerate(frases)]
    img = tela_de_texto(linhas)
    caixa = img.getbbox()
    if caixa:
        d = ImageDraw.Draw(img)
        for y in (caixa[1] - 70, caixa[3] + 70):
            d.line([(LARGURA / 2 - 60, y), (LARGURA / 2 + 60, y)], fill=DOURADO + (230,), width=2)
    return img


def suavizar(t):
    """Curva de saída suave (ease-out cúbico) para t entre 0 e 1."""
    t = min(max(t, 0.0), 1.0)
    return 1 - (1 - t) ** 3


def para_bytes(quadro):
    return np.clip(quadro, 0, 255).astype(np.uint8).tobytes()
