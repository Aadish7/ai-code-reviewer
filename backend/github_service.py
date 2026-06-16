import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}


def get_repositories():
    response = requests.get(
        "https://api.github.com/user/repos",
        headers=headers
    )
    return response.json()


def get_user_repositories(username):

    response = requests.get(
        f"https://api.github.com/users/{username}/repos",
        headers=headers
    )

    return response.json()


def get_pull_requests(owner, repo):
    response = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/pulls",
        headers=headers
    )
    return response.json()


def get_pull_request_files(owner, repo, pr_number):
    response = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files",
        headers=headers
    )
    return response.json()


def get_repository_code(owner, repo):

    url = f"https://api.github.com/repos/{owner}/{repo}/contents"

    response = requests.get(
        url,
        headers=headers
    )

    contents = response.json()

    combined_code = ""

    allowed_extensions = (
        ".py",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".java",
        ".cpp",
        ".c",
        ".html",
        ".css",
        ".md"
    )

    if not isinstance(contents, list):
        return ""

    for item in contents:

        if item.get("type") != "file":
            continue

        filename = item.get("name", "")

        if not filename.endswith(
            allowed_extensions
        ):
            continue

        download_url = item.get(
            "download_url"
        )

        if not download_url:
            continue

        try:

            file_response = requests.get(
                download_url
            )

            combined_code += (
                f"\n\n===== FILE: {filename} =====\n\n"
            )

            combined_code += (
                file_response.text[:5000]
            )

        except Exception:
            pass

    return combined_code