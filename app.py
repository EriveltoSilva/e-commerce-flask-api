from flask import Flask
from flask import request
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
    product = Product(
        name=data['name'],
        price=data.get('price'),
        description=data.get('description', ""),
        quantity=data.get('quantity', 0)
    )
    db.session.add(product)
    db.session.commit()

    return "Produto Salvo com Sucesso!"


if __name__ == '__main__':
    app.run(debug=True)
