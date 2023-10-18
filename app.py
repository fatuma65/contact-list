from flask import Flask, jsonify, request
import uuid
app = Flask(__name__)

db = []

@app.route('/contact')
def contact():
    return jsonify(db)

@app.route('/contact', methods = ['POST'])
def add_contact():
    add = request.get_json()
    db.append(add)
    id = uuid.uuid4()
    uuid_from_add = uuid.uuid4()
    print(id)
    return {'id': uuid_from_add}, 200

@app.route('/contact/<int:index>', methods = ['PUT'])
def update_contact(index):
    update = request.get_json()
    db[index] = update
    return jsonify(db[index])

@app.route('/contact/<int:index>', methods = ['DELETE'])   
def delete_contact(index):
    db.pop(index)
    return 'The contact is sucessfully deleted', 200

app.run(debug=True)