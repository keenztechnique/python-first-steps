# Список товаров для будщего парсера 
tracked_items = ["ноутбук", "смартфон", "наушники"]
# Добавляем новый товар в список
tracked_items.append ("монитор")
print(f"Список товаров для отслеживания: {tracked_items}")
print(f"Всего товаров в работе: {len(tracked_items)}")
# Проверяем наличие конкретного товара с помощью условий
search_target = "смартфон"
if search_target in tracked_items:
    print(f"Товар '{search_target}' найден в базе запускаем сбор цен")
else:
    print(f"Товар '{search_target}' отсутствует в списке отслеживания")
