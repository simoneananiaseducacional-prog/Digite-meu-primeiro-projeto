"""Lista estoica animada, no mesmo visual de depende_de_mim.py: título em serifa, itens que
entram um a um com número e palavra-chave em dourado (sublinhada por um traço que se
desenha), e uma frase final com a assinatura.

    python3 lista_estoica.py textos/segredos.txt [saida.mp4]

Formato do texto: 1ª linha = título ("|" quebra), linhas seguintes = itens (*palavra* fica
dourada), última linha começando com ">" = frase final ("|" quebra, *linha* dourada).
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

import estilo
import midia

CX = estilo.LARGURA // 2
X_NUM, X_TEXTO, X_MAX = 120, 210, estilo.LARGURA - 90
Y_LISTA, PASSO = 680, 140
ENTRADA, INTERVALO = 2.2, 1.9  # quando entra o 1º item e o espaço entre itens
FINAL = 5.5                    # segundos da frase final


def aparece(t, t0, dur=0.6):
    return estilo.suavizar((t - t0) / dur) if t > t0 else 0.0


def partes(linha):
    """'Foque no que *pode* controlar' -> [('Foque no que ', False), ('pode', True), (' controlar', False)]"""
    pedacos = linha.split("*")
    return [(p, i % 2 == 1) for i, p in enumerate(pedacos) if p]


def texto(img, xy, s, f, cor, alfa, ancora="mm"):
    if alfa <= 0:
        return
    camada = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(camada).text(xy, s, font=f, fill=cor + (int(255 * alfa),), anchor=ancora)
    img.alpha_composite(camada)


def item(img, y, num, linha, f, fi, alfa, traco):
    """Desenha um item; devolve nada. traco (0-1) é quanto do sublinhado dourado já foi desenhado."""
    if alfa <= 0:
        return
    camada = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    a = int(255 * alfa)
    d.text((X_NUM, y), f"{num:02d}", font=estilo.sem_serifa(30, 600), fill=estilo.DOURADO + (a,), anchor="ls")
    x = X_TEXTO
    for s, destaque in partes(linha):
        fonte = fi if destaque else f
        d.text((x, y), s, font=fonte, fill=(estilo.DOURADO if destaque else estilo.BRANCO) + (a,), anchor="ls")
        w = fonte.getlength(s)
        if destaque and traco > 0:
            # traço levemente ondulado, como feito à mão
            n = 24
            pts = [(x + w * k / n, y + 14 + 3 * np.sin(k * 0.9)) for k in range(int(n * traco) + 1)]
            if len(pts) > 1:
                d.line(pts, fill=estilo.DOURADO + (int(a * 0.85),), width=3, joint="curve")
        x += w
    img.alpha_composite(camada)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    linhas = [l.strip() for l in Path(sys.argv[1]).read_text().splitlines() if l.strip()]
    saida = Path(sys.argv[2]) if len(sys.argv) > 2 else estilo.PASTA / "saida" / "lista-estoica.mp4"
    saida.parent.mkdir(parents=True, exist_ok=True)
    titulo = linhas[0].split("|")
    final = [l[1:].strip() for l in linhas if l.startswith(">")]
    final = final[0].split("|") if final else []
    itens = [l for l in linhas[1:] if not l.startswith(">")]

    # Um tamanho só para todos os itens, o maior que caiba na largura
    tam = 56
    while True:
        f, fi = estilo.serifa(tam, 500), estilo.serifa_italica(tam + 2, 600)
        larg = max(sum((fi if dz else f).getlength(s) for s, dz in partes(l)) for l in itens)
        if X_TEXTO + larg <= X_MAX or tam <= 36:
            break
        tam -= 2

    t_cheio = ENTRADA + INTERVALO * (len(itens) - 1) + 2.2  # todos acesos por um instante
    t_final = t_cheio + 1.0
    duracao = t_final + FINAL
    fundo = np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)

    mudo = saida.with_suffix(".mudo.mp4")
    ff = midia.gravador(mudo, estatico=False)
    for k in range(int(duracao * estilo.FPS)):
        t = k / estilo.FPS
        img = Image.fromarray(fundo).convert("RGBA")
        some = 1 - aparece(t, t_cheio, 0.8)
        for i, l in enumerate(titulo):
            texto(img, (CX, estilo.TOPO_SEGURO + 110 + i * 78), l, estilo.serifa(64, 500), estilo.BRANCO,
                  aparece(t, 0.2 + 0.3 * i) * some)
        if some > 0:
            ImageDraw.Draw(img).line((CX - 40, Y_LISTA - 130, CX + 40, Y_LISTA - 130),
                                     fill=estilo.DOURADO + (int(200 * aparece(t, 1.0) * some),), width=2)
        for i, l in enumerate(itens):
            t0 = ENTRADA + INTERVALO * i
            # o item da vez fica aceso; os anteriores esmaecem até todos acenderem juntos no fim
            proximo = ENTRADA + INTERVALO * (i + 1) if i + 1 < len(itens) else t_cheio
            brilho = 1 - 0.45 * aparece(t, proximo, 0.4) + 0.45 * aparece(t, t_cheio - 1.6, 0.6)
            if i == len(itens) - 1:
                brilho = 1.0
            item(img, Y_LISTA + PASSO * i, i + 1, l, f, fi, aparece(t, t0) * min(brilho, 1) * some,
                 min(1.0, max(0.0, (t - t0 - 0.4) / 0.7)))

        y = 860 - 50 * (len(final) - 1)
        for j, l in enumerate(final):
            dourada = l.startswith("*") and l.endswith("*")
            texto(img, (CX, y), l.strip("*"), estilo.serifa_italica(62, 600) if dourada else estilo.serifa(64, 500),
                  estilo.DOURADO if dourada else estilo.BRANCO, aparece(t, t_final + 0.3 + 0.8 * j, 0.9))
            y += 100
        ac = aparece(t, t_final + 0.6 + 0.8 * len(final), 0.9)
        if ac > 0:
            cred = Image.new("RGBA", img.size, (0, 0, 0, 0))
            estilo.texto_espacado(ImageDraw.Draw(cred), (CX, y + 30), estilo.ASSINATURA, estilo.sem_serifa(24, 500),
                                  estilo.CINZA + (int(255 * ac),), 8)
            img.alpha_composite(cred)
        ff.stdin.write(estilo.para_bytes(np.asarray(img.convert("RGB"), np.float32)))
    ff.stdin.close()
    ff.wait()
    midia.juntar_audio(mudo, saida)
    mudo.unlink(missing_ok=True)
    print(f"Pronto: {saida} ({midia.duracao(saida):.1f} s)")


if __name__ == "__main__":
    sys.exit(main())
