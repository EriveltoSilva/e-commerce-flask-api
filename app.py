from flask import Flask
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import login_user, logout_user, LoginManager, UserMixin, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dsfasdfjhladsfhjkerfjduhichsdbfiuewfsfasdfsfsdfsffegds23223g'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

login_manager = LoginManager(app)
login_manager.login_view = '/api/v1/accounts/login'

db = SQLAlchemy(app)
CORS(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<User {self.full_name}>'


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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/api/v1/accounts/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email', "")
    password = data.get('password', "")
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        login_user(user)
        return jsonify({"status": "success", "message": "Login successful"})
    return jsonify({"status": "error", "message": "Usuário não encontrado!"}), 401


@app.route('/api/v1/accounts/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"status": "success", "message": "Logout realizado com sucesso!"}), 200


@app.route('/api/v1/products', methods=['POST',])
@login_required
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
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"status": "success", "message": "Produto excluído com sucesso!", }), 200
    return jsonify({"status": "error", "message": "Produto não encontrado!", }), 404


@app.route('/api/v1/products', methods=['DELETE',])
@login_required
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


@app.route('/api/v1/products/<int:product_id>', methods=['PUT',])
@login_required
def update_product(product_id):
    product = Product.query.get(product_id)
    if product:
        data = request.json
        if "name" in data:
            product.name = data['name']
        if "price" in data:
            product.price = data.get('price')
        if "description" in data:
            product.description = data.get('description')
        if "quantity" in data:
            product.quantity = data.get('quantity')
        db.session.commit()
        return jsonify({"status": "success", "message": "Produto atualizado com sucesso!", }), 200
    return jsonify({"status": "error", "message": "Produto não encontrado!", }), 404


@app.route('/api/v1/products', methods=['GET',])
def list_products():
    products = Product.query.all()
    return jsonify([
        {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description,
            "quantity": product.quantity,
            "created_at": product.created_at,
            "updated_at": product.updated_at
        }
        for product in products
    ]), 200


if __name__ == '__main__':
    app.run(debug=True)
