from flask import Flask
import psycopg2
import os
import time

app = Flask(__name__)

# Функция для подключения к базе (наш "переводчик")
def get_db_connection():
    for i in range(5):
        try:
            conn = psycopg2.connect(
                host='db', # имя сервиса из docker-compose
                database='shop_db',
                user='user',
                password='password'
            )
            return conn
        except Exception as e:
            print(f"База еще не готова, ждем... ({e})")
            time.sleep(2)
    return None

# Функция для создания таблицы (наводим порядок в базе сами)
def init_db():
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        # Создаем таблицу, если её нет
        cur.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id serial PRIMARY KEY,
                name varchar(100) NOT NULL
            );
        ''')
        # Добавляем товары, только если таблица пустая
        cur.execute('SELECT COUNT(*) FROM products;')
        if cur.fetchone()[0] == 0:
            cur.execute("INSERT INTO products (name) VALUES (%s)", ("Microservice",))
            cur.execute("INSERT INTO products (name) VALUES (%s)", ("Docker-Book",))
        conn.commit()
        cur.close()
        conn.close()
        print("База данных готова!")

# Запускаем подготовку базы при старте
init_db()

@app.route('/')
def hello():
    return "Catalog Service с Базой Данных работает!"

# Вот этот эндпоинт теперь берет данные из базы, а не из файла!
@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    if not conn:
        return "Ошибка: не удалось подключиться к базе", 500
    
    cur = conn.cursor()
    cur.execute('SELECT name FROM products;')
    rows = cur.fetchall()
    
    # Собираем названия товаров в список
    products_list = [row[0] for row in rows]
    
    cur.close()
    conn.close()
    return str(products_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)