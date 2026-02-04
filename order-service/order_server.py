import requests
from flask import Flask, jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route("/")
def index():
    return "Order Service работает!"

@app.route("/check_item/<name>")
def check_item(name):
    try:
        # Запрашиваем данные у каталога
        response = requests.get("http://catalog-service:5000/products", timeout=5)
        
        if response.status_code != 200:
            return jsonify({"message": "Каталог недоступен"}), 503

        # Получаем список из JSON
        catalog = response.json()
        
        # Ищем товар
        found = False
        for item in catalog:
            if name.lower() == item.lower():
                found = True
                break

        if found:
            # Слово 'found' нужно для нашего теста в GitHub!
            return jsonify({"message": f"found: Товар '{name}' найден!"})
        else:
            return jsonify({"message": f"not found: Товар '{name}' не найден"}), 404

    except Exception as e:
        return jsonify({"message": f"Ошибка связи: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)