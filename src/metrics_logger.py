
import json
from datetime import datetime, timezone
from pathlib import Path


LOG_FILE = Path(__file__).resolve().parent.parent / "logs" / "requests.jsonl"


def save_request_metrics(result: dict) -> None:
    """Append one request's metrics to a JSON Lines log file."""

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "complexity": result["complexity"],
        "model": result["model"],
        "provider": result["provider"],
        "input_tokens_estimated": result["input_tokens_estimated"],
        "output_tokens_estimated": result["output_tokens_estimated"],
        "latency_seconds": result["latency_seconds"],
        "estimated_api_cost_usd": result["estimated_api_cost_usd"],
    }

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record) + "\n")

    print(f"Metrics saved to: {LOG_FILE}")


if __name__ == "__main__":
    sample_result = {
        "complexity": "simple",
        "model": "llama3.2:3b",
        "provider": "ollama",
        "input_tokens_estimated": 5,
        "output_tokens_estimated": 12,
        "latency_seconds": 2.5,
        "estimated_api_cost_usd": 0.0,
    }

    save_request_metrics(sample_result)
