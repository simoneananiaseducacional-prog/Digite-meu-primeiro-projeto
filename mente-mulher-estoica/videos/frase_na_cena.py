"""Série "Estoicismo na prática": a cena animada com uma frase só na tela.

A frase fica no terço de baixo do vídeo (acima da área dos botões do Reels), do começo
ao fim, sobre uma faixa escura suave que garante a leitura. No final, o último quadro
escurece e entra o nome da série. O áudio do vídeo de origem é descartado (a música é
escolhida no próprio Instagram).

Com `--estilo tiktok`, a frase vira legenda de rede social: letra grossa branca com
contorno preto, no terço de baixo, sem faixa escura, e aceita emojis.

Exemplo:
    python3 frase_na_cena.py fila.mov \\
        --frase "Furaram a fila. Eu não gritei. Só mostrei, com educação, onde ela termina."
"""

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import estilo
import midia

SERIE = "ESTOICISMO NA PRÁTICA"
ENTRA, FECHO = 0.4, 2.5


def camada_frase(frase, cobrir=None, topo=False):
    """Faixa escura suave no terço de baixo e a frase em serifa clara, com sombra difusa.

    Com `cobrir=(y0, y1)`, a faixa fica quase opaca entre y0 e y1 e a frase vai no meio
    dela: serve para esconder um texto que o gerador de vídeo gravou na imagem."""
    f = estilo.serifa(60 if cobrir else 70, 600)
    linhas = [l for parte in frase.split("|")
              for l in estilo.quebrar_linhas(parte.strip(), f, estilo.LARGURA - 2 * estilo.MARGEM_X)]
    if cobrir:
        centro = (cobrir[0] + cobrir[1]) / 2
    elif topo:
        centro = estilo.TOPO_SEGURO + 40 + len(linhas) * 43
    else:
        centro = estilo.BASE_SEGURA - 170
    y = centro - (len(linhas) - 1) * 43

    escuro = Image.new("RGBA", (estilo.LARGURA, estilo.ALTURA), (0, 0, 0, 0))
    eixo = np.arange(estilo.ALTURA, dtype=np.float32)
    if cobrir:
        fora = np.maximum(cobrir[0] - eixo, eixo - cobrir[1])
        alfa = np.clip(1 - fora / 70, 0, 1)
    else:
        alfa = np.clip(1 - np.abs(eixo - centro) / (len(linhas) * 43 + 260), 0, 1) ** 0.8 * 0.72
    escuro.putalpha(Image.fromarray(np.repeat((alfa * 255).astype(np.uint8)[:, None], estilo.LARGURA, 1)))

    texto = Image.new("RGBA", (estilo.LARGURA, estilo.ALTURA), (0, 0, 0, 0))
    d = ImageDraw.Draw(texto)
    for linha in linhas:
        d.text((estilo.LARGURA / 2, y), linha, font=f, fill=estilo.BRANCO + (255,), anchor="mm")
        y += 86
    sombra = Image.new("RGBA", texto.size, (0, 0, 0, 0))
    sombra.putalpha(texto.getchannel("A").filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.85)))
    return estilo.Camada(escuro), estilo.Camada(Image.alpha_composite(sombra, texto))


EMOJI = Path("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf")


def _eh_emoji(c):
    o = ord(c)
    return o >= 0x1F000 or 0x2600 <= o <= 0x27BF or o in (0xFE0F, 0x200D)


def _trechos(linha):
    """Separa a linha em trechos de texto e de emoji: [(texto, eh_emoji)]."""
    saida = []
    for c in linha:
        e = _eh_emoji(c)
        if saida and saida[-1][1] == e:
            saida[-1] = (saida[-1][0] + c, e)
        else:
            saida.append((c, e))
    return saida


