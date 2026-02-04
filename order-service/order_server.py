import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
            return jsonify({
                "status": "success", 
                "order_id": 101, 
                "item": product_name,
                "message": f"Товар '{product_name}' успешно куплен!"
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