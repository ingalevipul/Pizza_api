# Pizza API

A modern, robust Pizza Delivery API built with FastAPI, SQLAlchemy, and JWT Authentication.

## 🚀 Features

- **User Authentication**: Secure signup and login using JWT (Access & Refresh tokens).
- **Order Management**: Create, view, update, and delete pizza orders.
- **Admin Controls**: Manage all orders and update order statuses.
- **Validation**: Strict data validation using Pydantic.
- **Database**: SQLAlchemy ORM with support for multiple databases (SQLite, PostgreSQL, etc.).

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Authentication**: [FastAPI-JWT-Auth](https://indominusbyte.github.io/fastapi-jwt-auth/)
- **Security**: [Werkzeug](https://werkzeug.palletsprojects.com/) (Password hashing)
- **Environment**: [python-dotenv](https://github.com/theskumar/python-dotenv)

## 📋 Prerequisites

- Python 3.8+
- Virtual environment (recommended)

## ⚙️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Pizza_api
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn sqlalchemy sqlalchemy_utils fastapi-jwt-auth pydantic python-dotenv werkzeug
   ```

4. **Environment Variables**:
   Create a `.env` file in the root directory and add:
   ```env
   DATABASE_URL=sqlite:///./pizza.db
   JWT_SECRET_KEY=your_secret_key_here
   ```

5. **Initialize Database**:
   ```bash
   python init_db.py
   ```

## 🔌 API Endpoints

### Authentication (`/auth`)
- `POST /auth/signup`: Register a new user.
- `POST /auth/login`: Login and receive access/refresh tokens.
- `GET /auth/refresh`: Refresh the access token.
- `GET /auth/`: Protected route test (Requires JWT).

### Orders (`/orders`)
- `POST /orders/order/`: Place a new order.
- `GET /orders/order/{order_id}/`: Get specific order details.
- `PUT /orders/order/update/{order_id}/`: Update an existing order.
- `DELETE /orders/order/delete/{order_id}/`: Cancel/Delete an order.
- `GET /orders/user/orders`: Get all orders for the current user.

### Admin Endpoints
- `PUT /orders/admin/order/status/{order_id}/`: Update the status of any order (Staff only).
- `GET /orders/admin/order/{user_id}`: Get all orders for a specific user (Staff only).

## 🗄️ Database Models

### User
- `id`: Primary Key
- `username`: Unique username
- `email`: Unique email
- `password`: Hashed password
- `is_active`: Boolean
- `is_staff`: Boolean (Admin access)

### Order
- `id`: Primary Key
- `quantity`: Integer
- `order_status`: (pending, in_progress, completed)
- `pizza_size`: (small, medium, large)
- `flavour`: String
- `user_id`: Foreign Key to User

## 🏃 Running the Application

Start the development server using uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.
You can access the interactive API documentation at `http://127.0.0.1:8000/docs`.
