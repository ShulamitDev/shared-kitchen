"""
recipes.py – ניהול נתיבי המתכונים.
אחראי על:
1. הוספת מתכון חדש (כולל עיבוד תמונה).
2. שליפת כל המתכונים להצגה ממסד הנתונים.
"""
import os
from flask import Blueprint, request, jsonify
from models import Recipe, IngredientEntry,  User, RecipeType, Difficulty
from database import db
import json
from utils.image_handler import process_recipe_image
from utils.auth_decorators import login_required, uploader_required, admin_required

# יצירת Blueprint למתכונים
# מאפשר לאגד את כל הראוטים של המתכונים תחת אובייקט אחד
recipes_bp = Blueprint('recipes', __name__)

@recipes_bp.route('/add', methods=['POST'])
@login_required # קודם כל בודק אם המשתמש בכלל מחובר
@uploader_required # לאחר מכן בודק אם יש לו הרשאת העלאה
def add_recipe():
    """נתיב להוספת מתכון חדש למערכת"""
    try:
        # שליפת נתונים מהטופס
        # --- שלב 1: שליפת נתוני הטקסט מהטופס ---
        title = request.form.get('title')
        description = request.form.get('description')
        instructions = request.form.get('instructions')
        prep_time = request.form.get('prep_time',0)
        cook_time = request.form.get('cook_time', 0)
        servings = request.form.get('servings', 1)
        recipe_type_str = request.form.get('type', 'PARVE')
        difficulty_str = request.form.get('difficulty', 'EASY')
        # המרה של מחרוזת "true"/"false" לבוליאני אמיתי
        is_anonymous = request.form.get('is_anonymous') == 'true'

        user_id = request.headers.get('User-ID') # המזהה של המעלה

        # --- שלב 2: טיפול ועיבוד התמונה ---
        image_file = request.files.get('image') # שליפת הקובץ הבינארי מהבקשה
        image_path = None
        variation_paths = ""

        if image_file:
            # שימוש ב-image_handler
            orig_path, variations = process_recipe_image(image_file)
            image_path = orig_path
            variation_paths = ",".join(variations) # שמירת הנתיבים כמחרוזת מופרדת בפסיקים כדי שנוכל לשמור בעמודה אחת במסד

        if not title or len(title) < 3:
            return jsonify({"message": "שם המתכון קצר מדי או חסר"}), 400

        if not instructions:
            return jsonify({"message": "חסרות הוראות הכנה"}), 400

            # בדיקה שהועלתה תמונה (חובה לפי הדרישות)
        if 'image' not in request.files:
            return jsonify({"message": "חובה להעלות תמונה למתכון"}), 400

        # --- שלב 3: שמירה למסד הנתונים ---
        # יצירת מופע חדש של מתכון עם הנתונים שנאספו
        new_recipe = Recipe(
            title=title,
            description=description,
            instructions=instructions,
            prep_time=int(prep_time), #המרה למספר שלם למניעת שגיאות סכימה
            cook_time=int(cook_time),
            servings=int(servings),
            recipe_type=RecipeType[recipe_type_str],  # (SQLAlchemy ימיר ל-Enum)
            difficulty=Difficulty[difficulty_str],  #  (SQLAlchemy ימיר ל-Enum)
            is_anonymous=is_anonymous,
            user_id=int(user_id), # קישור למשתמש שיצר את המתכון
            image_path=image_path,
            variation_paths=variation_paths
            # recipe_type ו-difficulty יקבלו את ערכי הדיפולט מהמודל (PARVE ו-EASY)
        )
        db.session.add(new_recipe)
        db.session.flush() # "משריין" ID למתכון במסד הנתונים לפני ה-Commit הסופי

        # --- שלב 4: טיפול ברשימת המצרכים ---
        ingredients_data = request.form.get('ingredients')
        if ingredients_data:
            # הפרונט-אנד ישלח את המצרכים כטקסט בפורמט JSON
            ingredients_list = json.loads(ingredients_data)

            for index, ing in enumerate(ingredients_list):
                new_ingredient = IngredientEntry(
                    product=ing.get('product'),
                    amount=int(ing.get('amount', 0)),
                    unit=ing.get('unit'),
                    order_index=index,  # שומר על הסדר שבו המשתמש הזין
                    recipe_id=new_recipe.id  # הקישור למתכון שזה עתה יצרנו
                )
                db.session.add(new_ingredient)

        # שמירה סופית של הכל (המתכון + כל המצרכים)
        db.session.commit()

        return jsonify({
            "message": "המתכון נוסף בהצלחה!",
            "id": new_recipe.id
        }), 201

    except Exception as e:
        db.session.rollback()  # במקרה של שגיאה - ביטול כל הפעולות (למניעת חצי מתכון ב-DB)
        return jsonify({"message": f"שגיאה בהוספת המתכון: {str(e)}"}), 500

