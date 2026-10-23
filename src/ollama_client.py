
import httpx

OLLAMA_URL = "http://localhost:11434/api/generate"


def generate_response(prompt: str, model: str = "llama3.2:3b") -> str:
    """Generate a response using a locally running Ollama model."""

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }

    response = httpx.post(
        OLLAMA_URL,
        json=payload,
        timeout=120.0,
    )
    response.raise_for_status()

    result = response.json()
    return result["response"].strip()


if __name__ == "__main__":
    answer = generate_response(
        "Explain AI model routing in two simple sentences."
    )
    print("\nModel: llama3.2:3b")
    print("Response:", answer)
