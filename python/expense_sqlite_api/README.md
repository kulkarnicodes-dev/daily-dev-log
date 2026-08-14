# 💰 Expense Tracker REST API with SQLite

A database-backed **Expense Tracker REST API** built with **Python, Flask, and SQLite**.

This project is part of my **100 Days of Building in Public** challenge.

Unlike my previous in-memory APIs, this project introduces **persistent database storage**, allowing expense records to remain available after restarting the application.

---

## 🚀 Features

* ➕ Create an expense
* 📋 Get all expenses
* 🔎 Get expense by ID
* ✏️ Update an expense
* 🗑️ Delete an expense
* 🏷️ Filter expenses by category
* 📊 Calculate expense summary
* 💾 SQLite database storage
* ⚠️ Input validation
* ❌ Error handling
* 📦 JSON API responses

---

## 🛠️ Tech Stack

| Technology  | Purpose               |
| ----------- | --------------------- |
| 🐍 Python   | Programming language  |
| ⚡ Flask     | Web framework         |
| 🗄️ SQLite  | Database              |
| 🌐 REST API | Backend communication |
| 📦 JSON     | Data exchange         |

---

## 📂 Project Structure

```text
expense_sqlite_api/
│
├── app.py
├── expenses.db
└── README.md
```

> `expenses.db` is automatically created when the application starts.

---

# 🔗 API Endpoints

| Method   | Endpoint                            | Description         |
| -------- | ----------------------------------- | ------------------- |
| `GET`    | `/api/expenses`                     | Get all expenses    |
| `GET`    | `/api/expenses/<id>`                | Get expense by ID   |
| `POST`   | `/api/expenses`                     | Create an expense   |
| `PUT`    | `/api/expenses/<id>`                | Update an expense   |
| `DELETE` | `/api/expenses/<id>`                | Delete an expense   |
| `GET`    | `/api/expenses/summary`             | Get expense summary |
| `GET`    | `/api/expenses/category/<category>` | Filter by category  |

---

# 📋 Get All Expenses

### GET

```http
GET /api/expenses
```

### Example

```text
http://127.0.0.1:5000/api/expenses
```

### Example Response

```json
[
  {
    "id": 1,
    "title": "Coffee",
    "amount": 120.0,
    "category": "Food"
  },
  {
    "id": 2,
    "title": "Bus Ticket",
    "amount": 50.0,
    "category": "Travel"
  }
]
```

---

# 🔎 Get Expense by ID

### GET

```http
GET /api/expenses/<id>
```

### Example

```text
http://127.0.0.1:5000/api/expenses/1
```

### Response

```json
{
  "id": 1,
  "title": "Coffee",
  "amount": 120.0,
  "category": "Food"
}
```

### If the expense does not exist

```json
{
  "error": "Expense not found"
}
```

**Status Code:**

```text
404 Not Found
```

---

# ➕ Create Expense

### POST

```http
POST /api/expenses
```

### Example Request

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

**Status Code:**

```text
201 Created
```

---

# ✏️ Update Expense

### PUT

```http
PUT /api/expenses/<id>
```

### Example

```text
http://127.0.0.1:5000/api/expenses/1
```

### Request Body

```json
{
  "title": "Lunch",
  "amount": 250,
  "category": "Food"
}
```

### Example Response

```json
{
  "id": 1,
  "title": "Lunch",
  "amount": 250.0,
  "category": "Food"
}
```

---

# 🗑️ Delete Expense

### DELETE

```http
DELETE /api/expenses/<id>
```

### Example

```text
http://127.0.0.1:5000/api/expenses/2
```

### Response

```json
{
  "message": "Expense deleted successfully"
}
```

---

# 📊 Expense Summary

### GET

```http
GET /api/expenses/summary
```

Returns the total amount of all expenses and the number of expense records.

### Example Response

```json
{
  "total_expenses": 370.0,
  "number_of_expenses": 2
}
```

---

# 🏷️ Filter by Category

### GET

```http
GET /api/expenses/category/<category>
```

### Example

```text
http://127.0.0.1:5000/api/expenses/category/Food
```

Returns expenses belonging to the selected category.

The category search is **case-insensitive**.

For example:

```text
/api/expenses/category/Food
/api/expenses/category/food
/api/expenses/category/FOOD
```

will return the same category results.

