def generate_tests(code_map: dict) -> str:
    joined_code = "\n\n".join(code_map.values())[:8000]
    prompt = (
        "На основе следующего кода сгенерируй базовые unit-тесты на подходящем языке "
        "(например pytest для Python, JUnit для Java, и т.д.):\n\n" + joined_code
    )
    from app.mistral_client import mistral_chat
    return mistral_chat(prompt)
