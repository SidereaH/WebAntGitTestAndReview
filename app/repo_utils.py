import tempfile, os
from git import Repo

def clone_repo(url: str) -> str:
    temp_dir = tempfile.mkdtemp()
    Repo.clone_from(url, temp_dir)
    return temp_dir

def load_all_code(path: str) -> dict:
    code_map = {}
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(('.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.go', '.rs', '.php')):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        code_map[full_path] = f.read()
                except Exception:
                    continue
    return code_map