---

# ⚙️ Run Locally

## 1. Navigate to the project

```bash
cd python/expense_sqlite_api
```

## 2. Install Flask

```bash
pip install flask
```

## 3. Run the application

```bash
python app.py
```

The API will be available at:

```text
http://127.0.0.1:5000
```

The SQLite database will automatically be created as:

```text
expenses.db
```

---

# 🧪 Testing

The API can be tested using:

* 🧪 Postman
* ⚡ Thunder Client
* 💻 cURL
* 🌐 Browser for GET requests

---

# 💻 Example cURL Requests

## Get Expenses

```bash
curl http://127.0.0.1:5000/api/expenses
```

## Create Expense

### Windows CMD

```cmd
curl -X POST http://127.0.0.1:5000/api/expenses ^
-H "Content-Type: application/json" ^
-d "{\"title\":\"Coffee\",\"amount\":120,\"category\":\"Food\"}"
```

### Linux / macOS / Git Bash

```bash
curl -X POST http://127.0.0.1:5000/api/expenses \
-H "Content-Type: application/json" \
-d '{"title":"Coffee","amount":120,"category":"Food"}'
```

## Get Summary

```bash
curl http://127.0.0.1:5000/api/expenses/summary
```

## Delete Expense

```bash
curl -X DELETE http://127.0.0.1:5000/api/expenses/1
```

---

# 🗄️ Database

This project uses **SQLite** for persistent data storage.

The application creates an `expenses` table:

```sql
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL
);
```

## Database Structure

| Column     | Type    | Description       |
| ---------- | ------- | ----------------- |
| `id`       | INTEGER | Unique expense ID |
| `title`    | TEXT    | Expense title     |
| `amount`   | REAL    | Expense amount    |
| `category` | TEXT    | Expense category  |

---

# 🔐 Input Validation

The API validates:

* ✅ Required title
* ✅ Required amount
* ✅ Required category
* ✅ Numeric expense amount
* ✅ Positive expense amount
* ✅ Existing expense ID

### Example Validation Response

```json
{
  "error": "amount must be greater than zero"
}
```

---

# 📚 Concepts Practiced

## Flask

* Flask application setup
* Routing
* Request handling
* JSON responses
* URL parameters

## REST API

* RESTful endpoint design
* HTTP methods
* CRUD operations
* HTTP status codes

## SQLite

* Database creation
* Table creation
* `INSERT` queries
* `SELECT` queries
* `UPDATE` queries
* `DELETE` queries
* SQL aggregation
* Parameterized SQL queries

## Python

* Functions
* Lists and dictionaries
* Exception handling
* Database connections
* Data processing

---

# 🔄 Request Flow

```text
Client
   ↓
HTTP Request
   ↓
Flask Route
   ↓
Input Validation
   ↓
SQLite Database
   ↓
SQL Query
   ↓
Process Result
   ↓
JSON Response
   ↓
Client
```

---

# 📈 What I Learned

The biggest improvement in this project was moving from **temporary in-memory data** to **persistent database storage**.

### Previously

```text
Python List
     ↓
    API
     ↓
   Data
```

Data stored in a Python list would be lost whenever the application restarted.

### Now

```text
API
 ↓
Flask
 ↓
SQLite
 ↓
Persistent Data
```

This means expense records are **not lost when the Flask application is restarted**.

---

# 🚀 Future Improvements

* 👤 Add user authentication
* 🔐 Add JWT authentication
* 📅 Add monthly expense reports
* 🕒 Add date and time tracking
* 📄 Add pagination
* ↕️ Add sorting
* 📊 Add advanced category analytics
* 🧪 Add automated tests
* 📖 Add Swagger/OpenAPI documentation
* ⚛️ Build a React frontend
* ☁️ Deploy the API
* 🗄️ Migrate from SQLite to MySQL/PostgreSQL

---

# ⭐ Project Goal

This project is part of my **100 Days of Building in Public** challenge.

The goal is to progressively improve my backend development skills by building practical projects and learning concepts such as:

* Python
* Flask
* REST APIs
* CRUD operations
* Databases
* SQL
* API validation
* Error handling
* Backend architecture
* Persistent data storage

---

## 👨‍💻 Author

Built as part of my **100 Days of Building in Public** journey.

> 🚀 Building. Learning. Improving. Every day.
