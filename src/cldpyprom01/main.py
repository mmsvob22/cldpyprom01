import uvicorn
from fastapi import FastAPI

from .database import init_db
from .router import router

app = FastAPI(
    title="cldpyprom01 Resource API",
    description="CRUD REST API over SQLite — Resource table",
    version="0.1.0",
)

app.include_router(router)


@app.on_event("startup")
def startup():
    init_db()


if __name__ == "__main__":
    uvicorn.run("cldpyprom01.main:app", host="0.0.0.0", port=8000, reload=True)
