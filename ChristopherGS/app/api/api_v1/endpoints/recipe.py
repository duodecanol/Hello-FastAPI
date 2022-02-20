from typing import Optional, Any
import httpx
import asyncio

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.recipe import (
    Recipe,
    RecipeCreate,
    RecipeSearchResults,
    RecipeUpdateRestricted,
)
from app.clients.reddit import RedditClient
from app.api import deps
from app import crud

router = APIRouter()
RECIPE_SUBREDDITS = ["recipes",
                     "easyrecipes",
                     "TopSecretRecipes",
                     "VegRecipes",
                     "cookingforbeginners",
                     "FoodPorn",
                     ]


@router.get("/{recipe_id}", status_code=200, response_model=Recipe)
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
    """
    recipes = crud.recipe.get_multi(db=db, limit=max_results)
    if not keyword:
        return {"results": recipes}

    # FIXME: keyword 필터를 먼저 하고 limit해야 하지 않은지??
    results = filter(lambda recipe: keyword.lower() in recipe.label.lower(), recipes)
    return {"results": list(results)[:max_results]}


@router.post("/", status_code=201, response_model=Recipe)
def create_recipe(
        *,
        recipe_in: RecipeCreate,
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_user)
) -> dict:
    """
    Create a new recipe in the database
    """
    if recipe_in.submitter_id != current_user.id:
        raise HTTPException(
            status_code=403, detail=f"You can only submit recipes as yourself"
        )
    recipe = crud.recipe.create(db=db, obj_in=recipe_in)

    return recipe


@router.put("/", status_code=201, response_model=Recipe)
def update_recipe(
        *,
        recipe_in: RecipeUpdateRestricted,
        db: Session = Depends(deps.get_db)
) -> dict:
    """Update recipe in the database"""
    recipe = crud.recipe.get(db, id=recipe_in.id)
    if not recipe:
        raise HTTPException(
            status_code=400, detail=f"Recipe with ID: {recipe_in.id} not found. Update Failure by unknown recipe id"
        )

    updated_recipe = crud.recipe.update(db=db, db_obj=recipe, obj_in=recipe_in)
    db.commit()
    return updated_recipe


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
def fetch_ideas(reddit_client: RedditClient = Depends(deps.get_reddit_client)) -> dict:
    return {
        key: reddit_client.get_reddit_top(subreddit=key) for key in RECIPE_SUBREDDITS
    }


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
