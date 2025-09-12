
```markdown
# 📝 Todo API (FastAPI)

A simple **Todo API** built with [FastAPI](https://fastapi.tiangolo.com/).  
It supports **full CRUD operations**, **input validation with Pydantic**, **auto-generated documentation**, and a **logging middleware**.

---

## 🚀 Features
- Create, Read, Update, and Delete Todos
- Input validation using **Pydantic models**
- Auto-generated **Swagger** and **ReDoc** documentation
- Basic middleware for request logging
- In-memory "database" (dictionary) for simplicity

---

## 📂 Project Structure
```

todo\_api/
│── main.py          # Entry point (FastAPI app + routes)
│── models.py        # Pydantic models for validation
│── database.py      # Simulated in-memory database
│── middleware.py    # Request logging middleware
│── README.md        # Project documentation

````

---

## ⚙️ Setup & Installation

1. **Clone repo & enter project**
   ```bash
   git clone <your-repo-url>
   cd todo_api
````

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Mac/Linux
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install fastapi uvicorn pydantic
   ```

4. **Run server**

   ```bash
   uvicorn main:app --reload
   ```

---

## 📖 API Documentation

* Swagger UI 👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc 👉 [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

FastAPI auto-generates these docs from routes & Pydantic models.

---

## 🔑 Endpoints

| Method | Endpoint      | Description       |
| ------ | ------------- | ----------------- |
| POST   | `/todos/`     | Create a new todo |
| GET    | `/todos/`     | List all todos    |
| GET    | `/todos/{id}` | Get a todo by ID  |
| PUT    | `/todos/{id}` | Update a todo     |
| DELETE | `/todos/{id}` | Delete a todo     |

---

## 🧪 How to Test Functionality

### 1. CRUD Operations

#### Create a Todo

```bash
curl -X POST "http://127.0.0.1:8000/todos/" \
-H "Content-Type: application/json" \
-d '{"title": "Learn FastAPI", "description": "Build CRUD API", "completed": false}'
```

#### Get All Todos

```bash
curl -X GET "http://127.0.0.1:8000/todos/"
```

#### Get Todo by ID

```bash
curl -X GET "http://127.0.0.1:8000/todos/1"
```

#### Update Todo

```bash
curl -X PUT "http://127.0.0.1:8000/todos/1" \
-H "Content-Type: application/json" \
-d '{"title": "Learn FastAPI Updated", "completed": true}'
```

#### Delete Todo

```bash
curl -X DELETE "http://127.0.0.1:8000/todos/1"
```

---

### 2. Input Validation (Pydantic)

Try sending **invalid data**:

* Title too short:

```json
{"title": "Hi"}
```

❌ Response → `422 Unprocessable Entity`

* Wrong type for `completed`:

```json
{"title": "Test", "completed": "yes"}
```

❌ Response → Validation error: `"value could not be parsed to a boolean"`

---

### 3. Auto-Generated Documentation

* Go to 👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* Try endpoints directly in Swagger UI
* See models, request/response schemas, and error responses

---

### 4. Middleware Logging

Every request logs in terminal:

```
GET http://127.0.0.1:8000/todos/ completed_in=1.23ms status=200
POST http://127.0.0.1:8000/todos/ completed_in=3.45ms status=201
GET http://127.0.0.1:8000/todos/1 completed_in=0.98ms status=404
```

---

## ✅ Next Steps

* Replace in-memory DB with **SQLite + SQLAlchemy** for persistence
* Add authentication (JWT or OAuth2)
* Add unit tests with `pytest`

---

## 📌 Tech Stack

* [FastAPI](https://fastapi.tiangolo.com/)
* [Pydantic](https://docs.pydantic.dev/)
* [Uvicorn](https://www.uvicorn.org/)

---

## 👩‍💻 Author

Developed with ❤️ using FastAPI.

```

---

Would you like me to also add **ready-made sample requests** in Swagger (using Pydantic `example` fields), so that when someone opens `/docs`, the request body is already pre-filled for easier testing?
```
