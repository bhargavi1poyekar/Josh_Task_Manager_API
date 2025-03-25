# Task Management API with Django & JWT

A RESTful API for managing tasks with user authentication powered by Django REST Framework and JWT.

## Sequence Diagram: 

[![Task-Manager-Sequence-Diagram.png](https://i.postimg.cc/d3Vy1bvF/Task-Manager-Sequence-Diagram.png)](https://postimg.cc/xJBCpFcp)

## Features

- User registration and authentication
- JWT token-based authentication
- Create tasks with descriptions
- Assign tasks to multiple users
- Retrieve tasks for specific users
- Secure endpoints with permission checks

## Installation

### Prerequisites
- Python 3.8+
- pip
- SQLite

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/bhargavi1poyekar/Josh_Task_Manager_API.git
   cd taskmanager
2. Create and activate virtual environments. 
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
3. Install dependencies.
    ```bash
    pip install -r requirements.txt
4. Set up environment variables:
    ```bash
    cp .env.example .env
    
    Edit .env with your settings:
    SECRET_KEY=your-secret-key-here
    DEBUG=True
    DATABASE_URL=sqlite:///db.sqlite3 
5. Run migrations
    ```bash
    python manage.py migrate

6. Run development server
    ```
    python manage.py runserver

## API Endpoints Structure

### Authentication Endpoints

| Endpoint                | Method | Description                          | Request Body                                                                 | Headers               |
|-------------------------|--------|--------------------------------------|------------------------------------------------------------------------------|-----------------------|
| `/api/v1/auth/register/`   | POST   | Register new user                    | `{username, email, password, password2, first_name, last_name, mobile}`     | `Content-Type: JSON` |
| `/api/v1/auth/login/`      | POST   | Obtain JWT tokens                   | `{username, password}`                                                      | `Content-Type: JSON` |
| `/api/v1/auth/refresh/`    | POST   | Refresh access token                 | `{refresh}`                                                                 | `Content-Type: JSON` |

### Task Endpoints

| Endpoint                      | Method | Description                          | Request Body                                                                 | Headers                           |
|-------------------------------|--------|--------------------------------------|------------------------------------------------------------------------------|-----------------------------------|
| `/api/v1/tasks/create/`          | POST   | Create new task                      | `{name, description, task_type}`                                            | `Authorization: Bearer <token>`   |
| `/api/v1/tasks/{id}/assign/`     | POST   | Assign task to users                 | `{user_ids: [id1, id2]}`                                                    | `Authorization: Bearer <token>`   |
| `/api/v1/users/{user_id}/tasks/` | GET    | Get tasks assigned to specific user  | -                                                                           | `Authorization: Bearer <token>`   |

## Request/Response Examples

### 1. Registration Request
```json
POST /api/auth/register/
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password2": "securepassword123",
    "first_name": "John",
    "last_name": "Doe",
    "mobile": "+1234567890"
}
```
### 2. Login Request
```json
POST /api/auth/login/
{
    "username": "john_doe",
    "password": "securepassword123"
}
```
### 3. Create Task Request
```json
POST /api/tasks/create/
{
    "name": "Complete project",
    "description": "Finish all pending tasks",
    "task_type": "W"
}
```
### 4. Assign Task Request
```json
POST /api/tasks/1/assign/
{
    "user_ids": [2, 3]
}
```
### 5. Get User Tasks Response
```json
GET /api/users/1/tasks/
[
    {
        "id": 1,
        "name": "Complete project",
        "description": "Finish all pending tasks",
        "status": "P",
        "assigned_users": [
            {"id": 1, "name": "John Doe"},
            {"id": 2, "name": "Jane Smith"}
        ]
    }
]


