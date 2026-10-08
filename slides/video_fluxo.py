"""Vídeo-aula em slides animados: o fluxo da adaptação de material e da flexibilização curricular.

Identidade do CREI Slide System (azul-marinho, laranja, off-white, serifa editorial).
Conteúdo do Módulo V (Práticas Pedagógicas Inclusivas), já com as correções da revisão:
EF07MA12 / EF04MA03, Res. SEE/MG 4.256/2020 arts. 8º, 9º VI, 11, 13 e 16,
Documento Orientador do PDI.

    python3 slides/video_fluxo.py            # gera o vídeo
    python3 slides/video_fluxo.py --previa   # só um PNG do fim de cada cena
"""

import argparse
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parent
FONTES = RAIZ.parent / "mente-mulher-estoica" / "videos" / "fontes"
SAIDA = RAIZ / "saida"

L, A, FPS = 1920, 1080, 30
NAVY_950, NAVY_900, NAVY_800 = (3, 26, 55), (6, 34, 71), (12, 49, 93)
LARANJA, OFF, CINZA = (244, 122, 0), (247, 243, 235), (160, 177, 199)
MARGEM = 110
TRANSICAO = 0.6


FIG = ["lnum"]  # algarismos alinhados: a Cormorant usa números antigos por padrão


def fonte(nome, tam, peso=None):
    f = ImageFont.truetype(str(FONTES / nome), tam)
    if peso:
        try:
            f.set_variation_by_axes([peso])
        except OSError:
            pass
    return f


def serifa(t, p=600):
    return fonte("CormorantGaramond.ttf", t, p)


def italica(t, p=600):
    return fonte("CormorantGaramond-Italic.ttf", t, p)


def sans(t, p=500):
    return fonte("Montserrat.ttf", t, p)


def quebrar(texto, f, largura):
    linhas, atual = [], ""
    for p in texto.split(" "):  # espaço comum: o não separável (R$ 12,00) não quebra
        teste = f"{atual} {p}".strip()
        if f.getlength(teste, features=FIG) <= largura or not atual:
            atual = teste
        else:
            linhas.append(atual)
            atual = p
    return linhas + [atual]


class Tela:
    """Uma camada RGBA do tamanho do quadro, com utilitários de desenho."""

    def __init__(self):
        self.img = Image.new("RGBA", (L, A), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img)

    def texto(self, xy, texto, f, cor, largura=None, entre=1.25, ancora="la", alinhar="esq"):
        x, y = xy
        linhas = quebrar(texto, f, largura) if largura else [texto]
        alt = int(f.size * entre)
        for i, linha in enumerate(linhas):
            if alinhar == "centro":
                self.d.text((x, y + i * alt), linha, font=f, fill=cor + (255,), anchor="ma", features=FIG)
            else:
                self.d.text((x, y + i * alt), linha, font=f, fill=cor + (255,), anchor=ancora, features=FIG)
        return y + len(linhas) * alt

    def espacado(self, xy, texto, f, cor, espaco=6, centro=False):
        larg = sum(f.getlength(c) for c in texto) + espaco * (len(texto) - 1)
        x = xy[0] - larg / 2 if centro else xy[0]
        for c in texto:
            self.d.text((x, xy[1]), c, font=f, fill=cor + (255,), features=FIG)
            x += f.getlength(c) + espaco

    def cartao(self, caixa, borda=None, cor=NAVY_800, raio=22):
        self.d.rounded_rectangle(caixa, raio, fill=cor + (235,),
                                 outline=(borda + (255,)) if borda else None, width=3 if borda else 0)

    def seta(self, a, b, cor=LARANJA, larg=5, ponta=18):
        self.d.line([a, b], fill=cor + (255,), width=larg)
        v = np.array(b, float) - np.array(a, float)
        v /= np.linalg.norm(v) + 1e-9
        n = np.array([-v[1], v[0]])
        p = np.array(b, float)
        tri = [tuple(p), tuple(p - v * ponta * 1.6 + n * ponta * 0.8), tuple(p - v * ponta * 1.6 - n * ponta * 0.8)]
        self.d.polygon(tri, fill=cor + (255,))

    def circulo_num(self, centro, n, r=34):
        x, y = centro
        self.d.ellipse((x - r, y - r, x + r, y + r), fill=LARANJA + (255,))
        self.d.text((x, y + 2), str(n), font=sans(34, 700), fill=NAVY_950 + (255,), anchor="mm", features=FIG)


