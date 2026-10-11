from bs4 import BeautifulSoup
import requests

# В качестве примера возьмем открытый тестовый сайт для парсинга
url = "https://quotes.toscrape.com/"

print("--- Запрос веб-страницы ---")

try:
    response = requests.get(url)
    
    if response.status_code == 200:
        print("Страница успешно получена!")
        
        # Передаем HTML-код страницы в BeautifulSoup для анализа
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Находим все блоки с цитатами на странице
        quote_blocks = soup.find_all("div", class_="quote")
        
        print(f"Найдено цитат на странице: {len(quote_blocks)}\n")
        
        # Проходим по каждой цитате и вытягиваем текст и автора
        for block in quote_blocks:
            text = block.find("span", class_="text").text
            author = block.find("small", class_="author").text
            
            print(f"• {author}: {text}")
            
    else:
        print(f"Ошибка загрузки страницы: код {response.status_code}")

except Exception as e:
    print(f"Произошла ошибка: {e}")

print("\n--- Парсинг завершен ---")