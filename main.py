import json
import requests

# URL открытого API, который возвращает список товаров
url = "https://dummyjson.com/products"

print("--- Запрос списка товаров с сервера ---")

try:
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        # Получаем сам список товаров из ключа "products"
        products = data.get("products", [])
        
        print(f"Успешно получено товаров с сервера: {len(products)}")
        
        # Создаем пустой список для отфильтрованных товаров
        cheap_products = []
        
        # Проходим по каждому товару и ищем выгодные (дешевле $50)
        for item in products:
            if item["price"] < 50:
                cheap_products.append({
                    "title": item["title"],
                    "price": item["price"],
                    "rating": item["rating"]
                })
                
        print(f"Найдено товаров дешевле $50: {len(cheap_products)}")
        
        # Сохраняем отфильтрованный результат в отдельный файл
        with open("cheap_products.json", "w", encoding="utf-8") as file:
            json.dump(cheap_products, file, ensure_ascii=False, indent=4)
            print("Отчет успешно сохранен в cheap_products.json!")
            
    else:
        print(f"Ошибка сервера: код ответа {response.status_code}")

except Exception as e:
    print(f"Произошла ошибка: {e}")

print("--- Обработка завершена ---")