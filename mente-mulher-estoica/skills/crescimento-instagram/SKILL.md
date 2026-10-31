---
name: crescimento-instagram
description: Checklist de crescimento para o perfil @mente_mulher_estoica. Use quando o pedido for sobre bio, foto de perfil, destaques, planejar ou revisar um reel antes de postar, o que fazer depois de postar, constância de postagem, banco de ganchos ou "por que esse post não performou". Use também quando a Simone pedir para conferir um vídeo ou carrossel antes de publicar.
---

# Crescimento do perfil @mente_mulher_estoica

Base: checklist de @ojeancarlo.s (Jean Carlos), adaptado às regras da página.
Responda em português simples e CURTO. A Simone não quer textos longos: vá direto ao que fazer.

## Regras da página (valem para tudo abaixo)

- Sem travessão nos textos da Simone.
- Toda citação ou dado tem fonte específica (obra, livro e trecho; ou autor, ano e revista). Nunca "a neurociência comprova" sem estudo nomeado. Tradução livre é identificada como tal.
- Linguagem inclusiva: a página tem identidade feminina, mas fala com todas as pessoas. "Participantes" ou "cursistas" sem marcar gênero quando o grupo é misto.
- Conteúdo de outra pessoa: crédito na legenda e em "Marcar pessoas".
- Fotos pessoais nunca vão para o repositório.

## 1. Perfil

**Bio em três linhas**
1. Quem ela é: estoicismo, inteligência emocional e neurociência do comportamento (pós em Neurociência, Comunicação e Desenvolvimento Humano).
2. O que a pessoa ganha: algo concreto, como "reagir menos no impulso" ou "mais clareza emocional".
3. O que fazer agora: uma ação só (seguir, comentar uma palavra, baixar o material).

**Foto de perfil:** rosto real da Simone, de perto, com fundo limpo.

**Destaque "Comece aqui":** história curta de quem ela é e por que a página existe, mais dois ou três dos posts que melhor representam o perfil.

## 2. Antes de gravar ou gerar o vídeo

- [ ] **Roteiro escrito antes.** Nada de improvisar a estrutura.
- [ ] **Gancho forte no primeiro quadro.** A primeira frase fala do problema de quem assiste ("Se você responde no impulso..."). Proibido começar com apresentação ou "hoje vou falar sobre".
- [ ] **Frase fixa no topo** dizendo do que é o vídeo, visível o tempo todo.
- [ ] **Menos de 30 segundos.** Os melhores resultados da página ficaram abaixo disso.
- [ ] **Um pedido no fim:** salvar, mandar para alguém, comentar ou seguir. Escolha um só. Para esta página, "manda para alguém" e "salva" funcionam melhor que "curte".
- [ ] **Fonte conferida** e escrita no vídeo ou na legenda.

## Formatos que funcionam

- **Diagrama animado** (fundo preto, serifa branca e dourada, caminhos vermelhos que apagam e um dourado que fica). "Para onde vai a sua energia?" passou de 34,5 mil views, 433 envios, 341 salvamentos e 133 seguidores, com média de 9 segundos assistidos, e seguiu crescendo dias depois de postado (aprendizado da própria página, não regra do Instagram). Para saber se o motivo é o formato, testar a mesma estrutura com temas diferentes antes de mudar o diagrama. Scripts: `videos/diagrama_energia.py`, `videos/diagrama_controle.py`, `videos/diagrama_pessoas_dificeis.py`.
- **Card tweet** (fundo preto, foto de perfil, nome com selo, frase grande com o fim em dourado). Inspirado num post de frase com 2,8 mil envios. Script: `posts/card_tweet.py`. Testar a frase no Stories antes de pôr no feed.

Repetir esses formatos com temas novos antes de inventar outro. Frases sem promessa absoluta ("você não vai se decepcionar", "não explode"): o estoicismo diminui o domínio da emoção, não a elimina.

## Comparação a favor

Ideia de @luanaalaminii: "use a comparação a seu favor, faça um pouco melhor que eles". Quando a Simone trouxer um post que performou bem em outro perfil, identificar por que funcionou (formato, gancho, interação) e criar a versão dela um pouco melhor: com fonte, com a identidade da página e com crédito quando usar material de outra pessoa. Nunca copiar o texto.

Exemplos que já deram certo:
- Post de frase da @grancursosonline virou card tweet com foto, selo e fonte (`posts/card_tweet.py`).
- Story de sábado do @paulodygital (foto do dia, frase em caixa branca e figurinha de controle deslizante) virou story com café, Sêneca e a pergunta "Quanto você precisava desse lembrete hoje?".

## Reel de teste

Para vídeo novo, sugerir ativar "Reel de teste" na tela final: vai só para não seguidores e não aparece no perfil. Se performar, publicar no perfil. Na grade ficam só os que deram certo.

## 3. Constância

O post original diz "posta todo santo dia, com ou sem vontade". Para a Simone, que também trabalha no CREI, a regra é: escolher um ritmo que ela consiga manter por meses (por exemplo, três reels e um carrossel por semana) e não quebrar. Constância vale mais que volume.

## 4. Depois de postar

- [ ] Responder os primeiros comentários na primeira hora.
- [ ] Anotar no banco de ganchos todo gancho de outro perfil que prendeu a atenção dela (texto do gancho, perfil, data). Usar como inspiração, nunca copiar.
- [ ] Depois de 48 horas, olhar: alcance de não seguidores, envios, salvamentos e retenção nos 3 primeiros segundos. Comparar com o vídeo da energia.

## Como usar esta skill

Quando a Simone mandar um vídeo, roteiro ou carrossel para revisar, passe pela lista da seção 2 e diga só o que está faltando, em ordem de importância. Quando ela pedir bio, entregue as três linhas prontas para colar.

## Arquivo

Tudo que for criado (script, roteiro, legenda) vai para o repositório GitHub da Simone: scripts em `videos/` ou `posts/`, legendas em `posts/textos/legendas-<mês>-<ano>.md`, e as lições novas entram nesta skill. Fotos pessoais nunca.
