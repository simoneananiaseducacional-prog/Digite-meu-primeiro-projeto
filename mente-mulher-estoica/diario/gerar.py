#!/usr/bin/env python3
"""Gerador do Diario das Mulheres Estoicas · Modulo 1 (30 dias).

Le a lista de reflexoes abaixo e produz duas saidas sempre identicas:
- diario-30-dias.md   (fonte em Markdown)
- diario-30-dias.html (pronto para imprimir ou salvar como PDF, A5)

Regras de voz da marca respeitadas no conteudo: sem exclamacao, sem travessao,
tom introspectivo e firme, fecho em imperativo universal.
"""

import html

TITULO = "Diario Estoico de 30 Dias"
SUBTITULO = "Reflexao guiada para nao se abandonar"
AUTORA = "Simone Ananias · Mente Mulher Estoica"

INTRO = [
    "Este diario nao promete transformar sua vida em trinta dias. Promete algo mais honesto: "
    "trinta encontros com voce mesma, um por dia, para sair do impulso e voltar ao que depende de voce.",
    "O estoicismo ensina a separar o que esta sob nosso controle do que nao esta. A fe ensina a "
    "confiar no que resta. Aqui os dois caminham juntos, com Cristo no centro e a filosofia como "
    "quem antecipa uma verdade antiga.",
    "Nao ha certo nem errado no que voce vai escrever. Ha apenas o gesto de parar, olhar e registrar.",
]

COMO_USAR = [
    "Reserve poucos minutos, sempre no mesmo horario, de preferencia em silencio.",
    "Leia a reflexao do dia devagar. Deixe a pergunta trabalhar antes de responder.",
    "Escreva a mao, se puder. A letra lenta pensa melhor que o teclado.",
    "Faca a pratica sugerida ainda no mesmo dia, por menor que pareca.",
    "No fim de cada semana, releia o que escreveu. O padrao aparece quando ninguem apaga o rastro.",
]

