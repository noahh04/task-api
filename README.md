# Task API 

Small REST API built with FastAPI as a backend learning project.

## Overview

- Managing Tasks (CRUD)
- Automatic reordering of task priorities when creating, updating or deleting tasks
- Input validation and HTTP status code handling
- Automated API tests with pytest
- Documentation with Swagger/OpenAPI

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
- Search for Tasks by specific properties (title, priority)

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
