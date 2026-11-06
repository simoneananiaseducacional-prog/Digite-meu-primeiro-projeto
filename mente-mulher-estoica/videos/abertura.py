"""Formato "abertura": sua foto com uma frase, depois o vídeo, e um fecho estoico.

Linha do tempo:
  1. Foto em tela cheia (P&B, zoom lento) com a frase de abertura no alto.
  2. Transição suave para o vídeo, com o crédito do autor.
  3. Tela final da marca com a citação estoica que amarra a cena.

Nos textos, `|` quebra a linha e `*trecho*` vira destaque em itálico dourado.

Exemplo:
    python3 abertura.py video.mp4 --foto foto.jpg \\
        --texto "O estoicismo|*em uma cena.*" \\
        --final "Não é pouco o tempo que temos.|*É muito o que perdemos.*" --autor SÊNECA \\
        --credito @autor --ate 12.7
"""

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageOps

import estilo
import midia

TEMPO_FOTO, TRANSICAO, TEMPO_FINAL = 3.0, 0.5, 4.5
ZOOM = 0.06


def linhas(texto):
    """'linha|*destaque*' -> [(texto, destaque)]"""
    saida = []
    for parte in texto.split("|"):
        parte = parte.strip()
        destaque = parte.startswith("*") and parte.endswith("*")
        saida.append((parte.strip("*").strip(), destaque))
    return saida


Y_FOTO, DEGRADE = 560, 360


def foto_base(caminho, foco_x, colorida):
    """Foto para a parte de baixo da tela, com folga para o zoom."""
    foto = ImageOps.exif_transpose(Image.open(caminho)).convert("RGB")
    if not colorida:
        foto = ImageOps.grayscale(foto).convert("RGB")
    largura = int(estilo.LARGURA * (1 + ZOOM))
    altura = int((estilo.ALTURA - Y_FOTO) * (1 + ZOOM))
    return ImageOps.fit(foto, (largura, altura), centering=(foco_x, 0.0))


def mascara_foto():
    """Alfa da foto: some em degradê no alto, para se fundir ao fundo preto."""
    altura = estilo.ALTURA - Y_FOTO
    alfa = np.ones((altura, estilo.LARGURA, 1), np.float32)
    alfa[:DEGRADE, :, 0] = (np.linspace(0, 1, DEGRADE, dtype=np.float32) ** 1.6)[:, None]
    return alfa


def camada_abertura(texto):
    """Assinatura e frase de abertura, no alto da tela, acima da foto."""
    img = Image.new("RGBA", (estilo.LARGURA, estilo.ALTURA), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    estilo.texto_espacado(d, (estilo.LARGURA / 2, estilo.TOPO_SEGURO - 70), estilo.ASSINATURA,
                          estilo.sem_serifa(22, 500), estilo.DOURADO + (255,), 9)
    y = estilo.TOPO_SEGURO + 30
    for t, destaque in linhas(texto):
        f = estilo.serifa_italica(100, 600) if destaque else estilo.serifa(92, 500)
        cor = estilo.DOURADO if destaque else estilo.BRANCO
        for linha in estilo.quebrar_linhas(t, f, estilo.LARGURA - 2 * estilo.MARGEM_X):
            d.text((estilo.LARGURA / 2, y + 55), linha, font=f, fill=cor + (255,), anchor="mm")
            y += 112
    return estilo.Camada(img)


def camada_credito(credito, y):
    img = Image.new("RGBA", (estilo.LARGURA, estilo.ALTURA), (0, 0, 0, 0))
    ImageDraw.Draw(img).text((estilo.LARGURA / 2, y), f"vídeo: {credito}",
                             font=estilo.sem_serifa(24, 400), fill=estilo.CINZA + (255,), anchor="mm")
    return estilo.Camada(img)


def tela_final(texto, autor):
    img = estilo.tela_final_linhas(linhas(texto))
    caixa = img.getbbox()
    if autor and caixa:
        estilo.texto_espacado(ImageDraw.Draw(img), (estilo.LARGURA / 2, caixa[3] + 70), autor,
                              estilo.sem_serifa(24, 500), estilo.CINZA + (255,), 8)
    return img


def base_de_contorno(video):
    """Onde termina a imagem útil do vídeo (abaixo vem tarja preta), para pôr o crédito."""
    import subprocess

    bruto = subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-ss", "1", "-i", str(video), "-frames:v", "1",
         "-vf", f"scale={estilo.LARGURA}:{estilo.ALTURA}", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
        capture_output=True, check=True,
    ).stdout
    a = np.frombuffer(bruto, np.uint8).reshape(estilo.ALTURA, estilo.LARGURA)
    claras = np.where(a.mean(1) > 12)[0]
    return int(claras[-1]) if len(claras) else estilo.BASE_SEGURA - 60


