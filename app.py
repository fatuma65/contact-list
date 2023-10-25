from flask import Flask, jsonify, request

#this is a module that generates unique id numbers
import uuid
import json

app = Flask(__name__)
db = []

# an endpint for retrieving or getting the data.
@app.route('/contact', methods = ['GET'])
def contact():
    return jsonify(db)

# creating a view that we can use to create a new contact in the server.
@app.route('/contact', methods = ['POST'])
def add_contact():
    data = json.loads(request.data)
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    phone_number = data.get('phone_number')

    if not first_name:
        return {"error": "first name is required"}, 400
    if len(first_name) < 3:
        return {"error": "first name must be atleast 3 characters"}, 400
    
    if not last_name:
        return {"error": "last name is required"}, 400
    if len(last_name) < 3:
        return {"error": "last name must have atleast 3 characters"}, 400
    
    if not phone_number :
        return {"error": "phone number is required"}, 400
    if len(phone_number) < 10:
        return {"error": "phone number must be atleast 10 characters"}, 400
   
    for index, number in enumerate(db):
        if number["phone_number"] == phone_number:
            return {"error": "phone number already exists in list"}

    new = {
        "first_name":  first_name,
        "last_name": last_name,
        "phone_number": phone_number,
        "id": str(uuid.uuid4())
    } 

    db.append(new) 

    response = {}
    response['message'] = 'Contact successfully added'
    response['data'] = new
    return response, 201

# # creating a view using the index to update or correct information in our contact list.
@app.route('/contact/<contact_id>', methods = ['PUT'])
def update_contact(contact_id):

    if not db:
        return {"Error": "Contact list is empty"}, 404

    db_contact = next((item for item in db if item['id'] == contact_id), None)
    if not db_contact:
        return {"Error": "Contact not found"}, 404
    
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    phone_number = data.get('phone_number')

    if not first_name:
        if len(first_name) < 3:
            return {"Error": "First name must be atleast 3 characters"}, 400
    else:
        first_name = db_contact["first_name"]

    if last_name:
        if len(last_name) < 3:
            return {"Error": "Last name must be atleast 3 characters"}, 400
    else:
        last_name = db_contact["last_name"]

    if phone_number:
        if len(phone_number) < 3:
            return {"Error": "Phone number must be atleast 10 characters"}, 400
    else:
        phone_number = db_contact["phone number"]

    new_contact = {
        "first_name": first_name,
        "last_name": last_name,
        "phone_number": phone_number,
        "id": db_contact['id']
    }
    for index, contact in enumerate(db):
        if contact['id'] == contact_id:
            db[index] = new_contact
    
    return {"message": "Contact has been updated", "data": new_contact}, 200

# returning an existing single contact using id
@app.route('/contact/<contact_id>', methods=['GET'])
def single_contact(contact_id):

    if db is None:
        {"error":"contact list is empty"}, 404
    
    db_contacts = next((x for x in db if x['id'] == contact_id), None)
    if not db_contacts:
        return {"error": "contact not found"}, 404

    return db_contacts

# we can delete a contact in our list by specifying its index.
@app.route('/contact/<contact_id>', methods = ['DELETE'])   
def delete_contact(contact_id):
    
    if not db:
        return {"error": "Contact list is empty"}, 404
    
    database = next((name for name in db if name['id'] == contact_id), None)
    if not database:
        return {"error": "contact id not found"}, 404
    
    for index, contact in enumerate(db):
        if contact['id'] == contact_id:
            db.pop(index)
    
    return {"message": "contact successfully deleted"}, 200
    
app.run(debug=True)