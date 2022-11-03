from fastapi import FastAPI, APIRouter

from typing import Optional

app = FastAPI(
    title="Recipe API", openapi_url="/openapi.json"
)

api_router = APIRouter()

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


@api_router.get("/", status_code=200)
async def root() -> dict:
    return {"message": "deployment ready"}


@api_router.get("/recipe/{recipe_id}", status_code=200)
async def fetch_recipe(*, recipe_id: int) -> dict:
    """Fetch single recipe by id

    Args:
        recipe_id (int): recipe id

    Returns:
        dict: recipe
    """
    result = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if result:
        return result[0]


@api_router.get("/search/", status_code=200)
async def search_recipes(
        keyword: Optional[str] = None, max_results: Optional[int] = 10
) -> dict:
    """search for recipes using query parameters

    Args:
        keyword (Optional[str], optional): keyword in recipe label. Defaults to None.
        max_results (Optional[int], optional): limit for results find query. Defaults to 10.

    Returns:
        dict: dict with key results containing matched recipes
    """
    results = filter(lambda recipe: keyword.lower()
                     in recipe["label"].lower(), RECIPES)
    return {
        "results": list(results)[:max_results]
    }


app.include_router(api_router)
