import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from app.config.base_config import dotenv_path
from app.routes.router import v1_router

load_dotenv(dotenv_path)
web_app = FastAPI()
web_app.include_router(v1_router)

if __name__ == "__main__":
    uvicorn.run(web_app, host="0.0.0.0", log_level="info", port=8000)
