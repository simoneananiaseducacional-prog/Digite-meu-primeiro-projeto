"""Série "a frase da caneca": foto da caneca com fumaça animada e uma linha de contexto.

A foto ganha um zoom lento em direção à caneca, fumaça subindo do café e, no alto,
o contexto que ajuda a frase da caneca a ser entendida. Nos textos, `|` quebra a
linha e `*trecho*` vira destaque dourado.

Exemplo:
    python3 caneca.py foto-caneca.png --cafe 440,660,200 \\
        --contexto "Antes de responder|aquela mensagem," --virada "*leia a caneca.*"

`--cafe x,y,raio` marca, em pixels da foto original, o centro da superfície do café e
a metade da largura dela: é de lá que a fumaça sobe.
"""

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import estilo
import midia

DURACAO = 10.0
ZOOM = 0.10
ENTRA_CONTEXTO, ENTRA_VIRADA = 0.8, 3.6
ESCALA_FUMACA = 4  # a fumaça é calculada em 1/4 da resolução e depois ampliada


def linhas(texto):
    saida = []
    for parte in texto.split("|"):
        parte = parte.strip()
        destaque = parte.startswith("*") and parte.endswith("*")
        saida.append((parte.strip("*").strip(), destaque))
    return saida


class Enquadramento:
    """Leva coordenadas da foto para a tela, com zoom lento centrado na caneca."""

    def __init__(self, foto, ancora, y_ancora=1080):
        self.foto = foto
        self.ax, self.ay = ancora
        self.y_ancora = y_ancora
        self.s0 = max(estilo.ALTURA / foto.height, estilo.LARGURA / foto.width) * 1.02

    def escala(self, t):
        return self.s0 * (1 + ZOOM * estilo.suavizar(t / DURACAO))

    def para_tela(self, x, y, t):
        s = self.escala(t)
        return (x - self.ax) * s + estilo.LARGURA / 2, (y - self.ay) * s + self.y_ancora

    def quadro(self, t):
        s = self.escala(t)
        # Transformação inversa (tela -> foto) para o Image.transform
        a, c = 1 / s, self.ax - (estilo.LARGURA / 2) / s
        e, f = 1 / s, self.ay - self.y_ancora / s
        img = self.foto.transform((estilo.LARGURA, estilo.ALTURA), Image.AFFINE,
                                  (a, 0, c, 0, e, f), resample=Image.BICUBIC)
        return np.asarray(img, np.float32)


