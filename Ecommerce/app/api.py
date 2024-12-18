from flask import Blueprint, jsonify

api = Blueprint('api', __name__)

@api.route('/product/<product_id>', methods=['GET'])
def get_product(product_id):
    # Placeholder for fetching product details
    return jsonify({"product_id": product_id, "details": "Product details here..."})
