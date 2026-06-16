import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("GITHUB_TOKEN")

print("Token exists:", token is not None)
print("Token length:", len(token) if token else 0)

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

response = requests.get(
    "https://api.github.com/user",
    headers=headers
)

print("Status:", response.status_code)
print("Response:", response.text)