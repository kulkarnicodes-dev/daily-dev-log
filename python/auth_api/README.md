# 🔐 User Authentication REST API

A lightweight **User Authentication REST API** built with **Python, Flask, and SQLite**.

This project is part of my **100 Days of Building in Public** challenge.

The project introduces authentication concepts including user registration, secure password hashing, login validation, SQLite database storage, and basic user management.

---

## 🚀 Features

* 👤 User registration
* 🔐 Secure password hashing
* 🔑 User login
* 📋 Get all users
* 🔎 Get user by ID
* 🗑️ Delete user
* 💾 SQLite database
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
| 🔐 Werkzeug | Password hashing      |
| 🌐 REST API | Backend communication |
| 📦 JSON     | Data exchange         |

---

## 📂 Project Structure

```text
auth_api/
│
├── app.py
├── README.md
└── .gitignore
```

The `users.db` file is generated automatically when the application starts.

It is excluded from Git using `.gitignore`.

---

# 🔗 API Endpoints

| Method   | Endpoint          | Description         |
| -------- | ----------------- | ------------------- |
| `POST`   | `/api/register`   | Register a new user |
| `POST`   | `/api/login`      | Login user          |
| `GET`    | `/api/users`      | Get all users       |
| `GET`    | `/api/users/<id>` | Get user by ID      |
| `DELETE` | `/api/users/<id>` | Delete user         |

---

# 👤 User Registration

### POST

```http
POST /api/register
```

### Request Body

```json
{
  "username": "yash",
  "email": "yash@example.com",
  "password": "MyPassword123"
}
```

### Example Response

```json
{
  "message": "User registered successfully",
  "user_id": 1,
  "username": "yash",
  "email": "yash@example.com"
}
```

**Status Code:**

```text
201 Created
```

---

# 🔑 User Login

### POST

```http
POST /api/login
```

### Request Body

```json
{
  "email": "yash@example.com",
  "password": "MyPassword123"
}
```

### Example Response

```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "yash",
    "email": "yash@example.com"
  }
}
```

---

# 📋 Get All Users

### GET

```http
GET /api/users
```

### Example

```text
http://127.0.0.1:5000/api/users
```

### Example Response

```json
[
  {
    "id": 1,
    "username": "yash",
    "email": "yash@example.com"
  }
]
```

> Password hashes are never returned by this endpoint.

---

# 🔎 Get User by ID

### GET

```http
GET /api/users/<id>
```

### Example

```text
http://127.0.0.1:5000/api/users/1
```

### Response

```json
{
  "id": 1,
  "username": "yash",
  "email": "yash@example.com"
}
```

### User Not Found

```json
{
  "error": "User not found"
}
```

**Status Code:**

```text
404 Not Found
```

---

# 🗑️ Delete User

### DELETE

```http
DELETE /api/users/<id>
```

### Example

```text
http://127.0.0.1:5000/api/users/1
```

### Response

```json
{
  "message": "User deleted successfully"
}
```

---

# 🔐 Password Security

Passwords are **never stored as plain text**.

The application uses Werkzeug's password hashing functions.

### Creating a Password Hash

```python
generate_password_hash(password)
```

This function converts the user's password into a secure hash before storing it in the database.

### Verifying a Password

During login:

```python
check_password_hash(stored_hash, password)
```

is used to verify the entered password against the stored password hash.

### Authentication Flow

```text
User
  ↓
Registration
  ↓
Password
  ↓
Hash Password
  ↓
SQLite Database
```

During login:

```text
User
  ↓
Email + Password
  ↓
Find User
  ↓
Verify Password Hash
  ↓
Login Response
```

---

# ⚠️ Validation

The API validates:

* ✅ Username
* ✅ Email
* ✅ Password
* ✅ Minimum password length
* ✅ Duplicate username
* ✅ Duplicate email
* ✅ Existing user ID
* ✅ Invalid login credentials

### Example Validation Response

```json
{
  "error": "Password must contain at least 6 characters"
}
```

---

# ❌ Error Responses

## Missing Request Body

```json
{
  "error": "Request body is required"
}
```

**Status Code:**

```text
400 Bad Request
```

---

