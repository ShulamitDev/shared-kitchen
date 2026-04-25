"""
קובץ זה הופך את תיקיית ה-models לחבילה (Package).
הוא מאפשר לייבא את המודלים בצורה ישירה ונוחה מתוך התיקייה,
במקום לגשת לכל קובץ בנפרד.
"""

# חשיפת מודל המשתמש (User) ברמת החבילה.
# זה מאפשר לקבצים חיצוניים לייבא אותו דרך 'from models import User'.
from .user import User
from .recipe import Recipe, RecipeType, Difficulty
from .ingredient import IngredientEntry