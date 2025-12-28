from dataclasses import dataclass
from typing import Dict, List, Optional, Union, cast

import mistune

from madr_parser.madr_labels import (
    CONSIDERED_OPTIONS_LABEL,
    CONTEXT_LABEL,
    DECISION_CONFIRMATION_LABEL,
    DECISION_CONSEQUENCES_LABEL,
    DECISION_DRIVERS_LABEL,
    DECISION_OUTCOME_LABEL,
    MORE_INFO_LABEL,
    PROS_AND_CONS_LABEL,
)

SectionValue = Union[str, List[str]]
SectionsMap = Dict[str, SectionValue]


@dataclass
class MADRParser:
    """
    A parser for Markdown Architectural Decision Records (MADR).
    """

    # Required
    title: str
    context: str
    decision_outcome: str

    # Decision quality (linter)
    decision_drivers: Optional[List[str]] = None
    considered_options: Optional[List[str]] = None
    decision_consequences: Optional[str] = None
    decision_confirmation: Optional[List[str]] = None

    options_pros_and_cons: Optional[Dict[str, List[str]]] = None
    more_info: Optional[str] = None

    # -------------------------
    # Public API
    # -------------------------

    @staticmethod
    def parse(madr_string: str) -> "MADRParser":
        """Parses a MADR from a Markdown string."""
        ast = MADRParser._parse_ast(madr_string)

        title = MADRParser._extract_title(ast)
        sections = MADRParser._extract_sections(ast)

        return MADRParser(
            title=title,
            context=MADRParser._get_str(sections, CONTEXT_LABEL),
            decision_outcome=MADRParser._get_str(sections, DECISION_OUTCOME_LABEL),
            decision_drivers=MADRParser._get_list(sections, DECISION_DRIVERS_LABEL),
            considered_options=MADRParser._get_list(sections, CONSIDERED_OPTIONS_LABEL),
            decision_consequences=MADRParser._get_str(
                sections, DECISION_CONSEQUENCES_LABEL
            ),
            decision_confirmation=MADRParser._get_list(
                sections, DECISION_CONFIRMATION_LABEL
            ),
            options_pros_and_cons=MADRParser._extract_options_pros_and_cons(ast),
            more_info=MADRParser._get_str(sections, MORE_INFO_LABEL),
        )

    # -------------------------
    # Parsing helpers
    # -------------------------

    @staticmethod
    def _parse_ast(markdown: str) -> List[dict]:
        md = mistune.create_markdown(renderer="ast")
        result = md(markdown)
        return cast(List[dict], result)

    @staticmethod
    def _extract_title(ast: List[dict]) -> str:
        for node in ast:
            if node["type"] == "heading" and node["attrs"]["level"] == 1:
                return MADRParser._extract_text(node)
        raise ValueError("MADR title (level-1 heading) not found")

    @staticmethod
    def _extract_sections(ast: List[dict]) -> SectionsMap:
        sections: Dict[str, List[dict]] = {}
        current_section: Optional[str] = None
        buffer: List[dict] = []

        for node in ast:
            if node["type"] == "heading":
                level = node["attrs"]["level"]
                heading_text = MADRParser._extract_text(node)

                if level == 2:
                    if current_section:
                        sections[current_section] = buffer
                    current_section = heading_text
                    buffer = []
                    continue

                # level >= 3 → pertence à seção atual
                if current_section:
                    buffer.append(node)
                continue

            if current_section:
                buffer.append(node)

        if current_section:
            sections[current_section] = buffer

        return MADRParser._normalize_sections(sections)

    # -------------------------
    # Normalization helpers
    # -------------------------

    @staticmethod
    def _normalize_sections(raw_sections: Dict[str, List[dict]]) -> SectionsMap:
        normalized: Dict[str, SectionValue] = {}

        for name, nodes in raw_sections.items():
            lists = MADRParser._extract_list(nodes)
            if lists:
                normalized[name] = lists
            else:
                normalized[name] = MADRParser._extract_nodes_text(nodes)

        return normalized

    @staticmethod
    def _extract_nodes_text(nodes: List[dict]) -> str:
        return "\n".join(
            MADRParser._extract_text(node)
            for node in nodes
            if MADRParser._extract_text(node)
        ).strip()

    @staticmethod
    def _extract_text(node: dict) -> str:
        # Recursively extract textual content from a node and its children.
        children = node.get("children")
        if not children:
            # Leaf text node in Mistune AST uses 'raw'.
            return cast(str, node.get("raw", ""))

        parts: List[str] = []
        for child in children:
            if isinstance(child, dict):
                parts.append(MADRParser._extract_text(child))
        return "".join(parts).strip()

    @staticmethod
    def _extract_list(nodes: List[dict]) -> Optional[List[str]]:
        items: List[str] = []

        for node in nodes:
            if node["type"] == "list":
                for item in node["children"]:
                    items.append(MADRParser._extract_nodes_text(item["children"]))

        return items or None

    @staticmethod
    def _extract_options_pros_and_cons(
        ast: List[dict],
    ) -> Optional[Dict[str, List[str]]]:
        """Extracts a mapping of option name -> list of pros/cons strings.

        Scans the AST for the level-2 section named by PROS_AND_CONS_LABEL.
        Within that section, each level-3 heading is treated as an option name,
        and any bullet list items following it are collected as that option's
        pros/cons.
        """

        in_section = False
        current_option: Optional[str] = None
        result: Dict[str, List[str]] = {}

        for node in ast:
            if node.get("type") == "heading":
                level = node.get("attrs", {}).get("level")
                heading_text = MADRParser._extract_text(node)

                # Enter/leave the Pros & Cons section
                if level == 2:
                    # Leaving the section when encountering the next level-2 heading
                    if in_section and heading_text != PROS_AND_CONS_LABEL:
                        break
                    in_section = heading_text == PROS_AND_CONS_LABEL
                    # Reset current option when (re)entering the section header
                    current_option = None
                    continue

                # Level-3 headings denote option names
                if in_section and level == 3:
                    current_option = heading_text
                    if current_option not in result:
                        result[current_option] = []
                    continue

            # Collect list items as pros/cons under the current option
            if in_section and node.get("type") == "list" and current_option:
                for item in node.get("children", []):
                    text = MADRParser._extract_nodes_text(item.get("children", []))
                    if text:
                        result[current_option].append(text)

        return result or None

    # -------------------------
    # Type-safe getters
    # -------------------------

    @staticmethod
    def _get_str(sections: SectionsMap, key: str, default: str = "") -> str:
        value = sections.get(key, default)
        if isinstance(value, str):
            return value
        return "\n".join(value)

    @staticmethod
    def _get_list(sections: SectionsMap, key: str) -> Optional[List[str]]:
        value = sections.get(key)
        if isinstance(value, list):
            return value
        return None