def camada_tiktok(frase):
    """Legenda de rede social: Montserrat grossa, branca, contorno preto, emojis coloridos."""
    f = estilo.sem_serifa(64, 800)
    fe = ImageFont.truetype(str(EMOJI), 109) if EMOJI.exists() else None
    lado_emoji = 74
    largura = estilo.LARGURA - 2 * 90
    linhas = [l for parte in frase.split("|")
              for l in estilo.quebrar_linhas(parte.strip(), f, largura)]
    img = Image.new("RGBA", (estilo.LARGURA, estilo.ALTURA), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    y = estilo.BASE_SEGURA - 40 - (len(linhas) - 1) * 84  # terço de baixo, longe dos rostos
    for linha in linhas:
        trechos = _trechos(linha)
        larg = sum(lado_emoji * len(t) if e else f.getlength(t) for t, e in trechos)
        x = (estilo.LARGURA - larg) / 2
        for t, e in trechos:
            if e and fe:
                for c in t:
                    if c in "\ufe0f\u200d":
                        continue
                    g = Image.new("RGBA", (136, 128), (0, 0, 0, 0))
                    ImageDraw.Draw(g).text((0, 0), c, font=fe, embedded_color=True)
                    g = g.crop(g.getbbox() or (0, 0, 1, 1)).resize((lado_emoji, lado_emoji), Image.LANCZOS)
                    img.alpha_composite(g, (int(x), int(y - lado_emoji / 2)))
                    x += lado_emoji
            else:
                d.text((x, y), t, font=f, fill=(255, 255, 255, 255), anchor="lm",
                       stroke_width=7, stroke_fill=(0, 0, 0, 255))
                x += f.getlength(t)
        y += 84
    vazia = Image.new("RGBA", (estilo.LARGURA, estilo.ALTURA), (0, 0, 0, 0))
    return estilo.Camada(vazia), estilo.Camada(img)


def camada_serie():
    img = Image.new("RGBA", (estilo.LARGURA, estilo.ALTURA), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cy = estilo.ALTURA / 2
    d.line((estilo.LARGURA / 2 - 60, cy - 70, estilo.LARGURA / 2 + 60, cy - 70), fill=estilo.DOURADO + (255,), width=2)
    estilo.texto_espacado(d, (estilo.LARGURA / 2, cy), SERIE, estilo.sem_serifa(34, 500), estilo.DOURADO + (255,), 10)
    estilo.texto_espacado(d, (estilo.LARGURA / 2, cy + 70), estilo.ASSINATURA, estilo.sem_serifa(22, 400),
                          estilo.BRANCO + (255,), 8)
    return estilo.Camada(img)


def gerar(video, saida, frase, ate=None, cobrir=None, topo=False, tiktok=False):
    fundo_txt, txt = camada_tiktok(frase) if tiktok else camada_frase(frase, cobrir, topo)
    serie = camada_serie()
    mudo = saida.with_suffix(".mudo.mp4")
    ff = midia.gravador(mudo, estatico=False)
    tamanho = estilo.LARGURA * estilo.ALTURA * 3
    entrada = midia.leitor(video, ate=ate)
    k, ultimo = 0, None
    while True:
        bruto = entrada.stdout.read(tamanho)
        if len(bruto) < tamanho:
            break
        q = np.frombuffer(bruto, np.uint8).reshape(estilo.ALTURA, estilo.LARGURA, 3).astype(np.float32)
        t = k / estilo.FPS
        p = estilo.suavizar((t - ENTRA) / 0.6) if t > ENTRA else 0.0
        if cobrir:
            fundo_txt.compor(q, 1.0)  # a faixa já começa opaca, para esconder o texto gravado
        ultimo = q.copy()  # o fecho parte do quadro sem a frase
        if not cobrir:
            fundo_txt.compor(q, p)
        txt.compor(q, p, int(round((1 - p) * 16)))
        ff.stdin.write(estilo.para_bytes(q))
        k += 1
    entrada.wait()
    # Fecho: o último quadro escurece e entra o nome da série
    for i in range(int(FECHO * estilo.FPS)):
        t = i / estilo.FPS
        m = estilo.suavizar(t / 0.7) * 0.8
        q = ultimo * (1 - m)
        p = estilo.suavizar((t - 0.4) / 0.7) if t > 0.4 else 0.0
        serie.compor(q, p)
        ff.stdin.write(estilo.para_bytes(q))
    ff.stdin.close()
    ff.wait()
    midia.juntar_audio(mudo, saida)
    return midia.duracao(saida)


def main():
    p = argparse.ArgumentParser(description="Cena animada com uma frase na tela e o fecho da série")
    p.add_argument("video")
    p.add_argument("--frase", required=True, help="| força a quebra de linha")
    p.add_argument("--ate", type=float, help="corta o vídeo neste segundo")
    p.add_argument("--estilo", choices=["marca", "tiktok"], default="marca",
                   help="marca: serifa clara com faixa escura; tiktok: letra grossa com contorno e emojis")
    p.add_argument("--topo", action="store_true", help="frase no alto da tela, em vez do terço de baixo")
    p.add_argument("--cobrir", help="y0,y1: faixa opaca que esconde texto gravado no vídeo; a frase vai nela")
    p.add_argument("--saida")
    a = p.parse_args()
    saida = Path(a.saida) if a.saida else estilo.PASTA / "saida" / f"{Path(a.video).stem[:40]}-frase.mp4"
    saida.parent.mkdir(parents=True, exist_ok=True)
    print(f"Pronto: {saida} ({gerar(a.video, saida, a.frase, a.ate,
                                         tuple(int(v) for v in a.cobrir.split(",")) if a.cobrir else None, a.topo,
                                         a.estilo == "tiktok"):.1f} s)")


if __name__ == "__main__":
    sys.exit(main())
