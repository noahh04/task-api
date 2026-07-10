# Task API 

Small REST API built with FastAPI as a backend learning project.

## Technologies 

- Python
- FastAPI
- SQLModel
- SQLite
- Git
- Docker

## Features

- Create Tasks
- Read Tasks
- Update Tasks
- Delete Tasks
- Search for Tasks by specific properties
- automatic update of tasks' priority when priority changed 

## Run

```bash
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Open your browser:

```
http://127.0.0.1:8000/docs
```

to test the API using the Swagger UI.
