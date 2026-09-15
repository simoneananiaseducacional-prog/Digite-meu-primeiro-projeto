#!/usr/bin/env python3
"""Gerador do Diario das Mulheres Estoicas · Modulo 1 (30 dias).

Le a lista de reflexoes abaixo e produz duas saidas sempre identicas:
- diario-30-dias.md   (fonte em Markdown)
- diario-30-dias.html (pronto para imprimir ou salvar como PDF, A5)

Regras de voz da marca respeitadas no conteudo: sem exclamacao, sem travessao,
tom introspectivo e firme, fecho em imperativo universal.
"""

import html

TITULO = "Diário Estoico de 30 Dias"
SUBTITULO = "Reflexão guiada para não se abandonar"
AUTORA = "Simone Ananias · Mente Mulher Estoica"

INTRO = [
    "Este diário não promete transformar sua vida em trinta dias. Promete algo mais honesto: "
    "trinta encontros com você mesma, um por dia, para sair do impulso e voltar ao que depende de você.",
    "O estoicismo ensina a separar o que está sob nosso controle do que não está. A fé ensina a "
    "confiar no que resta. Aqui os dois caminham juntos, com Cristo no centro e a filosofia como "
    "quem antecipa uma verdade antiga.",
    "Não há certo nem errado no que você vai escrever. Há apenas o gesto de parar, olhar e registrar.",
]

COMO_USAR = [
    "Reserve poucos minutos, sempre no mesmo horário, de preferência em silêncio.",
    "Leia a reflexão do dia devagar. Deixe a pergunta trabalhar antes de responder.",
    "Escreva à mão, se puder. A letra lenta pensa melhor que o teclado.",
    "Faça a prática sugerida ainda no mesmo dia, por menor que pareça.",
    "No fim de cada semana, releia o que escreveu. O padrão aparece quando ninguém apaga o rastro.",
]

