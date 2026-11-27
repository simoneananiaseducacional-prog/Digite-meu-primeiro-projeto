"""Série "Padrões em relacionamentos", Ep. 1: Cuidado ou controle?
Mensagens de celular aparecem uma a uma; virada (controle coercitivo, Evan Stark, 2007); ponte estoica
(Epicteto, Encheirídion, 1); chamada para salvar; aviso de que não é diagnóstico (sem telefone).
Uso: python3 serie_ep1_controle.py saida.mp4
"""
import sys, numpy as np
sys.path.insert(0, '/home/user/Digite-meu-primeiro-projeto/mente-mulher-estoica/videos')
import estilo, midia
from PIL import Image, ImageDraw
from pathlib import Path
W, H, FPS, T = 1080, 1920, 30, 29.0
B, G, C = estilo.BRANCO, estilo.DOURADO, estilo.CINZA
P, S = estilo.playfair, estilo.sem_serifa
def cl(p): return max(0.0, min(1.0, p))
def ap(t, t0, d=0.25): return estilo.suavizar((t - t0) / d) if t > t0 else 0.0
def jan(t, t0, t1, d=0.25): return ap(t, t0, d) * (1 - ap(t, t1 - d, d))
def camada(im, a, desenho):
    if a < 0.02: return im
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); desenho(ImageDraw.Draw(lay))
    lay.putalpha(lay.getchannel('A').point(lambda v: int(v * cl(a))))
    return Image.alpha_composite(im, lay)
def texto(im, xy, s, font, cor, a, anchor='mm'):
    return camada(im, a, lambda d: d.text(xy, s, font=font, fill=cor + (255,), anchor=anchor))

MSG = [(4.3, 'Me avisa quando chegar.'), (6.3, 'Por que você demorou?'), (8.3, 'Com quem você estava?'), (10.3, 'Eu só me preocupo com você.')]
FB = S(42, 500)
def balao(d, y, s, sobe):
    w = FB.getlength(s) + 70; x0 = 110; yy = y + 30 * (1 - sobe)
    d.rounded_rectangle((x0, yy - 50, x0 + w, yy + 50), radius=34, fill=(52, 50, 54, 255))
    d.polygon([(x0 + 8, yy + 30), (x0 - 16, yy + 54), (x0 + 40, yy + 46)], fill=(52, 50, 54, 255))
    d.text((x0 + 35, yy), s, font=FB, fill=(240, 236, 228, 255), anchor='lm')

fundo = Image.fromarray(np.clip(estilo.granulado(estilo.fundo()), 0, 255).astype(np.uint8)).convert('RGBA')
saida = Path(sys.argv[1]); ff = midia.gravador(saida.with_suffix('.mudo.mp4'))
for k in range(int(T * FPS)):
    t = k / FPS
    im = fundo.copy()
    d = ImageDraw.Draw(im, 'RGBA')
    estilo.texto_espacado(d, (W / 2, 230), 'SÉRIE  ·  EP. 1', S(34, 600), G + (235,), 10)
    # gancho: grande no início, depois fica pequeno no topo durante as mensagens
    g = 1 - ap(t, 3.8, 0.3)
    im = texto(im, (W / 2, 840), 'Isso é cuidado', P(92), B, g)
    im = texto(im, (W / 2, 960), 'ou é controle?', P(92, True), G, g)
    topo = jan(t, 4.0, 13.0, 0.3)
    im = texto(im, (W / 2, 330), 'Cuidado ou controle?', P(54, True), B, topo)
    for i, (t0, s) in enumerate(MSG):
        a = ap(t, t0, 0.3) * (1 - ap(t, 12.7, 0.3))
        im = camada(im, a, lambda dd, i=i, s=s, t0=t0: balao(dd, 620 + i * 170, s, ap(t, t0, 0.3)))
    f1 = jan(t, 13.2, 18.2)
    im = texto(im, (W / 2, 800), 'Cuidado amplia a sua vida.', P(70), B, f1)
    im = texto(im, (W / 2, 900), 'Controle encolhe o seu mundo.', P(68, True), G, f1 * ap(t, 13.9, 0.3))
    im = texto(im, (W / 2, 1010), 'Controle coercitivo, Evan Stark, 2007', P(32, True), C, f1 * ap(t, 14.4, 0.3))
    f2 = jan(t, 18.4, 22.8)
    im = texto(im, (W / 2, 780), '“Algumas coisas dependem de nós;', P(58, True), B, f2)
    im = texto(im, (W / 2, 860), 'outras não.”', P(58, True), B, f2)
    im = texto(im, (W / 2, 960), 'As suas escolhas são suas.', P(66, True), G, f2 * ap(t, 19.2, 0.3))
    im = texto(im, (W / 2, 1060), 'Epicteto, Encheirídion, 1', P(32, True), C, f2)
    f3 = ap(t, 23.0, 0.3)
    im = texto(im, (W / 2, 800), 'Salva para reler quando', P(70), B, f3)
    im = texto(im, (W / 2, 895), 'alguém disser que é', P(70), B, f3)
    im = texto(im, (W / 2, 990), 'pelo seu bem.', P(74, True), G, f3)
    av = ap(t, 23.8, 0.4)
    im = texto(im, (W / 2, 1480), 'Isto não é diagnóstico.', S(34, 500), C, av)
    im = texto(im, (W / 2, 1530), 'Se dói, procure apoio profissional.', S(34, 500), C, av)
    d2 = ImageDraw.Draw(im, 'RGBA')
    estilo.texto_espacado(d2, (W / 2, 1720), '@MENTE_MULHER_ESTOICA', S(26, 500), (170, 165, 158, 210), 6)
    ff.stdin.write(estilo.para_bytes(np.asarray(im.convert('RGB'), np.float32) * cl((T - t) / 0.4)))
ff.stdin.close(); ff.wait(); midia.juntar_audio(saida.with_suffix('.mudo.mp4'), saida)
saida.with_suffix('.mudo.mp4').unlink(missing_ok=True); print('ok', saida)
