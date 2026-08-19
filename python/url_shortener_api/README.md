# 🔗 URL Shortener REST API

A lightweight and practical **URL Shortener REST API** built with **Python, Flask, and SQLite**.

This project is part of my **100 Days of Building in Public** challenge.

The API accepts a long URL, generates a unique short code, stores the URL in a SQLite database, and redirects users from the short URL to the original destination.

---

## 🚀 Features

- 🔗 Shorten long URLs
- 🎲 Generate unique short codes
- 💾 Store URLs using SQLite
- ↩️ Redirect short URLs
- 📋 Get all shortened URLs
- 🔎 Get a URL by ID
- 🗑️ Delete shortened URLs
- ✅ URL validation
- ❌ Error handling
- 📦 JSON API responses
- 🔐 Secure random short-code generation

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| 🐍 Python | Programming language |
| ⚡ Flask | REST API framework |
| 🗄️ SQLite | Database |
| 🔗 REST API | Backend communication |
| 📦 JSON | Data exchange |

---

## 📂 Project Structure

```text
url_shortener_api/
│
├── app.py
├── README.md
├── .gitignore
└── urls.db