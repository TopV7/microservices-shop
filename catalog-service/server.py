import psycopg2
from flask import Flask, jsonify
import os
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

def get_db_connection():
    # Пробуем подключиться несколько раз, если база еще не загрузилась
    for i in range(10):
        try:
            conn = psycopg2.connect(
                host="db",
                database="shop_db",
                user="user",
                password="password"
            )
            return conn
        except Exception as e:
            print(f"Попытка {i+1}: База еще не готова, ждем...")
            time.sleep(2)
    return None

def init_db():
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        # Создаем таблицу
        cur.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id serial PRIMARY KEY,
                name varchar(100) NOT NULL
            );
        ''')
        # Проверяем, пустая ли она, и добавляем товары
        cur.execute('SELECT COUNT(*) FROM products;')
        if cur.fetchone()[0] == 0:
            cur.execute("INSERT INTO products (name) VALUES (%s)", ("Microservice",))
            cur.execute("INSERT INTO products (name) VALUES (%s)", ("Docker-Book",))
        conn.commit()
        cur.close()
        conn.close()
        print("База данных готова!")

# Инициализируем базу при запуске
init_db()

@app.route("/")
def index():
    return "Catalog Service с Базой Данных работает!"

@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Нет подключения к базе"}), 500
    
    cur = conn.cursor()
    cur.execute('SELECT name FROM products;')
    rows = cur.fetchall()
    products_list = [row[0] for row in rows]
    cur.close()
    conn.close()
    
    # ВАЖНО: отдаем JSON список
    return jsonify(products_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)