from typing import Optional, Any

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
