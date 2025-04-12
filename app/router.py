from fastapi import APIRouter
from pydantic import BaseModel
from app.repo_utils import clone_repo, load_all_code
from app.analyzer import extract_summary
from app.test_generator import generate_tests
from app.reviewer import review_code

router = APIRouter()

class RepoRequest(BaseModel):
    repo_url: str

@router.post("/analyze")
async def analyze_repo(req: RepoRequest):
    repo_path = clone_repo(req.repo_url)
    code_map = load_all_code(repo_path)
    summary = extract_summary(code_map)
    tests = generate_tests(code_map)
    review = review_code(code_map)
    return {
        "summary": summary,
        "generated_tests": tests,
        "review": review
    }
