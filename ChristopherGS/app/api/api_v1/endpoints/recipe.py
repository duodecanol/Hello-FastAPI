from typing import Optional, Any
import httpx
import asyncio

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session

from app.schemas.recipe import Recipe, RecipeCreate, RecipeSearchResults
from app.api import deps
from app import crud

router = APIRouter()

@router.get("/recipe/{recipe_id}", status_code=200, response_model=Recipe)
def fetch_recipe(
        *,
        recipe_id: int,
        db: Session = Depends(deps.get_db)
) -> Any:
    """
    Fetch a single recipe by ID
    :param recipe_id:
    :return:
    """
    result = crud.recipe.get(db=db, id=recipe_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Recipe with ID {recipe_id}  not found")
    return result


@router.get("/search/", status_code=200, response_model=RecipeSearchResults)
def search_recipes(
        *,
        keyword: Optional[str] = Query(None, min_length=3, example="chicken"),
        max_results: Optional[int] = 10,
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Search for recipes based on label keyword
    :param keyword:
    :param max_results:
    :return:
    """
    recipes = crud.recipe.get_multi(db=db, limit=max_results)
    if not keyword:
        return {"results": recipes}

    # FIXME: keyword 필터를 먼저 하고 limit해야 하지 않은지??
    results = filter(lambda recipe: keyword.lower() in recipe.label.lower(), recipes)
    return {"results": list(results)[:max_results]}


@router.post("/recipe/", status_code=201, response_model=Recipe)
def create_recipe(*, recipe_in: RecipeCreate, db: Session = Depends(deps.get_db)) -> dict:
    """
    Create a new recipe (in memory only)
    :param recipe_in:
    :return:
    """
    recipe = crud.recipe.create(db=db, obj_in=recipe_in)
    return recipe

def get_reddit_top(subreddit: str, data: dict) -> None:
    response = httpx.get(
        f"https://www.reddit.com/r/{subreddit}/top.json?sort=top&t=day&limit=5",
        headers={"User-agent": "recipe bot 0.1"},
    )
    subreddit_recipes = response.json()
    # print("==================================")
    # print(subreddit_recipes)
    subreddit_data = []
    for entry in subreddit_recipes["data"]["children"]:
        score = entry["data"]["score"]
        title = entry["data"]["title"]
        link = entry["data"]["url"]
        subreddit_data.append(f"{str(score)}: {title} ({link})")
    data[subreddit] = subreddit_data

@router.get("/ideas/")
def fetch_ideas() -> dict:
    data: dict = {}
    get_reddit_top("recipes", data)
    get_reddit_top("easyrecipes", data)
    get_reddit_top("TopSecretRecipes", data)
    get_reddit_top("VegRecipes", data)
    get_reddit_top("cookingforbeginners", data)
    get_reddit_top("FoodPorn", data)

    return data

async def get_reddit_top_async(subreddit: str, data: dict) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://www.reddit.com/r/{subreddit}/top.json?sort=top&t=day&limit=5",
            headers={"User-agent": "recipe bot 0.1"},
        )
    subreddit_recipes = response.json()
    subreddit_data = []
    for entry in subreddit_recipes["data"]["children"]:
        score = entry["data"]["score"]
        title = entry["data"]["title"]
        link = entry["data"]["url"]
        subreddit_data.append(f"{str(score)}: {title} ({link})")
    data[subreddit] = subreddit_data

@router.get("/ideas/async")
async def fetch_ideas_async() -> dict:
    data: dict = {}

    await asyncio.gather(
        get_reddit_top_async("recipes", data),
        get_reddit_top_async("easyrecipes", data),
        get_reddit_top_async("TopSecretRecipes", data),
        get_reddit_top_async("VegRecipes", data),
        get_reddit_top_async("cookingforbeginners", data),
        get_reddit_top_async("FoodPorn", data),
    )

    return data