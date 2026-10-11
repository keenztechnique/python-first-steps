from playwright.sync_api import sync_playwright

def run_dynamic_scraper():
  with sync_playwright() as p:
    # Запускаем браузер. headless=False покажет нам окно браузера в реальном времени!
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    print("Открываем страницу в браузере...")
    page.goto("https://quotes.toscrape.com/js/")

    # Ждем, пока JavaScript подгрузит элементы с классом .quote
    print("Ждем загрузку динамического контента...")
    page.wait_for_selector(".quote")

    # Находим все блоки с цитатами
    quote_elements = page.locator(".quote").all()
    print(f"Успешно найдено цитат через браузер: {len(quote_elements)}\n")

    # Выведем первые несколько цитат в консоль
    for idx, element in enumerate(quote_elements[:5], 1):
      text = element.locator(".text").inner_text()
      author = element.locator(".author").inner_text()
      print(f"{idx}. {author}:\n   {text}\n")

    # Закрываем браузер
    browser.close()
    print("Браузер успешно закрыт.")

if __name__ == "__main__":
  run_dynamic_scraper()