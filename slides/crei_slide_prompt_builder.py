"""CREI Slide System

Gerador simples de especificações para slides didáticos, ilustrativos e interativos.
Não gera a imagem final por conta própria: produz um briefing consistente para IA de imagem,
PowerPoint, Canva, SlidesGPT ou outro gerador visual.

Uso:
    from crei_slide_prompt_builder import SlideSpec, build_slide_brief

    slide = SlideSpec(
        number=15,
        title="Quem participa do Estudo de Caso?",
        slide_type="flow",
        core_message="O professor do AEE conduz o processo, mas não faz sozinho.",
        audience_action="Identificar quem participa e qual é o papel de cada ator.",
        legal_basis=["Decreto nº 12.686/2025, art. 11", "Portaria MEC nº 421/2026"],
    )
    print(build_slide_brief(slide))
"""

from dataclasses import dataclass, field
from typing import List, Optional


NAVY = "#031A37"
NAVY_2 = "#062247"
ORANGE = "#F47A00"
OFF_WHITE = "#F7F3EB"

ALLOWED_TYPES = {
    "impact",
    "question",
    "comparison",
    "flow",
    "case",
    "interactive",
    "decision",
    "synthesis",
    "law_translated_to_practice",
}


@dataclass
class SlideSpec:
    number: int
    title: str
    slide_type: str
    core_message: str
    audience_action: str = ""
    subtitle: str = ""
    visible_points: List[str] = field(default_factory=list)
    visual_metaphor: str = ""
    image_scene: str = ""
    legal_basis: List[str] = field(default_factory=list)
    speaker_notes: str = ""
    expected_response: str = ""
    presenter_intervention: str = ""
    footer: str = "CREI Pouso Alegre"

    def validate(self) -> List[str]:
        problems: List[str] = []

        if self.slide_type not in ALLOWED_TYPES:
            problems.append(f"Tipo de slide inválido: {self.slide_type}")
        if len(self.title.split()) > 10:
            problems.append("Título com mais de 10 palavras; encurtar se possível.")
        if len(self.visible_points) > 3:
            problems.append("Mais de 3 núcleos visíveis; simplificar.")
        if not self.core_message.strip():
            problems.append("Mensagem central ausente.")
        if not self.visual_metaphor.strip() and not self.image_scene.strip():
            problems.append("Falta recurso visual com função pedagógica.")

        return problems


def _format_list(items: List[str]) -> str:
    if not items:
        return "-"
    return "\n".join(f"- {item}" for item in items)


def build_slide_brief(slide: SlideSpec) -> str:
    """Retorna briefing completo para criação visual do slide."""

    problems = slide.validate()
    warning = ""
    if problems:
        warning = "\n\nALERTAS DE QA:\n" + "\n".join(f"- {p}" for p in problems)

    return f"""
CREI SLIDE SYSTEM — BRIEF DE PRODUÇÃO

SLIDE: {slide.number:02d}
TIPO: {slide.slide_type}
TÍTULO: {slide.title}
SUBTÍTULO: {slide.subtitle or '-'}

MENSAGEM CENTRAL
{slide.core_message}

O QUE O CURSISTA DEVE FAZER COGNITIVAMENTE
{slide.audience_action or '-'}

TEXTO VISÍVEL — no máximo 3 núcleos
{_format_list(slide.visible_points)}

METÁFORA / LÓGICA VISUAL
{slide.visual_metaphor or '-'}

CENA / ILUSTRAÇÃO
{slide.image_scene or '-'}

DIREÇÃO DE ARTE
- formato 16:9;
- fundo azul-marinho profundo ({NAVY} / {NAVY_2});
- laranja ({ORANGE}) para dirigir o olhar;
- texto branco/off-white ({OFF_WHITE});
- título serifado editorial elegante;
- corpo limpo e moderno;
- estética editorial, cinematográfica, sofisticada, humana e institucional;
- imagem deve explicar o conceito, nunca ser decorativa;
- preservar 5% de margem segura em todas as bordas;
- evitar parágrafos, tabelas miúdas, clipart, visual infantil e caixas repetitivas;
- não inserir texto dentro da imagem gerada por IA; compor o texto no slide;
- alternar composição em relação ao slide anterior para manter ritmo visual.

REGRA PEDAGÓGICA
O slide mostra; a formadora explica.
Quanto mais técnico o conteúdo, mais simples e visual deve ser a tela.

BASE NORMATIVA / RODAPÉ
{_format_list(slide.legal_basis)}

NOTAS DA FORMADORA
{slide.speaker_notes or '-'}

RESPOSTA / REFLEXÃO ESPERADA
{slide.expected_response or '-'}

INTERVENÇÃO SUGERIDA DA FORMADORA
{slide.presenter_intervention or '-'}

RODAPÉ
{slide.footer} | Slide {slide.number:02d}

QA OBRIGATÓRIO ANTES DE APROVAR
- uma única ideia principal;
- entendimento por leigo em poucos segundos;
- imagem com função pedagógica;
- texto grande e legível em projeção;
- nenhum texto cortado ou fora da caixa;
- nenhuma separação inadequada de sílabas;
- norma conferida e sem artigo inventado;
- aparência adulta, elegante e institucional;
- identidade navy + orange + off-white preservada;
- formadora não precisa ler a tela para explicar.
{warning}
""".strip()


def build_image_prompt(slide: SlideSpec) -> str:
    """Gera prompt curto para ilustração sem texto embutido."""

    scene = slide.image_scene or slide.visual_metaphor
    return (
        "Create a sophisticated editorial cinematic illustration for an inclusive education "
        "professional training presentation. Deep navy environment, warm burnt-orange accents, "
        "off-white highlights, elegant institutional visual language, realistic human proportions, "
        "high-end educational campaign aesthetic. The image must visually explain the pedagogical "
        f"concept. Scene: {scene}. No written text, no logos, no watermarks, no childish clipart, "
        "no generic corporate stock aesthetic, no deformed hands or faces. Leave negative space "
        "for slide title and explanatory text. 16:9 composition."
    )


if __name__ == "__main__":
    example = SlideSpec(
        number=15,
        title="Quem participa do Estudo de Caso?",
        slide_type="flow",
        core_message="O professor do AEE conduz e sistematiza; a construção é colaborativa.",
        audience_action="Diferenciar condução técnica de responsabilidade compartilhada.",
        visible_points=[
            "Professor do AEE: conduz e sistematiza",
            "Regente, família e equipe: fornecem evidências e participam",
            "Estudante participa quando pertinente",
        ],
        visual_metaphor="Estudante no centro e atores conectados ao redor; professor do AEE destacado como condutor.",
        image_scene="Equipe escolar e família analisando evidências em torno do estudante, com conexão visual entre sala comum e AEE.",
        legal_basis=[
            "Decreto nº 12.686/2025, art. 11",
            "Decreto nº 12.773/2025",
            "Portaria MEC nº 421/2026",
        ],
        speaker_notes="Conduzir não significa fazer sozinho. Explicar que o Estudo de Caso é processo pedagógico, não formulário isolado.",
        expected_response="Os cursistas reconhecem o professor do AEE como condutor técnico e a equipe como corresponsável pela produção das informações.",
        presenter_intervention="Perguntar: quem tem evidências da sala comum? Quem conhece o histórico? Quem organiza tudo isso em um raciocínio pedagógico?",
    )

    print(build_slide_brief(example))
