"""Visualizado (Epicteto, Encheirídion 5): tela dividida. Os dois recebem "Visualizado" e nenhuma resposta.
Nele a nuvem cresce com o que ele imagina (coração partido, X); ela guarda o celular e sorri.
Os dois celulares vibram: "Desculpa, estava dirigindo!". A nuvem dele se desfaz. Frase de Epicteto e @ no fim.
Uso: python3 visualizado.py saida.mp4
"""
import sys, math, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from personagens import ela, ele
from PIL import Image, ImageDraw
from pathlib import Path
W, H, FPS = 1080, 1920, 30
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
F = 2.6
saida = Path(sys.argv[1])
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.4): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.4): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
def rgba(c, a): return c + (int(255 * cl(a)),)
def seg(t, t0, t1): return estilo.suavizar(cl((t - t0) / (t1 - t0)))

class Esc:
    def __init__(self, d, f): self.d, self.f = d, f
    def _xy(self, xy):
        if isinstance(xy[0], (tuple, list)): return [(p[0] * self.f, p[1] * self.f) for p in xy]
        return [v * self.f for v in xy]
    def __getattr__(self, nome):
        orig = getattr(self.d, nome)
        def chama(xy, *args, **kw):
            for k in ('width', 'radius'):
                if k in kw: kw[k] = max(1, int(round(kw[k] * self.f)))
            return orig(self._xy(xy), *args, **kw)
        return chama

T = 22.0
X0, CHAO = 540, 1250
HY = CHAO - 6 - 240                      # altura da cabeça em pé
T_TELA1, T_DIV, T_VIBRA, T_DIV2, T_FIM = 0.0, 3.6, 11.0, 13.6, 17.2

def celular_na_mao(d, x, olhando, a):
    if a < 0.02: return
    hx, hy = x + 70, HY + 64 - 30 * olhando
    d.rounded_rectangle((hx - 14, hy - 24, hx + 14, hy + 24), radius=5, fill=(20, 20, 22, int(255 * a)), outline=rgba(B, a), width=3)
    d.rectangle((hx - 9, hy - 18, hx + 9, hy + 14), fill=(70, 90, 120, int(200 * a)))

def nuvem(d, cx, cy, s, a, t):
    if s < 0.03 or a < 0.02: return
    for dx, dy, r in [(-50, 8, 36), (-16, -16, 46), (26, -6, 40), (56, 12, 30), (0, 18, 38)]:
        d.ellipse((cx + (dx - r) * s, cy + (dy - r) * s, cx + (dx + r) * s, cy + (dy + r) * s), fill=(52, 52, 58, int(255 * a)), outline=rgba(C, a), width=3)
    # o que ele imagina: coração partido e um X
    if s > 0.6:
        ia = a * cl((s - 0.6) / 0.3)
        hx, hy, r = cx - 26 * s, cy + 2 * s, 9 * s
        for k, off in ((-1, -2), (1, 2)):
            d.ellipse((hx + k * r - r + off, hy - r, hx + k * r + r + off, hy + r), fill=rgba((200, 80, 80), ia))
        d.polygon([(hx - 2 * r - 2, hy + 3), (hx + 2 * r + 2, hy + 3), (hx, hy + 2.6 * r)], fill=rgba((200, 80, 80), ia))
        d.line([(hx, hy - r), (hx - 4, hy + 4), (hx + 3, hy + 10), (hx, hy + 2.6 * r)], fill=(52, 52, 58, int(255 * ia)), width=3)
        xx, xy, q = cx + 30 * s, cy, 10 * s
        d.line([(xx - q, xy - q), (xx + q, xy + q)], fill=rgba(B, ia), width=4)
        d.line([(xx - q, xy + q), (xx + q, xy - q)], fill=rgba(B, ia), width=4)

def painel(quem, t, a):
    """Desenha um personagem em close e devolve a imagem do painel (1080 x 960)."""
    big = Image.new('RGBA', (int(W * F), int(H * F)), (0, 0, 0, 0)); d = Esc(ImageDraw.Draw(big, 'RGBA'), F)
    if quem == 'ele':
        olhando = 0.5 + 0.5 * math.sin(t * 2.2) if T_DIV < t < T_VIBRA else 0.3
        raiva = seg(t, 5.0, 9.0) * (1 - seg(t, T_DIV2 + 0.6, T_DIV2 + 2.0))
        emo = dict(raiva=raiva, triste=0.5 * seg(t, T_DIV2, T_DIV2 + 0.6) * (1 - seg(t, T_DIV2 + 1.6, T_DIV2 + 2.4)),
                   sorriso=0.7 * seg(t, T_DIV2 + 1.8, T_DIV2 + 2.6))
        ele(d, X0, CHAO - 6, a, braco=0.3, lado=1, cabeca_baixa=0.35 * olhando, t=t, emo=emo)
        celular_na_mao(d, X0, olhando, a)
        nuv = seg(t, 5.0, 10.0) * (1 - seg(t, T_DIV2 + 0.8, T_DIV2 + 2.2))
        nuvem(d, X0, HY - 105, 1.15 * nuv, a, t)
    else:
        guarda = seg(t, 6.0, 7.0) * (1 - seg(t, T_VIBRA - 0.2, T_VIBRA + 0.2))
        emo = dict(sorriso=0.2 + 0.7 * seg(t, 6.4, 7.2))
        ela(d, X0, CHAO - 6, a, braco=0.3 * (1 - guarda), lado=1, cabeca_baixa=0.35 * (1 - guarda) * (t < 7), t=t, emo=emo)
        if guarda < 0.9: celular_na_mao(d, X0, 0.6 * (1 - guarda), a * (1 - guarda))
    K = 2.35; cx, cy = X0, HY + 10
    w, h = W / K * F, 960 / K * F
    crop = big.crop((int(cx * F - w / 2), int(cy * F - h / 2), int(cx * F + w / 2), int(cy * F + h / 2)))
    return crop.resize((W, 960), Image.LANCZOS)