def titulo(t, branco, laranja="", y=120, sub=""):
    """Assinatura do CREI: palavra branca + palavra laranja em itálico."""
    f1, f2 = serifa(76, 700), italica(76, 600)
    w1 = f1.getlength(branco + (" " if laranja else ""), features=FIG)
    t.d.text((MARGEM, y), branco, font=f1, fill=OFF + (255,), features=FIG)
    if laranja:
        t.d.text((MARGEM + w1, y), laranja, font=f2, fill=LARANJA + (255,), features=FIG)
    t.d.line([(MARGEM, y + 108), (MARGEM + 90, y + 108)], fill=LARANJA + (255,), width=4)
    if sub:
        t.texto((MARGEM, y + 132), sub, sans(28, 400), CINZA)


def rodape(t, ref):
    if ref:
        t.texto((L - MARGEM, A - 62), ref, sans(20, 400), CINZA, ancora="ra")


# ---------------------------------------------------------------- cenas
# Cada cena devolve (duração, [(Tela, instante de entrada), ...])

def cena_capa():
    a, b, c = Tela(), Tela(), Tela()
    a.espacado((L / 2, 300), "CREI POUSO ALEGRE  ·  MÓDULO V", sans(26, 600), LARANJA, 8, centro=True)
    a.texto((L / 2, 380), "Flexibilizar", serifa(150, 700), OFF, alinhar="centro")
    b.texto((L / 2, 545), "ou adaptar?", italica(150, 600), LARANJA, alinhar="centro")
    c.d.line([(L / 2 - 60, 760), (L / 2 + 60, 760)], fill=LARANJA + (255,), width=3)
    c.texto((L / 2, 800), "O fluxo, passo a passo, da observação ao registro", sans(36, 400), CINZA,
            alinhar="centro")
    return 6.5, [(a, 0.2), (b, 0.9), (c, 1.8)]


def cena_gps():
    t0, e, d, f = Tela(), Tela(), Tela(), Tela()
    titulo(t0, "Pense num", "GPS", sub="O destino é o objetivo de aprendizagem. O caminho é a forma de chegar até ele.")
    w = (L - 2 * MARGEM - 60) // 2
    for tela, x, rotulo, frase, corpo in (
        (e, MARGEM, "ADAPTAR O MATERIAL", "Muda o caminho.",
         "O destino é o mesmo da turma. Muda a forma de chegar: material concreto, apoio visual, tarefa em etapas."),
        (d, MARGEM + w + 60, "FLEXIBILIZAR O CURRÍCULO", "Ajusta o destino.",
         "A habilidade é reorganizada conforme o estágio do estudante, perto do tema da turma, e registrada no PDI."),
    ):
        tela.cartao((x, 400, x + w, 860))
        tela.espacado((x + 50, 450), rotulo, sans(24, 700), LARANJA, 5)
        tela.texto((x + 50, 505), frase, serifa(72, 700), OFF)
        tela.texto((x + 50, 640), corpo, sans(31, 400), OFF, largura=w - 100, entre=1.45)
    f.texto((L / 2, 920), "Na prática, os dois costumam caminhar juntos.", italica(46, 500), CINZA, alinhar="centro")
    return 14, [(t0, 0.2), (e, 1.4), (d, 4.6), (f, 9.0)]


def cena_como_que():
    t0, e, d = Tela(), Tela(), Tela()
    titulo(t0, "O como e", "o quê")
    w = (L - 2 * MARGEM - 60) // 2
    for tela, x, rot, turma, seta_txt, aluno in (
        (e, MARGEM, "ADAPTAÇÃO  ·  O COMO",
         "Turma: Resolva 6790 − 38",
         "o mesmo cálculo, com outro acesso",
         "Com Material Dourado, em duas etapas: tirar 30, depois tirar 8."),
        (d, MARGEM + w + 60, "FLEXIBILIZAÇÃO  ·  O QUÊ",
         "Turma: EF07MA12, operações com números racionais",
         "outra habilidade, do mesmo tema",
         "Estudante: EF04MA03, adição e subtração com números naturais."),
    ):
        tela.cartao((x, 300, x + w, 900))
        tela.espacado((x + 50, 345), rot, sans(24, 700), LARANJA, 5)
        tela.cartao((x + 40, 410, x + w - 40, 560), cor=NAVY_950, raio=16)
        tela.texto((x + 70, 440), turma, sans(32, 600), OFF, largura=w - 140, entre=1.4)
        tela.seta((x + w / 2, 585), (x + w / 2, 660))
        tela.texto((x + w / 2 + 28, 604), seta_txt, italica(28, 500), CINZA)
        tela.cartao((x + 40, 690, x + w - 40, 860), borda=LARANJA, cor=NAVY_950, raio=16)
        tela.texto((x + 70, 720), aluno, sans(32, 600), OFF, largura=w - 140, entre=1.4)
    rodape(d, "Res. SEE/MG nº 4.256/2020, arts. 8º e 11  ·  BNCC")
    return 15, [(t0, 0.2), (e, 1.2), (d, 6.2)]


