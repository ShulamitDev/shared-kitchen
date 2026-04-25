"""
app.py – נקודת הכניסה של השרת.

אחראי על:
- יצירת שרת Flask
- טעינת הגדרות (Config)
- חיבור למסד הנתונים
- יצירת טבלאות
"""

# הכל תקין, השגיאות בשורה הבאה באות סתם והכל עובד כראוי
from flask import Flask
from config import Config
from database import db
from models import User, Recipe, IngredientEntry # חשוב: גורם ליצירת טבלאות users, recipes ו-ingredient
from routes.auth import auth_bp
from routes.recipes import recipes_bp
from flask import send_from_directory
import os

# יצירת מופע של שרת Flask
app = Flask(__name__)

@app.route('/uploads/recipes/<path:filename>')
def uploaded_file(filename):
    """
    פונקציה המאפשרת גישה לקבצים מהתיקייה uploads/recipes
    דרך דפדפן או קריאה ישירה.
    """
    return send_from_directory('uploads/recipes', filename)


# לא חובה! ניתן למחוק!!
app.json.ensure_ascii = False  # זה יגרום ל-Flask להחזיר עברית קריאה בטרמינל


# טעינת הגדרות מתוך מחלקת Config
app.config.from_object(Config)

# חיבור SQLAlchemy לאפליקציה
db.init_app(app)

# רישום הנתיבים (Blueprints) בשרת
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(recipes_bp, url_prefix='/recipes')

# יצירת כל הטבלאות במסד הנתונים (פעם ראשונה בלבד)
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    """
    Endpoint בדיקה – מחזיר תשובה פשוטה
    כדי לוודא שהשרת רץ.
    """
    return {"message": "Server is running"}

if __name__ == "__main__":
    # הרצת השרת במצב פיתוח
    app.run(debug=True)