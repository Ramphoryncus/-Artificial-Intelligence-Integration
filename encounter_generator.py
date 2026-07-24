import json
import platform
import time
from datetime import datetime
from pathlib import Path

import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:1b"
TELEMETRY_DIRECTORY = Path("telemetry")


def nanoseconds_to_seconds(value: int) -> float:
    """Convert Ollama's nanosecond duration values into seconds."""
    return value / 1_000_000_000

def normalize_headings(text: str) -> str:
    """Standardise encounter headings and spacing."""

    headings = ["ENEMY", "HAZARD", "REWARD", "ENCOUNTER"]

    cleaned = text.strip()

    for heading in headings:
        variants = [
            f"{heading}:",
            f"{heading.title()}:",
            f"{heading.lower()}:",
        ]

        for variant in variants:
            cleaned = cleaned.replace(
                variant,
                f"\n\n{heading}:"
            )

    return cleaned.strip()
    

def generate_encounter(location: str) -> dict:
    """Ask the local model to generate a small game encounter."""

    prompt = f"""
Create a concise and geographically plausible game encounter for this location:

{location}

Use creatures, weather, hazards, and environmental details that are
appropriate for the stated location. Do not include animals or features
that would not normally exist there unless explicitly described as
fictional, escaped, genetically modified, or artificially introduced.

Return exactly these headings:
ENEMY:
HAZARD:
REWARD:
ENCOUNTER:

Use exactly this format and capitalization:

ENEMY:
<enemy description>

HAZARD:
<hazard description>

REWARD:
<reward description>

ENCOUNTER:
<encounter description>

Requirements:
- Each heading must be uppercase exactly as shown.
- Put one blank line before every heading.
- Do not create additional headings.

The ENCOUNTER section should briefly describe how the player experiences the enemy, hazard, and reward.

Keep the complete response below 200 words.
"""

    request_data = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
    }

    start_time = time.perf_counter()

    response = requests.post(
        OLLAMA_URL,
        json=request_data,
        timeout=300,
    )
    response.raise_for_status()

    measured_seconds = time.perf_counter() - start_time
    result = response.json()

    evaluation_count = result.get("eval_count", 0)
    evaluation_duration = result.get("eval_duration", 0)

    generation_seconds = nanoseconds_to_seconds(evaluation_duration)

    tokens_per_second = (
        evaluation_count / generation_seconds
        if generation_seconds > 0
        else 0.0
    )

    telemetry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "model": result.get("model", MODEL_NAME),
        "platform": platform.platform(),
        "location_input": location,
        "response": normalize_headings(result.get("response", "")),
        "measured_response_seconds": measured_seconds,
        "ollama_total_seconds": nanoseconds_to_seconds(
            result.get("total_duration", 0)
        ),
        "model_load_seconds": nanoseconds_to_seconds(
            result.get("load_duration", 0)
        ),
        "prompt_tokens": result.get("prompt_eval_count", 0),
        "generated_tokens": evaluation_count,
        "generation_seconds": generation_seconds,
        "tokens_per_second": tokens_per_second,
    }

    return telemetry


def save_telemetry(telemetry: dict) -> Path:
    """Save the generated result and measurements to a JSON file."""

    TELEMETRY_DIRECTORY.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = TELEMETRY_DIRECTORY / f"encounter_{timestamp}.json"

    with output_path.open("w", encoding="utf-8") as output_file:
        json.dump(telemetry, output_file, indent=4)

    return output_path


def main() -> None:
    print("LOCAL AI GAME ENCOUNTER GENERATOR")
    print("---------------------------------")

    location = input("Enter a game location: ").strip()

    if not location:
        location = "an abandoned underwater research station"

    try:
        telemetry = generate_encounter(location)
    except requests.ConnectionError:
        print("\nCould not connect to Ollama.")
        print("Make sure Ollama is installed and running.")
        return
    except requests.RequestException as error:
        print(f"\nOllama request failed: {error}")
        return

    output_path = save_telemetry(telemetry)

    print("\nGENERATED ENCOUNTER")
    print("-------------------")
    print(telemetry["response"])

    print("\nTELEMETRY")
    print("---------")
    print(f'Model:             {telemetry["model"]}')
    print(f'Platform:          {telemetry["platform"]}')
    print(
        f'Response time:     '
        f'{telemetry["measured_response_seconds"]:.3f} seconds'
    )
    print(
        f'Model load time:   '
        f'{telemetry["model_load_seconds"]:.3f} seconds'
    )
    print(f'Prompt tokens:     {telemetry["prompt_tokens"]}')
    print(f'Generated tokens:  {telemetry["generated_tokens"]}')
    print(
        f'Generation speed:  '
        f'{telemetry["tokens_per_second"]:.2f} tokens/second'
    )
    print(f"\nTelemetry saved to: {output_path}")


if __name__ == "__main__":
    main()