# Cada entrada: (tema, reflexao, pergunta, pratica, biblia_estoicismo, fecho_imperativo)
DIAS = [
    ("A dicotomia do controle",
     "Metade do sofrimento nasce de querer mandar no que nunca foi seu. O clima, a opiniao alheia, "
     "o passado. O que sobra para voce e grande o bastante: sua resposta.",
     "O que hoje voce tentou controlar e nao era seu para controlar?",
     "Escreva duas colunas: o que depende de mim, o que nao depende. Aja so na primeira.",
     "Epicteto separa o que esta em nosso poder do que nao esta. O salmista entrega o resto: aquieta-te "
     "diante do Senhor e espera nele.",
     "Cuide do que e seu, entregue o que nunca foi."),

    ("O impulso e a pausa",
     "Entre o que acontece e o que voce faz existe um espaco. Estreito, mas real. Nesse espaco mora "
     "a liberdade que a pressa rouba.",
     "Onde a pressa falou por voce hoje?",
     "Antes da proxima resposta dificil, conte ate dez respirando. So depois responda.",
     "Seneca dizia que a ira e uma loucura breve. O proverbio confirma: quem tarda em irar-se e melhor "
     "que o forte.",
     "Deixe o espaco existir antes da reacao."),

    ("A culpa que nao constroi",
     "Culpa util aponta um caminho e cala. Culpa inutil repete a acusacao sem ensinar nada. A segunda "
     "nao te melhora, so te consome.",
     "Que culpa voce carrega que ja cumpriu o que tinha para dizer?",
     "Nomeie um erro, escreva a licao dele em uma linha e feche o assunto.",
     "O estoico corrige a acao, nao se afoga nela. O evangelho oferece o mesmo: vai e nao peques mais, "
     "sem condenacao perpetua.",
     "Aprenda com a falta, depois solte a acusacao."),

    ("A comparacao silenciosa",
     "A comparacao mede sua vida inteira pelo recorte que o outro escolheu mostrar. E uma conta armada "
     "para voce perder.",
     "Com quem voce se comparou hoje, e o que isso escondeu de bom no seu proprio dia?",
     "Passe cinco minutos longe da tela onde a comparacao costuma comecar.",
     "Marco Aurelio lembra de cuidar da propria alma, nao das dos outros. Paulo escreve para cada um "
     "provar a sua obra e nao a do vizinho.",
     "Meca o seu caminho pelo seu ontem, nao pelo hoje alheio."),

    ("O valor que nao se pede",
     "Quem precisa provar o proprio valor a cada sala ainda nao acredita nele. O valor firme nao "
     "pede plateia.",
     "Onde voce tentou provar algo que nao precisava provar?",
     "Escolha uma situacao e decida ficar em silencio onde antes se justificaria.",
     "O sabio estoico nao depende do aplauso. A escritura ja diz que voce foi feita de modo assombroso, "
     "antes de qualquer aprovacao.",
     "Saiba do seu valor sem cobrar recibo dos outros."),

    ("O silencio como forca",
     "Nem toda provocacao merece resposta. O silencio escolhido nao e fraqueza, e o dominio de quem "
     "nao entrega as proprias chaves.",
     "A que voce respondeu hoje que teria mais forca em silencio?",
     "Deixe uma mensagem irritante sem resposta por vinte e quatro horas. Observe o que muda em voce.",
     "Zenao dizia que temos dois ouvidos e uma boca para ouvir mais e falar menos. O proverbio: ate o "
     "tolo, calado, passa por sabio.",
     "Guarde o silencio como quem guarda um bem."),

    ("A dor que ensina",
     "A dor evitada volta maior. A dor olhada de frente vira material. Nenhuma mulher se reconstroi "
     "fugindo do que doi.",
     "Que dor voce vem evitando olhar?",
     "Escreva sobre ela por dez minutos, sem corrigir, sem embelezar.",
     "Os estoicos treinavam encarar a adversidade como exercicio. Tiago fala do mesmo: a provacao "
     "produz perseveranca.",
     "Encare a dor como quem le uma carta dificil ate o fim."),

    ("O que se repete vira carater",
     "Voce nao e o que promete uma vez. E o que repete todos os dias. O carater e feito de gestos "
     "pequenos e teimosos.",
     "Que pequeno habito, repetido, esta te formando agora, para o bem ou para o mal?",
     "Escolha um gesto minimo de cuidado e faca hoje. Amanha, de novo.",
     "Aristoteles influenciou os estoicos: somos o que repetimos. A fe pede a mesma constancia: fieis "
     "no pouco.",
     "Repita o bem ate ele virar quem voce e."),

    ("A opiniao dos outros",
     "A opiniao alheia e um vento. Muda de direcao sem aviso e nao paga suas contas. Construir a vida "
     "sobre ela e construir sobre a areia.",
     "Que decisao sua ainda espera a aprovacao de alguem?",
     "Tome uma pequena decisao hoje sem consultar a plateia.",
     "Epicteto: se queres progredir, aceita parecer tola em coisas externas. O evangelho pergunta se "
     "buscamos agradar aos homens ou a Deus.",
     "Escolha pela sua consciencia, nao pela arquibancada."),

    ("O medo do futuro",
     "O medo antecipa mil versoes de amanha, quase todas falsas. Voce sofre por desastres que nunca "
     "chegam e perde o dia que existe.",
     "Que futuro imaginado esta roubando o seu presente?",
     "Escreva o pior cenario, depois escreva o que voce faria se ele viesse. O medo encolhe quando tem nome.",
     "Seneca: sofremos mais na imaginacao que na realidade. Jesus: nao vos preocupeis com o amanha, "
     "basta a cada dia o seu mal.",
     "Viva o dia que esta aqui, nao o que talvez venha."),

    ("A gratidao sobria",
     "Gratidao nao e negar o que falta. E enxergar o que ja existe antes que a falta ocupe toda a vista.",
     "Tres coisas simples de hoje pelas quais voce e grata?",
     "Anote as tres agora, sem procurar grandeza. O pequeno basta.",
     "Marco Aurelio comecava o dia agradecendo. Paulo pede: em tudo dai gracas.",
     "Conte o que tem antes de chorar o que falta."),

    ("O perdao sem ingenuidade",
     "Perdoar nao e dizer que a ferida nao doeu. E parar de beber o veneno esperando que o outro "
     "adoeca. O perdao liberta primeiro quem perdoa.",
     "Que ressentimento voce ainda carrega que so pesa em voce?",
     "Escreva o nome, escreva a magoa, e escreva: escolho nao carregar isso hoje.",
     "O estoico nao entrega sua paz a quem o feriu. Cristo ensina a perdoar setenta vezes sete, para "
     "nossa propria libertacao.",
     "Solte o veneno, mesmo sem receber desculpa."),

    ("A palavra que voce da a si mesma",
     "Voce cumpre com todos e falha so com uma pessoa: voce. A palavra dada a si mesma tambem e um "
     "compromisso de honra.",
     "Que promessa sua a voce mesma vem sendo quebrada?",
     "Escolha uma so, pequena, e cumpra hoje sem negociar.",
     "O estoico vive de acordo com o que afirma. O proverbio elogia quem jura para o proprio dano e "
     "nao muda.",
     "Honre a palavra dada a voce como honraria a de outro."),

    ("O corpo como aliado",
     "O corpo cansado distorce tudo. Antes de acreditar que a vida desabou, pergunte se voce apenas "
     "nao dormiu, nao comeu, nao parou.",
     "O que seu corpo pediu hoje que voce ignorou?",
     "Atenda um pedido simples do corpo: agua, sono, pausa, ar.",
     "Os estoicos cuidavam do corpo como instrumento da alma. A escritura chama o corpo de templo, "
     "digno de cuidado.",
     "Cuide do corpo que carrega a sua missao."),

    ("A raiva examinada",
     "A raiva quase sempre esconde outra coisa: medo, cansaco, uma fronteira invadida. Examinada, ela "
     "informa. Obedecida, ela destroi.",
     "O que sua ultima raiva estava tentando proteger?",
     "Da proxima vez, antes de agir, pergunte: o que aqui e meu para resolver?",
     "Seneca escreveu um tratado inteiro sobre dominar a ira. O proverbio: melhor o paciente que o "
     "valente que domina cidades.",
     "Leia a raiva antes de deixar que ela escreva por voce."),

    ("O desejo e a suficiencia",
     "O desejo sem freio nunca chega. Sempre falta a proxima coisa. A riqueza estoica nao e ter mais, "
     "e precisar de menos.",
     "O que voce acha que precisa e, olhando de perto, so quer?",
     "Adie uma compra por sete dias. Veja se o desejo sobrevive ao tempo.",
     "Epicteto: rico e quem se contenta com o que tem. Paulo aprendeu a viver com pouco e com muito, "
     "em contentamento.",
     "Deseje menos e descubra o quanto ja basta."),

    ("A morte como conselheira",
     "Lembrar que o tempo acaba nao entristece, organiza. Diante do fim, o mesquinho perde importancia "
     "e o essencial aparece.",
     "Se este ano fosse o ultimo, o que voce deixaria de adiar?",
     "Escolha uma coisa importante que voce vem adiando e de o primeiro passo hoje.",
     "Memento mori era pratica estoica diaria. O salmista pede: ensina-nos a contar os nossos dias, "
     "para alcancarmos coracao sabio.",
     "Conte os seus dias para nao desperdicar nenhum."),

    ("A rotina como ancora",
     "Nos dias de tempestade emocional, a rotina segura. Nao porque e brilhante, mas porque e firme. "
     "O habito sustenta quando a vontade falha.",
     "Que pequena rotina te devolve o chao quando tudo balanca?",
     "Defina um gesto fixo para amanha de manha e cumpra, mesmo sem vontade.",
     "Os estoicos tinham disciplina diaria de exercicios da alma. A fe conhece a mesma forca na "
     "oracao constante.",
     "Ancore o dia numa rotina que nao dependa do seu humor."),

    ("A escuta antes da reacao",
     "Muita briga e so falta de escuta. Ouvimos para responder, nao para entender. Quem escuta de "
     "verdade desarma metade dos conflitos.",
     "Quem voce ouviu hoje apenas esperando a sua vez de falar?",
     "Numa conversa, resuma o que o outro disse antes de dar sua opiniao.",
     "Os estoicos valorizavam a razao serena acima da reacao. Tiago: pronto para ouvir, tardio para falar.",
     "Escute ate o fim antes de formar a resposta."),

    ("O limite como cuidado",
     "Dizer nao a um pedido nao e egoismo, e o cuidado que protege o seu sim. Quem nunca recusa acaba "
     "presente em tudo e inteira em nada.",
     "A que voce disse sim hoje querendo dizer nao?",
     "Escolha um pedido e responda com um nao respeitoso e sem desculpas longas.",
     "O estoico guarda seu tempo como bem escasso. Ate Jesus se retirava da multidao para orar a sos.",
     "Proteja o seu sim aprendendo a dizer nao."),

    ("A inveja transformada",
     "A inveja aponta, sem querer, o que voce deseja. Em vez de morder por dentro, deixe que ela "
     "mostre a direcao e depois trabalhe por ela.",
     "O que a ultima ponta de inveja revelou que voce quer?",
     "Transforme isso em uma meta concreta e escreva o primeiro passo.",
     "Os estoicos viam a inveja como juizo equivocado sobre bens externos. O proverbio: a inveja e a "
     "podridao dos ossos.",
     "Deixe a inveja indicar o caminho e depois solte-a."),

    ("A constancia acima da intensidade",
     "Um dia de esforco enorme impressiona e nao muda nada. Trinta dias de esforco pequeno mudam a "
     "pessoa. A intensidade seduz, a constancia constroi.",
     "Onde voce vem esperando um grande gesto em vez de comecar pequeno todo dia?",
     "Reduza uma meta grande a uma versao minima e diaria. Faca a de hoje.",
     "Os estoicos treinavam a virtude como habito diario. A fe fala da corrida que se corre com "
     "perseveranca, nao em um salto.",
     "Prefira o passo diario ao surto de um dia so."),

    ("A fe no que nao se controla",
     "Fazer a sua parte e entregar o resto nao e desistir. E reconhecer os limites da propria mao e "
     "descansar naquilo que a excede.",
     "O que voce ja fez o que podia, e agora precisa soltar?",
     "Escreva o que esta nas suas maos e o que voce entrega. Depois respire e solte.",
     "O estoico age e aceita o destino sem revolta. A fe faz o mesmo com confianca: lanca sobre Ele a "
     "tua ansiedade.",
     "Faca a sua parte e confie o resto ao que te excede."),

    ("A vergonha e a verdade",
     "A vergonha escondida cresce no escuro. Dita em voz baixa para alguem de confianca, ela encolhe. "
     "O segredo e o alimento dela.",
     "Que verdade sobre voce ainda vive no escuro por vergonha?",
     "Escreva-a aqui, so para voce, com todas as letras. Tirar do escuro ja alivia.",
     "Os estoicos buscavam viver sem mascara, coerentes por dentro e por fora. A escritura: a verdade "
     "vos libertara.",
     "Traga a verdade para a luz e veja a vergonha diminuir."),

    ("O descanso nao e fraqueza",
     "A cultura do esgotamento chama pausa de preguica. Mas ninguem constroi nada durando sobre "
     "ruinas. Descansar tambem e trabalho.",
     "Quando foi a ultima vez que voce descansou sem culpa?",
     "Marque um intervalo de verdade hoje, sem tela, sem tarefa, sem justificativa.",
     "Ate os estoicos previam o repouso da alma. O proprio Criador descansou no setimo dia e chamou "
     "o descanso de sagrado.",
     "Descanse antes de o corpo te obrigar a parar."),

    ("A generosidade sem se anular",
     "Dar do que transborda alimenta. Dar do que voce nao tem esvazia e adoece. A generosidade "
     "saudavel comeca com o proprio copo cheio.",
     "Onde voce vem dando do que nao tem para sobrar?",
     "Reveja um compromisso feito por culpa e ajuste para o que cabe de verdade.",
     "O estoico serve a comunidade sem se destruir. Paulo: cada um de com alegria, nao por "
     "constrangimento.",
     "De do que transborda, nao do que te falta."),

    ("O passado que ja cumpriu seu papel",
     "O passado ensinou o que tinha para ensinar. Reviver a cena mil vezes nao muda o final, so "
     "prende voce no que ja passou.",
     "Que cena antiga voce ainda repete na cabeca sem necessidade?",
     "Escreva a licao que ela deixou e agradeca por ela ter passado.",
     "Os estoicos focavam no instante presente como unico campo de acao. Paulo: esquecendo o que fica "
     "para tras, avanco para o que esta adiante.",
     "Guarde a licao do passado e devolva o resto ao tempo."),

    ("A coerencia entre valor e escolha",
     "Voce diz que valoriza a paz e escolhe a briga. Diz que quer descanso e enche a agenda. A "
     "coerencia e quando a escolha confirma o valor.",
     "Onde suas escolhas contradizem o que voce diz valorizar?",
     "Escolha um valor e alinhe uma decisao de hoje a ele.",
     "Viver de acordo com a razao e o coracao do estoicismo. A fe pede o mesmo: nao ouvintes apenas, "
     "mas praticantes da palavra.",
     "Faca a escolha confirmar aquilo que voce diz valer."),

    ("A esperanca disciplinada",
     "Esperanca nao e esperar de bracos cruzados que tudo melhore. E agir hoje confiando que o esforco "
     "e a graca se encontram no caminho.",
     "Em que area voce espera mudanca sem ainda ter mudado a acao?",
     "Una uma oracao ou intencao a um passo concreto, ainda hoje.",
     "O estoico une aceitacao a acao virtuosa. A fe une confianca a obra: a fe sem obras e morta.",
     "Espere trabalhando, confie agindo."),

    ("Quem voce se tornou em trinta dias",
     "Trinta dias atras, outra mulher abriu este diario. Voce nao virou outra pessoa. Voce voltou "
     "para si, um pouco mais firme, um pouco menos no impulso.",
     "Relendo o caminho, o que mudou em como voce responde a vida?",
     "Releia seus primeiros registros e escreva uma carta curta a mulher que comecou.",
     "Os estoicos revisavam a propria alma ao fim de cada ciclo. A fe celebra o crescimento: de fe "
     "em fe, de forca em forca.",
     "Siga cuidando do que e seu, um dia de cada vez."),
]


