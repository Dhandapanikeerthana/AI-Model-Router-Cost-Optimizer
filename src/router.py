
from time import perf_counter

import httpx

from src.model_config import MODELS
from src.ollama_client import generate_response
from src.cost_tracker import track_request
from src.metrics_logger import save_request_metrics


def classify_task(prompt: str) -> str:
    """Classify a request using simple rules."""

    text = prompt.lower()
    word_count = len(text.split())

    coding_keywords = [
        "java", "python", "program", "coding", "code",
        "function", "algorithm", "reverse a string",
        "write code", "debug", "implement",
    ]

    complex_keywords = [
        "architecture", "compare", "analyse", "analyze",
        "optimize", "optimise", "design a system",
        "step by step", "multiple requirements",
        "trade-offs", "tradeoffs", "scalable",
        "comprehensive",
    ]

    medium_keywords = [
        "explain", "examples", "example", "difference",
        "differences", "summarize", "summarise", "how does",
    ]

    if any(keyword in text for keyword in coding_keywords):
        return "complex"

    if any(keyword in text for keyword in complex_keywords):
        return "complex"

    if any(keyword in text for keyword in medium_keywords):
        return "medium"

    if word_count > 50:
        return "complex"

    if word_count > 15:
        return "medium"

    return "simple"


def get_installed_models() -> set[str]:
    """Return model names currently available in Ollama."""

    try:
        response = httpx.get(
            "http://localhost:11434/api/tags",
            timeout=5.0,
        )
        response.raise_for_status()

        return {
            item["name"]
            for item in response.json().get("models", [])
        }

    except httpx.HTTPError as error:
        raise RuntimeError(
            f"Unable to connect to Ollama: {error}"
        ) from error


def select_model(prompt: str) -> dict:
    """Select a preferred installed model with fallback support."""

    complexity = classify_task(prompt)
    installed_models = get_installed_models()

    preferences = {
        "simple": ["llama3.2:3b", "qwen2.5-coder:3b"],
        "medium": ["qwen2.5-coder:3b", "llama3.2:3b"],
        "complex": ["qwen2.5-coder:3b", "llama3.2:3b"],
    }

    preferred_models = preferences[complexity]

    model_name = next(
        (
            name
            for name in preferred_models
            if name in installed_models and name in MODELS
        ),
        None,
    )

    used_fallback = False

    if model_name is None:
        model_name = next(
            (
                name
                for name, config in MODELS.items()
                if config["model_name"] in installed_models
            ),
            None,
        )
        used_fallback = model_name is not None

    if model_name is None:
        raise RuntimeError(
            "No configured model is installed in Ollama. "
            "Check src/model_config.py and run 'ollama list'."
        )

    reason = (
        f"Task classified as '{complexity}'. "
        f"Selected model: {model_name}."
    )

    if used_fallback:
        reason += " Preferred model unavailable; fallback selected."

    return {
        "complexity": complexity,
        "model": model_name,
        "provider": MODELS[model_name]["provider"],
        "reason": reason,
    }


def route_request(prompt: str) -> dict:
    """Select a model, generate a response, and track usage."""

    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    decision = select_model(prompt)

    start = perf_counter()

    answer = generate_response(
        prompt,
        model=decision["model"],
    )

    latency = perf_counter() - start

    metrics = track_request(prompt, answer, latency)

    save_request_metrics({
        **decision,
        **metrics,
    })

    return {
        **decision,
        "response": answer,
        **metrics,
    }


if __name__ == "__main__":
    try:
        prompt = input("Enter your question: ").strip()
        result = route_request(prompt)

        print("\n--- Routing Decision ---")
        print("Complexity:", result["complexity"])
        print("Model:", result["model"])
        print("Provider:", result["provider"])
        print("Reason:", result["reason"])

        print("\n--- AI Response ---")
        print(result["response"])

        print("\n--- Usage Metrics ---")
        print("Estimated input tokens:", result["input_tokens_estimated"])
        print("Estimated output tokens:", result["output_tokens_estimated"])
        print("Latency (seconds):", result["latency_seconds"])
        print("Estimated API cost (USD):", result["estimated_api_cost_usd"])

    except (RuntimeError, ValueError) as error:
        print(f"\nError: {error}")