def tela_celular(im, linhas, quem_escreve, a, visto=False):
    """Celular grande no centro com a conversa."""
    if a < 0.02: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay, 'RGBA')
    x0, y0, x1, y1 = 250, 420, 830, 1500
    d.rounded_rectangle((x0, y0, x1, y1), radius=60, fill=(16, 16, 18, 245), outline=(120, 120, 120, 255), width=6)
    d.rounded_rectangle((x0 + 30, y0 + 70, x1 - 30, y1 - 70), radius=24, fill=(28, 28, 32, 255))
    f = estilo.sem_serifa(42, 500)
    y = y0 + 200
    for txt, lado in linhas:
        tw = d.textlength(txt, font=f) + 60
        bx0 = x1 - 60 - tw if lado == 'eu' else x0 + 60
        cor = (40, 110, 220, 255) if lado == 'eu' else (60, 60, 66, 255)
        d.rounded_rectangle((bx0, y, bx0 + tw, y + 80), radius=36, fill=cor)
        d.text((bx0 + tw / 2, y + 40), txt, font=f, fill=(255, 255, 255, 255), anchor='mm')
        y += 110
    if visto:
        d.text((x1 - 70, y - 10), 'Visualizado', font=estilo.sem_serifa(38, 600), fill=(150, 150, 150, 255), anchor='rm')
    lay.putalpha(lay.getchannel('A').point(lambda v: int(v * a)))
    im.alpha_composite(lay)

fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
FT = estilo.sem_serifa(52, 500); TXT = (200, 196, 190)
ff = midia.gravador(saida.with_suffix('.mudo.mp4'), estatico=False)
for k in range(int(T * FPS)):
    t = k / FPS
    im = fundo.copy()
    div_a = jan(t, T_DIV, T_VIBRA) + jan(t, T_DIV2, T_FIM + 0.6)
    if div_a > 0.02:
        im.alpha_composite(painel('ele', t, div_a), (0, 0))
        im.alpha_composite(painel('ela', t, div_a), (0, 960))
        ImageDraw.Draw(im).line([(60, 960), (W - 60, 960)], fill=rgba(C, div_a * 0.6), width=2)
    # celular: a mensagem visualizada, depois a resposta
    tela_celular(im, [('Oi! Tudo bem?', 'eu')], 'eu', jan(t, 0.2, T_DIV, 0.3), visto=t > 1.4)
    vib = jan(t, T_VIBRA, T_DIV2, 0.3)
    if vib > 0.02:
        ox = 6 * math.sin(t * 60) * (t < T_VIBRA + 0.6)
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        tela_celular(lay, [('Oi! Tudo bem?', 'eu'), ('Desculpa, estava', 'ela'), ('dirigindo!', 'ela')], 'eu', vib)
        im.alpha_composite(lay, (int(ox), 0))
    d = ImageDraw.Draw(im, 'RGBA')
    fa = jan(t, T_FIM + 0.4, 20.6)
    if fa > 0.02:
        for i, l in enumerate(['Não são as coisas', 'que nos perturbam,', 'mas o que pensamos delas.']):
            d.text((W/2, 780 + i * 76), l, font=FT, fill=rgba(TXT if i < 2 else G, fa), anchor='mm')
        d.text((W/2, 1050), 'Epicteto, Encheirídion, 5', font=estilo.playfair(32, True), fill=rgba(C, fa), anchor='mm')
    ia = ap(t, 20.6, 0.5)
    if ia > 0.02:
        s = 70; cy = 860
        d.rounded_rectangle((W/2 - s, cy - s, W/2 + s, cy + s), radius=40, outline=rgba(B, ia), width=10)
        d.ellipse((W/2 - 34, cy - 34, W/2 + 34, cy + 34), outline=rgba(B, ia), width=10)
        d.ellipse((W/2 + 36, cy - 50, W/2 + 50, cy - 36), fill=rgba(B, ia))
        d.text((W/2, cy + 140), '@mente_mulher_estoica', font=estilo.sem_serifa(46, 600), fill=rgba(B, ia), anchor='mm')
    ff.stdin.write(estilo.para_bytes(np.asarray(im.convert('RGB'), np.float32) * (1 - ap(t, T - 0.4, 0.4))))
ff.stdin.close(); ff.wait()
midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida)
print('ok', saida)