PASSOS = [
    ("Conhecer o estudante", "Observação e avaliação diagnóstica: potencialidades e barreiras."),
    ("Partir da aula da turma", "Qual habilidade e qual tema a turma vai trabalhar?"),
    ("Decidir", "Basta mudar a forma de acesso? Ou é preciso reorganizar a habilidade?"),
    ("Registrar no PDI", "A decisão e a justificativa pedagógica, com apoio do AEE."),
    ("Planejar e produzir", "Material adaptado, mesmo tema, participação com os colegas."),
    ("Avaliar e revisar", "Conforme o PDI, registrando quanto suporte foi necessário."),
]


def cena_fluxo():
    t0 = Tela()
    titulo(t0, "O fluxo,", "passo a passo", y=90)
    w, h, gap = 520, 250, 80
    xs = [MARGEM + 20 + i * (w + gap) for i in range(3)]
    ys = [300, 680]
    # Ordem em "S": 1 2 3 na linha de cima, 4 5 6 da direita para a esquerda embaixo
    pos = [(xs[0], ys[0]), (xs[1], ys[0]), (xs[2], ys[0]), (xs[2], ys[1]), (xs[1], ys[1]), (xs[0], ys[1])]
    camadas = [(t0, 0.2)]
    for i, ((x, y), (nome, desc)) in enumerate(zip(pos, PASSOS)):
        t = Tela()
        destaque = i == 2
        t.cartao((x, y, x + w, y + h), borda=LARANJA if destaque else None)
        t.circulo_num((x + 60, y + 62), i + 1)
        t.texto((x + 115, y + 38), nome, serifa(44, 700), LARANJA if destaque else OFF)
        t.texto((x + 40, y + 125), desc, sans(26, 400), OFF, largura=w - 80, entre=1.4)
        if i in (0, 1):
            t.seta((x + w + 8, y + h / 2), (x + w + gap - 10, y + h / 2))
        elif i == 2:
            t.seta((x + w / 2, y + h + 8), (x + w / 2, ys[1] - 10))
        elif i in (3, 4):
            t.seta((x - 8, y + h / 2), (x - gap + 10, y + h / 2))
        camadas.append((t, 1.2 + i * 3.0))
    ciclo = Tela()
    x0 = xs[0] - 45
    ciclo.d.line([(xs[0] + 10, ys[1] + h / 2), (x0, ys[1] + h / 2)], fill=LARANJA + (255,), width=5)
    ciclo.d.line([(x0, ys[1] + h / 2), (x0, ys[0] + h / 2)], fill=LARANJA + (255,), width=5)
    ciclo.seta((x0, ys[0] + h / 2), (xs[0] - 8, ys[0] + h / 2))
    ciclo.texto((L / 2, ys[1] + h + 40), "e o ciclo recomeça a cada novo objetivo", italica(40, 500), CINZA,
                alinhar="centro")
    camadas.append((ciclo, 1.2 + 6 * 3.0))
    return 1.2 + 6 * 3.0 + 4.5, camadas


def cena_decisao():
    t0, q, sim, nao, quem = Tela(), Tela(), Tela(), Tela(), Tela()
    titulo(t0, "O momento da", "decisão")
    q.cartao((L / 2 - 560, 300, L / 2 + 560, 470), borda=LARANJA)
    q.texto((L / 2, 330), "Com outra forma de acesso, o estudante", serifa(50, 700), OFF, alinhar="centro")
    q.texto((L / 2, 395), "alcança o objetivo da turma?", serifa(50, 700), OFF, alinhar="centro")
    w = 640
    for tela, x, rot, frase, corpo in (
        (sim, L / 2 - 60 - w, "SIM", "Adaptar o material.", "Mesmo objetivo da turma, outro caminho."),
        (nao, L / 2 + 60, "NÃO", "Flexibilizar a habilidade.",
         "Escolher uma habilidade perto do tema da turma, e adaptar o material também."),
    ):
        tela.seta((x + w / 2, 480), (x + w / 2, 560))
        tela.cartao((x, 580, x + w, 860))
        tela.espacado((x + 45, 615), rot, sans(26, 700), LARANJA, 6)
        tela.texto((x + 45, 660), frase, serifa(52, 700), OFF)
        tela.texto((x + 45, 740), corpo, sans(28, 400), OFF, largura=w - 90, entre=1.4)
    quem.texto((L / 2, 905), "Quem decide: o regente, com apoio do AEE.   Onde fica: no PDI.",
               sans(32, 600), OFF, alinhar="centro")
    rodape(quem, "Res. SEE/MG nº 4.256/2020, art. 8º  ·  Doc. Orientador do PDI, p. 14 a 16")
    return 17, [(t0, 0.2), (q, 1.0), (sim, 4.5), (nao, 7.5), (quem, 11.5)]