class Fumaca:
    """Fios de vapor: manchas suaves que sobem, ondulam, crescem e somem."""

    def __init__(self, cafe, semente=3):
        self.cx, self.cy, self.raio = cafe
        rng = np.random.default_rng(semente)
        n = int(DURACAO * 14) + 60
        self.nasce = np.sort(rng.uniform(-4.0, DURACAO, n))
        self.vida = rng.uniform(2.8, 4.2, n)
        self.x0 = self.cx + rng.uniform(-0.75, 0.75, n) * self.raio
        self.subida = rng.uniform(85, 130, n)            # px da foto por segundo
        self.onda = rng.uniform(10, 26, n)
        self.freq = rng.uniform(0.9, 1.7, n)
        self.fase = rng.uniform(0, 2 * np.pi, n)
        self.deriva = rng.uniform(-10, 10, n)
        self.r0 = rng.uniform(5, 9, n)
        self.forca = rng.uniform(0.35, 0.6, n)
        h, w = estilo.ALTURA // ESCALA_FUMACA, estilo.LARGURA // ESCALA_FUMACA
        self.yy, self.xx = np.mgrid[0:h, 0:w].astype(np.float32)
        # Textura de fios verticais que sobe junto, para quebrar as manchas
        ruido = rng.random((h // 6, w // 2)).astype(np.float32)
        img = Image.fromarray((ruido * 255).astype(np.uint8)).resize((w, h * 2), Image.BICUBIC)
        r = np.asarray(img.filter(ImageFilter.GaussianBlur(2)), np.float32) / 255
        r = (r - r.min()) / (r.max() - r.min() + 1e-6)
        self.textura = np.clip(r * 1.8 - 0.5, 0, 1) ** 1.3

    def alfa(self, t, enq):
        h, w = self.yy.shape
        mapa = np.zeros((h, w), np.float32)
        s = enq.escala(t) / ESCALA_FUMACA
        idade = t - self.nasce
        vivas = np.where((idade > 0) & (idade < self.vida))[0]
        for i in vivas:
            a = idade[i]
            x = self.x0[i] + self.onda[i] * np.sin(self.freq[i] * a + self.fase[i]) + self.deriva[i] * a
            y = self.cy - self.subida[i] * a
            X, Y = enq.para_tela(x, y, t)
            X, Y = X / ESCALA_FUMACA, Y / ESCALA_FUMACA
            r = (self.r0[i] + 9 * a) * s
            brilho = self.forca[i] * np.sin(np.pi * a / self.vida[i]) ** 1.5
            x0, x1 = int(max(X - 3 * r, 0)), int(min(X + 3 * r, w))
            y0, y1 = int(max(Y - 3 * r, 0)), int(min(Y + 3 * r, h))
            if x0 >= x1 or y0 >= y1:
                continue
            dx = self.xx[y0:y1, x0:x1] - X
            dy = (self.yy[y0:y1, x0:x1] - Y) * 0.7     # manchas alongadas na vertical
            mapa[y0:y1, x0:x1] += brilho * np.exp(-(dx * dx + dy * dy) / (2 * r * r))
        desloc = int(t * 30) % h
        mapa *= 0.3 + 0.7 * self.textura[desloc:desloc + h]
        # O vapor nasce rente ao café: some suavemente perto da superfície
        _, borda = enq.para_tela(self.cx, self.cy, t)
        b = borda / ESCALA_FUMACA
        mapa *= np.clip((b - self.yy[:, :1]) / 18, 0, 1) ** 1.5
        mapa = (1 - np.exp(-mapa * 2.2)) * 0.7
        img = Image.fromarray(np.clip(mapa * 255, 0, 255).astype(np.uint8))
        img = img.resize((estilo.LARGURA, estilo.ALTURA), Image.BILINEAR).filter(ImageFilter.GaussianBlur(3))
        return np.asarray(img, np.float32)[..., None] / 255


def camada_textos(contexto, virada):
    """Contexto e virada no alto, sobre um degradê escuro que garante a leitura."""
    escuro = Image.new("RGBA", (estilo.LARGURA, estilo.ALTURA), (0, 0, 0, 0))
    alfa = np.zeros((estilo.ALTURA, estilo.LARGURA), np.float32)
    alfa[:980] = (np.clip(1 - np.arange(980) / 980, 0, 1) ** 1.1 * 0.88)[:, None]
    escuro.putalpha(Image.fromarray((alfa * 255).astype(np.uint8)))

    def escrever(texto, y):
        img = Image.new("RGBA", (estilo.LARGURA, estilo.ALTURA), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        for t, destaque in linhas(texto):
            f = estilo.serifa_italica(84, 600) if destaque else estilo.serifa(76, 500)
            cor = estilo.DOURADO if destaque else estilo.BRANCO
            for linha in estilo.quebrar_linhas(t, f, estilo.LARGURA - 2 * estilo.MARGEM_X):
                d.text((estilo.LARGURA / 2, y), linha, font=f, fill=cor + (255,), anchor="mm")
                y += 92
        # Sombra difusa por trás das letras, para ler mesmo sobre o vapor
        sombra = Image.new("RGBA", img.size, (0, 0, 0, 0))
        sombra.putalpha(img.getchannel("A").filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.8)))
        return Image.alpha_composite(sombra, img), y

    y = estilo.TOPO_SEGURO + 60
    ctx, y = escrever(contexto, y)
    vir, _ = escrever(virada, y + 10) if virada else (None, y)
    assinatura = Image.new("RGBA", (estilo.LARGURA, estilo.ALTURA), (0, 0, 0, 0))
    estilo.texto_espacado(ImageDraw.Draw(assinatura), (estilo.LARGURA / 2, estilo.TOPO_SEGURO - 50),
                          estilo.ASSINATURA, estilo.sem_serifa(22, 500), estilo.DOURADO + (255,), 9)
    return (estilo.Camada(Image.alpha_composite(escuro, assinatura)), estilo.Camada(ctx),
            estilo.Camada(vir) if vir else None)


def gerar(foto, saida, cafe, contexto, virada="", musica=None):
    img = Image.open(foto).convert("RGB")
    enq = Enquadramento(img, (cafe[0], cafe[1] + 140))
    fumaca = Fumaca(cafe)
    fundo_txt, ctx, vir = camada_textos(contexto, virada)
    vapor = np.array((246, 244, 240), np.float32)

    mudo = saida.with_suffix(".mudo.mp4")
    ff = midia.gravador(mudo, estatico=False)
    n = int(DURACAO * estilo.FPS)
    for k in range(n):
        t = k / estilo.FPS
        q = enq.quadro(t)
        a = fumaca.alfa(t, enq)
        q = q * (1 - a) + vapor * a
        fundo_txt.compor(q)
        p = estilo.suavizar((t - ENTRA_CONTEXTO) / 0.9) if t > ENTRA_CONTEXTO else 0
        ctx.compor(q, p, int(round((1 - p) * 20)))
        if vir is not None and t > ENTRA_VIRADA:
            p = estilo.suavizar((t - ENTRA_VIRADA) / 0.9)
            vir.compor(q, p, int(round((1 - p) * 20)))
        ff.stdin.write(estilo.para_bytes(q))
        if k % estilo.FPS == 0:
            print(f"\r  {k // estilo.FPS} s", end="", flush=True)
    ff.stdin.close()
    ff.wait()
    print()
    midia.juntar_audio(mudo, saida, musica=musica)
    return midia.duracao(saida)


def main():
    p = argparse.ArgumentParser(description="A frase da caneca, com fumaça e contexto")
    p.add_argument("foto")
    p.add_argument("--cafe", required=True, help="x,y,raio da superfície do café na foto original")
    p.add_argument("--contexto", required=True, help="linha de contexto; | quebra linha, *x* destaca")
    p.add_argument("--virada", default="", help="segunda linha, entra depois; ex.: *leia a caneca.*")
    p.add_argument("--musica", help="música de fundo (opcional; dá para pôr no app)")
    p.add_argument("--saida")
    a = p.parse_args()

    cafe = tuple(float(v) for v in a.cafe.split(","))
    saida = Path(a.saida) if a.saida else estilo.PASTA / "saida" / f"{Path(a.foto).stem}-caneca.mp4"
    saida.parent.mkdir(parents=True, exist_ok=True)
    total = gerar(a.foto, saida, cafe, a.contexto, a.virada, a.musica)
    print(f"Pronto: {saida} ({total:.1f} s)")


if __name__ == "__main__":
    sys.exit(main())
