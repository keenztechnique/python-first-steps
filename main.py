from bs4 import BeautifulSoup
import argparse
import csv
import requests

def scrape_multiple_pages(base_url, max_pages):
  """Функция для сбора цитат с указанного количества страниц"""
  all_quotes = []
  current_url = base_url
  page_count = 1

  while current_url and page_count <= max_pages:
    print(f"Парсим страницу {page_count} из {max_pages}: {current_url}")

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
      if next_btn and page_count < max_pages:
        next_page_relative = next_btn.find("a")["href"]
        current_url = base_url.rstrip("/") + next_page_relative
        page_count += 1
      else:
        current_url = None

    except Exception as e:
      print(f"Произошла ошибка: {e}")
      break

  return all_quotes

def save_to_csv(filename, data):
  """Функция для сохранения собранных данных в CSV-таблицу"""
  with open(filename, "w", newline="", encoding="utf-8-sig") as file:
    fieldnames = ["author", "text"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
  print(f"Табличный отчет успешно сохранен в файл {filename}!")

# Главная точка входа в программу
if __name__ == "__main__":
  # Настраиваем прием аргументов из командной строки
  parser = argparse.ArgumentParser(
      description="Профессиональный парсер цитат с поддержкой CLI"
  )
  parser.add_argument(
      "--pages", type=int, default=2, help="Количество страниц для парсинга"
  )
  parser.add_argument(
      "--output",
      type=str,
      default="quotes_cli.csv",
      help="Имя файла для сохранения",
  )

  args = parser.parse_args()

  base_url = "https://quotes.toscrape.com"

  print("--- Запуск утилиты сбора данных ---")
  print(f"Параметры: страниц={args.pages}, файл={args.output}\n")

  # Запускаем сбор с учетом переданных аргументов
  scraped_data = scrape_multiple_pages(base_url, max_pages=args.pages)

  if scraped_data:
    print(f"\nВсего успешно собрано цитат: {len(scraped_data)}")
    save_to_csv(args.output, scraped_data)

  print("--- Работа программы завершена ---")