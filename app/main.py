from fastapi import FastAPI, APIRouter

app = FastAPI(
    title="Recipe API", openapi_url="/openapi.json"
)

api_router = APIRouter()


@api_router.get("/", status_code=200)
async def root() -> dict:
    return {"message": "Hello world"}


app.include_router(api_router)
