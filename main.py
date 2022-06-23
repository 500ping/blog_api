from fastapi import FastAPI
import uvicorn

from blog.router import router

HOST = "localhost"
PORT = 8069

app = FastAPI()
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True, log_level="info")
