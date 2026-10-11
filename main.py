import json
filename = "report.json"
print("--- Попытка чтения отчета из файла ---")
try:
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
        print(f"Файл успешно прочитан! Найдено записей: {len(data)}")
        for item in data:
            print(f"- {item['title']}: {item['current_price']} руб.")
except FileNotFoundError:
    print(f"Внимание: файл {filename} не найден. Сначала запустите генерацию отчета!")
print("--- Процесс завершен ---")
