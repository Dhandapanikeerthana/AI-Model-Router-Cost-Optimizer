
import json
from pathlib import Path


LOG_FILE = Path(__file__).resolve().parent.parent / "logs" / "requests.jsonl"


def get_analytics() -> dict:
    """Summarize saved request metrics."""

    if not LOG_FILE.exists():
        return {
            "total_requests": 0,
            "average_latency_seconds": 0.0,
            "total_estimated_api_cost_usd": 0.0,
        }

    records = []

    with LOG_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                records.append(json.loads(line))

    if not records:
        return {
            "total_requests": 0,
            "average_latency_seconds": 0.0,
            "total_estimated_api_cost_usd": 0.0,
        }

    total_requests = len(records)

    average_latency = sum(
        record["latency_seconds"] for record in records
    ) / total_requests

    total_cost = sum(
        record["estimated_api_cost_usd"] for record in records
    )

    return {
        "total_requests": total_requests,
        "average_latency_seconds": round(average_latency, 3),
        "total_estimated_api_cost_usd": round(total_cost, 8),
    }


if __name__ == "__main__":
    analytics = get_analytics()

    print("--- Request Analytics ---")
    print("Total requests:", analytics["total_requests"])
    print("Average latency (seconds):", analytics["average_latency_seconds"])
    print("Total estimated API cost (USD):",
          analytics["total_estimated_api_cost_usd"])
