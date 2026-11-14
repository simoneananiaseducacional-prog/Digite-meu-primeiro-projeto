"""Reel "Facetas": a foto dela de costas com a pergunta, uma imagem para cada faceta da
personalidade (com o nome em serifa e o número em dourado) e, no fim, a resposta.
Sai com faixa muda, para escolher a música no próprio Instagram.

    python3 facetas.py pasta_imagens textos/facetas.txt abertura.png [saida.mp4]

As imagens da pasta entram em ordem alfabética (01.png, 02.png...), uma por linha do
arquivo de texto. No texto, "|" separa a palavra principal de um complemento opcional.
"""

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

import estilo
import midia

W, H, FPS = estilo.LARGURA, estilo.ALTURA, estilo.FPS
CX = W // 2
ABERTURA = 4.2      # segundos da pergunta
POR_FACETA = 1.8    # segundos de cada faceta
TROCA = 0.35        # duração da fusão entre imagens
FINAL = 5.0         # segundos da resposta
Y_NOME = 1433


def aparece(t, t0, dur=0.6):
    return estilo.suavizar((t - t0) / dur) if t > t0 else 0.0


def preparar(img, faixa=True):
    """1080x1920 com folga para o zoom, cor um pouco contida e bordas escurecidas."""
    img = ImageOps.fit(img.convert("RGB"), (int(W * 1.08), int(H * 1.08)), Image.LANCZOS)
    a = np.asarray(img, np.float32)
    cinza = a.mean(2, keepdims=True)
    a = cinza + (a - cinza) * 0.85
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    a *= (1 - 0.45 * np.clip(r - 0.55, 0, 1) ** 1.5)[..., None]
    # faixa escura discreta onde entra o nome
    y = np.linspace(0, 1, h)[:, None]
    if faixa:
        a *= (1 - 0.45 * np.exp(-((y - Y_NOME / H) / 0.07) ** 2))[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def zoom(img, z):
    w, h = img.size
    cw, ch = w / z, h / z
    x0, y0 = (w - cw) / 2, (h - ch) / 2
    return np.asarray(img.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch)), np.float32)


