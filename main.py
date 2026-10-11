from bs4 import BeautifulSoup
import json
import requests

def scrape_quotes(url):
  """Функция для парсинга цитат с веб-страницы"""
  try:
    response = requests.get(url)
    if response.status_code == 200:
      soup = BeautifulSoup(response.text, "html.parser")
      quote_blocks = soup.find_all("div", class_="quote")

      quotes_list = []
      for block in quote_blocks:
        text = block.find("span", class_="text").text
        author = block.find("small", class_="author").text
        quotes_list.append({"author": author, "text": text})

      return quotes_list
    else:
      print(f"Ошибка сервера: код {response.status_code}")
      return []
  except Exception as e:
    print(f"Произошла ошибка при парсинге: {e}")
    return []

def save_to_json(filename, data):
  """Функция для сохранения данных в JSON-файл"""
  with open(filename, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"Отчет успешно сохранен в файл {filename}!")

# Главная точка входа в программу
if __name__ == "__main__":
  url = "https://quotes.toscrape.com/"

  print("--- Запуск сбора данных с сайта ---")

  # Шаг 1. Спарсим цитаты
  scraped_data = scrape_quotes(url)

  # Шаг 2. Сохраним результат, если данные получены
  if scraped_data:
    print(f"Успешно собрано цитат: {len(scraped_data)}")
    save_to_json("scraped_quotes.json", scraped_data)

  print("--- Работа программы завершена ---")