@recipes_bp.route('/all', methods=['GET'])
def get_all_recipes():
    """
    נתיב לשליפת כל המתכונים להצגה באתר
    """
    # שליפת כל הרשומות מטבלת Recipe
    recipes = Recipe.query.all()
    output = []

    for r in recipes:
        # בניית אובייקט JSON לכל מתכון
        # בניית רשימת מצרכים עבור כל מתכון
        ing_list = []
        for ing in r.ingredients:
            ing_list.append({
                "product": ing.product,
                "amount": ing.amount,
                "unit": ing.unit
            })

        display_author = "אנונימי" if r.is_anonymous else (r.author.userName if r.author else "משתמש מערכת")  # author הוא ה-backref מה-User

        output.append({
            "id": r.id,
            "user_id": r.user_id, # מזהה המעלה על מנת שיוכל לצפות במתכונים שלו
            "author_name": display_author,  # שם המעלה מוכן לתצוגה
            "title": r.title,
            "description": r.description,
            "instructions": r.instructions,
            "image_path": r.image_path,
            "prep_time": r.prep_time or 0,
            "cook_time": r.cook_time or 0,
            "servings": r.servings or 0,
            "recipe_type": r.recipe_type.value if r.recipe_type else "פרווה",  #  הוספת הערך הטקסטואלי של ה-Enum
            "difficulty": r.difficulty.value if r.difficulty else "קל",
            "ingredients": ing_list,  # הוספת רשימת המצרכים ל-JSON המחולץ
            # פירוק מחרוזת הווריאציות בחזרה לרשימה (Array) עבור הפרונט-אנד
            "variations": r.variation_paths.split(',') if r.variation_paths else []
        })

    # החזרת רשימת המתכונים כ-JSON עם קוד סטטוס 200 (OK)
    return jsonify(output), 200

@recipes_bp.route('/delete/<int:recipe_id>', methods=['DELETE'])
@login_required
# @admin_required  נמחק כי גם המעלה יכול למחוק את המתכון שלו
def delete_recipe(recipe_id):
    """נתיב מחיקת מתכון - רק לאדמין או למעלה עצמו"""
    try:
        user_id = int(request.headers.get('User-ID'))
        user_role = request.headers.get('User-Role')

        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            return jsonify({"message": "המתכון לא נמצא"}), 404

        # 1. אם המשתמש הוא מנהל (לפי הדרישה במסמך)
        # 2. או אם המשתמש הוא זה שיצר את המתכון
        if user_role == 'Admin' or recipe.user_id == user_id:
        # --- שלב א': מחיקת הקבצים הפיזיים מהכונן ---
        # 1. מחיקת התמונה המקורית
            if recipe.image_path and os.path.exists(recipe.image_path):
                os.remove(recipe.image_path)

         # 2. מחיקת הווריאציות (דף הצביעה וכו')
            if recipe.variation_paths:
            # אנחנו מפרקים את המחרוזת חזרה לרשימה ועוברים על כל נתיב
                for v_path in recipe.variation_paths.split(','):
                    if os.path.exists(v_path):
                        os.remove(v_path)

            # --- שלב ב': מחיקת הרשומה ממסד הנתונים ---
            # המחיקה תמחק אוטומטית גם את המצרכים בגלל ה-cascade במודל
            db.session.delete(recipe)
            db.session.commit()

            return jsonify({"message": f"מתכון {recipe_id} נמחק בהצלחה"}), 200
        else:
            return jsonify({"message": "אין לך הרשאה למחוק מתכון זה"}), 403

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"שגיאה במחיקת המתכון: {str(e)}"}), 500


