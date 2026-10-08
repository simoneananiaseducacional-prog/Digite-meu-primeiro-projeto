# Vídeos — @mente.mulher.estoica

Fábrica de vídeos verticais (1080×1920, formato Reels) na identidade da marca:
preto editorial, serifa clara, destaques em itálico dourado, muito respiro.

O ponto de partida é sempre um **roteiro em Markdown** da pasta `../roteiros/`.
Escreveu o roteiro, o vídeo sai dele.

## Os dois formatos

### 1. Reel de frases animadas (`reel_frases.py`)

Cada parágrafo do roteiro vira uma tela. O texto entra subindo devagar e sai em fade.
Trechos em **negrito** viram destaque em itálico dourado. A "Frase final na tela"
fecha o vídeo entre dois filetes dourados.

```bash
# Primeiro, confira as telas como imagens (rápido)
python3 reel_frases.py ../roteiros/video-sonhos-grandes.md --previa

# Vídeo sem áudio (você escolhe a música no próprio Instagram)
python3 reel_frases.py ../roteiros/video-sonhos-grandes.md

# Com música de fundo
python3 reel_frases.py ../roteiros/video-sonhos-grandes.md --musica musica/piano.mp3

# Com narração (sua voz ou voz gerada) e música baixinha por baixo
python3 reel_frases.py ../roteiros/video-sonhos-grandes.md --narracao voz.mp3 --musica musica/piano.mp3
```

Sem narração, cada tela fica o tempo de uma leitura calma, cerca de 2,5 palavras
por segundo. Com narração, as telas se distribuem ao longo da fala, na proporção do
tamanho de cada trecho.

### 2. Legendas em vídeo gravado (`legendar.py`)

Você grava falando, e o script coloca o vídeo no formato vertical, aplica legendas
claras com sombra suave e, quando a fala termina, escurece até o fundo da marca e
mostra a frase final.

```bash
# Você leu o roteiro na gravação: as legendas seguem o texto dele
python3 legendar.py gravacao.mp4 --roteiro ../roteiros/video-sonhos-grandes.md

# Tempos exatos, a partir de um arquivo .srt
python3 legendar.py gravacao.mp4 --srt gravacao.srt --frase-final "Sonhar grande é o começo."

# Com música bem baixa sob a sua voz
python3 legendar.py gravacao.mp4 --roteiro ../roteiros/x.md --musica musica/piano.mp3
```

Com `--roteiro`, o tempo das legendas é **estimado** pelo tamanho de cada trecho. Isso
funciona bem quando você lê em ritmo constante. Se ficar dessincronizado, use um `.srt`.

### 3. Indicação: vídeo em cima, você apontando embaixo (`reagir.py`)

Para indicar um vídeo: ele fica em cima, numa moldura com filete dourado, e a sua
foto fica embaixo, apontando para ele e fundida ao fundo preto por um degradê. Entre
os dois aparecem o crédito do autor e uma chamada opcional.

```bash
# Confira o layout numa imagem antes
python3 reagir.py video.mp4 --foto minha-foto.jpg --credito @autor --previa

# Vídeo final, cortando a vinheta do autor no segundo 10,6
python3 reagir.py video.mp4 --foto minha-foto.jpg --credito @autor --chamada "Presta atenção nisso." --ate 10.6
```

- **A foto:** de preferência vertical, com você do peito para cima e a mão apontando para o alto. Por padrão ela fica em P&B, como a marca; use `--colorida` para manter as cores.
- **Enquadramento:** `--foco` escolhe que parte da foto aparece (0 = topo, 0,5 = meio). Se a cabeça ficar cortada, diminua o valor.
- **Sem foto:** o script usa uma silhueta de teste.

### 4. Abertura: sua foto, o vídeo e um fecho estoico (`abertura.py`)

Começa com a sua foto e uma frase no alto (3 s, zoom lento). Depois entra o vídeo, com
o crédito do autor, e fecha com uma citação estoica na tela da marca, que amarra a cena
ao estoicismo. Nos textos, `|` quebra a linha e `*trecho*` vira destaque dourado.

```bash
python3 abertura.py video.mp4 --foto minha-foto.jpg \
    --texto "O estoicismo|*em uma cena.*" \
    --final "Não é pouco o tempo que temos.|*É muito o que perdemos.*" --autor SÊNECA \
    --credito @autor --ate 12.7
```

## Áudio: as quatro formas

| Forma | Como |
| --- | --- |
| Sem áudio | Gere sem `--musica` e escolha a trilha no Instagram (dá acesso às músicas em alta). |
| Música de fundo | `--musica arquivo.mp3`. Use só músicas livres de direitos (veja `musica/`). |
| Sua voz | Grave a narração no celular e passe com `--narracao`. Ou grave o vídeo e use `legendar.py`. |
| Voz gerada | Peça ao Claude: "gera a narração do roteiro X". Ele usa o ElevenLabs conectado (gasta créditos) e devolve o `.mp3` para usar com `--narracao`. |

O Claude também pode **transcrever** uma gravação sua pelo ElevenLabs e criar o `.srt`
com os tempos exatos para o `legendar.py`.

## Como escrever um roteiro

```markdown
# Roteiro de vídeo — Título

## Texto para narração

Cada parágrafo vira uma tela.

**Negrito vira destaque dourado.**
E a linha logo abaixo aparece junto, na mesma tela.

## Frase final na tela

**Uma frase curta que fecha o vídeo.**
```

- A seção do texto também pode se chamar `## Versão final`, `## Texto` ou `## Cenas`.
- Parágrafos longos (mais de 24 palavras) são divididos em telas automaticamente.
- Seções como "Sugestão de ritmo", "Nota conceitual" e "Legenda" são ignoradas.
- Para ver como o roteiro foi entendido: `python3 roteiro.py ../roteiros/arquivo.md`.

## Arquivos

| Arquivo | O que faz |
| --- | --- |
| `reel_frases.py` | Gera o reel de frases animadas. |
| `legendar.py` | Legenda um vídeo gravado e acrescenta a frase final. |
| `reagir.py` | Formato indicação: vídeo em cima, sua foto apontando embaixo. |
| `abertura.py` | Formato abertura: sua foto com frase, o vídeo e um fecho estoico. |
| `roteiro.py` | Lê os roteiros em Markdown. |
| `estilo.py` | Identidade visual: cores, fontes, área segura do Reels, telas. Mude aqui para alterar a aparência de todos os vídeos. |
| `midia.py` | Integração com o ffmpeg (vídeo e mixagem de áudio). |
| `fontes/` | Cormorant Garamond e Montserrat (licença OFL, uso livre). |
| `musica/` | Onde ficam as trilhas de fundo. |
| `saida/` | Vídeos e prévias gerados (fora do Git, por serem pesados). |

## Requisitos

Python 3 com `Pillow` e `numpy`, e o `ffmpeg` instalado.

```bash
pip install pillow numpy
```

Um reel de cerca de 1 minuto leva por volta de 40 segundos para ser gerado e fica com uns 10 MB.
