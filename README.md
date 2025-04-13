# WebAntGitTestAndReview

## Запуск:

```
# заходим в свое вирт. окружение
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8083 --reload
```

### Пример запроса:

```
curl --location 'http://localhost:8083/analyze' \
--header 'Content-Type: application/json' \
--data '{
  "repo_url": "https://github.com/SidereaH/python-Viselica"
}'

```

### Формат ответа:

```
{
    "summary"
    "generated_tests"
    "review"
}
```

### Перед запуском определите переменные окружения

```
MISTRAL_API_KEY
MAX_FILE_SIZE
MAX_FILES_TO_ANALYZE
TEMP_DIR
```

#### dockerhub: aliquamsiderea/git_review_webant:0.1.0
