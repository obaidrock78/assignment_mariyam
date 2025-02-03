import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.payload_transformer.routes import router
from config.database import create_db_and_tables

app = FastAPI(
    title="Fast API Caching Service",
    version="1.0.0",
    description="This is a description of my API",
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# Redirect root ("/") to Swagger UI ("/docs")
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


app.include_router(router, prefix="/payload", tags=["Payload"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
