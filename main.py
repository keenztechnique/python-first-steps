def create_product_card(name, price, status):
    product = {
        "title": name,
        "current_price": price,
        "is_active": status
    }
    return product
catalog = [
    create_product_card("Ноутбук", 75000, True),
    create_product_card("Смартфон", 55000, True),
    create_product_card("Наушники", 12000, False),
]
print("--- Активный каталог интернет-магазина ---")
for item in catalog:
    if item["is_active"]:
        print(f"Товар: {item['title']} | Цена: {item['current_price']} руб. | Статус: в наличии")
    else:
        print(f"Товар: {item['title']} | Статус: Нет в наличии")
print("--- Обход каталога завершен ---")
