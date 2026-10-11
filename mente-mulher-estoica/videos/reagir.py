"""Formato "indicação": um vídeo em cima e a sua foto embaixo, apontando para ele.

O vídeo fica numa moldura com cantos arredondados e filete dourado. Abaixo dele
entram o crédito do autor e uma chamada opcional. A foto ocupa a parte de baixo
e se funde ao fundo preto por um degradê, em preto e branco por padrão.

Exemplos:
    python3 reagir.py video.mp4 --foto minha-foto.jpg --credito @autor --ate 10.6
    python3 reagir.py video.mp4 --foto minha-foto.jpg --chamada "Presta atenção nisso." --colorida
    python3 reagir.py video.mp4 --foto minha-foto.jpg --previa
"""

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageOps

import estilo
import midia

MARGEM = 40
Y_VIDEO = 300
RAIO = 28
Y_FOTO = 1000
DEGRADE = 300


def dimensoes_do_video(caminho):
    import json
    import subprocess

    saida = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "json", str(caminho)],
        capture_output=True, text=True, check=True,
    )
    s = json.loads(saida.stdout)["streams"][0]
    largura = estilo.LARGURA - 2 * MARGEM
    altura = int(largura * s["height"] / s["width"]) // 2 * 2
    return largura, min(altura, Y_FOTO - Y_VIDEO - 40)


def foto_de_baixo(caminho, foco, colorida):
    """Recorta a foto para a faixa de baixo e cria o degradê que a funde ao fundo."""
    foto = ImageOps.exif_transpose(Image.open(caminho)).convert("RGB")
    if not colorida:
        foto = ImageOps.grayscale(foto).convert("RGB")
    altura = estilo.ALTURA - Y_FOTO
    foto = ImageOps.fit(foto, (estilo.LARGURA, altura), centering=(0.5, foco))
    alfa = np.ones((altura, estilo.LARGURA), np.float32)
    rampa = np.linspace(0, 1, DEGRADE, dtype=np.float32) ** 1.5
    alfa[:DEGRADE] = rampa[:, None]
    img = foto.convert("RGBA")
    img.putalpha(Image.fromarray((alfa * 255).astype(np.uint8)))
    tela = Image.new("RGBA", (estilo.LARGURA, estilo.ALTURA), (0, 0, 0, 0))
    tela.paste(img, (0, Y_FOTO))
    return tela


def foto_provisoria():
    """Silhueta cinza para testar o layout antes de ter a foto."""
    img = Image.new("RGB", (900, 1200), (70, 70, 70))
    d = ImageDraw.Draw(img)
    d.ellipse((330, 260, 570, 520), fill=(110, 110, 110))
    d.rounded_rectangle((220, 560, 680, 1200), 120, fill=(110, 110, 110))
    d.polygon([(640, 380), (700, 120), (740, 130), (690, 400)], fill=(140, 140, 140))
    d.text((450, 700), "SUA FOTO AQUI", font=estilo.sem_serifa(44, 600),
           fill=(230, 230, 230), anchor="mm")
    caminho = estilo.PASTA / "saida" / "foto-provisoria.png"
    caminho.parent.mkdir(parents=True, exist_ok=True)
    img.save(caminho)
    return caminho


def mascara_arredondada(largura, altura):
    m = Image.new("L", (largura, altura), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, largura - 1, altura - 1), RAIO, fill=255)
    return np.asarray(m, np.float32)[..., None] / 255.0


