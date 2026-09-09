import os
import json
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

from prepare_pilot import read_file, build_user_prompt


MODEL = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"
SCENARIO_ID = "P0"

BASE_DIR = Path(__file__).parent

PROMPTS_DIR = BASE_DIR / "prompts"
SCENARIOS_DIR = BASE_DIR / "scenarios"
RESULTS_DIR = BASE_DIR / "results"


def main():
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

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    result = {
        "scenario_id": SCENARIO_ID,
        "model": MODEL,
        "provider": "Cloudflare Workers AI",
        "model_developer": "Meta",
        "timestamp_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "configuration": {
            "max_tokens": 5000,
        },
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "response": response_text,
        "raw_usage": response_data["result"].get("usage"),
    }

    output_path = (
        RESULTS_DIR
        / "P0_llama-3.3-70b-instruct-fp8-fast.json"
    )

    output_path.write_text(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    usage = response_data["result"].get("usage")

    if usage:
        print("\n===== USO DE TOKENS =====\n")
        print(json.dumps(
            usage,
            ensure_ascii=False,
            indent=2,
        ))

    print("\n===== RESPOSTA DO LLAMA =====\n")
    print(response_text)

    print(
        f"\nResultado salvo em: {output_path}"
    )


if __name__ == "__main__":
    main()