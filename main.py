import json
def create_product_card(name, price, status):
    return {
        "title": name,
        "current_price": price,
        "is_active": status
    }
catalog = [
    create_product_card("Ноутбук", 75000, True),
    create_product_card("Смартфон", 55000, True),
    create_product_card("Наушники", 12000, False)
]
with open("report.json", "w", encoding="utf-8") as file:
    json.dump(catalog, file, ensure_ascii=False, indent=4)
print("--- Данные успешно сохранены в файл report.json ---")
