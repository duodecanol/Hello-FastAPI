from fastapi import FastAPI, APIRouter, HTTPException

# 1
RECIPES = [
    {
        "id": 1,
        "label": "Chicken Vesuvio",
        "source": "Serious Eats",
        "url": "http://www.seriouseats.com/recipes/2011/12/chicken-vesuvio-recipe.html",
    },
    {
        "id": 2,
        "label": "Chicken Paprikash",
        "source": "No Recipes",
        "url": "http://norecipes.com/recipe/chicken-paprikash/",
    },
    {
        "id": 3,
        "label": "Cauliflower and Tofu Curry Recipe",
        "source": "Serious Eats",
        "url": "http://www.seriouseats.com/recipes/2011/02/cauliflower-and-tofu-curry-recipe.html",
    },
]

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


# 2 - New addition, path parameter
@api_router.get("/recipe/{recipe_id}", status_code=200)
def fetch_recipe(*, recipe_id: int) -> dict:  # 3
    """
    Fetch a single recipe by ID
    :param recipe_id:
    :return:
    """
    # 4
    result = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if result:
        return result[0]
    else:
        raise HTTPException(status_code=404, detail="Item not found")


app.include_router(api_router)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001, log_level="debug", reload=True)
