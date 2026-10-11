import json

filename = "report.json"

# Шаг 1. Пытаемся загрузить существующий каталог при старте программы
try:
    with open(filename, "r", encoding="utf-8") as file:
        catalog = json.load(file)
except FileNotFoundError:
    catalog = []

print("--- Система управления каталогом запущена ---")

# Шаг 2. Запускаем бесконечный цикл меню
while True:
    print("\nДоступные действия:")
    print("1. Посмотреть каталог")
    print("2. Добавить новый товар")
    print("3. Выход из программы")
    
    choice = input("Выберите пункт меню (1, 2 или 3): ")
    
    if choice == "1":
        print("\n--- Текущий каталог товаров ---")
        if not catalog:
            print("Каталог пока пуст.")
        else:
            for item in catalog:
                status_text = "В наличии" if item["is_active"] else "Нет в наличии"
                print(f"- {item['title']} | Цена: {item['current_price']} руб. | Статус: {status_text}")
                
    elif choice == "2":
        print("\n--- Добавление товара ---")
        title = input("Введите название товара: ")
        price = int(input("Введите цену (число): "))
        
        new_item = {
            "title": title,
            "current_price": price,
            "is_active": True
        }
        
        catalog.append(new_item)
        
        # Сразу сохраняем обновленный список в файл
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(catalog, file, ensure_ascii=False, indent=4)
            
        print(f"Товар «{title}» успешно добавлен и сохранен в файл!")
        
    elif choice == "3":
        print("Работа программы завершена. Хорошего дня!")
        break
    else:
        print("Ошибка: выберите пункт от 1 до 3.")