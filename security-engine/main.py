from fastapi import FastAPI

from api.routes import router

app = FastAPI(
    title="API Sentinel Security Engine",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "API Sentinel Security Engine is running"}