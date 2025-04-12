from pydantic import BaseSettings

class Settings(BaseSettings):
    mistral_api_key: str
    max_file_size: int = 1024 * 1024  # 1MB
    max_files_to_analyze: int = 20
    temp_dir: str = "/tmp/code_review"

    class Config:
        env_file = ".env"

settings = Settings()