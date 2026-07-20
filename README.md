# AcousticSpace — Backend (Member 3)

FastAPI backend for the Deepfake Detection via RIR project. Serves the
ML model, handles authentication, and stores prediction history.

## Setup

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

- API: http://127.0.0.1:8000
- Swagger docs: http://127.0.0.1:8000/docs

## Project Structure

```
backend/
  main.py              # App entry point, CORS, router registration
  database.py           # DB connection (SQLite for dev)
  models.py              # SQLAlchemy ORM models (User, Prediction)
  schemas.py              # Pydantic request/response schemas
  auth.py                  # JWT + password hashing utilities
  routers/
    auth_router.py          # /auth/signup, /auth/login
    predict.py                # /predict (currently using MOCK prediction)
    history.py                  # /history, /history/{id}
```

## ⚠️ Current Status: Mock Prediction

`routers/predict.py` currently uses `mock_predict()` — a placeholder that
returns random real/fake predictions. This lets the full API (auth, file
upload, DB storage, history) be built and tested without waiting for
Member 2's trained model.

**When Member 2's `model.pt` is ready:** replace `mock_predict()` in
`routers/predict.py` with the real inference function (template is
already written in a comment inside that file).

## API Endpoints

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| GET | `/health` | No | Health check |
| POST | `/auth/signup` | No | Register new user |
| POST | `/auth/login` | No | Login, returns JWT token |
| POST | `/predict/` | Yes | Upload audio, get prediction |
| GET | `/history/` | Yes | Get all past predictions |
| GET | `/history/{id}` | Yes | Get specific prediction |

## Docker

```bash
docker build -t acousticspace-backend .
docker run -p 8000:8000 acousticspace-backend
```

## Dependencies

- **Blocked on Member 2**: Real model integration in `/predict`
- **Parallel with Member 4**: API contract (request/response formats) — coordinate on CORS origins in `main.py`