def cena_caso():
    t0, tema, turma, aluno, fim = Tela(), Tela(), Tela(), Tela(), Tela()
    titulo(t0, "Na prática:", "7º ano, base de 4º ano")
    tema.cartao((MARGEM, 290, L - MARGEM, 380), cor=NAVY_950)
    tema.texto((L / 2, 312), "Tema da turma: problemas do cotidiano com compra e venda", sans(34, 600), OFF,
               alinhar="centro")
    w = (L - 2 * MARGEM - 60) // 2
    for tela, x, rot, cod, corpo, borda in (
        (turma, MARGEM, "A TURMA", "EF07MA12", "Resolve problemas com valores como R$ 12,75.", None),
        (aluno, MARGEM + w + 60, "O ESTUDANTE", "EF04MA03",
         "Resolve problemas com R$ 12,00, usando dinheiro de papel e etiquetas de preço.", LARANJA),
    ):
        tela.cartao((x, 420, x + w, 820), borda=borda)
        tela.espacado((x + 50, 465), rot, sans(26, 700), LARANJA, 6)
        tela.texto((x + 50, 515), cod, serifa(80, 700), OFF)
        tela.texto((x + 50, 640), corpo, sans(32, 400), OFF, largura=w - 100, entre=1.45)
    fim.texto((L / 2, 870), "Mesmo tema. Mesma aula. Outro ponto de partida.", italica(54, 600), LARANJA,
              alinhar="centro")
    return 16, [(t0, 0.2), (tema, 1.2), (turma, 3.2), (aluno, 6.2), (fim, 11.0)]


def cena_lista(branco, laranja, itens, ref, sub=""):
    t0 = Tela()
    titulo(t0, branco, laranja, sub=sub)
    camadas = [(t0, 0.2)]
    for i, item in enumerate(itens):
        t = Tela()
        y = 360 + i * 175
        t.cartao((MARGEM, y, L - MARGEM, y + 140))
        t.circulo_num((MARGEM + 80, y + 70), i + 1)
        t.texto((MARGEM + 150, y + 47), item, sans(38, 500), OFF, largura=L - 2 * MARGEM - 200)
        camadas.append((t, 1.4 + i * 3.2))
    if ref:
        r = Tela()
        rodape(r, ref)
        camadas.append((r, 1.4))
    return 1.4 + len(itens) * 3.2 + 4.0, camadas


def cena_legitima():
    return cena_lista("Flexibilizar é legítimo", "quando:", [
        "está registrado no PDI, com justificativa pedagógica;",
        "fica o mais próximo possível do tema da turma;",
        "desenvolve autonomia e participação junto aos colegas, sem infantilizar.",
    ], "Res. SEE/MG nº 4.256/2020, art. 8º  ·  Doc. Orientador do PDI, p. 14 a 16")


def cena_registro():
    return cena_lista("O que precisa ficar", "registrado", [
        "O Plano de Desenvolvimento Individual do estudante (art. 13).",
        "As adaptações e estratégias utilizadas (art. 9º, VI).",
        "A avaliação, feita com base no PDI (art. 16).",
    ], "Res. SEE/MG nº 4.256/2020")


def cena_sintese():
    a, b, c = Tela(), Tela(), Tela()
    a.texto((L / 2, 330), "Adaptar é abrir caminhos.", serifa(104, 700), OFF, alinhar="centro")
    b.texto((L / 2, 480), "Flexibilizar é dar sentido ao percurso.", italica(96, 600), LARANJA, alinhar="centro")
    c.d.line([(L / 2 - 60, 680), (L / 2 + 60, 680)], fill=LARANJA + (255,), width=3)
    c.texto((L / 2, 720), "Os dois começam no estudante e terminam no registro.", sans(38, 400), CINZA,
            alinhar="centro")
    c.espacado((L / 2, 900), "CREI POUSO ALEGRE", sans(24, 600), LARANJA, 8, centro=True)
    return 10, [(a, 0.3), (b, 1.6), (c, 3.6)]


