import os
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

from prompt_builder import read_file, build_user_prompt

MODEL = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"

ALLOWED_SCENARIOS = {
    "F1", "F2", "F3",
    "N1", "N2", "N3",
    "T1", "T2", "T3",
    "D1", "D2", "D3",
}

BASE_DIR = Path(__file__).parent
PROMPTS_DIR = BASE_DIR / "prompts"
SCENARIOS_DIR = BASE_DIR / "scenarios"
RESULTS_DIR = BASE_DIR / "results" / "llama"

def parse_args():
    parser = argparse.ArgumentParser(
        description="Executa um cenário oficial no Llama."
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
        / f"{scenario_id}_llama-3.3-70b-instruct-fp8-fast.json"
    )

    if output_path.exists():
        raise FileExistsError(
            "Já existe uma resposta oficial para "
            f"{scenario_id} no Llama: {output_path}"
        )

    load_dotenv()

    api_token = os.getenv("CLOUDFLARE_API_TOKEN")
    account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")

    if not api_token:
        raise RuntimeError(
            "CLOUDFLARE_API_TOKEN não encontrado no arquivo .env"
        )

    if not account_id:
        raise RuntimeError(
            "CLOUDFLARE_ACCOUNT_ID não encontrado no arquivo .env"
        )

    url = (
        "https://api.cloudflare.com/client/v4/accounts/"
        f"{account_id}/ai/run/{MODEL}"
    )

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "messages": [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        "max_tokens": 5000,
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=120,
    )

    response.raise_for_status()

    response_data = response.json()

    if not response_data.get("success"):
        raise RuntimeError(
            f"Erro na API da Cloudflare: {response_data}"
        )

    response_text = response_data["result"]["response"]
    usage = response_data["result"].get("usage")

    result = {
        "scenario_id": scenario_id,
        "model": MODEL,
        "model_developer": "Meta",
        "provider": "Cloudflare Workers AI",
        "timestamp_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "configuration": {
            "max_tokens": 5000,
        },
        "usage": usage,
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

    if usage:
        print("\n===== USO DE TOKENS =====\n")
        print(
            json.dumps(
                usage,
                ensure_ascii=False,
                indent=2,
            )
        )

    print("\n===== RESPOSTA DO LLAMA =====\n")
    print(response_text)

    print(
        f"\nResultado salvo em: {output_path}"
    )

if __name__ == "__main__":
    main()