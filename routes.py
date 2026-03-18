from flask import Blueprint, jsonify, request
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
from model import CartItem, Product, User, db

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/')
def hello():
    return 'helo world!'



@api_blueprint.route('/login', methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(name=data.get('name')).first()
    if user:
        if data.get('password') == user.password:
            login_user(user)
            return jsonify({"mensagem": "Logged in  successfully"})
    return jsonify({"mensagem":"Logged in fail"}),401


@api_blueprint.route('/logout', methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"mensagem": "Logout successfully"})


@api_blueprint.route('/api/products/add', methods=["POST"])
@login_required
def add_product():
    data = request.json
    if 'name' in data and 'preco' in data:
        product = Product(name=data.get("name", ""), preco=data.get("preco", ""), description=data.get("description", ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"mensagem": "Product added successfully"})
    return jsonify({"mensagem": "Invalid product data"}), 400


@api_blueprint.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"mensagem": "Product delete successfully"})
    return jsonify({"mensagem": "Invalid product data"}), 400


@api_blueprint.route('/api/products/<int:product_id>', methods=["GET"])
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


@api_blueprint.route('/api/products/update/<int:product_id>', methods=["PUT"])
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


@api_blueprint.route('/api/products', methods=["GET"])
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

@api_blueprint.route('/api/cart/add/<int:product_id>', methods=['POST'])
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


@api_blueprint.route('/api/cart/delete/<int:cart_id>', methods=["DELETE"])
@login_required
def delete_product_cartItem(cart_id):
    cart_id = CartItem.query.get(cart_id)
    if cart_id:
        db.session.delete(cart_id)
        db.session.commit()
        return jsonify({"mensagem": "Product delete of the cart successfully"})
    return jsonify({"mensagem": "Invalid product data"}), 400

@api_blueprint.route('/api/cart', methods=['GET'])
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

@api_blueprint.route('/api/cart/checkout', methods=['POST'])
@login_required
def checkout_cart():
    user = User.query.get(int(current_user.id))
    cartItems = user.cart
    for cartItem in cartItems:
        db.session.delete(cartItem)
    db.session.commit()
    return jsonify({"mensage": "checkout done succesfuly"}) 