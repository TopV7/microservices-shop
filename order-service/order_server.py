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


if __name__ == "__main__":
    # Запускаем на порту 5001, чтобы не конфликтовать с первым сервисом (он на 5000)
    app.run(host="0.0.0.0", port=5001)
