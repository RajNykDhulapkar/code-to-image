from fastapi import FastAPI, APIRouter, Query, HTTPException, Request
from fastapi.templating import Jinja2Templates

from typing import Optional, Any
from pathlib import Path

from app.schemas.recipe import RecipeSearchResult, Recipe, RecipeCreate

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

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
async def root(request: Request) -> dict:
    """ 
    Root Get route
    """
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "recipes": RECIPES}
    )


@api_router.get("/recipe/{recipe_id}", status_code=200, response_model=Recipe)
async def fetch_recipe(*, recipe_id: int) -> dict:
    """Fetch single recipe by id

    Args:
        recipe_id (int): recipe id

    Returns:
        dict: recipe
    """
    result = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]

    if not result:
        raise HTTPException(
            status_code=404, detail=f"Recipe with ID {recipe_id} does not exist"
        )

    if result:
        return result[0]


@api_router.get("/search/", status_code=200, response_model=RecipeSearchResult)
async def search_recipes(
    *,
    keyword: Optional[str] = Query(None, min_length=3, example="chicken"),
    max_results: Optional[int] = 10
) -> dict:
    """search for recipes using query parameters

    Args:
        keyword (Optional[str], optional): keyword in recipe label. Defaults to None.
        max_results (Optional[int], optional): limit for results find query. Defaults to 10.

    Returns:
        dict: dict with key results containing matched recipes
    """
    if not keyword:
        return {
            "results": RECIPES[:max_results]
        }

    results = filter(lambda recipe: keyword.lower()
                     in recipe["label"].lower(), RECIPES)
    return {
        "results": list(results)[:max_results]
    }


@api_router.post("/recipe/", status_code=201, response_model=Recipe)
async def create_recipe(*, recipe_in: RecipeCreate) -> dict:
    """create a new recipe

    Args:
        recipe_in (RecipeCreate): recipe create input

    Returns:
        dict: recipe
    """
    new_entry_id = len(RECIPES) + 1
    recipe_entry = Recipe(
        id=new_entry_id,
        label=recipe_in.label,
        source=recipe_in.source,
        url=recipe_in.url
    )
    RECIPES.append(recipe_entry.dict())

    return recipe_entry


app.include_router(api_router)
