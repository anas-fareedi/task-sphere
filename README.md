# TaskSphere 🚀
TaskSphere is a modern and feature-rich RESTful API for a to-do application, built with Python and FastAPI. It provides a robust backend system for managing tasks, users, and authentication with a focus on performance and scalability.

## Features

User Authentication: Secure user registration and login using JWT tokens.

Password Security: Passwords are never stored in plaintext, thanks to passlib and bcrypt hashing.

Full CRUD Functionality: Create, Read, Update, and Delete operations for user-specific tasks.

Database Migrations: Seamless database schema management using Alembic.

API Rate Limiting: Protects the API from brute-force attacks and abuse.

Pagination: Efficiently handles large lists of tasks.

Automated API Documentation: Interactive API documentation is automatically generated with Swagger UI and ReDoc.

## Tech Stack

Backend: Python, FastAPI

Database: PostgreSQL

ORM: SQLAlchemy

Migrations: Alembic

Authentication: python-jose for JWT, passlib with bcrypt for hashing

Testing: Pytest

Web Server: Uvicorn

## API Documentation

Once the application is running, you can access the interactive API documentation at:
```
Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc
```

## ⚙️ Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

Python 3.10+

PostgreSQL

Git

### Installation & Setup

#### Clone the repository:
```
bash
git clone https://github.com/anas-fareedi/task-sphere.git
cd task-sphere
```

#### Create and activate a virtual environment:
```
bash
# For Windows
python -m venv venv
.\venv\Scripts\activate
```
#### nstall dependencies:

It is recommended to use uv for faster package installation.
```
bash
pip install uv
uv pip install -r requirements.txt
```

#### Configure Environment Variables:
Create a .env file in the project's root directory. Copy the contents of .env.example into it and fill in your specific configuration details, especially for the database connection and JWT secret key.
```
text
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=tasksphere_db
SECRET_KEY=your_very_secret_key
ALGORITHM=HS256
```
#### Run Database Migrations:
Make sure your PostgreSQL server is running and you have created the database specified in your .env file. Then, apply the migrations.
```
bash
alembic upgrade head
```
#### Run the Application:
Start the development server using Uvicorn.
```
bash
uvicorn main:app --reload
The API will be available at http://127.0.0.1:8000.
```
### 🤝 How to Contribute

Contributions are welcome! If you'd like to contribute to TaskSphere, please follow these steps:

Fork the repository.

Create a new branch (git checkout -b feature/YourFeature).

Make your changes and commit them (git commit -m 'Add some feature').

Push to the branch (git push origin feature/YourFeature).

Open a Pull Request.
