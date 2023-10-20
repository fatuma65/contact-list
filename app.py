from flask import Flask, jsonify, request

#this is a module that generates unique id numbers
import uuid

app = Flask(__name__)

db = []

# an endpint for retrieving or getting the data.
@app.route('/contact')
def contact():
    return jsonify(db)

# creating a view that we can use to create a new contact in the server.
@app.route('/contact', methods = ['POST'])
def add_contact():
    add = request.get_json() 
    db.append(add) # the data add using json format is appended to our empty list
    id = uuid.uuid4() # a unique id is then created for every contact we add in the the list.
    uuid_from_add = uuid.uuid4()
    print(id)
    return {'id': id}, 200

# creating a view using the index to update or correct information in our contact list.
@app.route('/contact/<int:index>', methods = ['PUT'])
def update_contact(index):
    update = request.get_json()
    db[index] = update
    return jsonify(db[index])

# we can delete a contact in our list by specifying its index.
@app.route('/contact/<int:index>', methods = ['DELETE'])   
def delete_contact(index):
    db.pop(index)
    return 'The contact is sucessfully deleted', 200

app.run(debug=True)