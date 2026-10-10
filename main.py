def check_item_status(item_name):
    print(f"Запуск сканирования... Товар в работе: {item_name}")
tracked_items = ["ноутбук", "смартфон", "наушники", "монитор"]
print("--- Старт работы системы ---")
for product in tracked_items:
    check_item_status(product)
print("--- Система завершила обход ---")