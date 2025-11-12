from flask import Flask, render_template

app = Flask(__name__)

products = [
    {"id": 1, "name": "Wireless Earbuds", "price": 2999, "img": "https://via.placeholder.com/150"},
    {"id": 2, "name": "Smart Watch", "price": 4999, "img": "https://via.placeholder.com/150"},
    {"id": 3, "name": "Bluetooth Speaker", "price": 1999, "img": "https://via.placeholder.com/150"},
]

@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/product/<int:id>')
def product(id):
    product = next((p for p in products if p['id'] == id), None)
    return render_template('product.html', product=product)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

