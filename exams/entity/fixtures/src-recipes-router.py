"""FastAPI router for recipe endpoints."""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from .store import RecipeStore
from .deps import get_store, get_current_user

router = APIRouter(prefix="/recipes", tags=["recipes"])


class RecipeCreate(BaseModel):
    title: str
    ingredients: list[dict]
    steps: list[str]


class RecipeUpdate(BaseModel):
    title: str | None = None
    ingredients: list[dict] | None = None
    steps: list[str] | None = None


@router.post("/")
async def create_recipe(
    body: RecipeCreate,
    store: RecipeStore = Depends(get_store),
    user=Depends(get_current_user),
):
    try:
        recipe = store.create(
            user_id=user.id,
            title=body.title,
            ingredients=body.ingredients,
            steps=body.steps,
        )
        return {"id": recipe["id"], "status": "created"}
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/{recipe_id}")
async def get_recipe(
    recipe_id: str,
    store: RecipeStore = Depends(get_store),
):
    recipe = store.get(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.patch("/{recipe_id}")
async def update_recipe(
    recipe_id: str,
    body: RecipeUpdate,
    store: RecipeStore = Depends(get_store),
):
    try:
        store.update(recipe_id, **body.model_dump(exclude_none=True))
        return {"status": "updated"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{recipe_id}")
async def delete_recipe(
    recipe_id: str,
    store: RecipeStore = Depends(get_store),
):
    store.delete(recipe_id)
    return {"status": "deleted"}


@router.get("/")
async def search_recipes(
    q: str = "",
    store: RecipeStore = Depends(get_store),
):
    if not q:
        return []
    return store.search_by_title(q)
