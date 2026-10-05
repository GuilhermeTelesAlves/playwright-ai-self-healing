import pytest
from playwright.sync_api import sync_playwright
from self_healing_driver.py import SelfHealingDriver

def test_ai_self_healing_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) # Keep true for CI/CD
        page = browser.new_page()
        
        # Open a standard sandbox practice website
        page.goto("https://herokuapp.com")
        
        # Interact normally using standard playwright
        page.fill("#username", "tomsmith")
        page.fill("#password", "SuperSecretPassword!")
        
        # Initialize our custom AI Healing driver wrapper
        driver = SelfHealingDriver(page)
        
        # INTENTIONAL FAILURE: We pass a fake button ID (#wrong-login-submit-button)
        # The script will trigger the AI, which reads the page and finds the real button via the description string.
        driver.smart_click(
            fallback_description="The login submit button with a login icon", 
            original_selector="button#wrong-login-submit-button" 
        )
        
        # Verify that login was successful despite the bad selector
        assert page.is_visible("div.flash.success")
        print("🚀 Test complete. AI saved the build!")
        
        browser.close()
