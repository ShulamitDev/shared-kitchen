"""
auth_decorators.py – דקורטורים לניהול הרשאות.
קובץ זה מאפשר לנו להגן על נתיבים בשרת.
במקום לחזור על בדיקות אבטחה בכל פונקציה, אנו יוצרים "שומר"
שאפשר להציב מעל כל נתיב שדורש זיהוי.
"""
from flask import request, jsonify
from functools import wraps

def login_required(f):
    """מוודא שהמשתמש מחובר"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # בדיקה זמנית: האם נשלח מזהה משתמש ב-Headers של הבקשה?
        # כאן תבוא הבדיקה של ה-Token. כרגע נשאיר מקום ללוגיקה
        user_id = request.headers.get('User-ID') # דוגמה זמנית לבדיקה בטרמינל

        if not user_id:
            # אם אין מזהה - החזרת שגיאת "לא מורשה"
            return jsonify({"message": "אנא התחבר כדי להמשיך"}), 401

        # אם הכל תקין - המשך לפונקציה המקורית
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    מוודא שהמשתמש הוא מנהל (Admin)
    מיועד לנתיבים רגישים כמו מחיקת משתמשים או אישור מעלי מתכונים.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # בדיקה זמנית: נבדוק אם נשלח header שמציין תפקיד מתאים
        role = request.headers.get('User-Role')
        if role != 'Admin':
            # 403 = Forbidden (נמצא, אבל אין לך רשות להיכנס)
            return jsonify({"message": "פעולה זו שמורה למנהלים בלבד"}), 403
        return f(*args, **kwargs)
    return decorated_function


def uploader_required(f):
    """
    מוודא שהמשתמש מורשה להעלות מתכונים.
    מאפשר כניסה למי שתפקידו 'Uploader' או 'Admin'.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # בדיקה זמנית: נבדוק אם נשלח header שמציין תפקיד מתאים
        role = request.headers.get('User-Role')

        if role not in ['Uploader', 'Admin']:
            return jsonify({"message": "אין לך הרשאה להעלות מתכונים"}), 403

        return f(*args, **kwargs)
    return decorated_function