def camada_texto(itens):
    """itens: (texto, fonte, cor, (x, y)) centralizados; devolve uma Camada com sombra suave."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sombra = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds, d = ImageDraw.Draw(sombra), ImageDraw.Draw(img)
    for s, f, cor, xy in itens:
        ds.text((xy[0], xy[1] + 3), s, font=f, fill=(0, 0, 0, 210), anchor="mm")
    img = Image.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(7)), img)
    d = ImageDraw.Draw(img)
    for s, f, cor, xy in itens:
        d.text(xy, s, font=f, fill=cor + (255,), anchor="mm")
    return estilo.Camada(img)


def camada_assinatura(y):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    estilo.texto_espacado(ImageDraw.Draw(img), (CX, y), estilo.ASSINATURA, estilo.sem_serifa(26, 500),
                          estilo.BRANCO + (220,), 8)
    return estilo.Camada(img)


def main():
    p = argparse.ArgumentParser(description="Reel das facetas da personalidade")
    p.add_argument("pasta")
    p.add_argument("textos")
    p.add_argument("abertura", help="foto usada na pergunta e na resposta")
    p.add_argument("saida", nargs="?")
    p.add_argument("--pergunta", default="Gosto de você pela|sua personalidade…")
    p.add_argument("--qual", default="Qual delas?")
    p.add_argument("--resposta", default="Sou eu.|*Em todas elas.*")
    a = p.parse_args()
    saida = Path(a.saida) if a.saida else estilo.PASTA / "saida" / "facetas.mp4"
    saida.parent.mkdir(parents=True, exist_ok=True)

    nomes = [l.strip() for l in Path(a.textos).read_text().splitlines() if l.strip()]
    imagens = sorted(p for p in Path(a.pasta).iterdir() if p.suffix.lower() in (".png", ".jpg", ".jpeg"))
    if len(imagens) != len(nomes):
        sys.exit(f"{len(imagens)} imagens e {len(nomes)} nomes: precisam ser iguais")
    fotos = [preparar(Image.open(f)) for f in imagens]
    capa = preparar(Image.open(a.abertura), faixa=False)

    f_nome, f_num = estilo.serifa(104, 600), estilo.sem_serifa(36, 600)
    rotulos = []
    for i, n in enumerate(nomes):
        rotulos.append((camada_texto([(n, f_nome, estilo.BRANCO, (CX, Y_NOME))]),
                        camada_texto([(f"{i + 1:02d}", f_num, estilo.DOURADO, (CX, Y_NOME - 105))])))
    f1, f2 = estilo.serifa(80, 600), estilo.serifa_italica(100, 600)
    perg = a.pergunta.split("|")
    c_perg = camada_texto([(l, f1, estilo.BRANCO, (CX, 400 + 95 * i)) for i, l in enumerate(perg)])
    c_qual = camada_texto([(a.qual, f2, estilo.DOURADO, (CX, 400 + 95 * len(perg) + 40))])
    resp = a.resposta.split("|")
    c_resp = []
    for i, l in enumerate(resp):
        dourada = l.startswith("*") and l.endswith("*")
        c_resp.append(camada_texto([(l.strip("*"), f2 if dourada else f1,
                                     estilo.DOURADO if dourada else estilo.BRANCO, (CX, 430 + 110 * i))]))
    c_assin = camada_assinatura(430 + 110 * len(resp) + 30)

    t_fim = ABERTURA + POR_FACETA * len(fotos)
    duracao = t_fim + FINAL
    mudo = saida.with_suffix(".mudo.mp4")
    ff = midia.gravador(mudo, estatico=False)
    for k in range(int(duracao * FPS)):
        t = k / FPS
        if t < ABERTURA:
            q = zoom(capa, 1.0 + 0.03 * t / ABERTURA)
            c_perg.compor(q, aparece(t, 0.3, 0.8) * (1 - aparece(t, ABERTURA - 0.5, 0.4)))
            c_qual.compor(q, aparece(t, 2.0, 0.7) * (1 - aparece(t, ABERTURA - 0.5, 0.4)))
            if t > ABERTURA - TROCA:
                m = aparece(t, ABERTURA - TROCA, TROCA)
                q = q * (1 - m) + zoom(fotos[0], 1.0) * m
        elif t < t_fim:
            i = int((t - ABERTURA) // POR_FACETA)
            tl = t - ABERTURA - i * POR_FACETA
            q = zoom(fotos[i], 1.0 + 0.05 * tl / POR_FACETA)
            nome, num = rotulos[i]
            op = aparece(tl, 0.15, 0.45) * (1 - aparece(tl, POR_FACETA - 0.3, 0.25))
            num.compor(q, op)
            nome.compor(q, op, deslocamento_y=int(18 * (1 - aparece(tl, 0.15, 0.6))))
            if tl > POR_FACETA - TROCA:
                prox = fotos[i + 1] if i + 1 < len(fotos) else capa
                m = aparece(tl, POR_FACETA - TROCA, TROCA)
                q = q * (1 - m) + zoom(prox, 1.0) * m
        else:
            tl = t - t_fim
            q = zoom(capa, 1.0 + 0.04 * tl / FINAL)
            # escurece levemente para a resposta ganhar peso
            q *= 1 - 0.25 * aparece(tl, 0.0, 1.0)
            for j, c in enumerate(c_resp):
                c.compor(q, aparece(tl, 0.4 + 0.9 * j, 0.8))
            c_assin.compor(q, aparece(tl, 0.6 + 0.9 * len(c_resp), 0.8))
            q *= 1 - aparece(tl, FINAL - 0.6, 0.6)
        ff.stdin.write(estilo.para_bytes(estilo.granulado(q, intensidade=2.5)))
    ff.stdin.close()
    ff.wait()
    midia.juntar_audio(mudo, saida)
    mudo.unlink(missing_ok=True)
    print(f"Pronto: {saida} ({midia.duracao(saida):.1f} s)")


if __name__ == "__main__":
    sys.exit(main())
