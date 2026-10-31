"""Leitura dos roteiros em Markdown da pasta roteiros/.

Aceita o formato que os roteiros já usam:

    # Título
    ## Texto para narração      (ou "Versão final", "Texto", "Cenas")
    parágrafos...                -> cada parágrafo vira uma tela
    **trecho em negrito**        -> vira destaque em itálico dourado
    ## Frase final na tela
    **frase**                    -> tela de fechamento

Seções como "Sugestão de ritmo", "Nota conceitual" e "Legenda" são ignoradas.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path

SECOES_DE_TEXTO = ("texto para narração", "versão final", "texto", "narração", "cenas")
SECAO_FINAL = "frase final"
MAX_PALAVRAS_POR_TELA = 24


@dataclass
class Tela:
    linhas: list = field(default_factory=list)  # [(texto, destaque)]

    @property
    def texto(self):
        return " ".join(t for t, _ in self.linhas)

    @property
    def palavras(self):
        return len(self.texto.split())


@dataclass
class Roteiro:
    titulo: str
    telas: list
    frase_final: str = ""

    @property
    def texto_corrido(self):
        partes = [t.texto for t in self.telas]
        if self.frase_final:
            partes.append(self.frase_final)
        return "\n\n".join(partes)


def _limpar(texto):
    return re.sub(r"\s+", " ", texto).strip()


def _linhas_do_paragrafo(paragrafo):
    """Separa as linhas do parágrafo, marcando as que estão em negrito."""
    linhas = []
    for bruta in paragrafo.splitlines():
        bruta = re.sub(r"^([-*>]|\d+\.)\s+", "", bruta.strip())
        if not bruta:
            continue
        destaque = bruta.startswith("**")
        texto = _limpar(bruta.replace("**", ""))
        if texto:
            linhas.append((texto, destaque))
    # Negrito que abre numa linha e fecha na outra: une num só destaque
    unidas = []
    for texto, destaque in linhas:
        if unidas and unidas[-1][1] and destaque and not unidas[-1][0].endswith((".", "!", "?", ":")):
            unidas[-1] = (unidas[-1][0] + " " + texto, True)
        else:
            unidas.append((texto, destaque))
    return unidas


def _dividir_frases(texto):
    return [f for f in re.split(r"(?<=[.!?…])\s+", texto) if f]


def _telas_do_paragrafo(paragrafo):
    linhas = _linhas_do_paragrafo(paragrafo)
    if not linhas:
        return []
    tela = Tela(linhas)
    if tela.palavras <= MAX_PALAVRAS_POR_TELA or len(linhas) > 1:
        return [tela]
    # Parágrafo longo: agrupa frases até o limite de palavras por tela
    texto, destaque = linhas[0]
    telas, atual = [], []
    for frase in _dividir_frases(texto):
        candidato = " ".join(atual + [frase])
        if atual and len(candidato.split()) > MAX_PALAVRAS_POR_TELA:
            telas.append(Tela([(" ".join(atual), destaque)]))
            atual = [frase]
        else:
            atual.append(frase)
    if atual:
        telas.append(Tela([(" ".join(atual), destaque)]))
    return telas


def ler(caminho):
    conteudo = Path(caminho).read_text(encoding="utf-8")
    titulo = Path(caminho).stem.replace("-", " ").capitalize()
    secoes, nome_atual = {}, None
    for linha in conteudo.splitlines():
        if linha.startswith("# "):
            titulo = linha[2:].strip()
            titulo = re.sub(r"^roteiro de vídeo\s*[—-]\s*", "", titulo, flags=re.I)
        elif linha.startswith("## "):
            nome_atual = linha[3:].strip().lower()
            secoes[nome_atual] = []
        elif nome_atual is not None:
            secoes[nome_atual].append(linha)

    corpo = next((secoes[n] for n in secoes if n.startswith(SECOES_DE_TEXTO)), None)
    if corpo is None:
        raise ValueError(
            f"{caminho}: não encontrei a seção do texto. "
            "Use um título '## Texto para narração' (ou '## Versão final')."
        )
    final = next((secoes[n] for n in secoes if n.startswith(SECAO_FINAL)), [])

    paragrafos = re.split(r"\n\s*\n", "\n".join(corpo).strip())
    telas = [t for p in paragrafos for t in _telas_do_paragrafo(p)]
    frase_final = _limpar(" ".join(final).replace("**", ""))
    return Roteiro(titulo=titulo, telas=telas, frase_final=frase_final)


if __name__ == "__main__":
    import sys

    r = ler(sys.argv[1])
    print(f"Título: {r.titulo}")
    for i, t in enumerate(r.telas, 1):
        for texto, destaque in t.linhas:
            print(f"  {i:02d} {'★' if destaque else ' '} {texto}")
    print(f"Final: {r.frase_final or '(sem frase final)'}")
