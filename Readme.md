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
    python manage.py runsslserver

7. Run tests:
    ```
    python manage.py test tests
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
curl -k -X POST \
  https://localhost:8000/api/v1/auth/register/ \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "bhargavi_poyekar",
    "email": "bhargavi_poy@example.com",
    "password": "securepassword123",
    "password2": "securepassword123",
    "first_name": "Bhargavi",
    "last_name": "Poyekar",
    "mobile": "+1234567892"
  }'
```
If a user with the given username, email or mobile already exists, it would give a 400 Bad request error, since duplicates are not allowed. If you are trying to register a users, again with the same request, change these 3 fields. 

Note: -k disables SSL certificate verification. 

### Registration response:

![Register_Response](Response_images/user_register_response.png)

### 2. Login Request
```json
curl -k -X POST \
  https://localhost:8000/api/v1/auth/login/ \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "bhargavi_poyekar",
    "password": "securepassword123"
  }'
```
### Login Response:

![login_response](Response_images/user_login_response.png)
![alt text](image.png)
### 3. Create Task Request
```json
curl -k -X POST \
  https://localhost:8000/api/v1/tasks/create/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyOTI5MTk3LCJpYXQiOjE3NDI5MjU1OTcsImp0aSI6IjEwMTczMWQyNzM1NDQwZWRhNGMwM2JmYWI3NDJmM2EzIiwidXNlcl9pZCI6MywibmFtZSI6IkJoYXJnYXZpIFBveWVrYXIiLCJlbWFpbCI6ImJoYWdyYXZpQGV4YW1wbGUuY29tIiwibW9iaWxlIjoiKzExMjM0NTY3ODkwIn0.xf_1IFXE3zancOFSNnkoFBPNhQttPsk-mikG3nytSSw' \
  -d '{
    "name": "Task Manager API",
    "description": "Complete Josh Talks Assessment.",
    "task_type": "W"
  }'
```
You can use this hardcoded token, if it hasn't expired (Only for this assessment purpose.) If it has expired, you can just copy paste the access token from previous response of login. 

### Create Task Response:

![alt text](Response_images/task_creation_response.png)

### 4. Assign Task Request
```json
curl -k -X POST \
  https://localhost:8000/api/v1/tasks/1/assign/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyOTI5MTk3LCJpYXQiOjE3NDI5MjU1OTcsImp0aSI6IjEwMTczMWQyNzM1NDQwZWRhNGMwM2JmYWI3NDJmM2EzIiwidXNlcl9pZCI6MywibmFtZSI6IkJoYXJnYXZpIFBveWVrYXIiLCJlbWFpbCI6ImJoYWdyYXZpQGV4YW1wbGUuY29tIiwibW9iaWxlIjoiKzExMjM0NTY3ODkwIn0.xf_1IFXE3zancOFSNnkoFBPNhQttPsk-mikG3nytSSw' \
  -d '{
    "user_ids": [2, 3]
  }'
```
### Assign Task Response

![Task Assign response](Response_images/task_assign_response.png)

### 5. Get User Tasks Response
```json
curl -k -X GET \
  https://localhost:8000/api/v1/users/2/tasks/ \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyOTI5MTk3LCJpYXQiOjE3NDI5MjU1OTcsImp0aSI6IjEwMTczMWQyNzM1NDQwZWRhNGMwM2JmYWI3NDJmM2EzIiwidXNlcl9pZCI6MywibmFtZSI6IkJoYXJnYXZpIFBveWVrYXIiLCJlbWFpbCI6ImJoYWdyYXZpQGV4YW1wbGUuY29tIiwibW9iaWxlIjoiKzExMjM0NTY3ODkwIn0.xf_1IFXE3zancOFSNnkoFBPNhQttPsk-mikG3nytSSw' 

```
### Get User Tasks Response:

![Get User Tasks Response](Response_images/get_user_tasks_response.png)
