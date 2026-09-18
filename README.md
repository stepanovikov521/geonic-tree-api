# Genealogic Tree API (Async)



This is a high-performance, asynchronous FastAPI application for managing and visualizing family trees. It supports user authentication (JWT), relative management, and tree visualization using Pyvis.



## 🚀 Features



* **Asynchronous Architecture**: Built with `FastAPI` and `SQLAlchemy` (asyncio) for maximum concurrency.

* **Authentication**: Secure JWT-based authentication for users.

* **Family Tree Management**: CRUD operations for relatives (parents, children, spouses).

* **Tree Visualization**: Automatic generation of interactive HTML family trees using `Pyvis`.

* **Robust Error Handling**: Centralized exception handling and structured logging.



## 🛠️ Tech Stack



* **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/)

* **Database ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) (Async mode)

* **Database**: SQLite (for local/dev) or PostgreSQL (via Docker)

* **Authentication**: JWT (JSON Web Tokens) with `passlib` (bcrypt)

* **Visualization**: [Pyvis](https://pyvis.readthedocs.io/)

* **Testing**: `pytest`, `httpx`, `pytest-asyncio`



## 📦 Installation & Local Setup



### Prerequisites

* Python 3.11+

* `pip` and `venv` (recommended)



### Steps



1. **Clone the repository:**

   ```bash

   git clone <repository_url>

   cd async

   ```



2. **Create and activate a virtual environment:**

   ```powershell

   # Windows

   python -m venv .venv

   .\.venv\Scripts\activate

   ```



3. **Install dependencies:**

   ```bash

   pip install -r requirements.txt

   ```



4. **Run migrations (if using Alembic):**

   ```bash

   alembic upgrade head

   ```



5. **Start the server:**

   ```bash

   uvicorn services.main_API_async:app --reload

   ```



The API will be available at `http://127.0.0.1:8000`.

Access the interactive Swagger documentation at `http://127.0.0.1:8000/docs`.



## 🐳 Running with Docker



Using Docker Compose is the easiest way to set up the application along with a PostgreSQL database.



1. **Build and start containers:**

   ```bash

   docker-compose up --build

   ```



2. The API will be available at `http://localhost:8000`.



## 🧪 Running Tests



The project uses `pytest` for unit and integration tests.



To run all tests (including async tests):

```bash

# Make sure you are in your virtual environment

python -m pytest

```



## 📂 Project Structure



* `api/`: API endpoints (routes)

* `core/`: Configuration, exceptions, and logging setup

* `db/`: Database connection and repository patterns

* `models/`: SQLAlchemy models

* `schemas/`: Pydantic schemas for request/response validation

* `services/`: Business logic and core services

* `tests/`: Test suites (Unit & Integration)



## 📝 API Documentation



Once the server is running, you can explore all available endpoints via Swagger UI:

- **Swagger UI**: `/docs`

- **ReDoc**: `/redoc` 

