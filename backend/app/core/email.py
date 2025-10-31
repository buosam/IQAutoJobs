"""
Email service for IQAutoJobs.
"""
from typing import List
from app.core.config import settings
import httpx

class EmailService:
    """Email service for sending emails."""

    def __init__(self):
        self.api_key = settings.EMAIL_API_KEY
        self.from_address = settings.EMAIL_FROM_ADDRESS
        self.from_name = settings.EMAIL_FROM_NAME
        self.base_url = settings.RESEND_API_BASE_URL

    async def send_email(self, to: str, subject: str, html: str):
        """Send an email."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "from": f"{self.from_name} <{self.from_address}>",
            "to": [to],
            "subject": subject,
            "html": html,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()

email_service = EmailService()
