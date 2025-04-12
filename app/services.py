import os
import tempfile
from pathlib import Path
from git import Repo
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from app.config import settings

def clone_repository(repo_url: str, branch: str = "main") -> Path:
    """Клонирует репозиторий во временную директорию"""
    temp_dir = Path(settings.temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    repo_dir = temp_dir / repo_url.split("/")[-1].replace(".git", "")
    if repo_dir.exists():
        # Удаляем существующий клон
        import shutil
        shutil.rmtree(repo_dir)
    
    Repo.clone_from(repo_url, repo_dir, branch=branch)
    return repo_dir

def analyze_code_with_mistral(code: str, file_path: str) -> dict:
    """Анализирует код с помощью Mistral AI"""
    client = MistralClient(api_key=settings.mistral_api_key)
    
    # Определяем язык программирования по расширению файла
    lang = file_path.split(".")[-1] if "." in file_path else "unknown"
    
    messages = [
        ChatMessage(role="system", content=f"""You are a senior software engineer performing code analysis. 
        Analyze the following {lang} code from file {file_path} and provide:
        1. A concise summary of what the code does
        2. Key test cases that should be written
        3. Code review with potential improvements"""),
        ChatMessage(role="user", content=code)
    ]
    
    response = client.chat(
        model="mistral-medium",
        messages=messages,
        temperature=0.3,
    )
    
    return parse_mistral_response(response.choices[0].message.content)

def parse_mistral_response(response: str) -> dict:
    """Парсит ответ Mistral AI в структурированный формат"""
    sections = response.split("\n\n")
    result = {
        "summary": "",
        "tests": "",
        "review": "",
        "improvements": []
    }
    
    for section in sections:
        if section.startswith("1.") or "summary" in section.lower():
            result["summary"] = section
        elif section.startswith("2.") or "test" in section.lower():
            result["tests"] = section
        elif section.startswith("3.") or "review" in section.lower():
            result["review"] = section
        elif "improvement" in section.lower():
            result["improvements"] = section.split("\n")[1:]
    
    return result

def check_mistral_availability() -> bool:
    """Проверяет доступность Mistral API"""
    try:
        client = MistralClient(api_key=settings.mistral_api_key)
        client.list_models()
        return True
    except Exception:
        return False