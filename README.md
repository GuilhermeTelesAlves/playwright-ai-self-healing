# 🤖 Playwright AI Self-Healing Automation Engine

An intelligent, next-generation QA automation architecture built with **Python**, **Playwright**, and **OpenAI (GPT-4o-mini)**. This framework intercepting standard test execution failures (like stale or modified DOM locators) and dynamically updates selectors at runtime using LLM context analysis.

## 🌟 Core Features
- **Graceful Failure Interception:** Wraps standard Playwright actions inside custom exception handlers.
- **Context-Aware DOM Parsing:** Automatically extracts, strips down, and packages raw HTML layouts to pass to the AI model efficiently.
- **Dynamic Selector Regeneration:** Leverages Generative AI to map business descriptions to real-time UI components on the fly, eliminating pipeline test flakiness.

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **Core Testing Tool:** Playwright
- **AI Orchestration:** OpenAI API Engine
- **Test Runner:** Pytest

## 🚀 Getting Started

1. Clone the repository and install dependencies:
```bash
pip install playwright openai python-dotenv pytest
playwright install
```

2. Export your OpenAI key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

3. Run the self-healing demonstration test:
```bash
pytest test_login.py -s
```
