import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import RepositoryAnalysisRequest, CodeAnalysis, HealthCheck
from app.services import (
    clone_repository, 
    analyze_code_with_mistral,
    check_mistral_availability
)
from app.config import settings

app = FastAPI(
    title="Code Review Service",
    description="Микросервис для анализа кода репозиториев с Mistral AI",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", response_model=HealthCheck, tags=["health"])
async def health_check():
    """Проверка здоровья сервиса"""
    return {
        "status": "OK",
        "mistral_available": check_mistral_availability()
    }

@app.post("/analyze-repo", response_model=CodeAnalysis, tags=["analysis"])
async def analyze_repository(request: RepositoryAnalysisRequest):
    """Анализирует репозиторий по ссылке"""
    try:
        # Клонируем репозиторий
        repo_dir = clone_repository(request.repo_url, request.branch)
        
        # Находим все файлы с кодом
        code_files = []
        for ext in request.file_filter or ["py", "js", "java", "go", "rs", "ts"]:
            code_files.extend(list(repo_dir.rglob(f"*.{ext}")))
        
        if not code_files:
            raise HTTPException(status_code=400, detail="No code files found in the repository")
        
        # Ограничиваем количество анализируемых файлов
        code_files = code_files[:settings.max_files_to_analyze]
        
        # Анализируем каждый файл
        combined_result = {
            "summary": "",
            "tests": "",
            "review": "",
            "improvements": []
        }
        
        for file_path in code_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    code = f.read()
                    if len(code) > settings.max_file_size:
                        continue
                    
                    analysis = analyze_code_with_mistral(code, str(file_path.relative_to(repo_dir)))
                    
                    combined_result["summary"] += f"\n\nFile: {file_path}\n{analysis['summary']}"
                    combined_result["tests"] += f"\n\nTests for {file_path}:\n{analysis['tests']}"
                    combined_result["review"] += f"\n\nReview for {file_path}:\n{analysis['review']}"
                    combined_result["improvements"].extend(analysis['improvements'])
            except Exception as e:
                continue
        
        return combined_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-code", response_model=CodeAnalysis, tags=["analysis"])
async def analyze_code_directly(file: UploadFile):
    """Анализирует код из загруженного файла"""
    try:
        contents = await file.read()
        if len(contents) > settings.max_file_size:
            raise HTTPException(status_code=413, detail="File too large")
        
        code = contents.decode("utf-8")
        return analyze_code_with_mistral(code, file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))