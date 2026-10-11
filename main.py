import json
import requests

def fetch_products(url):
    """Функция для запроса данных с сервера"""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("products", [])
        else:
            print(f"Ошибка сервера: код ответа {response.status_code}")
            return []
    except Exception as e:
        print(f"Произошла ошибка при запросе: {e}")
        return []

def filter_products(products, max_price):
    """Функция для фильтрации товаров дешевле указанной цены"""
    filtered_list = []
    for item in products:
        if item["price"] < max_price:
            filtered_list.append({
                "title": item["title"],
                "price": item["price"],
                "rating": item["rating"]
            })
    return filtered_list

def save_to_json(filename, data):
    """Функция для сохранения данных в JSON-файл"""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Отчет успешно сохранен в файл {filename}!")

# Главная точка входа в программу
if __name__ == "__main__":
    url = "https://dummyjson.com/products"
    
    print("--- Запуск структурированного сборщика данных ---")
    
    # Шаг 1. Получаем данные
    all_products = fetch_products(url)
    
    if all_products:
        print(f"Успешно получено товаров с сервера: {len(all_products)}")
        
        # Шаг 2. Фильтруем (например, ищем всё, что дешевле $50)
        cheap_items = filter_products(all_products, 50)
        print(f"Найдено товаров дешевле $50: {len(cheap_items)}")
        
        # Шаг 3. Сохраняем результат
        save_to_json("cheap_products.json", cheap_items)
    
    print("--- Работа программы завершена ---")