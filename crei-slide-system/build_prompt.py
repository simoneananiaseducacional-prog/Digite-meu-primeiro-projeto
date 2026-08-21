#!/usr/bin/env python3
"""Gera um prompt de produção visual a partir de uma especificação JSON de slide.

Uso:
    python build_prompt.py examples/professor-aee.json

Saída:
    Texto pronto para colar em uma IA de criação de slides/imagens.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BASE_STYLE = """
Crie UM slide 16:9 no padrão CREI Slide System.

ESTÉTICA:
- fundo azul-marinho profundo / azul petróleo;
- laranja queimado para conduzir o olhar;
- branco/off-white para texto;
- título editorial serifado elegante;
- corpo sans serif limpo;
- visual cinematográfico/editorial, sofisticado e institucional;
- ilustração com função pedagógica;
- nada infantilizado, burocrático ou corporativo genérico;
- máximo de 3 núcleos visuais;
- bastante espaço visual;
- rodapé discreto com CREI Pouso Alegre e número do slide.

REGRA CENTRAL:
Quanto mais complexo o conceito, mais simples e visual deve ser a tela.
O slide mostra; a formadora explica.
""".strip()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def format_norms(items: list[dict]) -> str:
    if not items:
        return "Sem base normativa específica neste slide."
    lines = []
    for item in items:
        article = f", {item['article']}" if item.get("article") else ""
        lines.append(f"- {item['act']}{article} [{item.get('scope', 'não informado')}]")
    return "\n".join(lines)


def build(data: dict) -> str:
    visible = "\n".join(f"- {block}" for block in data["visibleText"])
    interaction = data.get("interaction") or {}
    interaction_text = interaction.get("question", "Sem pergunta interativa obrigatória.")

    return f"""{BASE_STYLE}

SLIDE {data['number']}

TÍTULO:
{data['title']}

IDEIA CENTRAL:
{data['centralIdea']}

TIPO DE COMPOSIÇÃO:
{data['layoutType']}

TEXTO VISÍVEL:
{visible}

CONCEITO VISUAL:
{data['visualConcept']}

INTERAÇÃO ORAL:
{interaction_text}

BASE NORMATIVA:
{format_norms(data.get('normativeBasis', []))}

REGRAS DE PRODUÇÃO:
1. Não transforme o slide em uma apostila.
2. Não invente novos conceitos ou obrigações legais.
3. Não coloque parágrafos longos.
4. Não coloque texto dentro da ilustração gerada; textos devem ser elementos gráficos do slide.
5. Use a imagem para exteriorizar relações, papéis, fluxo ou barreiras.
6. Preserve a hierarquia: título > imagem/diagrama > 2 ou 3 mensagens > referência.
7. O resultado deve parecer uma formação educacional de alto nível e ser compreensível para um leigo.
""".strip()


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python build_prompt.py <arquivo.json>")
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Arquivo não encontrado: {path}")
        return 2

    try:
        data = load(path)
    except Exception as exc:
        print(f"Erro ao ler JSON: {exc}")
        return 2

    print(build(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
