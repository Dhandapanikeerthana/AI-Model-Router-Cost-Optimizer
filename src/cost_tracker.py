
from time import perf_counter


def estimate_tokens(text: str) -> int:
    """Rough token estimate; not an exact tokenizer count."""
    if not text.strip():
        return 0

    return max(1, len(text.split()))


def calculate_cost(
    input_tokens: int,
    output_tokens: int,
    input_price_per_million: float = 0.0,
    output_price_per_million: float = 0.0,
) -> float:
    """Estimate model API cost in USD."""

    input_cost = input_tokens * input_price_per_million / 1_000_000
    output_cost = output_tokens * output_price_per_million / 1_000_000

    return input_cost + output_cost


def track_request(prompt: str, response: str, latency_seconds: float) -> dict:
    input_tokens = estimate_tokens(prompt)
    output_tokens = estimate_tokens(response)

    # Local Ollama model: no per-token API charge.
    cost_usd = calculate_cost(input_tokens, output_tokens)

    return {
        "input_tokens_estimated": input_tokens,
        "output_tokens_estimated": output_tokens,
        "latency_seconds": round(latency_seconds, 3),
        "estimated_api_cost_usd": round(cost_usd, 8),
    }


if __name__ == "__main__":
    start = perf_counter()

    sample_prompt = "Explain Java variables."
    sample_response = "A variable stores a value in a named location."

    elapsed = perf_counter() - start
    print(track_request(sample_prompt, sample_response, elapsed))
