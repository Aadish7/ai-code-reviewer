from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.github_service import (
    get_repositories,
    get_user_repositories,
    get_pull_requests,
    get_pull_request_files,
    get_repository_code
)

from backend.ai_reviewer import (
    review_code,
    review_repository
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "AI Code Reviewer Running"
    }


@app.get("/repos")
def repos():
    return get_repositories()


@app.get("/repos/{username}")
def user_repos(username: str):
    return get_user_repositories(username)


@app.get("/pulls/{owner}/{repo}")
def pulls(owner: str, repo: str):
    return get_pull_requests(owner, repo)


@app.get("/pull-files/{owner}/{repo}/{pr_number}")
def pull_files(
    owner: str,
    repo: str,
    pr_number: int
):
    return get_pull_request_files(
        owner,
        repo,
        pr_number
    )


@app.get("/review")
def review():

    sample_diff = """
+ print("Hello World")
"""

    return {
        "review": review_code(sample_diff)
    }


@app.get("/review-pr/{owner}/{repo}/{pr_number}")
def review_pr(
    owner: str,
    repo: str,
    pr_number: int
):

    files = get_pull_request_files(
        owner,
        repo,
        pr_number
    )

    diff_text = ""

    for file in files:

        if "patch" in file:
            diff_text += file["patch"]
            diff_text += "\n\n"

    review = review_code(diff_text)

    return {
        "review": review
    }


@app.get("/review-repo/{owner}/{repo}")
def review_repo(
    owner: str,
    repo: str
):

    code = get_repository_code(
        owner,
        repo
    )

    review = review_repository(code)

    return {
        "review": review
    }