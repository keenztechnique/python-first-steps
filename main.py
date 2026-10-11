from bs4 import BeautifulSoup
import json
import requests

def scrape_multiple_pages(base_url, max_pages=3):
  """Функция для сбора цитат с нескольких страниц (пагинация)"""
  all_quotes = []
  current_url = base_url
  page_count = 1

  while current_url and page_count <= max_pages:
    print(f"Парсим страницу {page_count}: {current_url}")

    try:
      response = requests.get(current_url)
      if response.status_code != 200:
        print(f"Ошибка загрузки: код {response.status_code}")
        break

      soup = BeautifulSoup(response.text, "html.parser")
      quote_blocks = soup.find_all("div", class_="quote")

      # Собираем цитаты с текущей страницы
      for block in quote_blocks:
        text = block.find("span", class_="text").text
        author = block.find("small", class_="author").text
        all_quotes.append({"author": author, "text": text})

      # Ищем ссылку на следующую страницу
      next_btn = soup.find("li", class_="next")
      if next_btn:
        next_page_relative = next_btn.find("a")["href"]
        # Базовый URL сайта + относительная ссылка на следующую страницу
        current_url = base_url.rstrip("/") + next_page_relative
        page_count += 1
      else:
        print("Больше нет страниц для парсинга.")
        current_url = None

    except Exception as e:
      print(f"Произошла ошибка: {e}")
      break

  return all_quotes

def save_to_json(filename, data):
  """Функция для сохранения данных в JSON-файл"""
  with open(filename, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"Отчет успешно сохранен в файл {filename}!")

# Главная точка входа в программу
if __name__ == "__main__":
  base_url = "https://quotes.toscrape.com"

  print("--- Запуск многостраничного сбора данных ---")

  # Соберем данные с первых 3 страниц (для примера)
  scraped_data = scrape_multiple_pages(base_url, max_pages=3)

  if scraped_data:
    print(f"\nВсего успешно собрано цитат со всех страниц: {len(scraped_data)}")
    save_to_json("multi_page_quotes.json", scraped_data)

  print("--- Работа программы завершена ---")