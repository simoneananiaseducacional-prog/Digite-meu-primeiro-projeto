"""Personagens fixos da página (usar em todos os vídeos para criar identidade).

ELA: traço dourado, cabelo preto bem liso e comprido até a cintura (inspirada na Simone).
ELE: traço cinza-claro, cabelo curto.
Ambos em traço simples, olhos de ponto, sobre fundo preto.

Uso: from personagens import ela, ele
     ela(d, x, chao_y, alpha, braco=0..1, lado=1, sentada=0..1, cabeca_baixa=0..1, t=tempo)
"""
import math
DOURADO = (196, 160, 92)
CINZA = (175, 175, 175)
CABELO = (24, 22, 22)
ROSTO = (18, 17, 16)   # preenchimento do rosto (trocar para a cor do papel no design claro)
def _rgba(c, a): return c + (int(255 * max(0, min(1, a))),)

def _corpo(d, x, y, cor, a, sentado, braco, cabeca_baixa, lado, w=5):
    hy = y - 240 + 95 * sentado + 16 * cabeca_baixa
    hx = x + lado * 8 * cabeca_baixa
    ombro = (x, hy + 36); quadril = (x, y - 95 + 72 * sentado)
    d.line([ombro, quadril], fill=_rgba(cor, a), width=w)
    if sentado < 0.5:
        for s in (-1, 1):
            d.line([quadril, (x + s * 30, y)], fill=_rgba(cor, a), width=w)
    else:
        jo = (x + lado * 55, quadril[1] - 30)
        d.line([quadril, jo, (x + lado * 72, y)], fill=_rgba(cor, a), width=w, joint='curve')
        d.line([(x, hy + 58), (x + lado * 58, quadril[1] - 32)], fill=_rgba(cor, a), width=w)
    if sentado < 0.5:
        mao = (x + lado * (40 + 110 * braco), hy + 72 - 22 * braco)
        d.line([(x, hy + 58), mao], fill=_rgba(cor, a), width=w)
        d.line([(x, hy + 58), (x - lado * 38, hy + 140)], fill=_rgba(cor, a), width=w)
    return hx, hy

def _rosto(d, hx, hy, cor, a, cabeca_baixa, r=36, w=5):
    d.ellipse((hx - r, hy - r, hx + r, hy + r), fill=ROSTO + (int(255 * a),), outline=_rgba(cor, a), width=w)
    oy = hy - 2 + 12 * cabeca_baixa
    for s in (-1, 1):
        d.ellipse((hx + s * 12 - 4, oy - 4, hx + s * 12 + 4, oy + 4), fill=_rgba(cor, a))

def _cabelo_liso(d, hx, hy, a, comp, t):
    """Cabelo preto, liso e comprido, caindo dos dois lados do rosto (o corpo fica visível no meio)."""
    bal = 3 * math.sin(t * 1.6)
    topo = [(hx + 41 * math.cos(math.radians(g)), hy - 2 + 43 * math.sin(math.radians(g))) for g in range(0, -181, -10)]
    d.polygon(topo + [(hx - 41, hy + 6), (hx + 41, hy + 6)], fill=CABELO + (int(255 * a),))
    for s_ in (-1, 1):
        mecha = [(hx + s_ * 41, hy - 4), (hx + s_ * 47 + bal, hy + 60), (hx + s_ * 44 + bal, hy + comp),
                 (hx + s_ * 18 + bal, hy + comp + 6), (hx + s_ * 20, hy + 40), (hx + s_ * 30, hy + 10)]
        d.polygon(mecha, fill=CABELO + (int(255 * a),))
        d.line(mecha + [mecha[0]], fill=_rgba(DOURADO, a), width=3, joint='curve')
    d.arc((hx - 41, hy - 45, hx + 41, hy + 41), 180, 360, fill=_rgba(DOURADO, a), width=3)

def ela(d, x, y, a, braco=0.0, lado=1, sentada=0.0, cabeca_baixa=0.0, t=0.0):
    if a <= 0.01: return
    hy0 = y - 240 + 95 * sentada + 16 * cabeca_baixa
    hx0 = x + lado * 8 * cabeca_baixa
    _cabelo_liso(d, hx0, hy0, a, 135 - 40 * sentada, t)          # atrás do corpo
    hx, hy = _corpo(d, x, y, DOURADO, a, sentada, braco, cabeca_baixa, lado)
    _rosto(d, hx, hy, DOURADO, a, cabeca_baixa)
    # franja lisa repartida ao meio cobrindo o alto da testa
    d.chord((hx - 36, hy - 36, hx + 36, hy + 36), 200, 340, fill=CABELO + (int(255 * a),), outline=_rgba(DOURADO, a), width=3)
    d.line([(hx, hy - 36), (hx, hy - 20)], fill=_rgba(DOURADO, a), width=2)

def ele(d, x, y, a, braco=0.0, lado=-1, sentado=0.0, cabeca_baixa=0.0, t=0.0):
    if a <= 0.01: return
    hx, hy = _corpo(d, x, y, CINZA, a, sentado, braco, cabeca_baixa, lado)
    _rosto(d, hx, hy, CINZA, a, cabeca_baixa)
    # cabelo curto: arco grosso no topo
    d.arc((hx - 38, hy - 40, hx + 38, hy + 34), 195, 345, fill=_rgba(CINZA, a), width=9)
