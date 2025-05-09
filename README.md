# 🧑‍💼 Employee Task Tracker
- Employee Task Tracker is a web application for managing employee tasks, built with Django, PostgreSQL, and Docker. It provides a RESTful API for creating, tracking, and managing tasks, including support for subtasks, assignment of performers, and deadlines.

## 🚀 Features
- Task management: create, update, delete, and view tasks.

- Task hierarchy support: create and manage subtasks.

- Task assignment: assign tasks to specific users.

- Status tracking: statuses include Created, Started, Done.

- Recommendations: API to suggest important tasks and suitable performers.

- Authentication: user registration and login.

- API documentation: available via Swagger and ReDoc.

## 🛠️ Technologies Used
- Backend: Django 4, Django REST Framework

- Database: PostgreSQL

- Authentication: JWT (Simple JWT)

- API Documentation: drf-yasg (Swagger / ReDoc)

- Testing: Pytest, Django TestCase

- Containerization: Docker, Docker Compose

- Environment Management: python-dotenv

## 📦 Installation & Setup
### 🔧 Prerequisites
- Python 3.11

- Docker & Docker Compose

- Git

## 📥 Clone the repository

- git clone https://github.com/Volodymyr-tech/employee_task_tracker.git
- cd employee_task_tracker
## ⚙️ Environment Configuration
- Create a .env file in the project root and add the following variables:

### env

- POSTGRES_DB= your db name
- POSTGRES_USER= your postgres user
- POSTGRES_PASSWORD= your password
- POSTGRES_HOST=db
- POSTGRES_PORT=5432
- SECRET_KEY=your_django_secret_key
- DEBUG=True
## 🐳 Run with Docker

- docker-compose up --build
- The app will be available at http://localhost

## 📚 API Documentation
- Swagger: http://localhost/swagger/

- ReDoc: http://localhost/redoc/

## 🧪 Running Tests
#### Test coverage is 84%
### if you want to run the tests:

- docker-compose exec web python manage.py test
