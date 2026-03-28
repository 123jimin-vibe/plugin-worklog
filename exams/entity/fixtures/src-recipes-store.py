"""Recipe storage layer.

Handles persistence for recipe documents. Each recipe has a title,
ingredient list, and step-by-step instructions.
"""

import time


class RecipeStore:
    def __init__(self, db):
        self.db = db

    def create(self, user_id, title, ingredients, steps):
        """Create a new recipe. Raises if title already exists."""
        if self.db.find_one({"title": title}):
            raise ValueError(f"Recipe with title '{title}' already exists")

        for ing in ingredients:
            if ing["quantity"] < 0:
                raise ValueError("Ingredient quantity must not be negative")

        recipe = {
            "user_id": user_id,
            "title": title,
            "ingredients": ingredients,
            "steps": steps,
            "created_at": time.time(),
            "deleted_at": None,
        }
        self.db.insert(recipe)
        return recipe

    def get(self, recipe_id):
        """Return a recipe by ID, or None if not found or deleted."""
        recipe = self.db.find_by_id(recipe_id)
        if recipe and recipe.get("deleted_at") is None:
            return recipe
        return None

    def update(self, recipe_id, **fields):
        """Update a recipe's fields. Raises if recipe not found."""
        recipe = self.get(recipe_id)
        if not recipe:
            raise ValueError("Recipe not found")

        if "title" in fields:
            existing = self.db.find_one({"title": fields["title"]})
            if existing and existing["id"] != recipe_id:
                raise ValueError(f"Recipe with title '{fields['title']}' already exists")

        if "ingredients" in fields:
            for ing in fields["ingredients"]:
                if ing["quantity"] < 0:
                    raise ValueError("Ingredient quantity must not be negative")

        self.db.update(recipe_id, fields)

    def delete(self, recipe_id):
        """Soft-delete a recipe. Recoverable within the retention window."""
        self.db.update(recipe_id, {
            "deleted_at": time.time(),
            "retain_until": time.time() + 7 * 86400,  # 7-day retention
        })

    def search_by_title(self, query):
        """Search recipes by title substring. Excludes deleted recipes."""
        results = self.db.find({"title": {"$regex": query}})
        return [r for r in results if r.get("deleted_at") is None]

    def purge_expired(self):
        """Permanently remove recipes past their retention window."""
        self.db.delete_many({"retain_until": {"$lt": time.time()}})
