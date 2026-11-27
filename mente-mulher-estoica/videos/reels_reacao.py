"""Reel "reação": a foto dela apontando para um vídeo que toca num cartão, com uma chamada
embaixo e, no fim, a frase autoral da marca. O áudio é o do próprio vídeo.

    python3 reels_reacao.py foto.jpg video.mp4 [saida.mp4] --cartao x0,y0,largura
        [--chamada "Um recado pra você, mulher:"] [--frase "linha 1|linha 2|*linha dourada*"]

`--cartao` diz onde o vídeo aparece (em pixels de 1080x1920) e a largura dele; a altura
segue o formato do vídeo. Na frase, "|" quebra a linha e *asteriscos* deixam a linha dourada.
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


def aparece(t, t0, dur=0.6):
    return estilo.suavizar((t - t0) / dur) if t > t0 else 0.0


def texto(img, xy, s, f, cor, alfa):
    if alfa <= 0:
        return
    camada = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    d.text((xy[0] + 3, xy[1] + 3), s, font=f, fill=(0, 0, 0, int(170 * alfa)), anchor="mm")
    d.text(xy, s, font=f, fill=cor + (int(255 * alfa),), anchor="mm")
    img.alpha_composite(camada)


def main():
    p = argparse.ArgumentParser(description="Reel de reação: foto + vídeo num cartão + frase final")
    p.add_argument("foto")
    p.add_argument("video")
    p.add_argument("saida", nargs="?")
    p.add_argument("--cartao", required=True, help="x0,y0,largura do vídeo na tela")
    p.add_argument("--chamada", default="Um recado pra você, mulher:")
    p.add_argument("--frase", default="Você não veio ao mundo|para sobreviver a ninguém.|*Veio para viver.*")
    p.add_argument("--final", type=float, default=5.0, help="segundos da frase final no fim do vídeo")
    a = p.parse_args()
    saida = Path(a.saida) if a.saida else estilo.PASTA / "saida" / "reels-reacao.mp4"
    saida.parent.mkdir(parents=True, exist_ok=True)

    duracao = midia.duracao(a.video)
    x0, y0, cw = (int(v) for v in a.cartao.split(","))
    # Altura do cartão no formato do vídeo (par, para o ffmpeg)
    import subprocess, json
    info = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                      "stream=width,height", "-of", "json", a.video],
                                     capture_output=True, text=True, check=True).stdout)["streams"][0]
    ch = int(round(cw * info["height"] / info["width"] / 2)) * 2

    fundo = ImageOps.fit(Image.open(a.foto).convert("RGB"), (W, H), Image.LANCZOS, centering=(0.5, 0.3))
    # Escurece a base para a chamada ficar legível
    y = np.linspace(0, 1, H)[:, None, None]
    base = np.asarray(fundo, np.float32) * (1 - 0.65 * np.clip((y - 0.62) / 0.25, 0, 1))
    fundo = Image.fromarray(base.astype(np.uint8)).convert("RGBA")

    raio = 34
    mascara = Image.new("L", (cw, ch), 0)
    ImageDraw.Draw(mascara).rounded_rectangle((0, 0, cw - 1, ch - 1), raio, fill=255)
    sombra = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sombra).rounded_rectangle((x0 + 8, y0 + 14, x0 + cw + 8, y0 + ch + 14), raio, fill=(0, 0, 0, 150))
    sombra = sombra.filter(ImageFilter.GaussianBlur(18))
    moldura = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(moldura).rounded_rectangle((x0 - 3, y0 - 3, x0 + cw + 2, y0 + ch + 2), raio + 3,
                                              outline=estilo.DOURADO + (255,), width=4)
    base_fixa = Image.alpha_composite(fundo, sombra)

    linhas = a.frase.split("|")
    t_final = duracao - a.final
    leitor = midia.leitor(a.video, cw, ch)
    mudo = saida.with_suffix(".mudo.mp4")
    ff = midia.gravador(mudo, estatico=False)
    tam = cw * ch * 3
    ultimo = None
    for k in range(int(duracao * FPS)):
        t = k / FPS
        bruto = leitor.stdout.read(tam)
        if len(bruto) == tam:
            ultimo = Image.frombytes("RGB", (cw, ch), bruto)
        img = base_fixa.copy()
        if ultimo is not None:
            img.paste(ultimo, (x0, y0), mascara)
        img.alpha_composite(moldura)
        texto(img, (CX, 1560), a.chamada, estilo.serifa_italica(70, 600), estilo.BRANCO,
              aparece(t, 0.6) * (1 - aparece(t, t_final - 0.6, 0.6)))

        # Frase final: a tela escurece e a frase entra linha a linha
        esc = aparece(t, t_final, 1.0)
        if esc > 0:
            veu = Image.new("RGBA", (W, H), (11, 11, 11, int(225 * esc)))
            img.alpha_composite(veu)
            y_l = 900 - 55 * (len(linhas) - 1)
            for i, l in enumerate(linhas):
                dourada = l.startswith("*") and l.endswith("*")
                f = estilo.serifa_italica(96, 600) if dourada else estilo.serifa(72, 500)
                texto(img, (CX, y_l), l.strip("*"), f, estilo.DOURADO if dourada else estilo.BRANCO,
                      aparece(t, t_final + 0.6 + 0.5 * i, 0.8))
                y_l += 120 if dourada else 95
            ac = aparece(t, t_final + 0.8 + 0.5 * len(linhas), 0.8)
            if ac > 0:
                cred = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                estilo.texto_espacado(ImageDraw.Draw(cred), (CX, y_l + 60), estilo.ASSINATURA,
                                      estilo.sem_serifa(26, 500), estilo.CINZA + (int(255 * ac),), 8)
                img.alpha_composite(cred)
        ff.stdin.write(np.asarray(img.convert("RGB")).tobytes())
    ff.stdin.close()
    ff.wait()
    leitor.stdout.close()
    leitor.wait()
    midia.juntar_audio(mudo, saida, voz=a.video)
    print(f"Pronto: {saida} ({midia.duracao(saida):.1f} s)")


if __name__ == "__main__":
    sys.exit(main())