def gerar(video, foto, saida, texto, final, autor="", credito="", ate=None,
          foco_x=0.15, colorida=False):
    fps = estilo.FPS
    grande = foto_base(foto, foco_x, colorida)
    alfa_foto = mascara_foto()
    fundo_foto = estilo.granulado(estilo.fundo())
    abertura = camada_abertura(texto)
    y_credito = min(base_de_contorno(video) + 40, estilo.BASE_SEGURA)
    credito_cam = camada_credito(credito, y_credito) if credito else None
    fundo = estilo.granulado(estilo.Camada(estilo.moldura()).compor(estilo.fundo()))
    final_cam = estilo.Camada(tela_final(final, autor)) if final else None

    mudo = saida.with_suffix(".mudo.mp4")
    ff = midia.gravador(mudo, estatico=False)

    def quadro_foto(k):
        t = k / fps
        z = 1 + ZOOM * (1 - t / (TEMPO_FOTO + TRANSICAO))
        altura = estilo.ALTURA - Y_FOTO
        w, h = int(estilo.LARGURA * z), int(altura * z)
        x0 = (grande.width - w) // 2
        img = grande.crop((x0, 0, x0 + w, h)).resize((estilo.LARGURA, altura))
        q = fundo_foto.copy()
        regiao = q[Y_FOTO:]
        regiao *= 1 - alfa_foto
        regiao += np.asarray(img, np.float32) * alfa_foto
        op = min(1.0, t / 0.4)
        return abertura.compor(q, op)

    # 1. Foto
    n_foto = int(TEMPO_FOTO * fps)
    for k in range(n_foto):
        ff.stdin.write(estilo.para_bytes(quadro_foto(k)))

    # 2. Vídeo (as primeiras imagens se misturam com a foto)
    tamanho = estilo.LARGURA * estilo.ALTURA * 3
    entrada = midia.leitor(video, ate=ate)
    n_trans = int(TRANSICAO * fps)
    i, ultimo = 0, None
    while True:
        bruto = entrada.stdout.read(tamanho)
        if len(bruto) < tamanho:
            break
        q = np.frombuffer(bruto, np.uint8).reshape(estilo.ALTURA, estilo.LARGURA, 3).astype(np.float32)
        if credito_cam:
            credito_cam.compor(q, min(1.0, i / fps))
        if i < n_trans:
            m = estilo.suavizar(i / n_trans)
            q = quadro_foto(n_foto + i) * (1 - m) + q * m
        ff.stdin.write(estilo.para_bytes(q))
        ultimo, i = q, i + 1
    entrada.wait()

    # 3. Fecho estoico
    if final_cam is not None and ultimo is not None:
        for k in range(int(TEMPO_FINAL * fps)):
            t = k / fps
            m = estilo.suavizar(t / 0.8)
            q = ultimo * (1 - m) + fundo * m
            p = estilo.suavizar((t - 0.6) / 0.8) if t > 0.6 else 0.0
            final_cam.compor(q, p, int(round((1 - p) * 26)))
            ff.stdin.write(estilo.para_bytes(q))
    ff.stdin.close()
    ff.wait()

    voz = video if midia.tem_audio(video) else None
    midia.juntar_audio(mudo, saida, voz=voz, atraso_voz=TEMPO_FOTO, fade_final=2.0)
    return midia.duracao(saida)


def main():
    p = argparse.ArgumentParser(description="Sua foto com uma frase, o vídeo, e um fecho estoico")
    p.add_argument("video")
    p.add_argument("--foto", required=True)
    p.add_argument("--texto", required=True, help="frase sobre a foto; | quebra linha, *x* destaca")
    p.add_argument("--final", default="", help="frase da tela final; | quebra linha, *x* destaca")
    p.add_argument("--autor", default="", help="assinatura da citação final, ex.: SÊNECA")
    p.add_argument("--credito", default="", help="arroba do autor do vídeo")
    p.add_argument("--ate", type=float, help="corta o vídeo neste segundo")
    p.add_argument("--foco-x", type=float, default=0.15,
                   help="parte da foto na horizontal: 0 = esquerda, 0.5 = centro (padrão 0.15)")
    p.add_argument("--colorida", action="store_true")
    p.add_argument("--saida")
    a = p.parse_args()

    saida = Path(a.saida) if a.saida else estilo.PASTA / "saida" / f"{Path(a.video).stem[:40]}-abertura.mp4"
    saida.parent.mkdir(parents=True, exist_ok=True)
    total = gerar(a.video, a.foto, saida, a.texto, a.final, a.autor, a.credito, a.ate,
                  a.foco_x, a.colorida)
    print(f"Pronto: {saida} ({total:.1f} s)")


if __name__ == "__main__":
    sys.exit(main())
