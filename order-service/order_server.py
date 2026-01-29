import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Простой список заказов (имитация базы данных)
orders = [
    {"order_id": 1, "product_name": "Microservice Course", "status": "shipped"},
    {"order_id": 2, "product_name": "Python Book", "status": "pending"},
]


@app.route("/orders", methods=["GET"])
def get_orders():
    return jsonify(orders)


@app.route("/check_item/<name>")
def check_item(name):
    # 1. Спрашиваем список товаров у первого сервиса (порт 5000)
    response = requests.get("http://127.0.0.1:5000/products")

    # 2. Превращаем ответ из JSON в обычный список Python
    catalog = response.json()

    # 3. Проверяем, есть ли наше имя в этом списке
    # 3. Ищем, встречается ли наше слово внутри любой строки каталога
    found = False
    for item in catalog:
        # Проверяем вхождение и приводим всё к маленьким буквам для надежности
        if name.lower() in item.lower():
            found = True
            break

    if found:
        return jsonify({"message": f"Да, товар '{name}' найден в каталоге!"})
    else:
        return (
            jsonify({"message": f"Нет, товара '{name}' в каталоге не существует"}),
            404,
        )


if __name__ == "__main__":
    # Запускаем на порту 5001, чтобы не конфликтовать с первым сервисом (он на 5000)
    app.run(host="0.0.0.0", port=5001)
