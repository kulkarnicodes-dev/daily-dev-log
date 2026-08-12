# 💰 Expense Tracker REST API

A lightweight **Expense Tracker REST API** built with **Python and Flask** for creating, retrieving, deleting, filtering, and analyzing expense data.

This project is part of my **100 Days of Building in Public** challenge. It was built to practice backend development, REST API design, HTTP methods, JSON data handling, input validation, error handling, filtering, and basic data aggregation.

---

## 🚀 Features

* 📋 Get all expenses
* 🔎 Get an expense by ID
* ➕ Create a new expense
* 🗑️ Delete an expense
* 📊 Calculate total expenses
* 🔢 Count the number of expenses
* 🏷️ Filter expenses by category
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
expense_api/
│
├── app.py
└── README.md
```

---

# 🔗 API Endpoints

| Method | Endpoint                            | Description                 |
| ------ | ----------------------------------- | --------------------------- |
| GET    | `/api/expenses`                     | Get all expenses            |
| GET    | `/api/expenses/<id>`                | Get expense by ID           |
| POST   | `/api/expenses`                     | Create an expense           |
| DELETE | `/api/expenses/<id>`                | Delete an expense           |
| GET    | `/api/expenses/summary`             | Get expense summary         |
| GET    | `/api/expenses/category/<category>` | Filter expenses by category |

---

# 📋 Get All Expenses

### GET

```text
/api/expenses
```

Returns all available expenses.

### Example Request

```text
http://127.0.0.1:5000/api/expenses
```

### Example Response

```json
[
    {
        "id": 1,
        "title": "Lunch",
        "amount": 150,
        "category": "Food"
    },
    {
        "id": 2,
        "title": "Bus Ticket",
        "amount": 50,
        "category": "Transport"
    }
]
```

---

# 🔎 Get Expense by ID

### GET

```text
/api/expenses/<id>
```

Returns a specific expense using its ID.

### Example

```text
/api/expenses/1
```

### Example Response

```json
{
    "id": 1,
    "title": "Lunch",
    "amount": 150,
    "category": "Food"
}
```

### If the Expense Does Not Exist

```json
{
    "error": "Expense not found"
}
```

**HTTP Status:** `404 Not Found`

---

# ➕ Create Expense

### POST

```text
/api/expenses
```

Creates a new expense.

### Request Body

```json
{
    "title": "Coffee",
    "amount": 120,
    "category": "Food"
}
```

### Example Response

```json
{
    "id": 3,
    "title": "Coffee",
    "amount": 120.0,
    "category": "Food"
}
```

## Required Fields

| Field      | Type   | Required |
| ---------- | ------ | -------- |
| `title`    | String | ✅        |
| `amount`   | Number | ✅        |
| `category` | String | ✅        |

If required fields are missing, the API returns a validation error.

### Example

```json
{
    "error": "title, amount and category are required"
}
```

**HTTP Status:** `400 Bad Request`

---

# 🗑️ Delete Expense

### DELETE

```text
/api/expenses/<id>
```

Deletes an expense using its ID.

### Example

```text
/api/expenses/1
```

### Example Response

```json
{
    "message": "Expense deleted successfully"
}
```

### If the Expense Does Not Exist

```json
{
    "error": "Expense not found"
}
```

**HTTP Status:** `404 Not Found`

---

# 📊 Expense Summary

### GET

```text
/api/expenses/summary
```

Returns a summary of the stored expenses.

### Example Response

```json
{
    "total_expenses": 200,
    "number_of_expenses": 2
}
```

## Summary Includes

* Total amount spent
* Number of recorded expenses

This endpoint demonstrates basic data aggregation using Python.

---

# 🏷️ Filter by Category

### GET

```text
/api/expenses/category/<category>
```

Returns expenses belonging to a specific category.

### Example

```text
/api/expenses/category/Food
```

### Example Response

```json
[
    {
        "id": 1,
        "title": "Lunch",
        "amount": 150,
        "category": "Food"
    }
]
```

The category comparison is performed **without considering uppercase/lowercase differences**.

For example:

```text
Food
food
FOOD
```

can all match the same category.

---

# ⚙️ Run Locally

## 1. Clone the Repository

```bash
git clone https://github.com/kulkarnicodes-dev/daily-dev-log.git
```

## 2. Navigate to the Project

```bash
cd daily-dev-log/python/expense_api
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

## Example cURL Request

```bash
curl http://127.0.0.1:5000/api/expenses
```

## Create an Expense with cURL

```bash
curl -X POST http://127.0.0.1:5000/api/expenses \
-H "Content-Type: application/json" \
-d "{\"title\":\"Coffee\",\"amount\":120,\"category\":\"Food\"}"
```

---

# 📚 Concepts Practiced

This project helped me practice several backend development concepts.

## Flask

* Flask application setup
* Route creation
* URL parameters
* Request handling
* JSON responses

## REST API

* RESTful endpoint design
* HTTP methods
* Resource-based URLs
* API response codes

## Python

* Lists
* Dictionaries
* Functions
* List comprehensions
* `next()`
* Filtering
* Data aggregation

## Validation

* Required field validation
* Number validation
* Missing resource handling
* Error responses

## Data Processing

* Filtering expenses by category
* Calculating total expenses
* Counting records
* Searching by ID

---

# 📊 HTTP Methods Used

| Method | Purpose         |
| ------ | --------------- |
| GET    | Retrieve data   |
| POST   | Create new data |
| DELETE | Remove data     |

The project intentionally focuses on the fundamental HTTP methods needed to understand REST API development.

---

# ⚠️ Error Handling

The API provides basic error responses for invalid operations.

## Expense Not Found

```json
{
    "error": "Expense not found"
}
```

**HTTP Status:** `404 Not Found`

---

## Missing Request Body

```json
{
    "error": "Request body is required"
}
```

**HTTP Status:** `400 Bad Request`

---

## Missing Required Fields

```json
{
    "error": "title, amount and category are required"
}
```

**HTTP Status:** `400 Bad Request`

---

## Invalid Amount

```json
{
    "error": "amount must be a number"
}
```

**HTTP Status:** `400 Bad Request`

---

# 🎯 Learning Outcome

By building this project, I practiced how a backend application can expose functionality through REST API endpoints.

The project helped me understand the flow:

```text
Client
  ↓
HTTP Request
  ↓
Flask Route
  ↓
Request Processing
  ↓
Data Operation
  ↓
JSON Response
  ↓
Client
```

This provides a foundation for building larger backend applications and connecting APIs with frontend applications.

---

# 🚀 Future Improvements

The current version uses **in-memory data** for simplicity.

Possible future improvements include:

* Add SQLite database
* Add MySQL database
* Add PUT/PATCH functionality
* Add expense update functionality
* Add authentication
* Add user accounts
* Add expense dates
* Add monthly expense reports
* Add spending statistics
* Add automated tests
* Add API documentation
* Deploy the API online
* Connect a React frontend

---

## ⭐ Project Purpose

This project is a practical backend development exercise created as part of my **100 Days of Building in Public** challenge.

It focuses on building a simple but functional REST API while strengthening fundamental skills in **Python, Flask, REST architecture, API design, validation, error handling, and data processing**.
