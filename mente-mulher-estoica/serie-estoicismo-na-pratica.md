# Série "Estoicismo na prática"

Vídeos curtos (15 s) em desenho, com a própria Simone como personagem
(`personagem/soberana-contemporanea.png`: blusa preta e cardigã vinho). Sem fala.
Destaque no Instagram: **"Da série..."**, com a capa do rosto dela.

## A lógica de cada episódio

1. **Uma situação reconhecível:** preocupações, provocação, comparação, vontade de
   responder no impulso.
2. **Um exagero visual engraçado:** três leões entrando na cozinha, por exemplo.
3. **Uma escolha da personagem:** ela sente, faz aquela cara de "ah, não…" e escolhe
   como agir. Ela não é uma sábia perfeita: pode se irritar, hesitar, fazer cara feia,
   perder a paciência por um segundo,
   respirar e se recompor. A graça está na distância entre o impulso e a atitude escolhida.
4. **Uma frase curta que fecha a piada.** A explicação filosófica fica em uma ou duas
   linhas na legenda.

A pessoa ri, se reconhece e entende uma escolha estoica sem sentir que recebeu uma palestra.

## Cuidados

- **Nada que soe como indireta a colegas de trabalho.** Os temas são da vida pessoal:
  casa, rua, família, preocupações. Nada de "setor", chefe ou reunião.
- **Citação conferida, com referência exata**, só na legenda. Se a cena for inspirada numa
  ideia estoica, e não tradução dela, dizer "inspirado em".
- **O rosto dela:** olhos castanho-escuros quase pretos, maquiagem leve. Gerar de novo se a
  IA clarear os olhos ou trocar o rosto.
- **Ninguém olha para a câmera.**

## Produção

1. Gerar a cena no CapCut a partir do prompt, com a imagem de referência.
2. Montar com `videos/frase_na_cena.py`: tira o som do CapCut, coloca a frase e o fecho
   da série. Opções: `--topo` (frase no alto), `--cobrir y0,y1` (esconde texto que o
   CapCut gravou na imagem), `|` força quebra de linha. Para esta série, o padrão é
   `--estilo tiktok`: legenda de rede social, letra grossa com contorno e emojis. A frase
   não precisa ser refinada; o tom é de bom humor.
3. A música é escolhida no Instagram.
4. Primeira linha da legenda: *Da série: estoicismo na prática.*

## Episódios

| Episódio | Frase | Fundamento (legenda) |
| --- | --- | --- |
| A fila da padaria | "Minha vontade: soltar os leões do Coliseu. / Meu estoicismo: 'O fim da fila é ali, querido.'" | Marco Aurélio, *Meditações*, 8.59 |
| Os três leões | "Matar um leão por dia, tudo bem… / mas os três vão ter que pegar senha 😂☕" | Marco Aurélio, *Meditações*, 8.36 |
