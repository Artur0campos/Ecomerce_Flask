from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'


db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float,nullable=False)
    description = db.Column(db.Text, nullable=True)



@app.route('/')
def hello():
    return 'helo world!'

@app.route('/api/products/add', methods=["POST"])
def add_product():
    data = request.json
    if 'name' in data and 'preco' in data:
        product = Product(name=data.get("name", ""), preco=data.get("preco", ""), description=data.get("description", ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"mensagem": "Product added successfully"})
    return jsonify({"mensagem": "Invalid product data"}), 400


@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"mensagem": "Product delete successfully"})
    return jsonify({"mensagem": "Invalid product data"}), 400


@app.route('/api/products/<int:product_id>', methods=["GET"])
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "id": product.id, 
            "name": product.name,
            "preco": product.preco,
            "description": product.description
        })
    return jsonify({"mensagem":"product not found"}), 404


@app.route('/api/products/update/<int:product_id>', methods=["PUT"])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"mensagem":"product not found"}), 404
    
    data = request.json
    if 'name' in data:
        product.name = data['name']

    if 'preco' in data:
        product.preco = data['preco']

    if 'description' in data:
        product.description = data['description']

    db.session.commit()
    return jsonify({"mensagem": "Product update sucess"})


@app.route('/api/products', methods=["GET"])
def get_products():
    products = Product.query.all()
    product_list = []
    for product in products:
        product_data = {
        "id" : product.id,
        "name" : product.name,
        "preco" : product.preco,
        "description" : product.description
        }
        product_list.append(product_data)
    return jsonify(product_list)

if __name__ == "__main__":
    app.run(debug=True)