def build_md():
    L = []
    L.append(f"# {TITULO}")
    L.append("")
    L.append(f"*{SUBTITULO}*")
    L.append("")
    L.append(f"**{AUTORA}**")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Apresentacao")
    L.append("")
    for p in INTRO:
        L.append(p)
        L.append("")
    L.append("## Como usar este diario")
    L.append("")
    for c in COMO_USAR:
        L.append(f"- {c}")
    L.append("")
    L.append("---")
    L.append("")
    for i, (tema, refl, perg, prat, bib, fecho) in enumerate(DIAS, 1):
        L.append(f"## Dia {i} · {tema}")
        L.append("")
        L.append(refl)
        L.append("")
        L.append(f"**Pergunta do dia.** {perg}")
        L.append("")
        L.append(f"**Pratica.** {prat}")
        L.append("")
        L.append(f"**Biblia e Estoicismo.** {bib}")
        L.append("")
        L.append(f"> {fecho}")
        L.append("")
        L.append("_Registro:_")
        L.append("")
        L.append("")
        L.append("---")
        L.append("")
    return "\n".join(L)


def esc(s):
    return html.escape(s)


def build_html():
    dias_html = []
    for i, (tema, refl, perg, prat, bib, fecho) in enumerate(DIAS, 1):
        dias_html.append(f"""
    <article class="dia">
      <div class="dia-num">Dia {i:02d}</div>
      <h2>{esc(tema)}</h2>
      <p class="reflexao">{esc(refl)}</p>
      <p class="campo"><span>Pergunta do dia.</span> {esc(perg)}</p>
      <p class="campo"><span>Pratica.</span> {esc(prat)}</p>
      <p class="campo be"><span>Biblia e Estoicismo.</span> {esc(bib)}</p>
      <p class="fecho">{esc(fecho)}</p>
      <div class="registro">
        <div class="registro-rotulo">Registro</div>
        <div class="linhas"></div>
      </div>
    </article>""")

    intro_html = "".join(f"<p>{esc(p)}</p>" for p in INTRO)
    como_html = "".join(f"<li>{esc(c)}</li>" for c in COMO_USAR)

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{esc(TITULO)}</title>
<style>
  @page {{ size: A5; margin: 16mm 14mm; }}
  :root {{
    --preto: #14110d;
    --branco: #f6f2ea;
    --cinza: #6f6a60;
    --dourado: #b8912f;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    background: var(--branco);
    color: var(--preto);
    font-family: Georgia, "Times New Roman", serif;
    line-height: 1.65;
    font-size: 12pt;
  }}
  .capa {{
    min-height: 92vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    background: var(--preto);
    color: var(--branco);
    padding: 3rem 2rem;
    page-break-after: always;
  }}
  .capa .selo {{
    letter-spacing: 0.5em; font-size: 0.6rem; text-transform: uppercase; color: var(--dourado);
  }}
  .capa h1 {{
    font-size: 2rem; font-weight: normal; margin: 1.2rem 0 0.6rem; letter-spacing: 0.04em;
  }}
  .capa .sub {{ color: var(--dourado); font-style: italic; }}
  .capa .autora {{ margin-top: 2.5rem; font-size: 0.8rem; letter-spacing: 0.2em; text-transform: uppercase; color: var(--cinza); }}

  .bloco {{ padding: 1rem 0.5rem; page-break-after: always; }}
  .bloco h2, .dia h2 {{
    font-size: 1.3rem; font-weight: normal; letter-spacing: 0.03em; margin: 0 0 1rem;
  }}
  .rotulo {{
    font-size: 0.62rem; letter-spacing: 0.4em; text-transform: uppercase; color: var(--dourado); margin-bottom: 0.6rem;
  }}
  .bloco ul {{ padding-left: 1.1rem; }}
  .bloco li {{ margin-bottom: 0.5rem; }}

  .dia {{ padding: 0.6rem 0.4rem 1rem; page-break-after: always; }}
  .dia-num {{
    font-size: 0.62rem; letter-spacing: 0.4em; text-transform: uppercase; color: var(--dourado);
  }}
  .dia .reflexao {{ font-size: 1.02rem; }}
  .campo {{ font-size: 0.95rem; }}
  .campo span {{ color: var(--dourado); font-variant: small-caps; letter-spacing: 0.05em; }}
  .fecho {{
    border-left: 2px solid var(--dourado); padding-left: 0.9rem; font-style: italic; margin: 1.2rem 0;
  }}
  .registro-rotulo {{
    font-size: 0.58rem; letter-spacing: 0.4em; text-transform: uppercase; color: var(--cinza); margin-bottom: 0.4rem;
  }}
  .linhas {{
    background-image: repeating-linear-gradient(
      to bottom, transparent 0, transparent 26px, #d8d0c2 26px, #d8d0c2 27px);
    height: 135px;
  }}
  @media screen {{
    body {{ max-width: 640px; margin: 0 auto; padding: 2rem 1.5rem; }}
    .capa {{ min-height: 60vh; border-radius: 4px; }}
  }}
</style>
</head>
<body>
  <section class="capa">
    <div class="selo">Mente Mulher Estoica</div>
    <h1>{esc(TITULO)}</h1>
    <div class="sub">{esc(SUBTITULO)}</div>
    <div class="autora">{esc(AUTORA)}</div>
  </section>

  <section class="bloco">
    <div class="rotulo">Apresentacao</div>
    {intro_html}
  </section>

  <section class="bloco">
    <div class="rotulo">Como usar este diario</div>
    <ul>{como_html}</ul>
  </section>
{''.join(dias_html)}
</body>
</html>
"""


def main():
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "diario-30-dias.md"), "w", encoding="utf-8") as f:
        f.write(build_md())
    with open(os.path.join(here, "diario-30-dias.html"), "w", encoding="utf-8") as f:
        f.write(build_html())
    print("Gerados: diario-30-dias.md e diario-30-dias.html")


if __name__ == "__main__":
    main()
