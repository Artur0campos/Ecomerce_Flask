from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_login import (LoginManager, UserMixin, current_user, login_required,
                         login_user, logout_user)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "minha_chave_123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

login_manager = LoginManager()
db = SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
 
CORS(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(12), nullable=False)
    cart = db.relationship('CartItem', backref='user', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float,nullable=False)
    description = db.Column(db.Text, nullable=True)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_Id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    


@app.route('/')
def hello():
    return 'helo world!'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(name=data.get('name')).first()
    if user:
        if data.get('password') == user.password:
            login_user(user)
            return jsonify({"mensagem": "Logged in  successfully"})
    return jsonify({"mensagem":"Logged in fail"}),401


@app.route('/logout', methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"mensagem": "Logout successfully"})


@app.route('/api/products/add', methods=["POST"])
@login_required
def add_product():
    data = request.json
    if 'name' in data and 'preco' in data:
        product = Product(name=data.get("name", ""), preco=data.get("preco", ""), description=data.get("description", ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"mensagem": "Product added successfully"})
    return jsonify({"mensagem": "Invalid product data"}), 400


@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
@login_required
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
@login_required
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

@app.route('/api/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_products_cartItem(product_id):
    user = User.query.get(int(current_user.id))
    product = Product.query.get(product_id)
    if product and user:
        cartItem = CartItem(user_Id=user.id, product_id=product.id)
        db.session.add(cartItem)
        db.session.commit()
        return jsonify({"mensagem": "Product add to the cart successfully"})
    return jsonify({"mensagem": "Invalid product data"}), 400


@app.route('/api/cart/delete/<int:cart_id>', methods=["DELETE"])
@login_required
def delete_product_cartItem(cart_id):
    cart_id = CartItem.query.get(cart_id)
    if cart_id:
        db.session.delete(cart_id)
        db.session.commit()
        return jsonify({"mensagem": "Product delete of the cart successfully"})
    return jsonify({"mensagem": "Invalid product data"}), 400

@app.route('/api/cart', methods=['GET'])
@login_required
def listar_cart():
    cartItems = CartItem.query.all()
    cartList = []
    for cartItem in cartItems:
        cart_data = {
            "id": cartItem.id,
            "user_Id": cartItem.user_Id,
            "product_id": cartItem.product_id
        }
        cartList.append(cart_data)
    return jsonify(cartList)

@app.route('/api/cart/checkout', methods=['POST'])
@login_required
def checkout_cart():
    user = User.query.get(int(current_user.id))
    cartItems = user.cart
    for cartItem in cartItems:
        db.session.delete(cartItem)
    db.session.commit()
    return jsonify({"mensage": "checkout done succesfuly"})


if __name__ == "__main__":
    app.run(debug=True) 