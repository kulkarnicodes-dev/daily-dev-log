# 📦 Product Inventory REST API

A practical **Product Inventory REST API** built with **Python, Flask, and SQLite**.

This project is part of my **100 Days of Building in Public** challenge.

**Day 10** focuses on combining REST API development, database CRUD operations, search, filtering, inventory calculations, and basic business logic.

---

## 🚀 Features

* ➕ Create products
* 📦 Get all products
* 🔎 Get product by ID
* ✏️ Update products
* 🗑️ Delete products
* 🔍 Search products
* 🏷️ Filter products by category
* ⚠️ Detect low-stock products
* 📊 Generate inventory summary
* 💾 SQLite database
* ✅ Input validation
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
inventory_api/
│
├── app.py
├── README.md
├── .gitignore
└── inventory.db
```

> `inventory.db` is generated automatically and is excluded from Git.

---

# 🔗 API Endpoints

| Method | Endpoint                            | Description            |
| ------ | ----------------------------------- | ---------------------- |
| GET    | `/api/products`                     | Get all products       |
| GET    | `/api/products/<id>`                | Get product by ID      |
| POST   | `/api/products`                     | Create a product       |
| PUT    | `/api/products/<id>`                | Update a product       |
| DELETE | `/api/products/<id>`                | Delete a product       |
| GET    | `/api/products/search?q=`           | Search products        |
| GET    | `/api/products/category/<category>` | Filter by category     |
| GET    | `/api/products/low-stock`           | Get low-stock products |
| GET    | `/api/products/summary`             | Get inventory summary  |

---

# ➕ Create Product

### POST

```text
/api/products
```

### Request

```json
{
    "name": "Wireless Mouse",
    "price": 799,
    "category": "Electronics",
    "stock": 15
}
```

### Response

```json
{
    "message": "Product created successfully",
    "product_id": 1,
    "product": {
        "name": "Wireless Mouse",
        "price": 799.0,
        "category": "Electronics",
        "stock": 15
    }
}
```

---

# 📦 Get All Products

### GET

```text
/api/products
```

### Example Response

```json
[
    {
        "id": 1,
        "name": "Wireless Mouse",
        "price": 799.0,
        "category": "Electronics",
        "stock": 15
    }
]
```

---

# 🔎 Get Product by ID

### GET

```text
/api/products/1
```

### Response

```json
{
    "id": 1,
    "name": "Wireless Mouse",
    "price": 799.0,
    "category": "Electronics",
    "stock": 15
}
```

---

# ✏️ Update Product

### PUT

```text
/api/products/1
```

### Request

```json
{
    "name": "Wireless Mouse Pro",
    "price": 999,
    "category": "Electronics",
    "stock": 20
}
```

### Response

```json
{
    "message": "Product updated successfully"
}
```

---

# 🗑️ Delete Product

### DELETE

```text
/api/products/1
```

### Response

```json
{
    "message": "Product deleted successfully"
}
```

---

# 🔍 Search Products

Search products by **name or category**.

### GET

```text
/api/products/search?q=mouse
```

### Example

```text
http://127.0.0.1:5000/api/products/search?q=mouse
```

---

# 🏷️ Filter by Category

### GET

```text
/api/products/category/Electronics
```

The API returns products belonging to the selected category.

---

# ⚠️ Low Stock Products

Products with fewer than **5 units** are considered low stock.

### GET

```text
/api/products/low-stock
```

### Example Response

```json
{
    "low_stock_limit": 5,
    "count": 2,
    "products": [
        {
            "id": 3,
            "name": "Keyboard",
            "price": 1200.0,
            "category": "Electronics",
            "stock": 2
        }
    ]
}
```

---

# 📊 Inventory Summary

### GET

```text
/api/products/summary
```

### Example Response

```json
{
    "total_products": 10,
    "total_stock": 125,
    "inventory_value": 87500.0,
    "low_stock_products": 3
}
```

The summary provides:

* Total number of products
* Total available stock
* Total inventory value
* Number of low-stock products

---

# ⚙️ Run Locally

## 1. Navigate to the project

```bash
cd python/inventory_api
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

---

# 🧪 Testing

The API can be tested using:

* Postman
* Thunder Client
* cURL
* Browser for GET requests

---

## 🧪 Recommended Testing Flow

### 1. Create products

```text
POST /api/products
```

### 2. View products

```text
GET /api/products
```

### 3. Search

```text
GET /api/products/search?q=mouse
```

### 4. Filter

```text
GET /api/products/category/Electronics
```

### 5. Check low stock

```text
GET /api/products/low-stock
```

### 6. Check summary

```text
GET /api/products/summary
```

### 7. Update

```text
PUT /api/products/1
```

### 8. Delete

```text
DELETE /api/products/1
```

---

# 🧠 Business Logic

This project introduces simple inventory business logic.

### Low Stock

```text
stock < 5
```

Products below this threshold are returned by:

```text
/api/products/low-stock
```

### Inventory Value

The inventory value is calculated using:

```text
price × stock
```

This value is then aggregated across all products.

---

# 📚 Concepts Practiced

### Python

* Functions
* Lists
* Dictionaries
* Exception handling
* Type conversion
* String operations

### Flask

* Routing
* HTTP methods
* URL parameters
* Query parameters
* JSON responses
* REST API design

### SQLite

* Database creation
* `INSERT`
* `SELECT`
* `UPDATE`
* `DELETE`
* Aggregate queries
* Parameterized queries

### Backend Development

* CRUD operations
* Search
* Filtering
* Validation
* Business logic
* Data aggregation
* HTTP status codes
* Error handling

---

# 🔄 Development Flow

```text
Product Data
     ↓
Input Validation
     ↓
Flask API
     ↓
SQLite Database
     ↓
Business Logic
     ↓
JSON Response
```

---

# 📈 Day 10 Progress

The backend development journey is gradually becoming more advanced:

```text
Day 7  → Authentication
   ↓
Day 8  → JWT Authentication
   ↓
Day 9  → Book CRUD + Search
   ↓
Day 10 → Inventory + Business Logic
```

Each project builds on concepts learned in previous days.

---

# 🚀 Future Improvements

* Add user authentication
* Add role-based access
* Add stock increase/decrease endpoints
* Add product images
* Add pagination
* Add advanced filtering
* Add automated tests
* Add API documentation
* Add React frontend
* Deploy the API

---

## 👨‍💻 Author

**Yash Kulkarni**

GitHub: [@kulkarnicodes-dev](https://github.com/kulkarnicodes-dev)

---

<p align="center">

### 📦 Day 10 / 100

**Learn • Build • Improve • Repeat**

</p>
