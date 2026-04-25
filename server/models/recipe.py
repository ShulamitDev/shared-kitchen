import enum
from database import db
from models.base_model import BaseModel

# הגדרת ה-Enum ב-Python
class RecipeType(enum.Enum):
    MEAT = "בשרי"
    DAIRY = "חלבי"
    PARVE = "פרווה"

class Difficulty(enum.Enum): # שדרוג לסינון נוסף
    EASY = "קל"
    MEDIUM = "בינוני"
    HARD = "מאתגר"

class Recipe(BaseModel):
    """
        מודל המייצג מתכון במערכת.
        מכיל את נתוני הליבה של המתכון, כולל סוג (חלבי/בשרי) ונתיבים לתמונות המעובדות.
    """
    # שם המתכון
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)  # תיאור קצר של המתכון
    instructions = db.Column(db.Text, nullable=False)  # הוראות הכנה מפורטות

    # זמני הכנה
    prep_time = db.Column(db.Integer, default=0)  # זמן הכנה
    cook_time = db.Column(db.Integer, default=0)  # זמן בישול/אפייה
    # שיניתי לstring כדי שיוכלו לכתוב 2-10 (עם מקף)
    servings = db.Column(db.String(50), nullable=True)  # מספר מנות

    # סוג המתכון: חלבי, בשרי או פרווה
    # משמש לסינון ב-Angular (Dairy, Meat, Parve)
    # שימוש ב-Enum עבור סוג המתכון
    recipe_type = db.Column(db.Enum(RecipeType), nullable=False, default=RecipeType.PARVE)

    difficulty = db.Column(db.Enum(Difficulty), default=Difficulty.EASY) # רמת קושי

    rating = db.Column(db.Float, default=0.0)  # דירוג (ממוצע)

    # תמונות
    image_path = db.Column(db.String(255)) # נתיב לתמונה המקורית
    variation_paths = db.Column(db.Text) # נתיבים ל-3 הווריאציות של התמונות (ישמר כמחרוזת)

    # קשר לרכיבים - One-to-Many
    # זה מאפשר לנו לכתוב recipe.ingredients ולקבל רשימה
    # cascade="all, delete-orphan"- במחיקת מתכון כל הרכיבים שלו יימחקו אוטומטית
    ingredients = db.relationship('IngredientEntry', backref='recipe', lazy=True, cascade="all, delete-orphan")

    # פרטים על המשתמש שיצר את המתכון
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # המפתח הזר למשתמש שיצר את המתכון
    is_anonymous = db.Column(db.Boolean, default=False)  # אפשרות לאנונימיות


    def __repr__(self):
        return f'<Recipe {self.title}>'