# Action Item Extractor

A FastAPI + SQLite application that converts free-form notes into enumerated action items. Supports both heuristic-based and LLM-powered extraction via Ollama.

## Project Structure

```
week2/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── db.py                # SQLite database layer
│   ├── schemas.py           # Pydantic request/response models
│   ├── routers/
│   │   ├── notes.py         # CRUD endpoints for notes
│   │   └── action_items.py  # Extraction & action-item endpoints
│   └── services/
│       └── extract.py       # Heuristic + LLM extraction logic
├── frontend/
│   └── index.html           # Single-page HTML/JS frontend
├── tests/
│   └── test_extract.py      # Unit tests for extraction functions
└── data/
    └── app.db               # SQLite database (auto-created)
```

## Setup

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (or pip)
- [Ollama](https://ollama.com/) installed and running locally

### Install Dependencies

```bash
uv sync
```

### Pull an Ollama Model

```bash
ollama pull llama3.2
```

### Run the Server

```bash
uv run uvicorn week2.app.main:app --reload
```

Then open http://127.0.0.1:8000/ in your browser.

## API Endpoints

### Notes

| Method | Path             | Description              |
|--------|------------------|--------------------------|
| POST   | `/notes`         | Create a new note        |
| GET    | `/notes`         | List all saved notes     |
| GET    | `/notes/{id}`    | Retrieve a single note   |

### Action Items

| Method | Path                            | Description                                  |
|--------|---------------------------------|----------------------------------------------|
| POST   | `/action-items/extract`         | Extract items using heuristic rules          |
| POST   | `/action-items/extract-llm`     | Extract items using LLM (Ollama)             |
| GET    | `/action-items`                 | List all action items (optional `?note_id=`) |
| POST   | `/action-items/{id}/done`       | Mark an action item as done/not done         |

## Running Tests

```bash
uv run pytest week2/tests/ -v
```