CENAS = [cena_capa, cena_gps, cena_como_que, cena_fluxo, cena_decisao, cena_caso,
         cena_legitima, cena_registro, cena_sintese]


# ---------------------------------------------------------------- render

def fundo():
    y, x = np.mgrid[0:A, 0:L].astype(np.float32)
    luz = np.clip(1 - (((x - L * 0.3) / (L * 0.9)) ** 2 + ((y - A * 0.2) / (A * 1.1)) ** 2), 0, 1) ** 1.5
    base, claro = np.array(NAVY_950, np.float32), np.array(NAVY_900, np.float32) * 1.15
    img = base + (claro - base) * luz[..., None]
    img += np.random.default_rng(2).normal(0, 2.5, (A, L, 1)).astype(np.float32)
    return img


class Camada:
    def __init__(self, tela):
        img = tela.img
        caixa = img.getbbox() or (0, 0, 1, 1)
        self.x0, self.y0 = caixa[:2]
        arr = np.asarray(img.crop(caixa), np.float32) / 255
        self.a = arr[..., 3:4]
        self.c = arr[..., :3] * 255 * self.a

    def compor(self, q, op, dy=0):
        if op <= 0:
            return
        h, w = self.a.shape[:2]
        y0 = min(max(self.y0 + dy, 0), A - h)
        r = q[y0:y0 + h, self.x0:self.x0 + w]
        r *= 1 - self.a * op
        r += self.c * op


def suave(t):
    t = min(max(t, 0.0), 1.0)
    return 1 - (1 - t) ** 3


def barra(q, progresso):
    """Linha fina de progresso no pé da tela."""
    q[A - 6:A, :int(L * progresso)] = np.array(LARANJA, np.float32)


def montar():
    cenas = []
    for fn in CENAS:
        dur, camadas = fn()
        cenas.append((dur, [(Camada(t), ti) for t, ti in camadas]))
    return cenas


def quadro_da_cena(base, camadas, t):
    q = base.copy()
    for cam, ti in camadas:
        p = suave((t - ti) / 0.7) if t > ti else 0.0
        cam.compor(q, p, int(round((1 - p) * 24)))
    return q


def gerar(saida):
    base = fundo()
    cenas = montar()
    total = sum(d for d, _ in cenas)
    ff = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{L}x{A}",
         "-r", str(FPS), "-i", "-", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
         "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-tune", "stillimage", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-shortest", "-movflags", "+faststart", str(saida)],
        stdin=subprocess.PIPE)
    decorrido = 0.0
    for n, (dur, camadas) in enumerate(cenas):
        prox = cenas[n + 1] if n + 1 < len(cenas) else None
        for k in range(int(dur * FPS)):
            t = k / FPS
            q = quadro_da_cena(base, camadas, t)
            restante = dur - t
            if prox and restante < TRANSICAO:
                m = suave(1 - restante / TRANSICAO)
                q = q * (1 - m) + quadro_da_cena(base, prox[1], -1) * m
            barra(q, (decorrido + t) / total)
            ff.stdin.write(np.clip(q, 0, 255).astype(np.uint8).tobytes())
        decorrido += dur
        print(f"  cena {n + 1}/{len(cenas)}", flush=True)
    ff.stdin.close()
    ff.wait()
    return total


def previa(pasta):
    pasta.mkdir(parents=True, exist_ok=True)
    base = fundo()
    for n, (dur, camadas) in enumerate(montar(), 1):
        q = quadro_da_cena(base, camadas, dur)
        Image.fromarray(np.clip(q, 0, 255).astype(np.uint8)).save(pasta / f"cena-{n:02d}.png")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--previa", action="store_true")
    p.add_argument("--saida", default=str(SAIDA / "fluxo-flexibilizacao-adaptacao.mp4"))
    a = p.parse_args()
    SAIDA.mkdir(parents=True, exist_ok=True)
    if a.previa:
        previa(SAIDA / "previa-fluxo")
        print(f"Prévias em {SAIDA / 'previa-fluxo'}")
        return
    total = gerar(Path(a.saida))
    print(f"Pronto: {a.saida} ({total:.0f} s)")


if __name__ == "__main__":
    sys.exit(main())
