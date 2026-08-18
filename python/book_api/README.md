# 📚 Book Management REST API

A simple and practical **Book Management REST API** built with **Python, Flask, and SQLite**.

This project is part of my **100 Days of Building in Public** challenge.

**Day 9** focuses on practicing database-driven REST API development using CRUD operations, searching, filtering, validation, and SQLite.

---

## 🚀 Features

* 📖 Get all books
* 🔎 Get a book by ID
* ➕ Add a new book
* ✏️ Update book details
* 🗑️ Delete a book
* 🔍 Search books by title or author
* 🏷️ Filter books by category
* 💾 SQLite database
* ⚠️ Input validation
* ❌ Error handling
* 📦 JSON API responses

---

## 🛠️ Tech Stack

| Technology  | Purpose               |
| ----------- | --------------------- |
| 🐍 Python   | Programming language  |
| ⚡ Flask     | REST API framework    |
| 🗄️ SQLite  | Database              |
| 🌐 REST API | Backend communication |
| 📦 JSON     | Data exchange         |

---

## 📂 Project Structure

```text
book_api/
│
├── app.py
├── README.md
├── .gitignore
└── books.db
```

> `books.db` is generated automatically when the application starts and is excluded from Git.

---

## 🔗 API Endpoints

| Method | Endpoint                         | Description        |
| ------ | -------------------------------- | ------------------ |
| GET    | `/api/books`                     | Get all books      |
| GET    | `/api/books/<id>`                | Get book by ID     |
| POST   | `/api/books`                     | Create a new book  |
| PUT    | `/api/books/<id>`                | Update a book      |
| DELETE | `/api/books/<id>`                | Delete a book      |
| GET    | `/api/books/search?q=`           | Search books       |
| GET    | `/api/books/category/<category>` | Filter by category |

---

## ➕ Create a Book

### POST

```text
/api/books
```

### Example Request

```json
{
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "category": "Programming",
    "year": 2008
}
```

### Example Response

```json
{
    "message": "Book created successfully",
    "book_id": 1,
    "book": {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "category": "Programming",
        "year": 2008
    }
}
```

---

## 📖 Get All Books

### GET

```text
/api/books
```

### Example Response

```json
[
    {
        "id": 1,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "category": "Programming",
        "year": 2008
    }
]
```

---

## 🔎 Get Book by ID

### GET

```text
/api/books/1
```

### Example Response

```json
{
    "id": 1,
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "category": "Programming",
    "year": 2008
}
```

If the book does not exist:

```json
{
    "error": "Book not found"
}
```

---

## ✏️ Update a Book

### PUT

```text
/api/books/1
```

### Example Request

```json
{
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "category": "Software Development",
    "year": 2008
}
```

### Response

```json
{
    "message": "Book updated successfully"
}
```

---

## 🗑️ Delete a Book

### DELETE

```text
/api/books/1
```

### Response

```json
{
    "message": "Book deleted successfully"
}
```

---

## 🔍 Search Books

Books can be searched by **title or author**.

### GET

```text
/api/books/search?q=clean
```

### Example

```text
http://127.0.0.1:5000/api/books/search?q=clean
```

The API searches both:

* Book title
* Author name

---

## 🏷️ Filter by Category

### GET

```text
/api/books/category/Programming
```

### Example

```text
http://127.0.0.1:5000/api/books/category/Programming
```

The API returns books belonging to the selected category.

---

## 💾 Database

The application uses **SQLite** for persistent data storage.

The database contains a `books` table:

```sql
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    category TEXT NOT NULL,
    year INTEGER
);
```

### Database Fields

| Field      | Type    | Description      |
| ---------- | ------- | ---------------- |
| `id`       | INTEGER | Unique book ID   |
| `title`    | TEXT    | Book title       |
| `author`   | TEXT    | Book author      |
| `category` | TEXT    | Book category    |
| `year`     | INTEGER | Publication year |

---

## ⚙️ Run Locally

### 1. Navigate to the project

```bash
cd python/book_api
```

### 2. Install Flask

```bash
pip install flask
```

### 3. Run the application

```bash
python app.py
```

The API will be available at:

```text
http://127.0.0.1:5000
```

---

## 🧪 Testing

The API can be tested using:

* Postman
* Thunder Client
* cURL
* Browser for GET requests

---

## 🧪 Recommended Testing Flow

### 1. Create a book

```text
POST /api/books
```

### 2. Get all books

```text
GET /api/books
```

### 3. Get a specific book

```text
GET /api/books/1
```

### 4. Search books

```text
GET /api/books/search?q=clean
```

### 5. Filter books

```text
GET /api/books/category/Programming
```

### 6. Update a book

```text
PUT /api/books/1
```

### 7. Delete a book

```text
DELETE /api/books/1
```

---

## 📚 Concepts Practiced

### Python

* Functions
* Dictionaries
* Lists
* String operations
* Request handling

### Flask

* Routing
* HTTP methods
* URL parameters
* Query parameters
* JSON responses
* REST API design

### SQLite

* Database creation
* Table creation
* `INSERT`
* `SELECT`
* `UPDATE`
* `DELETE`
* Parameterized SQL queries

### API Development

* CRUD operations
* Search
* Filtering
* Input validation
* HTTP status codes
* Error handling

---

## 🔄 CRUD Flow

```text
CREATE
  ↓
POST /api/books
  ↓
SQLite
```

```text
READ
  ↓
GET /api/books
  ↓
SQLite
```

```text
UPDATE
  ↓
PUT /api/books/<id>
  ↓
SQLite
```

```text
DELETE
  ↓
DELETE /api/books/<id>
  ↓
SQLite
```

---

## 📈 Day 9 Progress

This project continues the backend development progression of the challenge:

```text
Day 7
Authentication
      ↓
Day 8
JWT Authentication
      ↓
Day 9
Database CRUD + Search
```

The focus is moving toward building APIs that are closer to **real-world backend applications**.

---

## 🚀 Future Improvements

* [ ] Add user authentication
* [ ] Connect books with users
* [ ] Add pagination
* [ ] Add book ratings
* [ ] Add publication date
* [ ] Add advanced search
* [ ] Add automated tests
* [ ] Add API documentation
* [ ] Deploy the API
* [ ] Build a React frontend

---

## 🎯 Learning Outcome

By completing this project, I practiced building a database-driven REST API with Flask and SQLite while implementing complete CRUD functionality, search, filtering, validation, and error handling.

This project provides a foundation for developing more advanced backend applications and full-stack systems.

---

## 👨‍💻 100 Days of Building in Public

**Day 9 — Book Management REST API**

> Building consistently, learning continuously, and improving one project at a time. 🚀

---
