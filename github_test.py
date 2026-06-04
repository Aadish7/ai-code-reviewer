import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

response = requests.get(
    "https://api.github.com/user",
    headers=headers
)

print("Status:", response.status_code)
print(response.json())
