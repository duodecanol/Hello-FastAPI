from pathlib import Path

from fastapi import FastAPI, APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.api import deps
from app import crud
from app.api.api_v1.api import api_router
from app.core.config import settings

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

app = FastAPI(
    title="Recipe API", openapi_url="/openapi.json"
)

root_router = APIRouter()


@root_router.get("/", status_code=200)
def root(
        request: Request,
        db: Session = Depends(deps.get_db),
):
    """
    Root Get
    :return:
    """
    recipes = crud.recipe.get_multi(db=db, limit=10)
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "recipes": recipes}
    )


app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001, log_level="debug", reload=True)
