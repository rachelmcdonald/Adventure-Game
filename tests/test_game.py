import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:5000"

def test_homepage_loads(page: Page):
    """Check the game intro screen loads successfully"""
    page.goto(BASE_URL)
    expect(page).to_have_title("The Mosslit Path")

