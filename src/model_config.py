
MODELS = {
    "llama3.2:3b": {
        "provider": "ollama",
        "model_name": "llama3.2:3b",
        "cost_per_1m_input_tokens": 0.0,
        "cost_per_1m_output_tokens": 0.0,
        "capability": "general",
        "supports_local": True,
    },
    "qwen2.5-coder:3b": {
        "provider": "ollama",
        "model_name": "qwen2.5-coder:3b",
        "cost_per_1m_input_tokens": 0.0,
        "cost_per_1m_output_tokens": 0.0,
        "capability": "coding",
        "supports_local": True,
    },
}

DEFAULT_MODEL = "llama3.2:3b"
