from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("GITHUB_TOKEN")

print("Token exists:", token is not None)
print("Token length:", len(token) if token else 0)
print("Token prefix:", token[:4] if token else "None")