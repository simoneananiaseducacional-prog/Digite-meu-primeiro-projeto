"""Reel "Cadeira vazia": a foto dela com a promessa do que ela faz quando é desrespeitada,
e depois a cadeira vazia em preto e branco, com a resposta. Sai sem som.

    python3 cadeira_vazia.py foto.jpg cadeira.jpg [saida.mp4] [--recorte-cadeira x0,y0,x1,y1]

`foto` é ela sentada; `cadeira` é o mesmo lugar vazio (pode ser a mesma foto com
--recorte-cadeira apontando para a cadeira vazia).
"""

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

import estilo
import midia

W, H, FPS = estilo.LARGURA, estilo.ALTURA, estilo.FPS
DURACAO = 13.0
TROCA = 6.0  # segundo em que entra a cadeira vazia
CX = W // 2


def aparece(t, t0, dur=0.6):
    return estilo.suavizar((t - t0) / dur) if t > t0 else 0.0


def preencher(img):
    """Ajusta a imagem para 1080x1920 cortando as sobras, com 10% de folga para o zoom."""
    return ImageOps.fit(img.convert("RGB"), (int(W * 1.1), int(H * 1.1)), Image.LANCZOS)


def zoom(img, z):
    """Recorte central de 1080x1920 com aproximação z (1.0 = mais aberto)."""
    w, h = W * 1.1 / z, H * 1.1 / z
    x0, y0 = (img.width - w) / 2, (img.height - h) / 2
    return img.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + w, y0 + h))


def sombra(alfa, centro=0.5):
    """Faixa escura na altura do texto para ele ficar legível sobre a foto."""
    y = np.linspace(0, 1, H)[:, None]
    faixa = np.exp(-((y - centro) / 0.2) ** 2) * alfa
    return (1 - faixa)[..., None]


def texto(img, xy, s, f, cor, alfa):
    if alfa <= 0:
        return
    camada = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    d.text((xy[0] + 3, xy[1] + 3), s, font=f, fill=(0, 0, 0, int(160 * alfa)), anchor="mm")
    d.text(xy, s, font=f, fill=cor + (int(255 * alfa),), anchor="mm")
    img.alpha_composite(camada)


def quadro(t, foto, cadeira, cadeira_pb, y1=945):
    # Cena 1: ela, aproximando devagar; cena 2: a cadeira, perdendo a cor
    if t < TROCA + 0.8:
        a = np.asarray(zoom(foto, 1.0 + 0.06 * t / TROCA), np.float32)
    if t >= TROCA:
        z = 1.0 + 0.05 * (t - TROCA) / (DURACAO - TROCA)
        cor = np.asarray(zoom(cadeira, z), np.float32)
        pb = np.asarray(zoom(cadeira_pb, z), np.float32)
        b = cor + (pb - cor) * aparece(t, TROCA + 0.6, 1.4)
        mistura = aparece(t, TROCA, 0.8)
        a = b if mistura >= 1 else a * (1 - mistura) + b * mistura
    a = a * sombra(0.55 * (1 - aparece(t, TROCA - 0.6, 0.6)), y1 / H) * sombra(0.6 * aparece(t, TROCA + 1.6, 0.8))
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")

    some1 = 1 - aparece(t, TROCA - 0.6, 0.5)
    f1, f2 = estilo.serifa(84, 600), estilo.serifa_italica(104, 600)
    texto(img, (CX, y1 - 105), "Vou te contar o que eu faço", f1, estilo.BRANCO, aparece(t, 0.4) * some1)
    texto(img, (CX, y1 - 5), "quando alguém", f1, estilo.BRANCO, aparece(t, 1.4) * some1)
    texto(img, (CX, y1 + 115), "me desrespeita.", f2, estilo.DOURADO, aparece(t, 2.2, 0.8) * some1)

    texto(img, (CX, 810), "Eu não discuto.", f1, estilo.BRANCO, aparece(t, TROCA + 1.8))
    texto(img, (CX, 910), "Eu não explico.", f1, estilo.BRANCO, aparece(t, TROCA + 2.8))
    texto(img, (CX, 1050), "Eu me retiro.", estilo.serifa_italica(110, 600), estilo.DOURADO,
          aparece(t, TROCA + 4.0, 0.8))
    ac = aparece(t, TROCA + 5.0, 0.8)
    if ac > 0:
        cred = Image.new("RGBA", img.size, (0, 0, 0, 0))
        estilo.texto_espacado(ImageDraw.Draw(cred), (CX, 1180), estilo.ASSINATURA, estilo.sem_serifa(26, 500),
                              estilo.BRANCO + (int(200 * ac),), 8)
        img.alpha_composite(cred)
    return estilo.granulado(np.asarray(img.convert("RGB"), np.float32), intensidade=3.0)


def main():
    p = argparse.ArgumentParser(description="Reel cadeira vazia")
    p.add_argument("foto")
    p.add_argument("cadeira")
    p.add_argument("saida", nargs="?")
    p.add_argument("--recorte-cadeira", help="x0,y0,x1,y1 da cadeira vazia dentro da imagem")
    p.add_argument("--altura-texto", type=int, default=945,
                   help="altura (px, de 1920) do centro do texto na foto dela; use onde a roupa é lisa")
    a = p.parse_args()
    saida = Path(a.saida) if a.saida else estilo.PASTA / "saida" / "cadeira-vazia.mp4"
    saida.parent.mkdir(parents=True, exist_ok=True)

    foto = preencher(Image.open(a.foto))
    cad = Image.open(a.cadeira).convert("RGB")
    if a.recorte_cadeira:
        cad = cad.crop(tuple(int(v) for v in a.recorte_cadeira.split(",")))
        cad = cad.filter(ImageFilter.GaussianBlur(0.6))  # recorte pequeno: suaviza o serrilhado
    cadeira = preencher(cad)
    cadeira_pb = ImageOps.grayscale(cadeira).convert("RGB")

    mudo = saida.with_suffix(".mudo.mp4")
    ff = midia.gravador(mudo, estatico=False)
    for k in range(int(DURACAO * FPS)):
        ff.stdin.write(estilo.para_bytes(quadro(k / FPS, foto, cadeira, cadeira_pb, a.altura_texto)))
    ff.stdin.close()
    ff.wait()
    midia.juntar_audio(mudo, saida)
    print(f"Pronto: {saida} ({midia.duracao(saida):.1f} s)")


if __name__ == "__main__":
    sys.exit(main())
