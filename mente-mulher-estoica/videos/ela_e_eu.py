"""Formato "Ela é… / Eu sou…": tela dividida, rótulo no alto e você embaixo.

Cada par mostra, na metade de cima (fundo claro), o rótulo que os outros dão e, na de
baixo, uma foto ou vídeo seu, com o rosto livre. A resposta fica logo abaixo do rótulo. Fecha com uma citação na tela da marca.
As fotos e vídeos entram em preto e branco, como a marca.

Exemplo:
    python3 ela_e_eu.py \\
        --par "Ela é fria.|Eu sou serena.|foto1.jpg" \\
        --par "Ela é difícil.|Eu tenho limites.|video.mp4" \\
        --final "Ele não conhecia meus outros defeitos,|*senão teria falado deles também.*" \\
        --autor "EPICTETO · MANUAL, 33"
"""

import argparse
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageOps

import estilo
import midia

TEMPO_PAR, TEMPO_FINAL = 2.6, 4.5
METADE = estilo.ALTURA // 2
CLARO = (233, 229, 223)
ESCURO = (34, 32, 30)
VIDEO = {".mp4", ".mov", ".m4v"}


def quadros_midia(caminho, n):
    """n quadros (largura x METADE), em P&B, de uma foto (zoom lento) ou de um vídeo."""
    caminho = Path(caminho)
    if caminho.suffix.lower() in VIDEO:
        bruto = subprocess.run(
            ["ffmpeg", "-loglevel", "error", "-i", str(caminho), "-vf",
             f"fps={estilo.FPS},scale={estilo.LARGURA}:{METADE}:force_original_aspect_ratio=increase,"
             f"crop={estilo.LARGURA}:{METADE}:(iw-{estilo.LARGURA})/2:(ih-{METADE})*0.15,format=gray",
             "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "gray", "-"],
            capture_output=True, check=True).stdout
        tam = estilo.LARGURA * METADE
        qs = [np.frombuffer(bruto[i * tam:(i + 1) * tam], np.uint8).reshape(METADE, estilo.LARGURA)
              for i in range(len(bruto) // tam)]
        while len(qs) < n:  # vídeo curto: congela o último quadro
            qs.append(qs[-1])
        return [np.repeat(q[..., None], 3, 2).astype(np.float32) for q in qs]
    foto = ImageOps.grayscale(ImageOps.exif_transpose(Image.open(caminho))).convert("RGB")
    grande = ImageOps.fit(foto, (int(estilo.LARGURA * 1.08), int(METADE * 1.08)), centering=(0.5, 0.12))
    saida = []
    for k in range(n):
        z = 1.08 - 0.08 * k / max(n - 1, 1)
        w, h = int(estilo.LARGURA * z), int(METADE * z)
        x0, y0 = (grande.width - w) // 2, 0
        saida.append(np.asarray(grande.crop((x0, y0, x0 + w, y0 + h)).resize((estilo.LARGURA, METADE)), np.float32))
    return saida


def camada_texto(rotulo, resposta):
    img = Image.new("RGBA", (estilo.LARGURA, estilo.ALTURA), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, estilo.LARGURA, METADE), fill=CLARO + (255,))
    estilo.texto_espacado(d, (estilo.LARGURA / 2, estilo.TOPO_SEGURO - 20), "@MENTE.MULHER.ESTOICA",
                          estilo.sem_serifa(22, 500), ESCURO + (255,), 6)
    # Rótulo (o que dizem) e resposta (quem eu sou) ficam na metade clara: o rosto fica livre
    f = estilo.sem_serifa(52, 500)
    largura = estilo.LARGURA - 2 * estilo.MARGEM_X
    y = METADE * 0.40
    for l in estilo.quebrar_linhas(f"“{rotulo}”", f, largura):
        d.text((estilo.LARGURA / 2, y), l, font=f, fill=(110, 104, 98, 255), anchor="mm")
        y += 64
    d.line((estilo.LARGURA / 2 - 40, y + 4, estilo.LARGURA / 2 + 40, y + 4), fill=estilo.DOURADO + (255,), width=3)
    f2 = estilo.sem_serifa(68, 800)
    y += 80
    for l in estilo.quebrar_linhas(resposta, f2, largura):
        d.text((estilo.LARGURA / 2, y), l, font=f2, fill=ESCURO + (255,), anchor="mm")
        y += 82
    return estilo.Camada(img)


def gerar(pares, final, autor, saida):
    ff = midia.gravador(saida.with_suffix(".mudo.mp4"), estatico=False)
    n = int(TEMPO_PAR * estilo.FPS)
    ultimo = None
    for rotulo, resposta, midia_par in pares:
        txt = camada_texto(rotulo, resposta)
        for k, m in enumerate(quadros_midia(midia_par, n)):
            q = np.zeros((estilo.ALTURA, estilo.LARGURA, 3), np.float32)
            q[METADE:] = m
            txt.compor(q)
            ff.stdin.write(estilo.para_bytes(q))
            ultimo = q
    if final:
        fundo = estilo.granulado(estilo.Camada(estilo.moldura()).compor(estilo.fundo()))
        img = estilo.tela_final_linhas([(p.strip().strip("*"), p.strip().startswith("*")) for p in final.split("|")])
        caixa = img.getbbox()
        if autor and caixa:
            estilo.texto_espacado(ImageDraw.Draw(img), (estilo.LARGURA / 2, caixa[3] + 70), autor,
                                  estilo.sem_serifa(24, 500), estilo.CINZA + (255,), 8)
        cam = estilo.Camada(img)
        for k in range(int(TEMPO_FINAL * estilo.FPS)):
            t = k / estilo.FPS
            m = estilo.suavizar(t / 0.6)
            q = ultimo * (1 - m) + fundo * m
            p = estilo.suavizar((t - 0.4) / 0.8) if t > 0.4 else 0.0
            cam.compor(q, p, int(round((1 - p) * 26)))
            ff.stdin.write(estilo.para_bytes(q))
    ff.stdin.close()
    ff.wait()
    midia.juntar_audio(saida.with_suffix(".mudo.mp4"), saida)
    return midia.duracao(saida)


def main():
    p = argparse.ArgumentParser(description="Formato 'Ela é… / Eu sou…'")
    p.add_argument("--par", action="append", required=True, help='"rótulo|resposta|foto-ou-video"')
    p.add_argument("--final", default="", help="citação final; | quebra linha, *x* destaca")
    p.add_argument("--autor", default="")
    p.add_argument("--saida")
    a = p.parse_args()
    pares = [tuple(x.strip() for x in par.split("|", 2)) for par in a.par]
    saida = Path(a.saida) if a.saida else estilo.PASTA / "saida" / "ela-e-eu.mp4"
    saida.parent.mkdir(parents=True, exist_ok=True)
    print(f"Pronto: {saida} ({gerar(pares, a.final, a.autor, saida):.1f} s)")


if __name__ == "__main__":
    sys.exit(main())
