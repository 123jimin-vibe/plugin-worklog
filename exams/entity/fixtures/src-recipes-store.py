class RecipeStore:
    def __init__(self, db):
        self.db = db

    def create(self, user_id, title, ingredients, steps):
        recipe = {
            "user_id": user_id,
            "title": title,
            "ingredients": ingredients,
            "steps": steps,
        }
        self.db.insert(recipe)
        return recipe

    def delete(self, recipe_id):
        self.db.delete(recipe_id)

    def search_by_title(self, query):
        return self.db.find({"title": {"$regex": query}})
