
from src.router import classify_task, select_model


def test_simple_task():
    assert classify_task("What is the capital of India?") == "simple"


def test_coding_task():
    assert classify_task("Write a Java program to reverse a string") == "complex"


def test_simple_task_selects_llama():
    result = select_model("What is the capital of India?")
    assert result["model"] == "llama3.2:3b"


def test_coding_task_selects_qwen():
    result = select_model("Write a Java program to reverse a string")
    assert result["model"] == "qwen2.5-coder:3b"
