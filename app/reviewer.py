def review_code(code_map: dict) -> str:
    joined_code = "\n\n".join(code_map.values())[:8000]
    prompt = (
        "Проведи ревью следующего кода. Подчеркни потенциальные ошибки, улучшения, "
        "рекомендации по стилю и производительности:\n\n" + joined_code
    )
    from app.mistral_client import mistral_chat
    return mistral_chat(prompt)
