def extract_summary(code_map: dict) -> str:
    joined_code = "\n\n".join(code_map.values())[:8000]
    prompt = (
        "Проанализируй следующий код и выдели его основную суть: "
        "что делает проект, какие технологии использует, ключевые компоненты и структура.\n\n"
        + joined_code
    )
    from app.mistral_client import mistral_chat
    return mistral_chat(prompt)
