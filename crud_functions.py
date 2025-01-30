import sqlite3

DB_NAME = "not_telegram.db"

def execute_query(query, params=(), fetch=False, fetchall=False):
    """Универсальная функция для выполнения SQL-запросов."""
    with sqlite3.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute(query, params)
        if fetchall:
            return cursor.fetchall()
        elif fetch:
            return cursor.fetchone()
        connection.commit()

def initiate_db():
    """Создает таблицу Products, если она еще не создана."""
    execute_query('''
    CREATE TABLE IF NOT EXISTS Products (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL
    )
    ''')

def get_all_products():
    """Возвращает список всех продуктов из таблицы Products."""
    return execute_query("SELECT id, title, description, price FROM Products", fetchall=True)

def add_product(title, description, price):
    """Добавляет новый продукт в таблицу Products."""
    execute_query("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)", (title, description, price))


initiate_db()
add_product("Product1", "Описание продукта 1", 100)
add_product("Product2", "Описание продукта 2", 200)
add_product("Product3", "Описание продукта 3", 300)
add_product("Product4", "Описание продукта 4", 400)
