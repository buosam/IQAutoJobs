
import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Sign up as Candidate
        await page.goto("http://localhost:5000/auth/register")
        await page.fill('input[name="first_name"]', "Test")
        await page.fill('input[name="last_name"]', "Candidate")
        await page.fill('input[name="email"]', "test.candidate@example.com")
        await page.fill('input[name="password"]', "password123")
        await page.fill('input[name="confirmPassword"]', "password123")
        await page.click('button:has-text("Create Account")')
        await page.wait_for_url("http://localhost:5000/dashboard")

        # Log out
        await page.goto("http://localhost:5000/api/auth/logout")

        # Sign up as Employer
        await page.goto("http://localhost:5000/auth/register")
        await page.fill('input[name="first_name"]', "Test")
        await page.fill('input[name="last_name"]', "Employer")
        await page.fill('input[name="email"]', "test.employer@example.com")
        await page.fill('input[name="password"]', "password123")
        await page.fill('input[name="confirmPassword"]', "password123")
        await page.click('button:has-text("I am a")')
        await page.click('text=Employer looking to hire')
        await page.click('button:has-text("Create Account")')
        await page.wait_for_url("http://localhost:5000/dashboard")

        await page.screenshot(path="jules-scratch/verification/verification.png")
        await browser.close()

asyncio.run(main())
