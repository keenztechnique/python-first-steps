import json
import requests

# URL открытого тестового API с информацией о товаре
url = "https://dummyjson.com/products/1"

print("--- Отправляем запрос к серверу ---")

try:
    # Делаем GET-запрос к сайту/API
    response = requests.get(url)
    
    # Проверяем, успешен ли запрос (код 200 означает успех)
    if response.status_code == 200:
        print("Данные успешно получены с сервера!")
        
        # Превращаем ответ сервера из текста в словарь Python
        product_data = response.json()
        
        # Вытягиваем нужные поля
        title = product_data.get("title")
        price = product_data.get("price")
        
        print(f"Полученный товар: {title} | Цена: ${price}")
        
        # Сохраняем полученные данные в наш локальный файл отчета
        with open("report.json", "w", encoding="utf-8") as file:
            json.dump(product_data, file, ensure_ascii=False, indent=4)
            print("Данные сохранены в report.json!")
    else:
        print(f"Ошибка сервера: код ответа {response.status_code}")

except Exception as e:
    print(f"Произошла ошибка при запросе: {e}")

print("--- Запрос завершен ---")