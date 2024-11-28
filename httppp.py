from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
data = [
    {'id': 1, 'name': 'Item 1'},
    {'id': 2, 'name': 'Item 2'}
]

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(data)

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in data if item['id'] == item_id), None)
    if item:
        return jsonify(item)
    else:
        return jsonify({'message': 'Item not found'}), 404

@app.route('/items', methods=['POST'])
def create_item():
    new_item = request.get_json()
    data.append(new_item)
    return jsonify(new_item), 201

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((item for item in data if item['id'] == item_id), None)
    if item:
        updated_item = request.get_json()
        item.update(updated_item)
        return jsonify(item)
    else:
        return jsonify({'message': 'Item not found'}), 404

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global data
    data = [item for item in data if item['id'] != item_id]
    return jsonify({'message': 'Item deleted'})

if __name__ == '__main__':
    app.run(debug=True, port=5005)