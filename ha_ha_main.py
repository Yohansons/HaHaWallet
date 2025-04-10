# -*- coding: utf-8 -*-
import asyncio
from playwright.async_api import async_playwright, Page
from mnemonic import Mnemonic

EXTENSION_PATH = r"C:\_IDE\_CURSOR\HaHa_walet\Ha_ha_W"
USER_DATA_DIR = r"C:\_IDE\_CURSOR\HaHa_walet\UserData"
DEFAULT_PASSWORD = "YourSecurePass123"
EXTENSION_ID = "andhndehpcjpmneneealacgnmealilal"

mnemo = Mnemonic("english")

def generate_haha_seed() -> list[str]:
    return mnemo.generate(strength=128).split()

async def remove_auto_warning(page: Page):
    # Блокируем все URL с ключевыми словами
    await page.route("**/*warning*", lambda route: route.abort())
    await page.route("**/*banner*", lambda route: route.abort())
    
    # Удаляем через поиск текста
    await page.evaluate('''() => {
        const elements = document.body.getElementsByTagName('*');
        for (let el of elements) {
            if (el.textContent.includes('авто тестовое ПО')) {
                el.parentNode.removeChild(el);
            }
        }
    }''')
    print("[УДАЛЕНИЕ] Текстовые баннеры удалены")

async def setup_haha_wallet(page: Page, seed_phrase: list[str]):
    await page.click('[data-testid="accept-terms"]', timeout=20000)
    await page.click('button:has-text("Импортировать")', timeout=15000)
    
    for i in range(12):
        await page.fill(f'input[name="seed-word-{i+1}"]', seed_phrase[i])
    
    await page.click('#confirm-seed-btn', timeout=20000)
    
    await page.fill('#new-password', DEFAULT_PASSWORD)
    await page.fill('#confirm-password', DEFAULT_PASSWORD)
    await page.click('#submit-password', timeout=15000)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            USER_DATA_DIR,
            headless=False,
            args=[
                f"--load-extension={EXTENSION_PATH}",
                "--disable-extensions-except={EXTENSION_PATH}",
                "--no-sandbox",
                "--disable-component-extensions-with-background-pages"
            ],
            timeout=120000
        )
        
        wallet_page = await browser.new_page()
        
        # Перехват перед загрузкой
        await remove_auto_warning(wallet_page)
        await wallet_page.goto(f'chrome-extension://{EXTENSION_ID}/home.html', wait_until="networkidle")
        
        # Повторное удаление после загрузки
        await remove_auto_warning(wallet_page)
        await wallet_page.wait_for_timeout(5000)
        await remove_auto_warning(wallet_page)
        
        seed = generate_haha_seed()
        await setup_haha_wallet(wallet_page, seed)
        
        print("Все баннеры удалены. Процесс завершён.")
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())