"""Conversa com o ffmpeg: duração de arquivos, gravação de quadros e mixagem de áudio."""

import json
import subprocess
from pathlib import Path

from estilo import ALTURA, FPS, LARGURA


def duracao(caminho):
    saida = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(caminho)],
        capture_output=True, text=True, check=True,
    )
    return float(json.loads(saida.stdout)["format"]["duration"])


def tem_audio(caminho):
    saida = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index",
         "-of", "csv=p=0", str(caminho)],
        capture_output=True, text=True, check=True,
    )
    return bool(saida.stdout.strip())


def gravador(caminho, estatico=True):
    """Abre o ffmpeg esperando quadros RGB crus pela entrada padrão.

    `estatico` ajusta o codificador para telas de texto paradas; use False em
    vídeo gravado, com movimento.
    """
    ajuste = ["-tune", "stillimage"] if estatico else []
    return subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{LARGURA}x{ALTURA}", "-r", str(FPS), "-i", "-",
         "-c:v", "libx264", "-preset", "medium", "-crf", "20", *ajuste,
         "-pix_fmt", "yuv420p",
         str(caminho)],
        stdin=subprocess.PIPE,
    )


def leitor(caminho):
    """Abre um vídeo já ajustado para 1080x1920 a 30 fps, entregando quadros RGB crus."""
    filtro = (f"scale={LARGURA}:{ALTURA}:force_original_aspect_ratio=increase,"
              f"crop={LARGURA}:{ALTURA},fps={FPS}")
    return subprocess.Popen(
        ["ffmpeg", "-loglevel", "error", "-i", str(caminho), "-vf", filtro,
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        stdout=subprocess.PIPE,
    )


def juntar_audio(video_mudo, saida, voz=None, musica=None, volume_musica=0.25,
                 atraso_voz=0.0):
    """Coloca no vídeo a voz (narração ou áudio original) e/ou a música de fundo.

    A música é repetida se for curta, cortada no fim do vídeo e some em fade-out.
    """
    total = duracao(video_mudo)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(video_mudo)]
    filtros, rotulos = [], []
    n = 1
    if voz:
        cmd += ["-i", str(voz)]
        atraso = int(atraso_voz * 1000)
        filtros.append(f"[{n}:a]adelay={atraso}|{atraso},apad[voz]")
        rotulos.append("[voz]")
        n += 1
    if musica:
        cmd += ["-stream_loop", "-1", "-i", str(musica)]
        fade = max(total - 2.5, 0)
        filtros.append(
            f"[{n}:a]volume={volume_musica},afade=t=in:d=1.5,afade=t=out:st={fade:.2f}:d=2.5[mus]"
        )
        rotulos.append("[mus]")
    if not rotulos:
        # Faixa de áudio silenciosa: o Instagram lida melhor com vídeos que têm áudio
        cmd += ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo"]
        filtros.append(f"[{n}:a]anull[aud]")
    elif len(rotulos) == 2:
        filtros.append("[voz][mus]amix=inputs=2:duration=longest:normalize=0[aud]")
    else:
        filtros.append(f"{rotulos[0]}anull[aud]")
    cmd += ["-filter_complex", ";".join(filtros), "-map", "0:v", "-map", "[aud]",
            "-t", f"{total:.3f}", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", str(saida)]
    subprocess.run(cmd, check=True)
    Path(video_mudo).unlink()
