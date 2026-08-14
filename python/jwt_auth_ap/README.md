# 🔐 JWT Authentication REST API

A secure and lightweight **JWT Authentication REST API** built with **Python, Flask, SQLite, and JSON Web Tokens**.

This project is part of my **100 Days of Building in Public** challenge.

**Day 8** focuses on moving from basic authentication to **token-based authentication** using JWT.

---

## 🚀 Features

* 👤 User registration
* 🔐 Secure password hashing
* 🔑 User login
* 🎟️ JWT access token generation
* 🛡️ Protected profile endpoint
* 💾 SQLite database
* 📋 Get all users
* 🔎 Get user by ID
* 🗑️ Delete user
* ⚠️ Input validation
* ❌ JWT error handling
* 📦 JSON API responses

---

## 🛠️ Tech Stack

| Technology             | Purpose               |
| ---------------------- | --------------------- |
| 🐍 Python              | Programming language  |
| ⚡ Flask                | Web framework         |
| 🎟️ Flask-JWT-Extended | JWT authentication    |
| 🗄️ SQLite             | Database              |
| 🔐 Werkzeug            | Password hashing      |
| 🌐 REST API            | Backend communication |
| 📦 JSON                | Data exchange         |

---

# 📂 Project Structure

```text id="9d7p3c"
jwt_auth_api/
│
├── app.py
├── README.md
└── .gitignore
```

The `users.db` database is generated automatically when the application starts.

It is excluded from Git using `.gitignore`.

---

# 🔗 API Endpoints

| Method   | Endpoint          | Authentication | Description              |
| -------- | ----------------- | -------------- | ------------------------ |
| `POST`   | `/api/register`   | ❌              | Register a new user      |
| `POST`   | `/api/login`      | ❌              | Login and receive JWT    |
| `GET`    | `/api/profile`    | ✅              | Access protected profile |
| `GET`    | `/api/users`      | ❌              | Get all users            |
| `GET`    | `/api/users/<id>` | ❌              | Get user by ID           |
| `DELETE` | `/api/users/<id>` | ❌              | Delete a user            |

---

# 👤 Register User

### POST

```http id="q3m6fy"
POST /api/register
```

### Request

```json id="g2xj7x"
{
  "username": "yash",
  "email": "yash@example.com",
  "password": "MyPassword123"
}
```

### Response

```json id="zj5b4t"
{
  "message": "User registered successfully",
  "user_id": 1,
  "username": "yash",
  "email": "yash@example.com"
}
```

**Status Code:**

```text id="j3z6jz"
201 Created
```

---

# 🔑 Login

### POST

```http id="v9t7t3"
POST /api/login
```

### Request

```json id="v2q0de"
{
  "email": "yash@example.com",
  "password": "MyPassword123"
}
```

### Response

```json id="h7c4zv"
{
  "message": "Login successful",
  "access_token": "YOUR_JWT_TOKEN",
  "user": {
    "id": 1,
    "username": "yash",
    "email": "yash@example.com"
  }
}
```

The `access_token` should be used to access protected endpoints.

---

# 🛡️ Protected Profile

### GET

```http id="c8t8nd"
GET /api/profile
```

This endpoint requires a valid JWT access token.

### Authorization Header

```http id="t4l9rs"
Authorization: Bearer YOUR_JWT_TOKEN
```

### Example Response

```json id="1z7e4g"
{
  "message": "Protected profile accessed successfully",
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

```http id="9r8kqp"
GET /api/users
```

### Example

```text id="4w5jcg"
http://127.0.0.1:5000/api/users
```

### Example Response

```json id="d0h8rv"
[
  {
    "id": 1,
    "username": "yash",
    "email": "yash@example.com"
  }
]
```

> Passwords and password hashes are never returned.

---

# 🔎 Get User by ID

### GET

```http id="6akqpj"
GET /api/users/1
```

### Response

```json id="tq7r6d"
{
  "id": 1,
  "username": "yash",
  "email": "yash@example.com"
}
```

---

# 🗑️ Delete User

### DELETE

```http id="0b5p1n"
DELETE /api/users/1
```

### Response

```json id="3b9n4d"
{
  "message": "User deleted successfully"
}
```

---

# 🔐 How JWT Authentication Works

The authentication process works like this:

## Registration

```text id="k8ny9x"
User
  │
  ▼
Register
  │
  ▼
Hash Password
  │
  ▼
SQLite Database
```

## Login

```text id="k7lq5x"
User
  │
  ▼
Login
  │
  ▼
Verify Password
  │
  ▼
Generate JWT
  │
  ▼
Return Access Token
```

## Protected Resources

```text id="r3w0k7"
Client
  │
  ▼
JWT Token
  │
  ▼
Authorization Header
  │
  ▼
JWT Verification
  │
  ▼
Protected Endpoint
  │
  ▼