def camada_superior(largura, altura, credito, chamada):
    """Assinatura, filete em volta do vídeo, crédito e chamada."""
    img = Image.new("RGBA", (estilo.LARGURA, estilo.ALTURA), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    estilo.texto_espacado(d, (estilo.LARGURA / 2, Y_VIDEO - 70), estilo.ASSINATURA,
                          estilo.sem_serifa(22, 500), estilo.DOURADO + (255,), 9)
    d.rounded_rectangle((MARGEM - 1, Y_VIDEO - 1, MARGEM + largura, Y_VIDEO + altura),
                        RAIO, outline=estilo.DOURADO + (200,), width=2)
    y = Y_VIDEO + altura + 34
    if credito:
        d.text((MARGEM + largura, y), f"vídeo: {credito}", font=estilo.sem_serifa(22, 400),
               fill=estilo.CINZA + (255,), anchor="rm")
    if chamada:
        f = estilo.serifa_italica(62, 600)
        for i, linha in enumerate(estilo.quebrar_linhas(chamada, f, estilo.LARGURA - 2 * estilo.MARGEM_X)):
            d.text((estilo.LARGURA / 2, y + 80 + i * 72), linha, font=f,
                   fill=estilo.DOURADO + (255,), anchor="mm")
    return estilo.Camada(img)


def montar_base(foto, foco, colorida):
    base = estilo.granulado(estilo.fundo())
    return estilo.Camada(foto_de_baixo(foto, foco, colorida)).compor(base)


def gerar(video, foto, saida, credito="", chamada="", ate=None, foco=0.1,
          colorida=False, musica=None, volume_musica=0.15, previa=False):
    largura, altura = dimensoes_do_video(video)
    base = montar_base(foto, foco, colorida)
    topo = camada_superior(largura, altura, credito, chamada)
    mascara = mascara_arredondada(largura, altura)
    tamanho = largura * altura * 3

    def compor(bruto):
        quadro = base.copy()
        v = np.frombuffer(bruto, np.uint8).reshape(altura, largura, 3).astype(np.float32)
        regiao = quadro[Y_VIDEO:Y_VIDEO + altura, MARGEM:MARGEM + largura]
        regiao *= 1 - mascara
        regiao += v * mascara
        return topo.compor(quadro)

    entrada = midia.leitor(video, largura, altura, ate)
    if previa:
        quadros = [entrada.stdout.read(tamanho) for _ in range(estilo.FPS * 3)]
        entrada.kill()
        quadro = compor(quadros[-1])
        Image.frombytes("RGB", (estilo.LARGURA, estilo.ALTURA), estilo.para_bytes(quadro)).save(saida)
        return 0

    mudo = saida.with_suffix(".mudo.mp4")
    ff = midia.gravador(mudo, estatico=False)
    i = 0
    while True:
        bruto = entrada.stdout.read(tamanho)
        if len(bruto) < tamanho:
            break
        ff.stdin.write(estilo.para_bytes(compor(bruto)))
        i += 1
        if i % estilo.FPS == 0:
            print(f"\r  {i // estilo.FPS} s", end="", flush=True)
    entrada.wait()
    ff.stdin.close()
    ff.wait()
    print()

    voz = video if midia.tem_audio(video) else None
    midia.juntar_audio(mudo, saida, voz=voz, musica=musica, volume_musica=volume_musica)
    return midia.duracao(saida)


def main():
    p = argparse.ArgumentParser(description="Vídeo em cima, sua foto apontando embaixo")
    p.add_argument("video", help="vídeo que você quer indicar")
    p.add_argument("--foto", help="sua foto, apontando para cima (sem ela, usa uma silhueta de teste)")
    p.add_argument("--credito", default="", help="arroba do autor do vídeo, ex.: @autor")
    p.add_argument("--chamada", default="", help="frase curta entre o vídeo e a foto")
    p.add_argument("--ate", type=float, help="corta o vídeo neste segundo (ex.: tirar a vinheta final)")
    p.add_argument("--foco", type=float, default=0.1,
                   help="que parte da foto aparece: 0 = topo, 0.5 = meio, 1 = base (padrão 0.1)")
    p.add_argument("--colorida", action="store_true", help="mantém a foto colorida (padrão: P&B)")
    p.add_argument("--musica", help="música de fundo, baixinha sob o áudio original")
    p.add_argument("--volume-musica", type=float, default=0.15)
    p.add_argument("--previa", action="store_true", help="gera só uma imagem para conferir o layout")
    p.add_argument("--saida", help="arquivo de saída (padrão: saida/<video>-indicacao.mp4)")
    a = p.parse_args()

    foto = a.foto or foto_provisoria()
    nome = Path(a.video).stem[:40]
    extensao = ".png" if a.previa else ".mp4"
    saida = Path(a.saida) if a.saida else estilo.PASTA / "saida" / f"{nome}-indicacao{extensao}"
    saida.parent.mkdir(parents=True, exist_ok=True)
    total = gerar(a.video, foto, saida, a.credito, a.chamada, a.ate, a.foco, a.colorida,
                  a.musica, a.volume_musica, a.previa)
    print(f"Pronto: {saida}" + (f" ({total:.1f} s)" if total else ""))


if __name__ == "__main__":
    sys.exit(main())