# Cada entrada: (tema, reflexao, pergunta, pratica, biblia_estoicismo, fecho_imperativo)
DIAS = [
    ("A dicotomia do controle",
     "Metade do sofrimento nasce de querer mandar no que nunca foi seu. O clima, a opinião alheia, "
     "o passado. O que sobra para você é grande o bastante: sua resposta.",
     "O que hoje você tentou controlar e não era seu para controlar?",
     "Escreva duas colunas: o que depende de mim, o que não depende. Aja só na primeira.",
     "Epicteto separa o que está em nosso poder do que não está. O salmista entrega o resto: aquieta-te "
     "diante do Senhor e espera nele.",
     "Cuide do que é seu, entregue o que nunca foi."),

    ("O impulso e a pausa",
     "Entre o que acontece e o que você faz existe um espaço. Estreito, mas real. Nesse espaço mora "
     "a liberdade que a pressa rouba.",
     "Onde a pressa falou por você hoje?",
     "Antes da próxima resposta difícil, conte até dez respirando. Só depois responda.",
     "Sêneca dizia que a ira é uma loucura breve. O provérbio confirma: quem tarda em irar-se é melhor "
     "que o forte.",
     "Deixe o espaço existir antes da reação."),

    ("A culpa que não constrói",
     "Culpa útil aponta um caminho e cala. Culpa inútil repete a acusação sem ensinar nada. A segunda "
     "não te melhora, só te consome.",
     "Que culpa você carrega que já cumpriu o que tinha para dizer?",
     "Nomeie um erro, escreva a lição dele em uma linha e feche o assunto.",
     "O estoico corrige a ação, não se afoga nela. O evangelho oferece o mesmo: vai e não peques mais, "
     "sem condenação perpétua.",
     "Aprenda com a falta, depois solte a acusação."),

    ("A comparação silenciosa",
     "A comparação mede sua vida inteira pelo recorte que o outro escolheu mostrar. É uma conta armada "
     "para você perder.",
     "Com quem você se comparou hoje, e o que isso escondeu de bom no seu próprio dia?",
     "Passe cinco minutos longe da tela onde a comparação costuma começar.",
     "Marco Aurélio lembra de cuidar da própria alma, não das dos outros. Paulo escreve para cada um "
     "provar a sua obra e não a do vizinho.",
     "Meça o seu caminho pelo seu ontem, não pelo hoje alheio."),

    ("O valor que não se pede",
     "Quem precisa provar o próprio valor a cada sala ainda não acredita nele. O valor firme não "
     "pede plateia.",
     "Onde você tentou provar algo que não precisava provar?",
     "Escolha uma situação e decida ficar em silêncio onde antes se justificaria.",
     "O sábio estoico não depende do aplauso. A escritura já diz que você foi feita de modo assombroso, "
     "antes de qualquer aprovação.",
     "Saiba do seu valor sem cobrar recibo dos outros."),

    ("O silêncio como força",
     "Nem toda provocação merece resposta. O silêncio escolhido não é fraqueza, é o domínio de quem "
     "não entrega as próprias chaves.",
     "A que você respondeu hoje que teria mais força em silêncio?",
     "Deixe uma mensagem irritante sem resposta por vinte e quatro horas. Observe o que muda em você.",
     "Zenão dizia que temos dois ouvidos e uma boca para ouvir mais e falar menos. O provérbio: até o "
     "tolo, calado, passa por sábio.",
     "Guarde o silêncio como quem guarda um bem."),

    ("A dor que ensina",
     "A dor evitada volta maior. A dor olhada de frente vira material. Nenhuma mulher se reconstrói "
     "fugindo do que dói.",
     "Que dor você vem evitando olhar?",
     "Escreva sobre ela por dez minutos, sem corrigir, sem embelezar.",
     "Os estoicos treinavam encarar a adversidade como exercício. Tiago fala do mesmo: a provação "
     "produz perseverança.",
     "Encare a dor como quem lê uma carta difícil até o fim."),

    ("O que se repete vira caráter",
     "Você não é o que promete uma vez. É o que repete todos os dias. O caráter é feito de gestos "
     "pequenos e teimosos.",
     "Que pequeno hábito, repetido, está te formando agora, para o bem ou para o mal?",
     "Escolha um gesto mínimo de cuidado e faça hoje. Amanhã, de novo.",
     "Aristóteles influenciou os estoicos: somos o que repetimos. A fé pede a mesma constância: fiéis "
     "no pouco.",
     "Repita o bem até ele virar quem você é."),

    ("A opinião dos outros",
     "A opinião alheia é um vento. Muda de direção sem aviso e não paga suas contas. Construir a vida "
     "sobre ela é construir sobre a areia.",
     "Que decisão sua ainda espera a aprovação de alguém?",
     "Tome uma pequena decisão hoje sem consultar a plateia.",
     "Epicteto: se queres progredir, aceita parecer tola em coisas externas. O evangelho pergunta se "
     "buscamos agradar aos homens ou a Deus.",
     "Escolha pela sua consciência, não pela arquibancada."),

    ("O medo do futuro",
     "O medo antecipa mil versões de amanhã, quase todas falsas. Você sofre por desastres que nunca "
     "chegam e perde o dia que existe.",
     "Que futuro imaginado está roubando o seu presente?",
     "Escreva o pior cenário, depois escreva o que você faria se ele viesse. O medo encolhe quando tem nome.",
     "Sêneca: sofremos mais na imaginação que na realidade. Jesus: não vos preocupeis com o amanhã, "
     "basta a cada dia o seu mal.",
     "Viva o dia que está aqui, não o que talvez venha."),

    ("A gratidão sóbria",
     "Gratidão não é negar o que falta. É enxergar o que já existe antes que a falta ocupe toda a vista.",
     "Três coisas simples de hoje pelas quais você é grata?",
     "Anote as três agora, sem procurar grandeza. O pequeno basta.",
     "Marco Aurélio começava o dia agradecendo. Paulo pede: em tudo dai graças.",
     "Conte o que tem antes de chorar o que falta."),

    ("O perdão sem ingenuidade",
     "Perdoar não é dizer que a ferida não doeu. É parar de beber o veneno esperando que o outro "
     "adoeça. O perdão liberta primeiro quem perdoa.",
     "Que ressentimento você ainda carrega que só pesa em você?",
     "Escreva o nome, escreva a mágoa, e escreva: escolho não carregar isso hoje.",
     "O estoico não entrega sua paz a quem o feriu. Cristo ensina a perdoar setenta vezes sete, para "
     "nossa própria libertação.",
     "Solte o veneno, mesmo sem receber desculpa."),

    ("A palavra que você dá a si mesma",
     "Você cumpre com todos e falha só com uma pessoa: você. A palavra dada a si mesma também é um "
     "compromisso de honra.",
     "Que promessa sua a você mesma vem sendo quebrada?",
     "Escolha uma só, pequena, e cumpra hoje sem negociar.",
     "O estoico vive de acordo com o que afirma. O provérbio elogia quem jura para o próprio dano e "
     "não muda.",
     "Honre a palavra dada a você como honraria a de outro."),

    ("O corpo como aliado",
     "O corpo cansado distorce tudo. Antes de acreditar que a vida desabou, pergunte se você apenas "
     "não dormiu, não comeu, não parou.",
     "O que seu corpo pediu hoje que você ignorou?",
     "Atenda um pedido simples do corpo: água, sono, pausa, ar.",
     "Os estoicos cuidavam do corpo como instrumento da alma. A escritura chama o corpo de templo, "
     "digno de cuidado.",
     "Cuide do corpo que carrega a sua missão."),

    ("A raiva examinada",
     "A raiva quase sempre esconde outra coisa: medo, cansaço, uma fronteira invadida. Examinada, ela "
     "informa. Obedecida, ela destrói.",
     "O que sua última raiva estava tentando proteger?",
     "Da próxima vez, antes de agir, pergunte: o que aqui é meu para resolver?",
     "Sêneca escreveu um tratado inteiro sobre dominar a ira. O provérbio: melhor o paciente que o "
     "valente que domina cidades.",
     "Leia a raiva antes de deixar que ela escreva por você."),

    ("O desejo e a suficiência",
     "O desejo sem freio nunca chega. Sempre falta a próxima coisa. A riqueza estoica não é ter mais, "
     "é precisar de menos.",
     "O que você acha que precisa e, olhando de perto, só quer?",
     "Adie uma compra por sete dias. Veja se o desejo sobrevive ao tempo.",
     "Epicteto: rico é quem se contenta com o que tem. Paulo aprendeu a viver com pouco e com muito, "
     "em contentamento.",
     "Deseje menos e descubra o quanto já basta."),

    ("A morte como conselheira",
     "Lembrar que o tempo acaba não entristece, organiza. Diante do fim, o mesquinho perde importância "
     "e o essencial aparece.",
     "Se este ano fosse o último, o que você deixaria de adiar?",
     "Escolha uma coisa importante que você vem adiando e dê o primeiro passo hoje.",
     "Memento mori era prática estoica diária. O salmista pede: ensina-nos a contar os nossos dias, "
     "para alcançarmos coração sábio.",
     "Conte os seus dias para não desperdiçar nenhum."),

    ("A rotina como âncora",
     "Nos dias de tempestade emocional, a rotina segura. Não porque é brilhante, mas porque é firme. "
     "O hábito sustenta quando a vontade falha.",
     "Que pequena rotina te devolve o chão quando tudo balança?",
     "Defina um gesto fixo para amanhã de manhã e cumpra, mesmo sem vontade.",
     "Os estoicos tinham disciplina diária de exercícios da alma. A fé conhece a mesma força na "
     "oração constante.",
     "Ancore o dia numa rotina que não dependa do seu humor."),

    ("A escuta antes da reação",
     "Muita briga é só falta de escuta. Ouvimos para responder, não para entender. Quem escuta de "
     "verdade desarma metade dos conflitos.",
     "Quem você ouviu hoje apenas esperando a sua vez de falar?",
     "Numa conversa, resuma o que o outro disse antes de dar sua opinião.",
     "Os estoicos valorizavam a razão serena acima da reação. Tiago: pronto para ouvir, tardio para falar.",
     "Escute até o fim antes de formar a resposta."),

    ("O limite como cuidado",
     "Dizer não a um pedido não é egoísmo, é o cuidado que protege o seu sim. Quem nunca recusa acaba "
     "presente em tudo e inteira em nada.",
     "A que você disse sim hoje querendo dizer não?",
     "Escolha um pedido e responda com um não respeitoso e sem desculpas longas.",
     "O estoico guarda seu tempo como bem escasso. Até Jesus se retirava da multidão para orar a sós.",
     "Proteja o seu sim aprendendo a dizer não."),

    ("A inveja transformada",
     "A inveja aponta, sem querer, o que você deseja. Em vez de morder por dentro, deixe que ela "
     "mostre a direção e depois trabalhe por ela.",
     "O que a última ponta de inveja revelou que você quer?",
     "Transforme isso em uma meta concreta e escreva o primeiro passo.",
     "Os estoicos viam a inveja como juízo equivocado sobre bens externos. O provérbio: a inveja é a "
     "podridão dos ossos.",
     "Deixe a inveja indicar o caminho e depois solte-a."),

    ("A constância acima da intensidade",
     "Um dia de esforço enorme impressiona e não muda nada. Trinta dias de esforço pequeno mudam a "
     "pessoa. A intensidade seduz, a constância constrói.",
     "Onde você vem esperando um grande gesto em vez de começar pequeno todo dia?",
     "Reduza uma meta grande a uma versão mínima e diária. Faça a de hoje.",
     "Os estoicos treinavam a virtude como hábito diário. A fé fala da corrida que se corre com "
     "perseverança, não em um salto.",
     "Prefira o passo diário ao surto de um dia só."),

    ("A fé no que não se controla",
     "Fazer a sua parte e entregar o resto não é desistir. É reconhecer os limites da própria mão e "
     "descansar naquilo que a excede.",
     "O que você já fez o que podia, e agora precisa soltar?",
     "Escreva o que está nas suas mãos e o que você entrega. Depois respire e solte.",
     "O estoico age e aceita o destino sem revolta. A fé faz o mesmo com confiança: lança sobre Ele a "
     "tua ansiedade.",
     "Faça a sua parte e confie o resto ao que te excede."),

    ("A vergonha e a verdade",
     "A vergonha escondida cresce no escuro. Dita em voz baixa para alguém de confiança, ela encolhe. "
     "O segredo é o alimento dela.",
     "Que verdade sobre você ainda vive no escuro por vergonha?",
     "Escreva-a aqui, só para você, com todas as letras. Tirar do escuro já alivia.",
     "Os estoicos buscavam viver sem máscara, coerentes por dentro e por fora. A escritura: a verdade "
     "vos libertará.",
     "Traga a verdade para a luz e veja a vergonha diminuir."),

    ("O descanso não é fraqueza",
     "A cultura do esgotamento chama pausa de preguiça. Mas ninguém constrói nada durando sobre "
     "ruínas. Descansar também é trabalho.",
     "Quando foi a última vez que você descansou sem culpa?",
     "Marque um intervalo de verdade hoje, sem tela, sem tarefa, sem justificativa.",
     "Até os estoicos previam o repouso da alma. O próprio Criador descansou no sétimo dia e chamou "
     "o descanso de sagrado.",
     "Descanse antes de o corpo te obrigar a parar."),

    ("A generosidade sem se anular",
     "Dar do que transborda alimenta. Dar do que você não tem esvazia e adoece. A generosidade "
     "saudável começa com o próprio copo cheio.",
     "Onde você vem dando do que não tem para sobrar?",
     "Reveja um compromisso feito por culpa e ajuste para o que cabe de verdade.",
     "O estoico serve a comunidade sem se destruir. Paulo: cada um dê com alegria, não por "
     "constrangimento.",
     "Dê do que transborda, não do que te falta."),

    ("O passado que já cumpriu seu papel",
     "O passado ensinou o que tinha para ensinar. Reviver a cena mil vezes não muda o final, só "
     "prende você no que já passou.",
     "Que cena antiga você ainda repete na cabeça sem necessidade?",
     "Escreva a lição que ela deixou e agradeça por ela ter passado.",
     "Os estoicos focavam no instante presente como único campo de ação. Paulo: esquecendo o que fica "
     "para trás, avanço para o que está adiante.",
     "Guarde a lição do passado e devolva o resto ao tempo."),

    ("A coerência entre valor e escolha",
     "Você diz que valoriza a paz e escolhe a briga. Diz que quer descanso e enche a agenda. A "
     "coerência é quando a escolha confirma o valor.",
     "Onde suas escolhas contradizem o que você diz valorizar?",
     "Escolha um valor e alinhe uma decisão de hoje a ele.",
     "Viver de acordo com a razão é o coração do estoicismo. A fé pede o mesmo: não ouvintes apenas, "
     "mas praticantes da palavra.",
     "Faça a escolha confirmar aquilo que você diz valer."),

    ("A esperança disciplinada",
     "Esperança não é esperar de braços cruzados que tudo melhore. É agir hoje confiando que o esforço "
     "e a graça se encontram no caminho.",
     "Em que área você espera mudança sem ainda ter mudado a ação?",
     "Una uma oração ou intenção a um passo concreto, ainda hoje.",
     "O estoico une aceitação a ação virtuosa. A fé une confiança a obra: a fé sem obras é morta.",
     "Espere trabalhando, confie agindo."),

    ("Quem você se tornou em trinta dias",
     "Trinta dias atrás, outra mulher abriu este diário. Você não virou outra pessoa. Você voltou "
     "para si, um pouco mais firme, um pouco menos no impulso.",
     "Relendo o caminho, o que mudou em como você responde à vida?",
     "Releia seus primeiros registros e escreva uma carta curta à mulher que começou.",
     "Os estoicos revisavam a própria alma ao fim de cada ciclo. A fé celebra o crescimento: de fé "
     "em fé, de força em força.",
     "Siga cuidando do que é seu, um dia de cada vez."),
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
    L.append("## Apresentação")
    L.append("")
    for p in INTRO:
        L.append(p)
        L.append("")
    L.append("## Como usar este diário")
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
        L.append(f"**Prática.** {prat}")
        L.append("")
        L.append(f"**Bíblia e Estoicismo.** {bib}")
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
      <p class="campo"><span>Prática.</span> {esc(prat)}</p>
      <p class="campo be"><span>Bíblia e Estoicismo.</span> {esc(bib)}</p>
      <p class="fecho">{esc(fecho)}</p>
      <div class="registro">
        <div class="registro-rotulo">Registro</div>
        <div class="linhas"></div>
      </div>
    </article>""")

    intro_html = "".join(f"<p>{esc(p)}</p>" for p in INTRO)
    como_html = "".join(f"<li>{esc(c)}</li>" for c in COMO_USAR)

    emblema = (
        '<svg width="66" height="66" viewBox="0 0 66 66" fill="none" '
        'xmlns="http://www.w3.org/2000/svg">'
        '<circle cx="33" cy="33" r="29" stroke="#b8912f" stroke-width="1"/>'
        '<circle cx="33" cy="33" r="22.5" stroke="#b8912f" stroke-width="0.5"/>'
        '<path d="M33 17 V49" stroke="#d8b558" stroke-width="1"/>'
        '<path d="M17 33 H49" stroke="#d8b558" stroke-width="0.5"/>'
        '<circle cx="33" cy="33" r="2.6" fill="#d8b558"/>'
        "</svg>"
    )

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{esc(TITULO)}</title>
<style>
  @page {{ size: A5; margin: 0; }}
  :root {{
    --preto: #14110d;
    --branco: #f6f2ea;
    --cinza: #6f6a60;
    --dourado: #b8912f;
    --dourado-claro: #d8b558;
  }}
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; padding: 0; }}
  body {{
    background: var(--branco);
    color: var(--preto);
    font-family: Georgia, "Times New Roman", serif;
    line-height: 1.65;
    font-size: 12pt;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}

  /* Capa */
  .capa {{
    height: 100vh; width: 100%;
    display: flex; flex-direction: column;
    justify-content: center; align-items: center; text-align: center;
    background: radial-gradient(circle at 50% 30%, #241f17 0%, var(--preto) 72%);
    color: var(--branco);
    padding: 3rem 2rem;
    page-break-after: always;
    position: relative;
  }}
  .capa::before, .capa::after {{
    content: ""; position: absolute; left: 12mm; right: 12mm; height: 1px;
    background: linear-gradient(to right, transparent, var(--dourado), transparent);
  }}
  .capa::before {{ top: 14mm; }}
  .capa::after {{ bottom: 14mm; }}
  .capa .selo {{ letter-spacing: 0.55em; font-size: 0.62rem; text-transform: uppercase; color: var(--dourado-claro); }}
  .emblema {{ margin: 1.6rem 0 1.3rem; line-height: 0; }}
  .capa h1 {{ font-size: 2.15rem; font-weight: normal; margin: 0.3rem 0.5rem 0.7rem; letter-spacing: 0.03em; line-height: 1.2; }}
  .capa .sub {{ color: var(--dourado-claro); font-style: italic; font-size: 1.02rem; }}
  .capa .autora {{ margin-top: 2.6rem; font-size: 0.72rem; letter-spacing: 0.28em; text-transform: uppercase; color: #b7b0a2; }}

  /* Abertura e encerramento */
  .epigrafe, .encerra {{
    height: 100vh; display: flex; flex-direction: column;
    justify-content: center; align-items: center; text-align: center;
    padding: 3rem 2.6rem; page-break-after: always;
  }}
  .epigrafe p {{ font-size: 1.25rem; font-style: italic; max-width: 24em; line-height: 1.6; }}
  .epigrafe .fonte, .encerra .fonte {{ margin-top: 1.4rem; font-size: 0.64rem; letter-spacing: 0.32em; text-transform: uppercase; color: var(--dourado); }}
  .encerra h2 {{ font-size: 1.5rem; font-weight: normal; color: var(--dourado); margin: 0 0 1rem; }}
  .encerra p {{ max-width: 24em; }}
  .encerra .imperativo {{ font-style: italic; font-size: 1.12rem; margin-top: 1.4rem; }}

  /* Blocos e dias */
  .bloco {{ padding: 18mm 15mm; page-break-after: always; }}
  .bloco h2, .dia h2 {{ font-size: 1.3rem; font-weight: normal; letter-spacing: 0.02em; margin: 0.2rem 0 1rem; }}
  .rotulo {{ font-size: 0.62rem; letter-spacing: 0.4em; text-transform: uppercase; color: var(--dourado); margin-bottom: 0.7rem; }}
  .bloco ul {{ padding-left: 1.1rem; }}
  .bloco li {{ margin-bottom: 0.55rem; }}

  .dia {{ padding: 16mm 15mm; page-break-after: always; }}
  .dia-num {{ font-size: 0.62rem; letter-spacing: 0.4em; text-transform: uppercase; color: var(--dourado); }}
  .dia h2 {{ border-bottom: 1px solid #e2dccc; padding-bottom: 0.5rem; }}
  .dia .reflexao {{ font-size: 1.04rem; }}
  .campo {{ font-size: 0.95rem; }}
  .campo span {{ color: var(--dourado); font-variant: small-caps; letter-spacing: 0.05em; }}
  .fecho {{ border-left: 2px solid var(--dourado); padding-left: 0.9rem; font-style: italic; margin: 1.2rem 0; }}
  .registro-rotulo {{ font-size: 0.58rem; letter-spacing: 0.4em; text-transform: uppercase; color: var(--cinza); margin: 0.4rem 0; }}
  .linhas {{
    background-image: repeating-linear-gradient(
      to bottom, transparent 0, transparent 26px, #d8d0c2 26px, #d8d0c2 27px);
    height: 130px;
  }}
  @media screen {{
    body {{ background: #565048; padding: 14px 0; }}
    .capa, .epigrafe, .encerra, .bloco, .dia {{
      max-width: 560px; margin: 14px auto; background-color: var(--branco);
      box-shadow: 0 3px 18px rgba(0,0,0,0.3);
    }}
    .capa {{ background: radial-gradient(circle at 50% 30%, #241f17 0%, var(--preto) 72%); }}
  }}
</style>
</head>
<body>
  <section class="capa">
    <div class="selo">Mente Mulher Estoica</div>
    <div class="emblema">{emblema}</div>
    <h1>{esc(TITULO)}</h1>
    <div class="sub">{esc(SUBTITULO)}</div>
    <div class="autora">{esc(AUTORA)}</div>
  </section>

  <section class="epigrafe">
    <p>Não é o que acontece com você, é o que você faz com o que acontece. Este diário existe para devolver essa escolha às suas mãos, um dia de cada vez.</p>
    <div class="fonte">Abertura</div>
  </section>

  <section class="bloco">
    <div class="rotulo">Apresentação</div>
    {intro_html}
  </section>

  <section class="bloco">
    <div class="rotulo">Como usar este diário</div>
    <ul>{como_html}</ul>
  </section>
{''.join(dias_html)}
  <section class="encerra">
    <h2>Palavra final</h2>
    <p>Trinta dias não terminam nada. Começam um jeito diferente de responder à vida: com mais pausa, menos impulso e um cuidado firme por si mesma.</p>
    <p>Volte a estas páginas sempre que precisar lembrar do que é seu.</p>
    <p class="imperativo">Siga cuidando do que é seu, um dia de cada vez.</p>
    <div class="fonte">Mente Mulher Estoica · Simone Ananias</div>
  </section>
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
