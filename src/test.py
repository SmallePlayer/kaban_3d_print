import sqlite3

def create_database():
    """Создает базу данных и таблицу, если их нет"""
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ База данных и таблица созданы!")

def add_product():
    """Добавляет новый товар через консоль"""
    name = input("Введите название товара: ")

    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()
    print("✅ Товар добавлен!")

def view_products():
    """Выводит список всех товаров"""
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM products")
    products = cursor.fetchall()

    if not products:
        print("❌ Товаров нет в базе!")
    else:
        print("\nСписок товаров:")
        for product in products:
            print(f"ID: {product[0]}, Название: {product[1]}")

    conn.close()

def main():
    """Главное меню"""
    create_database()  # Создаем БД при запуске

    while True:
        print("\n--- Меню ---")
        print("1. Добавить товар")
        print("2. Показать все товары")
        print("3. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            add_product()
        elif choice == "2":
            view_products()
        elif choice == "3":
            print("Выход...")
            break
        else:
            print("❌ Неверный ввод!")

if __name__ == "__main__":
    main()
