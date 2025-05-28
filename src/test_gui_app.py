import json

try:
    # Читаем JSON-файл
    with open("cam.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        
    # Выводим список камер
    print("📷 Список камер из JSON:")
    for camera in data["cameras"]:
        print(f"ID: {camera['id']}, Название: {camera['name']}")

except FileNotFoundError:
    print("❌ Ошибка: Файл cameras.json не найден!")
except json.JSONDecodeError:
    print("❌ Ошибка: Неправильный формат JSON!")
except KeyError:
    print("❌ Ошибка: В файле нет ключа 'cameras'!")