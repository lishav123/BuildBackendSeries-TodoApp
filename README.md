# BuildBackendSeries - TodoApp

Just different varieties for common and uncommon backend project, using Python and FastAPI.

This is a simple app 
- `main.app` - where routers and logics are there
- `database.py` - database connection details
- `model.py` - Mongo and Base models are defined
- `security.py` - hashing logic is present there

# How to use it in your system

- Step 1: Clone it via `git clone`
- Step 2: use `uv sync` command
- Step 3: create a `.env` file and define `JWT_SECRECT` and `MONGO_URI` of yours
- Step 4: execute `uv run uvicorn main:app --port 8000 --reload`

# For Readers

Suggestions are always welcome! Thank you!
