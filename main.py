from bs4 import BeautifulSoup
import argparse
import csv
import logging
import os
import requests

# Настраиваем логирование
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
  """Сохранение данных в CSV"""
  with open(filename, "w", newline="", encoding="utf-8-sig") as file:
    fieldnames = ["author", "text"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

  success_msg = f"Табличный отчет успешно сохранен в файл {filename}!"
  logging.info(success_msg)
  print(success_msg)

def send_telegram_message(token, chat_id, message):
  """Функция отправки текстового сообщения в Telegram"""
  url = f"https://api.telegram.org/bot{token}/sendMessage"
  payload = {"chat_id": chat_id, "text": message}
  try:
    response = requests.post(url, data=payload)
    if response.status_code == 200:
      print("Уведомление успешно отправлено в Telegram!")
    else:
      print(f"Ошибка отправки в Telegram: {response.text}")
  except Exception as e:
    print(f"Ошибка соединения с Telegram API: {e}")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
      description="Профессиональный скрейпер с Telegram"
  )
  parser.add_argument("--pages", type=int, default=2)
  parser.add_argument("--output", type=str, default="quotes_tg.csv")
  # Добавим аргументы для бота (можно передавать из терминала или прописать по умолчанию)
  parser.add_argument(
      "--token", type=str, default="", help="Telegram Bot Token"
  )
  parser.add_argument("--chat_id", type=str, default="", help="Telegram Chat ID")
  args = parser.parse_args()

  base_url = "https://quotes.toscrape.com"

  logging.info("--- Запуск утилиты сбора данных ---")
  print("--- Запуск утилиты сбора данных ---")

  scraped_data = scrape_multiple_pages(base_url, max_pages=args.pages)

  if scraped_data:
    print(f"\nВсего успешно собрано цитат: {len(scraped_data)}")
    save_to_csv(args.output, scraped_data)

    # Если токен и чат указаны, отправляем отчет в Telegram
    if args.token and args.chat_id:
      report_text = (
          f"✅ Скрейпер завершил работу!\nСобрано цитат: {len(scraped_data)}"
          f"\nФайл: {args.output}"
      )
      send_telegram_message(args.token, args.chat_id, report_text)
    else:
      print(
          "Токен или Chat ID не указаны, отправка в Telegram пропущена."
      )

  logging.info("--- Работа программы завершена ---")
  print("--- Работа программы завершена ---")