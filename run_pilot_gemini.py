import os
import json
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from prepare_pilot import read_file, build_user_prompt

MODEL = "gemini-3.5-flash"
SCENARIO_ID = "P0"

BASE_DIR = Path(__file__).parent

PROMPTS_DIR = BASE_DIR / "prompts"
SCENARIOS_DIR = BASE_DIR / "scenarios"
RESULTS_DIR = BASE_DIR / "results"

def main():
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY não encontrada no arquivo .env"
        )

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
        scenario,
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
            "max_output_tokens": 5000
        }
    )

    usage = interaction.usage

    print("\n===== USO DE TOKENS =====\n")
    print(f"Entrada: {usage.total_input_tokens}")
    print(f"Raciocínio: {usage.total_thought_tokens}")
    print(f"Saída: {usage.total_output_tokens}")
    print(f"Total: {usage.total_tokens}")

    response_text = interaction.output_text

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    result = {
        "scenario_id": SCENARIO_ID,
        "model": MODEL,
        "provider": "Google Gemini Developer API",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "configuration": {
            "thinking_level": "medium",
            "max_output_tokens": 3000,
        },
        "usage": {
            "input_tokens": usage.total_input_tokens,
            "thought_tokens": usage.total_thought_tokens,
            "output_tokens": usage.total_output_tokens,
            "total_tokens": usage.total_tokens,
        },
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "response": response_text
    }

    output_path = (
        RESULTS_DIR / "P0_gemini-3.5-flash.json"
    )

    output_path.write_text(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8",
    )

    print("\n===== RESPOSTA DO GEMINI =====\n")
    print(response_text)

    print(
        f"\nResultado salvo em: {output_path}"
    )

if __name__ == "__main__":
    main()