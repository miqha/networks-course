import json
import os

from flask import Flask, request, jsonify, abort, send_file

app = Flask(__name__)

products: dict[int, 'Product'] = {}

def check(id):
    if id not in products:
        abort(404, description="Resource not found")


class Product:
    last_id = 0
    icons_folder = "icons/"

    def __init__(self, name=None, description=None):
        self.id = self._id_gen()
        self.name = name if name else "-"
        self.description = description if description else "-"
        self.image_path = None

    def to_json(self):
        return json.dumps({
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "icon": self.image_path
        })

    def save_image(self, file):
        if not os.path.exists(Product.icons_folder + f'{self.id}'):
            os.makedirs(Product.icons_folder + f'{self.id}')
            
        file.save(Product.icons_folder + f'{self.id}/{file.filename}')
        self.image_path = Product.icons_folder + f'{self.id}/{file.filename}'

    @staticmethod
    def _id_gen():
        Product.last_id += 1
        return Product.last_id


@app.route('/')
def index():
    return "Index page"


@app.route('/product', methods=['POST'])
def post_product():
    if request.is_json:
        name = request.json.get("name")
        description = request.json.get("description")
        product = Product(name, description)
        products[product.id] = product
        return product.to_json()
    else:
        return jsonify({"error": "Data type must be json"}), 400


@app.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    check(id)
    return products[id].to_json()


@app.route('/product/<int:id>', methods=['PUT'])
def update_product(id):
    check(id)
    new_data = request.json

    if new_name := new_data.get('name'):
        products[id].name = new_name

    if new_description := new_data.get('description'):
        products[id].description = new_description

    return products[id].to_json()


@app.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    check(id)
    return (products.pop(id)).to_json()


@app.route('/products', methods=['GET'])
def get_products():
    return jsonify([p.to_json() for p in products.values()])


@app.route('/product/<int:id>/image', methods=['POST'])
def post_img(id):
    check(id)
    if 'icon' not in request.files:
        return 'No file', 400

    file = request.files['icon']
    products[id].save_image(file)
    return 'Icon was updated'


@app.route('/product/<int:id>/image', methods=['GET'])
def get_img(id):
    check(id)
    path = products[id].image_path
    if not path:
        return 'No file', 400
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run()
