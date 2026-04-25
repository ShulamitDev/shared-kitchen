"""
image_handler.py – כלי עזר לעיבוד תמונות.
אחראי על שמירת תמונות ויצירת וריאציות שונות לתמונה(Variations).
"""
import os
from PIL import Image, ImageFilter
from uuid import uuid4  # ליצירת שם ייחודי לכל תמונה

# הגדרת נתיב התיקייה שבה יישמרו התמונות
UPLOAD_FOLDER = 'uploads/recipes'

# בדיקה בטיחותית: אם התיקייה לא קיימת במחשב, תיווצר אוטומטית
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def process_recipe_image(image_file):
    """
   הפונקציה המרכזית לעיבוד תמונה.
    ארגומנט: image_file - הקובץ הגולמי שהגיע מהדפדפן.
    מחזירה: (נתיב המקור, רשימת נתיבי הווריאציות).
    """
    # יצירת זהות ותקייה ייחודיות לתמונה כדי שלא יהיו כפילויות
    unique_id = str(uuid4()) # מזהה ייחודי
    recipe_folder = os.path.join(UPLOAD_FOLDER, unique_id) # תיקייה ייחודית לכל מתכון
    if not os.path.exists(recipe_folder): # יצירת התיקייה אם לא קיימת
        os.makedirs(recipe_folder)

    # חילוץ סיומת הקובץ המקורי (למשל .jpg או .png)
    extension = os.path.splitext(image_file.filename)[1]

    # שמירת התמונה המקורית כפי שהיא
    orig_name = f"original{extension}"
    orig_path = os.path.join(recipe_folder, orig_name)
    image_file.save(orig_path)

    # פתיחת התמונה עם Pillow לצורך עיבוד
    img = Image.open(orig_path)
    # ד. טיפול בשקיפות (RGBA):
    #תמונות PNG לעיתים מכילות ערוץ שקיפות.
    # פונקציות מסוימות לא אוהבות את זה,
    # לכן אנו ממירים את התמונה לפורמט RGB סטנדרטי.
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    variation = []

    # וריאציה 1: שחור לבן
    bw_path = os.path.join(recipe_folder, f"bw{extension}")
    img.convert('L').save(bw_path)
    variation.append(bw_path)

    # וריאציה 2: מטושטש (Blur)
    blur_path = os.path.join(recipe_folder, f"blur{extension}")
    img.filter(ImageFilter.GaussianBlur(radius=5)).save(blur_path) # טשטוש מופחת- .BLUR
    variation.append(blur_path)

    # וריאציה 3: תמונה מוקטנת (Thumbnail)
    # משמש להצגת ריבוע קטן ברשימת כל המתכונים באתר
    thumb_path = os.path.join(recipe_folder, f"thumb{extension}")
    thumb_img = img.copy()  # יצירת עותק כדי לא להקטין את המקור שנמצא בזיכרון
    thumb_img.thumbnail((300, 300))  # הקטנה תוך שמירה על פרופורציות
    thumb_img.save(thumb_path)
    variation.append(thumb_path)

    return orig_path, variation