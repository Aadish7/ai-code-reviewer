import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def review_code(diff):

    prompt = f"""
You are a Senior Software Engineer.

Analyze this GitHub Pull Request diff.

Provide:

# Summary of Changes

# Bugs Detected

# Code Quality Improvements

# Security Concerns

# Performance Concerns

# Final Recommendation

Pull Request Diff:

{diff}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


def review_repository(code):

    prompt = f"""
You are a Senior Software Engineer.

Review this complete GitHub repository.

Return the response in Markdown format.

# Project Summary

# Strengths

# Code Quality Issues

# Security Issues

# Performance Issues

# Suggested Improvements

# Resume Value

# Industry Readiness

# Rating out of 10

# Hiring Recommendation

Repository Code:

{code}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content