import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Make sure to set this environment variable on your machine or GitHub Actions
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-fallback-key-if-applicable")
    OPENAI_MODEL = "gpt-4o-mini"  # Fast, cheap, and excellent at parsing HTML strings
