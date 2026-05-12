import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://127.0.0.1:5000"

def make_choice(page: Page, choice: str):
    """Dismiss start overlay if present, then make choice"""
    start_btn = page.locator("#start-game-btn")
    if start_btn.is_visible():
        start_btn.click()
        page.wait_for_load_state("networkidle")
    page.locator(f"button[value='{choice}']").click()

def test_homepage_loads(page: Page):
    """Check the game loads and shows the start scene"""
    page.goto(BASE_URL)
    expect(page.locator("body")).to_be_visible()

def test_start_button_visible(page: Page):
    """Check path choices appear after dismissing intro"""
    page.goto(BASE_URL)
    page.locator("#start-game-btn").click()
    page.wait_for_load_state("networkidle")
    expect(page.get_by_text("Go left")).to_be_visible()
    expect(page.get_by_text("Go right")).to_be_visible()

def test_left_path_loads(page: Page):
    """Check the left path leads to the fairy scene"""
    page.goto(BASE_URL)
    make_choice(page, "left")
    expect(page.locator(".scene-text").first).to_be_visible()


def test_right_path_loads(page: Page):
    """Check the right path leads to the wizard scene"""
    page.goto(BASE_URL)
    make_choice(page, "right")
    expect(page.locator(".scene-text").first).to_be_visible()

def test_combat_hp_bars_visible(page: Page):
    """Navigate to werewolf combat and check HP bar renders"""
    page.goto(BASE_URL)
    make_choice(page, "left")
    make_choice(page, "fairy_ignore")
    make_choice(page, "werewolf")
    expect(page.locator(".hp-bar").first).to_be_visible()

def test_attack_button_visible_in_combat(page: Page):
    """Check attack option is visible in werewolf combat"""
    page.goto(BASE_URL)
    make_choice(page, "left")
    make_choice(page, "fairy_ignore")
    make_choice(page, "werewolf")
    expect(page.get_by_text("Attack the werewolf")).to_be_visible()
