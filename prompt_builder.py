import re
from pathlib import Path

BASE_DIR = Path(__file__).parent

PROMPTS_DIR = BASE_DIR / "prompts"
SCENARIOS_DIR = BASE_DIR / "scenarios"

def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()

def extract_section(markdown: str, heading: str) -> str:
    pattern = rf"## {re.escape(heading)}\s*\n(.*?)(?=\n## |\Z)"

    match = re.search(
        pattern,
        markdown,
        re.DOTALL
    )

    if not match:
        raise ValueError(
            f"Seção não encontrada: {heading}"
        )

    return match.group(1).strip()

def build_user_prompt(
    template: str,
    scenario: str,
) -> str:
    values = {
        "context": extract_section(
            scenario,
            "Contexto",
        ),
        "functionality": extract_section(
            scenario,
            "Funcionalidade",
        ),
        "data_involved": extract_section(
            scenario,
            "Dados envolvidos",
        ),
        "behavior_rule": extract_section(
            scenario,
            "Comportamento/regra",
        ),
        "user_information": extract_section(
            scenario,
            "Informação ao usuário",
        ),
    }

    return template.format(**values)

def main():
    system_prompt = read_file(
        PROMPTS_DIR / "system_prompt.md"
    )

    user_template = read_file(
        PROMPTS_DIR / "user_prompt.md"
    )

    scenario = read_file(
        SCENARIOS_DIR / "P0.md"
    )

    user_prompt = build_user_prompt(
        user_template,
        scenario
    )

    print("\n===== SYSTEM PROMPT =====\n")
    print(system_prompt)

    print("\n===== USER PROMPT =====\n")
    print(user_prompt)

if __name__ == "__main__":
    main()