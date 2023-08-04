export  FASTAPI=resources.app:app
uvicorn app:app --host localhost --port 5000 --reload
