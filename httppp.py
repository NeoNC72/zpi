from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
reg = set()

@app.route('/register_id', methods=['POST'])
def register_id():
    data = request.json
    if data["id_n"] in data:
        return "ID already taken"
    reg.add(data['id_n'])
    return "OK"



if __name__ == '__main__':
    app.run(debug=True, port=5005, host="147.228.173.15")