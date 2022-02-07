from ChristopherGS.app.crud.base import CRUDBase
from ChristopherGS.app.models.recipe import Recipe
from ChristopherGS.app.schemas.recipe import RecipeCreate, RecipeUpdate

class CRUDRecipe(CRUDBase[Recipe, RecipeCreate, RecipeUpdate]):
    ...

recipe = CRUDRecipe(Recipe)