from bs4 import BeautifulSoup
import csv
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

      for block in quote_blocks:
        text = block.find("span", class_="text").text
        author = block.find("small", class_="author").text
        all_quotes.append({"author": author, "text": text})

      next_btn = soup.find("li", class_="next")
      if next_btn:
        next_page_relative = next_btn.find("a")["href"]
        current_url = base_url.rstrip("/") + next_page_relative
        page_count += 1
      else:
        print("Больше нет страниц для парсинга.")
        current_url = None

    except Exception as e:
      print(f"Произошла ошибка: {e}")
      break

  return all_quotes

def save_to_csv(filename, data):
  """Функция для сохранения собранных данных в CSV-таблицу"""
  # Используем utf-8-sig, чтобы кириллица идеально открывалась в Excel
  with open(filename, "w", newline="", encoding="utf-8-sig") as file:
    # Указываем названия колонок таблицы
    fieldnames = ["author", "text"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()  # Записываем шапку таблицы
    writer.writerows(data)  # Записываем все строки с данными

  print(f"Табличный отчет успешно сохранен в файл {filename}!")

# Главная точка входа в программу
if __name__ == "__main__":
  base_url = "https://quotes.toscrape.com"

  print("--- Запуск сбора данных и экспорта в таблицу ---")

  # Шаг 1. Собираем данные с 3 страниц
  scraped_data = scrape_multiple_pages(base_url, max_pages=3)

  # Шаг 2. Сохраняем в CSV, если данные есть
  if scraped_data:
    print(f"\nВсего успешно собрано цитат: {len(scraped_data)}")
    save_to_csv("quotes_table.csv", scraped_data)

  print("--- Работа программы завершена ---")