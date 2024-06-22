
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status
from src.routes import contacts


app = FastAPI()

app.include_router(contacts.router, prefix='/api')

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)