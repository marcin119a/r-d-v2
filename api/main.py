from fastapi import FastAPI

from api.routes import localities, predict

app = FastAPI(title="Housing API")

app.include_router(predict.router)
app.include_router(localities.router)


@app.get("/")
def root():
    return {"message": "API do mieszkań w Łodzi"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
