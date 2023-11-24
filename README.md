# backend_python_FastAPI
Backend from scratch in python with FastAPI

# Install

## FastAPI
Framework
```bash
pip install "fastapi[all]"
```
## JWT
JSON Web Token
```bash
pip install "python-jose[cryptography]"
```
## PassLib
Python package to handle password hashes.
Recommended algorithm is "Bcrypt"
```bash
pip install "passlib[bcrypt]"
```
## Create SECRET_KEY
```bash
openssl rand -hex 32
```

## Server start
```bash
uvicorn main:app --reload
```

## Documentation

### Swagger
```bash
localhost:8000/docs
```
### Redocly
```bash
localhost:8000/redoc
```