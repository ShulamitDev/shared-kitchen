from database import db
from models.base_model import BaseModel


class IngredientEntry(BaseModel):
    """
        מודל המייצג שורה בודדת של רכיב בתוך מתכון.
        מקשר בין מוצר, כמות ויחידת מידה למתכון ספציפי (Foreign Key).
        כולל עמודת order_index כדי לשמור על סדר המצרכים כפי שהוזנו.
    """
    # שם הרכיב (למשל: קמח)
    product = db.Column(db.String(100), nullable=False)

    # כמות (למשל: 1.5)
    amount = db.Column(db.String(50), nullable=False)

    # יחידת מידה (למשל: כוס, גרם)
    unit = db.Column(db.String(50))

    # עמודה חדשה לשמירת הסדר
    order_index = db.Column(db.Integer, default=0)


    # האם הרכיב חיוני למתכון (ברירת מחדל: True)
    # שדה שעוזר לאלגוריתם החיפוש לקדם מתכונים שחסר בשבילם מוצרים פחות חשובים
    is_essential = db.Column(db.Boolean, default=True)

    # המפתח הזר שמחבר אותנו למתכון האב
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

    def __repr__(self):
        return f'<Ingredient {self.product}: {self.amount} {self.unit}>'