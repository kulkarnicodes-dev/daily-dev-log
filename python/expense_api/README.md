# 💰 Expense Tracker REST API

A lightweight REST API built with **Python and Flask** for managing and analyzing expenses.

This project is part of my **100 Days of Building in Public** challenge and focuses on REST API development, JSON handling, validation, and basic data processing.

## 🚀 Features

- 📋 Get all expenses
- 🔎 Get an expense by ID
- ➕ Add a new expense
- 🗑️ Delete an expense
- 📊 Calculate total expenses
- 🏷️ Filter expenses by category
- 📦 JSON request and response handling
- ⚠️ Input validation
- ❌ Basic error handling

## 🛠️ Tech Stack

- Python
- Flask
- REST API
- JSON

## 📂 Project Structure

```text
expense_api/
│
├── app.py
└── README.md

## API Endpoint

| Method | Endpoint                            | Description         |
| ------ | ----------------------------------- | ------------------- |
| GET    | `/api/expenses`                     | Get all expenses    |
| GET    | `/api/expenses/<id>`                | Get expense by ID   |
| POST   | `/api/expenses`                     | Create an expense   |
| DELETE | `/api/expenses/<id>`                | Delete an expense   |
| GET    | `/api/expenses/summary`             | Get expense summary |
| GET    | `/api/expenses/category/<category>` | Filter by category  |
