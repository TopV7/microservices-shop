import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import time

app = Flask(__name__)
CORS(app)

def get_db_connection():
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

# Отключаем ASCII, чтобы в JSON был русский текст, а не кракозябры
app.config['JSON_AS_ASCII'] = False

# Ссылка на каталог внутри Docker-сети
CATALOG_SERVICE_URL = "http://catalog-service:5000/products"

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    product_name = data.get('product_name')

    if not product_name:
        return jsonify({"status": "error", "message": "Не указано имя товара"}), 400

    try:
        # Спрашиваем список товаров у каталога
        response = requests.get(CATALOG_SERVICE_URL, timeout=5)
        if response.status_code != 200:
            return jsonify({"status": "error", "message": "Каталог недоступен"}), 503
        
        products = response.json()
        
        # Проверяем, есть ли товар в списке (без учета регистра)
        if any(p.lower() == product_name.lower() for p in products):
            # Подключаемся к базе
            conn = get_db_connection()
            if not conn:
                return jsonify({"status": "error", "message": "БД недоступна"}), 500
            
            cur = conn.cursor()
            # Выполняем SQL команду на вставку данных
            cur.execute('INSERT INTO orders (product_name) VALUES (%s) RETURNING id;', (product_name,))
            
            # Получаем ID, который база сама присвоила этому заказу
            new_id = cur.fetchone()[0]
            
            conn.commit() # ФИКСИРУЕМ результат в базе
            cur.close()
            conn.close()

            return jsonify({
                "status": "success", 
                "order_id": new_id, # Отдаем реальный ID из базы
                "item": product_name,
                "message": f"Товар '{product_name}' куплен и сохранен в БД!"
            }), 201
        else:
            return jsonify({"status": "error", "message": f"Товар '{product_name}' не найден в каталоге"}), 404

    except Exception as e:
        return jsonify({"status": "error", "message": f"Ошибка связи: {str(e)}"}), 500

@app.route("/")
def index():
    return "Order Service работает!"

if __name__ == "__main__":
    # Запускаем строго на порту 5001
    app.run(host="0.0.0.0", port=5001)