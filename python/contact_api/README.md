# 📇 Contact Management REST API

A lightweight **Contact Management REST API** built with **Python and Flask** for creating, retrieving, updating, deleting, and searching contacts.

This project is part of my **100 Days of Building in Public** challenge.

The project focuses on practicing **REST API development, CRUD operations, JSON handling, input validation, searching, error handling, and HTTP methods**.

---

## 🚀 Features

* 📋 Get all contacts
* 🔎 Get contact by ID
* ➕ Create a new contact
* ✏️ Update an existing contact
* 🗑️ Delete a contact
* 🔍 Search contacts by name
* 📦 JSON request and response handling
* ⚠️ Input validation
* ❌ Basic error handling
* 🌐 RESTful API endpoints

---

## 🛠️ Tech Stack

| Technology  | Purpose               |
| ----------- | --------------------- |
| 🐍 Python   | Programming language  |
| ⚡ Flask     | Web framework         |
| 🌐 REST API | Backend communication |
| 📦 JSON     | Data exchange format  |

---

## 📂 Project Structure

```text
contact_api/
│
├── app.py
└── README.md
```

---

# 🔗 API Endpoints

| Method   | Endpoint                      | Description       |
| -------- | ----------------------------- | ----------------- |
| `GET`    | `/api/contacts`               | Get all contacts  |
| `GET`    | `/api/contacts/<id>`          | Get contact by ID |
| `POST`   | `/api/contacts`               | Create a contact  |
| `PUT`    | `/api/contacts/<id>`          | Update a contact  |
| `DELETE` | `/api/contacts/<id>`          | Delete a contact  |
| `GET`    | `/api/contacts/search/<name>` | Search contacts   |

---

# 📋 Get All Contacts

### `GET`

```text
/api/contacts
```

Returns all contacts stored by the application.

### Example Request

```text
http://127.0.0.1:5000/api/contacts
```

### Example Response

```json
[
    {
        "id": 1,
        "name": "Yash Kulkarni",
        "email": "yash@example.com",
        "phone": "9876543210"
    },
    {
        "id": 2,
        "name": "Rahul Patil",
        "email": "rahul@example.com",
        "phone": "9876543211"
    }
]
```

---

# 🔎 Get Contact by ID

### `GET`

```text
/api/contacts/<id>
```

Returns a specific contact using its ID.

### Example

```text
/api/contacts/1
```

### Example Response

```json
{
    "id": 1,
    "name": "Yash Kulkarni",
    "email": "yash@example.com",
    "phone": "9876543210"
}
```

### Contact Not Found

```json
{
    "error": "Contact not found"
}
```

**Status:** `404 Not Found`

---

# ➕ Create Contact

### `POST`

```text
/api/contacts
```

Creates a new contact.

### Request Body

```json
{
    "name": "Amit Sharma",
    "email": "amit@example.com",
    "phone": "9876543212"
}
```

### Example Response

```json
{
    "id": 3,
    "name": "Amit Sharma",
    "email": "amit@example.com",
    "phone": "9876543212"
}
```

**Status:** `201 Created`

### Required Fields

| Field   | Type   | Required |
| ------- | ------ | -------- |
| `name`  | String | ✅        |
| `email` | String | ✅        |
| `phone` | String | ✅        |

---

# ✏️ Update Contact

### `PUT`

```text
/api/contacts/<id>
```

Updates an existing contact.

### Example

```text
/api/contacts/1
```

### Request Body

```json
{
    "name": "Yash Kulkarni Updated",
    "email": "yash.updated@example.com",
    "phone": "9999999999"
}
```

### Example Response

```json
{
    "id": 1,
    "name": "Yash Kulkarni Updated",
    "email": "yash.updated@example.com",
    "phone": "9999999999"
}
```

---

# 🗑️ Delete Contact

### `DELETE`

```text
/api/contacts/<id>
```

Deletes a contact using its ID.

### Example

```text
/api/contacts/2
```

### Example Response

```json
{
    "message": "Contact deleted successfully"
}
```

---

# 🔍 Search Contacts

### `GET`

```text
/api/contacts/search/<name>
```

Searches contacts using part or all of their name.

### Example

```text
/api/contacts/search/yash
```

### Example Response

```json
[
    {
        "id": 1,
        "name": "Yash Kulkarni",
        "email": "yash@example.com",
        "phone": "9876543210"
    }
]
```

The search is **case-insensitive**.

For example:

```text
yash
Yash
YASH
```

can all find the same contact.

---

# ⚙️ Run Locally

## 1. Clone the Repository

```bash
git clone https://github.com/kulkarnicodes-dev/daily-dev-log.git
```

## 2. Navigate to the Project

```bash
cd daily-dev-log/python/contact_api
```

## 3. Install Flask

```bash
pip install flask
```

## 4. Run the Application

```bash
python app.py
```

The API will be available at:

```text
http://127.0.0.1:5000
```

---

# 🧪 Testing the API

The API can be tested using:

* Postman
* Thunder Client
* cURL
* Browser for GET requests

### Example GET Request

```bash
curl http://127.0.0.1:5000/api/contacts
```

### Example POST Request

```bash
curl -X POST http://127.0.0.1:5000/api/contacts \
-H "Content-Type: application/json" \
-d "{\"name\":\"Amit Sharma\",\"email\":\"amit@example.com\",\"phone\":\"9876543212\"}"
```

---

# 📚 Concepts Practiced

This project helped me practice:

### Flask

* Flask application setup
* Routing
* URL parameters
* Request handling
* JSON responses

### REST API

* RESTful endpoint design
* HTTP methods
* Resource-based URLs
* API status codes

### CRUD Operations

* Create
* Read
* Update
* Delete

### Python

* Lists
* Dictionaries
* Functions
* List comprehensions
* Searching
* Data manipulation

### Validation

* Required field validation
* Request body validation
* Missing resource handling
* Error responses

---

# 🔄 CRUD Flow

```text
Create
  ↓
POST /api/contacts
  ↓
Read
  ↓
GET /api/contacts
  ↓
Update
  ↓
PUT /api/contacts/<id>
  ↓
Delete
  ↓
DELETE /api/contacts/<id>
```

---

# ⚠️ Error Handling

The API provides basic error responses for invalid operations.

### Missing Request Body

```json
{
    "error": "Request body is required"
}
```

**Status:** `400 Bad Request`

### Missing Required Fields

```json
{
    "error": "name, email and phone are required"
}
```

**Status:** `400 Bad Request`

### Contact Not Found

```json
{
    "error": "Contact not found"
}
```

**Status:** `404 Not Found`

---

# 🎯 Learning Outcome

This project helped me move beyond basic GET and POST operations and practice a more complete REST API workflow.

I practiced how a backend application can:

```text
Receive Request
      ↓
Validate Data
      ↓
Process Data
      ↓
Perform CRUD Operation
      ↓
Return JSON Response
```

The project also strengthened my understanding of how frontend applications and API clients communicate with backend services.

---

# 🚀 Future Improvements

* Add SQLite database
* Add MySQL database
* Add email validation
* Add phone number validation
* Add authentication
* Add user accounts
* Add pagination
* Add sorting
* Add automated tests
* Add API documentation
* Deploy the API online
* Build a React frontend

---

## ⭐ Project Purpose

This project is a practical backend development exercise created as part of my **100 Days of Building in Public** challenge.

It focuses on strengthening my fundamentals in **Python, Flask, REST API development, CRUD operations, validation, JSON handling, and backend development**.
