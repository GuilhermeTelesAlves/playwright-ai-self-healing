import re
from playwright.sync_api import Page
from openai import OpenAI
from config import Config

class SelfHealingDriver:
    def __init__(self, page: Page):
        self.page = page
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)

    def smart_click(self, fallback_description: str, original_selector: str = None):
        """
        Attempts to click using the original selector. If it fails, 
        AI analyzes the page DOM to heal the test and find the correct element.
        """
        if original_selector:
            try:
                # Try standard execution first
                self.page.click(original_selector, timeout=3000)
                print(f"✅ Successfully clicked using original selector: '{original_selector}'")
                return
            except Exception as e:
                print(f"⚠️ Original selector '{original_selector}' failed. Activating AI Self-Healing...")

        # 1. Capture the DOM structure (Cleaned up to save AI tokens)
        html_content = self.page.content()
        cleaned_html = self._clean_html(html_content)

        # 2. Craft the prompt for the LLM
        prompt = f"""
        You are an expert QA Automation AI. A UI test failed because an element could not be found.
        
        Target Element Description: {fallback_description}
        Original Failed Selector: {original_selector}
        
        Analyze the following HTML snippet and find the single best Playwright locator string (e.g. text selector, CSS, or internal locator) that matches the target description.
        Return ONLY the raw string value of the locator, nothing else. No markdown, no quotes, no explanations.

        HTML DOM:
        {cleaned_html}
        """

        # 3. Request healing solution from OpenAI
        try:
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            
            healed_locator = response.choices[0].message.content.strip()
            print(f"🤖 AI Self-Healing Suggested New Locator: '{healed_locator}'")
            
            # 4. Execute the healed click
            self.page.click(healed_locator, timeout=5000)
            print(f"🎉 Self-healing successful! Interacted with healed locator.")
            
        except Exception as ai_err:
            raise RuntimeError(f"❌ AI Healing failed to resolve the issue. Original Error: {e}. AI Error: {ai_err}")

    def _clean_html(self, html: str) -> str:
        """Helper to strip scripts and styles to keep tokens low and focus on structure."""
        html = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', html)
        html = re.sub(r'<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>', '', html)
        return html[:8000] # Cap length to avoid context bloat
