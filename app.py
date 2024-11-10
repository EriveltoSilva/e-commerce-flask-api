from flask import Flask
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)

    quantity = db.Column(db.Integer, nullable=True)
    # category = db.Column(db.String(80), nullable=True)
    # image_url = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Product {self.name}>'

    def __str__(self):
        return f'<Product {self.name}>'


@app.route('/api/v1/products', methods=['POST',])
def add_products():
    data = request.json
    if "name" in data and "price" in data and "quantity" in data:
        product = Product(
            name=data['name'],
            price=data.get('price'),
            description=data.get('description', ""),
            quantity=data.get('quantity', 0)
        )
        db.session.add(product)
        db.session.commit()
        return jsonify({"status": "success", "message": "Produto cadastrado com sucesso!", }), 201
    return jsonify({"status": "error", "message": "Campos faltando!", "data": data}), 400


@app.route('/api/v1/products/<int:product_id>', methods=['DELETE',])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"status": "success", "message": "Produto excluído com sucesso!", }), 200
    return jsonify({"status": "error", "message": "Produto não encontrado!", }), 404


@app.route('/api/v1/products', methods=['DELETE',])
def delete_product_list():
    product_list = request.json
    if type(product_list) is list:
        for product_id in product_list:
            product = Product.query.get(product_id)
            if product:
                db.session.delete(product)
        db.session.commit()
        return jsonify({"status": "success", "message": "Produtos excluídos com sucesso!", }), 200
    else:
        return jsonify({"status": "error", "message": "Os dados enviados não são uma lista!", }), 400


@app.route('/api/v1/products/<int:product_id>', methods=['GET',])
def read_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "status": "success",
            "data": {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "description": product.description,
                "quantity": product.quantity,
                "created_at": product.created_at,
                "updated_at": product.updated_at
            }
        }), 200
    return jsonify({"status": "error", "message": "Produto não encontrado!", }), 404


if __name__ == '__main__':
    app.run(debug=True)
