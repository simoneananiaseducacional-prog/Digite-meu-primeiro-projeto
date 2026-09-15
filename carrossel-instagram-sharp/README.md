# Gerador de carrosséis — Mente Mulher Estoica

Projeto em Node.js que usa a biblioteca **Sharp** para montar o layout e exportar **nove cards PNG em 1080 × 1350 px**, prontos para o Instagram.

O motor visual trabalha com SVG: textos, cores, formas, hierarquia e paginação são compostos em código e renderizados pelo Sharp.

## Arquivos principais

- `create_carousel.js`: motor visual e validação dos nove cards.
- `conteudo.json`: textos, paleta, fontes, ordem e nomes dos arquivos.
- `package.json`: dependência do Sharp e comandos do projeto.
- `PROMPT-PARA-CLAUDE.md`: instruções para reutilizar o gerador no Claude Code.
- `saida/`: criada automaticamente; contém os nove PNGs e `preview.png`.

## Requisitos

- Node.js 18 ou superior
- npm

## Como gerar

```bash
npm install
npm run gerar
npm run validar
```

Os cards serão salvos na pasta `saida/`.

## Como criar um novo carrossel

1. Edite primeiro o arquivo `conteudo.json`.
2. Preserve o motor visual quando a mudança for apenas de tema, texto ou cor.
3. Execute `npm run gerar`.
4. Abra `saida/preview.png` e confira cortes, margens, quebras de linha e português.
5. Execute `npm run validar` antes de publicar.

## Regras editoriais

- Um pensamento principal por card.
- Texto curto, tipografia grande e leitura imediata no celular.
- A legenda aprofunda o que não precisa ficar dentro da arte.
- Não transformar reflexão geral em confissão pessoal da autora sem pedido explícito.
- Dados e citações devem ser verificados e atribuídos corretamente.
- Manter a assinatura `MENTE MULHER ESTOICA`.

## Sete conteúdos a partir de uma ideia

Para repetir uma tese sem parecer repetitivo, ela pode ser trabalhada por sete ângulos:

1. Inimigo
2. História
3. Dados
4. Confissão editorial
5. Contraste
6. Passo a passo
7. Demonstração

Cada publicação escolhe um desses ângulos. A ideia central permanece, mas a porta de entrada muda.
