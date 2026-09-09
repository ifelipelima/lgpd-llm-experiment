import os
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from prepare_pilot import read_file, build_user_prompt

MODEL = "gemini-3.5-flash"

ALLOWED_SCENARIOS = {
    "F1", "F2", "F3",
    "N1", "N2", "N3",
    "T1", "T2", "T3",
    "D1", "D2", "D3",
}

BASE_DIR = Path(__file__).parent
PROMPTS_DIR = BASE_DIR / "prompts"
SCENARIOS_DIR = BASE_DIR / "scenarios"
RESULTS_DIR = BASE_DIR / "results" / "gemini"

def parse_args():
    parser = argparse.ArgumentParser(
        description="Executa um cenário oficial no Gemini."
    )

    parser.add_argument(
        "scenario_id",
        type=str.upper,
        choices=sorted(ALLOWED_SCENARIOS),
        help="Identificador do cenário, por exemplo: F1",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Monta e exibe o prompt sem chamar a API.",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    scenario_id = args.scenario_id

    system_prompt = read_file(
        PROMPTS_DIR / "system_prompt.md"
    )

    user_template = read_file(
        PROMPTS_DIR / "user_prompt.md"
    )

    scenario_path = (
        SCENARIOS_DIR / f"{scenario_id}.md"
    )

    scenario = read_file(scenario_path)

    user_prompt = build_user_prompt(
        user_template,
        scenario,
    )

    if args.dry_run:
        print("\n===== DRY RUN =====\n")
        print(f"Cenário: {scenario_id}")
        print(f"Modelo: {MODEL}")

        print("\n===== SYSTEM PROMPT =====\n")
        print(system_prompt)

        print("\n===== USER PROMPT =====\n")
        print(user_prompt)

        print(
            "\nNenhuma chamada à API foi realizada."
        )

        return

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        RESULTS_DIR
        / f"{scenario_id}_gemini-3.5-flash.json"
    )

    if output_path.exists():
        raise FileExistsError(
            "Já existe uma resposta oficial para "
            f"{scenario_id} no Gemini: {output_path}"
        )

    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY não encontrada no arquivo .env"
        )

    client = genai.Client(
        api_key=api_key
    )

    interaction = client.interactions.create(
        model=MODEL,
        system_instruction=system_prompt,
        input=user_prompt,
        generation_config={
            "thinking_level": "medium",
            "max_output_tokens": 5000,
        },
    )

    response_text = interaction.output_text
    usage = interaction.usage

    result = {
        "scenario_id": scenario_id,
        "model": MODEL,
        "provider": "Google Gemini Developer API",
        "timestamp_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "configuration": {
            "thinking_level": "medium",
            "max_output_tokens": 5000,
        },
        "usage": {
            "input_tokens": usage.total_input_tokens,
            "thought_tokens": usage.total_thought_tokens,
            "output_tokens": usage.total_output_tokens,
            "total_tokens": usage.total_tokens,
        },
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "response": response_text,
    }

    output_path.write_text(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("\n===== USO DE TOKENS =====\n")
    print(f"Entrada: {usage.total_input_tokens}")
    print(f"Raciocínio: {usage.total_thought_tokens}")
    print(f"Saída: {usage.total_output_tokens}")
    print(f"Total: {usage.total_tokens}")

    print("\n===== RESPOSTA DO GEMINI =====\n")
    print(response_text)

    print(
        f"\nResultado salvo em: {output_path}"
    )

if __name__ == "__main__":
    main()