## Duplicate User

```json
{
  "error": "Username or email already exists"
}
```

**Status Code:**

```text
409 Conflict
```

---

## Invalid Login

```json
{
  "error": "Invalid email or password"
}
```

**Status Code:**

```text
401 Unauthorized
```

---

## User Not Found

```json
{
  "error": "User not found"
}
```

**Status Code:**

```text
404 Not Found
```

---

# 🗄️ Database

The project uses **SQLite** for persistent data storage.

The application automatically creates a `users` table:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
```

## Database Structure

| Column     | Type    | Description     |
| ---------- | ------- | --------------- |
| `id`       | INTEGER | Unique user ID  |
| `username` | TEXT    | Unique username |
| `email`    | TEXT    | Unique email    |
| `password` | TEXT    | Hashed password |

> The `password` column stores a password hash, not the user's original password.

---

# ⚙️ Run Locally

## 1. Navigate to the project

```bash
cd python/auth_api
```

## 2. Install Flask

```bash
pip install flask
```

Werkzeug is installed automatically as a Flask dependency.

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
users.db
```

---

# 🧪 Testing

You can test the API using:

* 🧪 Postman
* ⚡ Thunder Client
* 💻 cURL
* 🌐 Browser for GET requests

---

# 🔄 Example Testing Flow

## Step 1 — Register

### Request

```http
POST /api/register
```

### Body

```json
{
  "username": "yash",
  "email": "yash@example.com",
  "password": "MyPassword123"
}
```

---

## Step 2 — Login

### Request

```http
POST /api/login
```

### Body

```json
{
  "email": "yash@example.com",
  "password": "MyPassword123"
}
```

---

## Step 3 — View Users

```http
GET /api/users
```

---

## Step 4 — Get Specific User

```http
GET /api/users/1
```

---

## Step 5 — Delete User

```http
DELETE /api/users/1
```

---

# 📚 Concepts Practiced

## Flask

* Flask application setup
* Routing
* HTTP methods
* Request handling
* JSON responses

## Authentication

* User registration
* User login
* Password hashing
* Password verification
* Duplicate account prevention

## SQLite

* Database creation
* Table creation
* `INSERT`
* `SELECT`
* `DELETE`
* Unique constraints
* Parameterized SQL queries

## Security

* Password hashing
* Never returning passwords
* Generic invalid-login response
* Input validation

---

# 🔄 Authentication Flow

## REGISTER

```text
REGISTER
   │
   ▼
Receive User Data
   │
   ▼
Validate Input
   │
   ▼
Hash User Password
   │
   ▼
Save to SQLite
   │
   ▼
Registration Complete
```

## LOGIN

```text
LOGIN
   │
   ▼
Receive Credentials
   │
   ▼
Find User
   │
   ▼
Verify Password Hash
   │
   ├───────────────┐
   ▼               ▼
Valid            Invalid
   │               │
   ▼               ▼
Login Success     Error
```

---

# 📈 What I Learned

Day 7 introduced an important backend concept: **authentication**.

The project combines concepts learned during previous days:

```text
Python
  ↓
Flask
  ↓
REST API
  ↓
CRUD
  ↓
SQLite
  ↓
Password Hashing
  ↓
Authentication
```

This project helped me understand how a backend can securely handle user credentials without storing passwords in plain text.

---

# 🚀 Future Improvements

* 🔑 JWT authentication
* 🛡️ Protected routes
* 👤 User profile endpoint
* 🔄 Password reset
* 📧 Email verification
* 👥 Role-based access control
* 🚦 Login rate limiting
* 🧪 Automated tests
* 📖 API documentation
* ⚛️ React frontend
* ☁️ Production deployment

---

# ⭐ Project Goal

This project is part of my **100 Days of Building in Public** challenge.

The goal is to progressively improve my backend development skills by building practical projects and learning concepts such as:

* Python
* Flask
* REST APIs
* CRUD operations
* SQLite
* Authentication
* Password hashing
* API validation
* Error handling
* Backend security
* Database management

---

## 👨‍💻 Author

Built as part of my **100 Days of Building in Public** journey.

> 🚀 Building. Learning. Improving. Every day.