# --- נתיב חדש: שליפת מתכון בודד לפי ID ---
@recipes_bp.route('/details/<int:recipe_id>', methods=['GET'])
def get_recipe_details(recipe_id):
    """נתיב השולף מתכון ספציפי עבור דף הפירוט באנגולר"""
    try:
        # שליפת המתכון מהמסד לפי ה-ID שנתקבל ב-URL
        recipe = Recipe.query.get(recipe_id)

        if not recipe:
            return jsonify({"message": "המתכון לא נמצא"}), 404

        # בניית רשימת המצרכים עבור המתכון הספציפי
        ing_list = []
        for ing in recipe.ingredients:
            ing_list.append({
                "product": ing.product,
                "amount": ing.amount,
                "unit": ing.unit
            })

            # אם המתכון אנונימי, נחזיר "אנונימי", אחרת את שם המשתמש מהקשר author
            display_author = "אנונימי" if recipe.is_anonymous else (
                recipe.author.userName if recipe.author else "משתמש מערכת")

        # החזרת אובייקט מתכון יחיד (לא בתוך רשימה [])
        return jsonify({
            "id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "instructions": recipe.instructions,
            "image_path": recipe.image_path,
            "prep_time": recipe.prep_time or 0,
            "cook_time": recipe.cook_time or 0,
            "servings": recipe.servings or 0,
            "recipe_type": recipe.recipe_type.value if recipe.recipe_type else "פרווה",
            "difficulty": recipe.difficulty.value if recipe.difficulty else "קל",
            "ingredients": ing_list,
            # פירוק מחרוזת הווריאציות חזרה למערך
            "variations": recipe.variation_paths.split(',') if recipe.variation_paths else [],
            "author_name": display_author
        }), 200

    except Exception as e:
        return jsonify({"message": f"שגיאה בשליפת פרטי המתכון: {str(e)}"}), 500


@recipes_bp.route('/search', methods=['POST'])
def search_by_ingredients():
    """
    נתיב חיפוש מתכונים לפי רכיבים.
    """
    try:
        # קבלת רשימת המצרכים שיש למשתמש מהבקשה (JSON)
        data = request.json
        # נרמול קלט המשתמש: הסרת רווחים והפיכה לאותיות קטנות (אם באנגלית)
        raw_ingredients = data.get('ingredients', [])
        # שלב 1: יצירת Set של המצרכים שהמשתמש הזין
        user_ingredients = set([i.strip().lower() for i in raw_ingredients if i.strip()])

        if not user_ingredients:
            return jsonify({"message": "לא הוזנו מצרכים לחיפוש"}), 400

        # שליפת כל המתכונים מה-DB לביצוע השוואה
        all_recipes = Recipe.query.all()
        results = []

        for recipe in all_recipes:
            # שלב 1: הכנת סט מנורמל מהמתכון
            recipe_ing_set = set([ing.product.strip().lower() for ing in recipe.ingredients])

            # שלב 2: חיתוך (Intersection) למציאת רכיבים משותפים - הפעולה היעילה ביותר
            common_ingredients = user_ingredients & recipe_ing_set

            # שלב 3: חישוב הציון לפי אורך המשותפים חלקי הנדרשים
            if recipe_ing_set:
                score = (len(common_ingredients) / len(recipe_ing_set)) * 100
            else:
                score = 0

            if score >= 20:  # סינון מתכונים פחות רלוונטיים
                results.append({
                    "id": recipe.id,
                    "title": recipe.title,
                    "score": round(score, 2),
                    "image_path": recipe.image_path,
                    "recipe_type": recipe.recipe_type.value if recipe.recipe_type else "פרווה",
                    "difficulty": recipe.difficulty.value if recipe.difficulty else "קל"
                })



        # מיון התוצאות מהציון הגבוה לנמוך
        results.sort(key=lambda x: x['score'], reverse=True)

        return jsonify(results), 200

    except Exception as e:
        return jsonify({"message": f"שגיאה באלגוריתם החיפוש: {str(e)}"}), 500