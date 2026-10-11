from bs4 import BeautifulSoup
import argparse
import csv
import logging
import requests

# Настраиваем логирование: все статусы и ошибки будут записываться в файл scraper.log
logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)

def scrape_multiple_pages(base_url, max_pages):
  """Функция для сбора цитат с User-Agent и логированием"""
  all_quotes = []
  current_url = base_url
  page_count = 1

  # Заголовки маскируют наш скрипт под обычный браузер Chrome
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
          " like Gecko) Chrome/120.0.0.0 Safari/537.36"
      )
  }

  while current_url and page_count <= max_pages:
    msg = f"Парсим страницу {page_count} из {max_pages}: {current_url}"
    logging.info(msg)
    print(msg)

    try:
      # Передаем headers в запрос, чтобы защититься от банов
      response = requests.get(current_url, headers=headers)
      if response.status_code != 200:
        error_msg = f"Ошибка загрузки: код {response.status_code}"
        logging.error(error_msg)
        print(error_msg)
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
      error_msg = f"Произошла критическая ошибка: {e}"
      logging.exception(error_msg)
      print(error_msg)
      break

  return all_quotes

def save_to_csv(filename, data):
  """Сохранение данных в CSV с записью события в лог"""
  with open(filename, "w", newline="", encoding="utf-8-sig") as file:
    fieldnames = ["author", "text"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

  success_msg = f"Табличный отчет успешно сохранен в файл {filename}!"
  logging.info(success_msg)
  print(success_msg)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
      description="Профессиональный скрейпер с Headers и Logging"
  )
  parser.add_argument("--pages", type=int, default=2)
  parser.add_argument("--output", type=str, default="quotes_pro.csv")
  args = parser.parse_args()

  base_url = "https://quotes.toscrape.com"

  logging.info("--- Запуск утилиты сбора данных ---")
  print("--- Запуск утилиты сбора данных ---")

  scraped_data = scrape_multiple_pages(base_url, max_pages=args.pages)

  if scraped_data:
    print(f"\nВсего успешно собрано цитат: {len(scraped_data)}")
    save_to_csv(args.output, scraped_data)

  logging.info("--- Работа программы завершена ---")
  print("--- Работа программы завершена ---")