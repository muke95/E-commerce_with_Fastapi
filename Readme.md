# 🛒 FastAPI E-Commerce API

A fully functional **FastAPI** backend for an e-commerce platform, featuring:

- User authentication (signup, login, refresh token, profile update)
- Product management (CRUD with admin protection)
- Category management
- Cart management
- Pagination, search, and role-based access control
- Token-based authentication (JWT)

---

## 🚀 Features

- **FastAPI** for high performance APIs
- **SQLAlchemy ORM** for database operations
- **JWT authentication** for secure access
- **Role-based permissions** (User / Admin)
- **Pagination & Search** in all list APIs
- **Swagger UI** & **ReDoc** auto-generated documentation

---

## 📦 Tech Stack

- Python 3.10+
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- JWT (Python-Jose / PyJWT)
- PostgreSQL / MySQL / SQLite (configurable)

---

## 📂 Project Structure

.
├── main.py # Entry point of FastAPI app
├── routers/ # API route definitions
│ ├── user_routes.py
│ ├── product_routes.py
│ ├── category_routes.py
│ └── cart_routes.py
├── services/ # Business logic
│ ├── user_service.py
│ ├── product_service.py
│ ├── category_service.py
│ └── cart_service.py
├── models/ # SQLAlchemy models
├── schemas/ # Pydantic schemas
├── database.py # DB connection setup
├── auth/ # Authentication & JWT helpers
├── requirements.txt # Dependencies
└── README.md # Project documentation


---

## 🛠 Installation & Setup

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/fastapi-ecommerce.git
cd fastapi-ecommerce

2️⃣ Create Virtual Environment
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate

3️⃣ Install Dependencies
    pip install -r requirements.txt

4️⃣ Configure Environment
Create a .env file:

    db_username=mukesh
    db_password=Mukesh%4095
    db_hostname=127.0.0.1 
    db_port=3306
    db_name=ecom

▶️ Running the Server
   uvicorn main:app --reload
    Swagger Docs → http://127.0.0.1:8000/docs

    ReDoc Docs → http://127.0.0.1:8000/red

📌 API Overview
👤 Users
GET /users/ → List users (pagination, search, role filter)

POST /users/create → Create new user

POST /signup → Register user

POST /login → Login (get JWT tokens)

POST /refresh → Refresh access token

GET /account/ → Get logged-in user info

PUT /account/ → Edit logged-in user info

DELETE /users/{id} → Delete user

🛍 Products
GET /products/ → List products (pagination & search)

POST /products/ → Create product (admin only)

PUT /products/{id} → Update product

DELETE /products/{id} → Delete product

🏷 Categories
GET /categories/ → List categories (pagination & search)

GET /categories/{id} → Get category by ID

POST /categories/ → Create category (admin only)

PUT /categories/{id} → Update category

DELETE /categories/{id} → Delete category

🛒 Carts
GET /carts/ → List carts (requires login)

GET /carts/{id} → Get cart by ID

POST /carts/ → Add item to cart

PUT /carts/{id} → Update cart item

DELETE /carts/{id} → Remove item from cart



🔑 Authentication
This project uses JWT Bearer tokens.
After login, include the token in the Authorization header for protected endpoints:

http
Copy
Edit
Authorization: Bearer <your_token>

