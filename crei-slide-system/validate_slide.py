#!/usr/bin/env python3
"""Validador simples do CREI Slide System.

Uso:
    python validate_slide.py examples/professor-aee.json

O script não valida a correção jurídica da norma. Ele verifica regras formais e
sinaliza pontos que precisam de revisão humana/técnica antes da aprovação.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ALLOWED_LAYOUTS = {
    "impact",
    "question",
    "comparison",
    "flow",
    "case",
    "interactive",
    "synthesis",
}

MAX_TITLE_WORDS = 10
PREFERRED_VISIBLE_WORDS = 40
HARD_VISIBLE_WORDS = 70
MAX_VISIBLE_BLOCKS = 3


def count_words(text: str) -> int:
    return len([word for word in text.replace("\n", " ").split(" ") if word.strip()])


def validate(data: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    required = [
        "number",
        "title",
        "centralIdea",
        "layoutType",
        "visibleText",
        "visualConcept",
        "speakerNotes",
        "quality",
    ]

    for key in required:
        if key not in data:
            errors.append(f"Campo obrigatório ausente: {key}")

    if errors:
        return errors, warnings

    title_words = count_words(str(data["title"]))
    if title_words > MAX_TITLE_WORDS:
        warnings.append(
            f"Título com {title_words} palavras; preferir até {MAX_TITLE_WORDS}."
        )

    if data["layoutType"] not in ALLOWED_LAYOUTS:
        errors.append(f"Layout inválido: {data['layoutType']}")

    visible_text = data["visibleText"]
    if not isinstance(visible_text, list):
        errors.append("visibleText deve ser uma lista de blocos de texto.")
    else:
        if len(visible_text) > MAX_VISIBLE_BLOCKS:
            errors.append(
                f"Há {len(visible_text)} blocos; máximo permitido: {MAX_VISIBLE_BLOCKS}."
            )
        visible_words = sum(count_words(str(block)) for block in visible_text)
        if visible_words > HARD_VISIBLE_WORDS:
            errors.append(
                f"Texto visível com {visible_words} palavras; limite máximo: {HARD_VISIBLE_WORDS}."
            )
        elif visible_words > PREFERRED_VISIBLE_WORDS:
            warnings.append(
                f"Texto visível com {visible_words} palavras; preferir até {PREFERRED_VISIBLE_WORDS}."
            )

    visual_concept = str(data.get("visualConcept", "")).strip()
    if len(visual_concept) < 20:
        warnings.append("Conceito visual pouco detalhado; explique como a imagem ensina a ideia.")

    quality = data.get("quality", {})
    quality_fields = [
        "oneIdea",
        "laypersonUnderstands",
        "imageTeaches",
        "textIsShort",
        "normativeAccuracyChecked",
        "creiAesthetic",
    ]
    for field in quality_fields:
        if quality.get(field) is not True:
            errors.append(f"Quality gate não aprovado: {field}")

    normative = data.get("normativeBasis", [])
    if normative:
        for idx, item in enumerate(normative, start=1):
            if not item.get("act"):
                errors.append(f"Base normativa {idx} sem ato identificado.")
            if not item.get("scope"):
                warnings.append(f"Base normativa {idx} sem escopo (federal/estadual/etc.).")

    notes = data.get("speakerNotes", {})
    if not notes.get("opening"):
        errors.append("speakerNotes.opening está vazio.")
    if not notes.get("explanation"):
        errors.append("speakerNotes.explanation está vazio.")
    if not notes.get("transferQuestion"):
        errors.append("speakerNotes.transferQuestion está vazio.")

    return errors, warnings


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python validate_slide.py <arquivo.json>")
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Arquivo não encontrado: {path}")
        return 2

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"JSON inválido: {exc}")
        return 2

    errors, warnings = validate(data)

    print(f"CREI Slide System — validação de {path.name}")
    print("-" * 56)

    if warnings:
        print("AVISOS:")
        for warning in warnings:
            print(f"  - {warning}")

    if errors:
        print("ERROS:")
        for error in errors:
            print(f"  - {error}")
        print("\nRESULTADO: REVISAR")
        return 1

    print("RESULTADO: APROVADO NAS REGRAS FORMAIS")
    print("Observação: conferir conteúdo pedagógico e base normativa antes da versão final.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