Response
```

---

# 🔒 Password Security

Passwords are **never stored as plain text**.

The application uses:

```python id="1h9x0c"
generate_password_hash(password)
```

to create a secure password hash.

During login:

```python id="x4w8hy"
check_password_hash(stored_hash, password)
```

is used to verify the password.

---

# 🎟️ JWT Authentication

The project uses **JSON Web Tokens (JWT)** for authentication.

After successful login, the API creates an access token:

```python id="v1f8pz"
access_token = create_access_token(
    identity=str(user["id"])
)
```

The client sends the token using:

```http id="t7v4bn"
Authorization: Bearer <token>
```

Protected routes use:

```python id="4m3q1s"
@jwt_required()
```

to verify the token.

---

# ⚠️ Validation

The API validates:

* ✅ Username
* ✅ Email
* ✅ Password
* ✅ Minimum password length
* ✅ Duplicate username
* ✅ Duplicate email
* ✅ User existence
* ✅ JWT authorization
* ✅ JWT expiration

---

# ❌ Error Handling

## Missing Token

```json id="g8t6km"
{
  "error": "Authorization token is required"
}
```

## Invalid Token

```json id="j9c2qz"
{
  "error": "Invalid authorization token"
}
```

## Expired Token

```json id="f4x7cw"
{
  "error": "Authorization token has expired"
}
```

## Invalid Login

```json id="z6m1vn"
{
  "error": "Invalid email or password"
}
```

---

# 🗄️ Database

SQLite is used for local persistent storage.

The application automatically creates:

```text id="k1h5nq"
users.db
```

with the following table:

```sql id="9x5qtw"
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

> The `password` column stores a password hash, not the original password.

---

# ⚙️ Run Locally

## 1. Navigate to the project

```bash id="w8j1rp"
cd python/jwt_auth_api
```

## 2. Install dependencies

```bash id="j7x5zq"
pip install flask flask-jwt-extended
```

## 3. Run the application

```bash id="f2w8c1"
python app.py
```

The API will be available at:

```text id="5x8m2q"
http://127.0.0.1:5000
```

---

# 🧪 Testing

Recommended tools:

* 🧪 Postman
* ⚡ Thunder Client
* 💻 cURL

---

# 🧪 Testing Workflow

## Step 1 — Register

```http id="6v8j0p"
POST /api/register
```

```json id="7k2w8s"
{
  "username": "yash",
  "email": "yash@example.com",
  "password": "MyPassword123"
}
```

---

## Step 2 — Login

```http id="q8f1nm"
POST /api/login
```

```json id="5t3m9c"
{
  "email": "yash@example.com",
  "password": "MyPassword123"
}
```

Copy the returned:

```text id="3v6q1a"
access_token
```

---

## Step 3 — Access Protected Route

```http id="x6m8r2"
GET /api/profile
```

Add the following authorization header:

```http id="7w3k9p"
Authorization: Bearer YOUR_ACCESS_TOKEN
```

---

## Step 4 — Test Users

```http id="v4q8m2"
GET /api/users
```

```http id="p5z7x1"
GET /api/users/1
```

---

# 📚 Concepts Practiced

## Python

* Functions
* Dictionaries
* Exception handling
* Modules

## Flask

* Routing
* HTTP methods
* Request handling
* JSON responses
* REST API structure

## SQLite

* Database creation
* SQL queries
* `INSERT`
* `SELECT`
* `DELETE`
* Unique constraints

## Authentication

* User registration
* Login
* Password hashing
* Password verification
* JWT generation
* JWT validation
* Protected routes

## Security

* Password hashing
* Token-based authentication
* Authorization headers
* JWT expiration
* Generic authentication errors

---

# 🔄 Authentication Flow

## REGISTER

```text id="h3y7z1"
REGISTER
   ↓
Validate Input
   ↓
Hash Password
   ↓
Save User
   ↓
Database
```

## LOGIN

```text id="q6n2v8"
LOGIN
   ↓
Find User
   ↓
Verify Password
   ↓
Generate JWT
   ↓
Return Token
```

## PROTECTED REQUEST

```text id="j8k4x2"
PROTECTED REQUEST
   ↓
Send JWT
   ↓
Verify Token
   ↓
Identify User
   ↓
Return Protected Data
```

---

# 📈 Day 8 Progress

This project builds directly on the concepts from previous days.

```text id="s3k8m2"
Day 1
Python Utility
    ↓
Day 2
Input Validation
    ↓
Day 3
REST API
    ↓
Day 4
Expense API
    ↓
Day 5
Contact API
    ↓
Day 6
SQLite
    ↓
Day 7
Authentication
    ↓
Day 8
JWT Authentication
```

---

# 🚀 Future Improvements

* 🔄 Refresh tokens
* 🚪 Logout / token revocation
* 👥 Role-based authorization
* 🔑 Password reset
* 📧 Email verification
* 🛡️ Protected user management
* 🚦 Rate limiting
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
* SQLite
* Authentication
* JWT
* Password hashing
* API security
* Protected routes
* Database management

---

## 👨‍💻 Author

Built as part of my **100 Days of Building in Public** journey.

> 🚀 Building. Learning. Improving. Every day.
