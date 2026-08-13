from flask import Flask, request, jsonify

app = Flask(__name__)

contacts = [
    {
        "id": 1,
        "name": "Yash Kulkarni",
        "email": "yash@example.com",
        "phone": "9876543210"
    },
    {
        "id": 2,
        "name": "Lalit Jagdale",
        "email": "Lalit@example.com",
        "phone": "9876543211"
    }
]


# Get all contacts
@app.route("/api/contacts", methods=["GET"])
def get_contacts():
    return jsonify(contacts)


# Get contact by ID
@app.route("/api/contacts/<int:contact_id>", methods=["GET"])
def get_contact(contact_id):
    contact = next(
        (contact for contact in contacts if contact["id"] == contact_id),
        None
    )

    if contact is None:
        return jsonify({"error": "Contact not found"}), 404

    return jsonify(contact)


# Create a new contact
@app.route("/api/contacts", methods=["POST"])
def create_contact():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")

    if not name or not email or not phone:
        return jsonify({
            "error": "name, email and phone are required"
        }), 400

    new_contact = {
        "id": max([contact["id"] for contact in contacts], default=0) + 1,
        "name": name,
        "email": email,
        "phone": phone
    }

    contacts.append(new_contact)

    return jsonify(new_contact), 201


# Update an existing contact
@app.route("/api/contacts/<int:contact_id>", methods=["PUT"])
def update_contact(contact_id):
    contact = next(
        (contact for contact in contacts if contact["id"] == contact_id),
        None
    )

    if contact is None:
        return jsonify({"error": "Contact not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")

    if not name or not email or not phone:
        return jsonify({
            "error": "name, email and phone are required"
        }), 400

    contact["name"] = name
    contact["email"] = email
    contact["phone"] = phone

    return jsonify(contact)


# Delete a contact
@app.route("/api/contacts/<int:contact_id>", methods=["DELETE"])
def delete_contact(contact_id):
    contact = next(
        (contact for contact in contacts if contact["id"] == contact_id),
        None
    )

    if contact is None:
        return jsonify({"error": "Contact not found"}), 404

    contacts.remove(contact)

    return jsonify({
        "message": "Contact deleted successfully"
    })


# Search contacts by name
@app.route("/api/contacts/search/<string:name>", methods=["GET"])
def search_contacts(name):
    results = [
        contact
        for contact in contacts
        if name.lower() in contact["name"].lower()
    ]

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)