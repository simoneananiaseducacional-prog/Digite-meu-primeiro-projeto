# CREI Slide System

Sistema reutilizável de direção pedagógica, visual e de oratória para apresentações do CREI.

## Objetivo

Transformar conteúdo técnico de Educação Especial Inclusiva em slides didáticos, ilustrativos, elegantes, interativos e fáceis de compreender, preservando rigor normativo sem transformar a apresentação em uma apostila.

## Regra central

> Quanto mais complexo for o conceito, mais simples e visual deve ser a tela.

O slide mostra. A formadora explica.

## Princípios permanentes

1. Uma ideia principal por slide.
2. Títulos preferencialmente em forma de pergunta, tensão ou contraste.
3. Pouco texto visível; legislação detalhada fica no rodapé ou nas notas.
4. Toda imagem deve ensinar algo: representar processo, relação, barreira, recurso, papel profissional ou mudança de olhar.
5. Evitar aparência burocrática, infantilizada ou corporativa genérica.
6. Usar narrativa visual: cenas escolares, caminhos, conexões, lupa, fluxo, antes/depois, comparação, estudante no centro.
7. Sempre distinguir fato, interpretação, barreira, potencialidade, apoio e acompanhamento quando houver Estudo de Caso.
8. Quando houver norma, citar ato e artigo sem poluir a tela.
9. O cursista deve conseguir compreender a ideia central em poucos segundos.
10. O slide só é considerado pronto depois de passar pelo checklist de qualidade.

## Arquivos deste sistema

- `slide-system.yaml`: regras visuais, pedagógicas e de conteúdo.
- `prompt-master.md`: prompt-base para qualquer IA criar novos slides no mesmo padrão.
- `slide.schema.json`: estrutura padronizada para especificar um slide.
- `validate_slide.py`: validador simples para verificar excesso de texto e regras formais.
- `examples/professor-aee.json`: exemplo de especificação no padrão aprovado.

## Identidade visual

- Fundo: azul-marinho profundo / azul petróleo.
- Destaque: laranja queimado/intenso.
- Texto: branco ou off-white.
- Títulos: serifada editorial elegante.
- Corpo: sans serif limpa e contemporânea.
- Formato: 16:9.
- Estética: editorial, cinematográfica, sofisticada, pedagógica e institucional.

## Tipos de composição

Alternar ritmos para evitar fadiga visual:

- impacto: frase curta + cena forte;
- pergunta: pergunta dominante + poucos elementos;
- comparação: 2 ou 3 conceitos;
- fluxo: processo visual com setas e etapas;
- caso: estudante fictício + evidências observáveis;
- interativo: pergunta ao grupo + espaço para resposta;
- síntese: mapa, quadro ou revelação final.

## Fórmula de oratória

1. Provocar — “Olhem para esta situação.”
2. Ouvir — “O que vocês perceberam?”
3. Organizar — separar fatos de interpretações.
4. Ensinar — apresentar conceito, fluxo ou norma.
5. Transferir — “E amanhã, na escola de vocês, onde isso aparece?”

## Regra sobre legislação

A norma sustenta a fala; não domina o slide.

Sempre que a apresentação utilizar uma norma, registrar:

- nome do ato;
- número e ano;
- artigo, quando relevante;
- linguagem simples no corpo do slide;
- referência completa no rodapé ou nas notas.

## Regra para conteúdos técnicos

Quando o conteúdo for muito técnico, aumentar o uso de metáfora visual, cena pedagógica ou diagrama e reduzir o volume de texto.

Exemplo: em vez de listar dez atribuições do professor do AEE, mostrar o professor articulando estudante, família, regente e equipe, com 4–6 verbos-chave ao redor.

## Critério de aprovação

Um slide precisa responder “sim” para estas perguntas:

- Está didático?
- Um leigo entende a ideia central?
- Há imagem ou diagrama que ajuda a explicar?
- O texto está curto?
- A norma está correta e bem posicionada?
- A imagem tem função pedagógica?
- O slide é elegante e coerente com o CREI?
- A fala da formadora complementa, em vez de repetir, o slide?
- A composição é diferente o suficiente dos slides anteriores para manter atenção?

Se qualquer resposta for “não”, revisar antes de aprovar.
