"""Cartão final de série (aprendizado 027): "Parte N", a pergunta que fica aberta e o convite para seguir.
Uso dentro de um vídeo:  from continua import cartao
    cartao(d, t, t0, parte=1, pergunta=['Por que ela não percebia?'], W=1080)
d: ImageDraw em modo RGBA que mistura (não desenhar texto com alfa zero).
"""
import estilo
def _ap(t, t0, d=0.6): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def _rgba(c, a): return c + (int(255 * max(0, min(1, a))),)
def cartao(d, t, t0, parte, pergunta, W=1080, y=1430):
    a1, a2, a3 = _ap(t, t0), _ap(t, t0 + 0.8), _ap(t, t0 + 1.8)
    if a1 > 0.02:
        estilo.texto_espacado(d, (W / 2, y), f'PARTE {parte}', estilo.sem_serifa(30, 600), _rgba(estilo.DOURADO, a1), 8)
    for i, l in enumerate(pergunta):
        if a2 > 0.02:
            d.text((W / 2, y + 80 + i * 66), l, font=estilo.playfair(54, True), fill=_rgba(estilo.BRANCO, a2), anchor='mm')
    if a3 > 0.02:
        yy = y + 100 + len(pergunta) * 66
        d.text((W / 2, yy), 'No próximo capítulo.', font=estilo.sem_serifa(36, 500), fill=_rgba((200, 196, 190), a3), anchor='mm')
        d.text((W / 2, yy + 58), 'Segue para não perder a continuação.', font=estilo.sem_serifa(36, 600), fill=_rgba(estilo.DOURADO, a3), anchor='mm')
