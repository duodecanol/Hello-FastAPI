from typing import Optional

from fastapi import FastAPI, APIRouter, HTTPException, Query

from recipe_data import RECIPES
from schemas import Recipe, RecipeCreate, RecipeSearchResults

app = FastAPI(
    title="Recipe API", openapi_url="/openapi.json"
)

api_router = APIRouter()


@api_router.get("/", status_code=200)
def root() -> dict:
    """
    Root Get
    :return:
    """
    return {"msg": "Hello World!"}


@api_router.get("/recipe/{recipe_id}", status_code=200)
def fetch_recipe(*, recipe_id: int) -> dict:
    """
    Fetch a single recipe by ID
    :param recipe_id:
    :return:
    """
    result = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if result:
        return result[0]
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@api_router.get("/search/", status_code=200, response_model=RecipeSearchResults)
def search_recipes(
        *,
        keyword: Optional[str] = Query(None, min_length=3, example="chicken"),
        max_results: Optional[int] = 10
) -> dict:
    """
    Search for recipes based on label keyword
    :param keyword:
    :param max_results:
    :return:
    """
    if not keyword:
        return {"results": RECIPES[:max_results]}

    results = filter(lambda recipe: keyword.lower() in recipe["label"].lower(), RECIPES)
    return {"results": list(results)[:max_results]}

@api_router.post("/recipe/", status_code=201, response_model=Recipe)
def create_recipe(*, recipe_in: RecipeCreate)->dict:
    """
    Create a new recipe (in memory only)
    :param recipe_in:
    :return:
    """
    new_entry_id = len(RECIPES) + 1
    recipe_entry = Recipe(
        id=new_entry_id,
        label=recipe_in.label,
        source=recipe_in.source,
        url=recipe_in.url,
    )
    RECIPES.append(recipe_entry.dict())

    return recipe_entry

app.include_router(api_router)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001, log_level="debug", reload=True)
