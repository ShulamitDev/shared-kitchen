from utils.auth_decorators import login_required, admin_required
"""
auth.py – ניהול תהליכי הזדהות (Authentication).

קובץ זה מרכז את כל הפעולות שקשורות למשתמשים:
1. הרשמה של משתמש חדש למערכת.
2. אימות פרטי משתמש קיים (התחברות).
"""

from flask import Blueprint, request, jsonify
from models import User
from database import db

# יצירת Blueprint - מארגן את הנתיבים תחת השם 'auth'
# זה מאפשר להפריד את הלוגיקה מהקובץ הראשי (app.py)
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    נתיב להרשמת משתמש חדש.
    מקבל מהלקוח (Angular) אובייקט JSON המכיל: userName, email, password.
    """
    print("!!! Request reached Flask !!!")
    data = request.get_json()

    if not data or not data.get('userName') or not data.get('email') or not data.get('password'):
        return jsonify({"message": "כל השדות חובה: שם משתמש, אימייל וסיסמה"}), 400
    # החזרת שגיאת 400- שונה לקוד שקיים למטה ע"מ להעביר אח"כ את המשתמש להתחברות


    email = data.get('email')

    # בדיקה אם המשתמש כבר רשום
    existing_user = User.query.filter_by(email=email).first()


    if existing_user:
        # במקום להחזיר שגיאה רגילה, נחזיר קוד 200 (הצלחה) עם סטטוס מיוחד
        # החזרת JSON ברור לאנגולר
        return jsonify({
            "status": "exists", # exists- קיים
            "message": "המשתמש כבר קיים במערכת, מעביר להתחברות..."
        }), 200



    try:
        # 2. יצירת אובייקט משתמש חדש
        # שימי לב: השדה role יקבל אוטומטית 'Reader' מהגדרת המודל
        new_user = User(
            userName=data.get('userName'),
            # email=data.get('email')
            email=email
        )

        # 3. הצפנת הסיסמה לפני השמירה
        # פונקציה זו הופכת את הסיסמה לגיבוב (Hash) בלתי ניתן לפענוח
        new_user.set_password(data.get('password'))

        # 4. שמירה במסד הנתונים
        new_user.save()

        return jsonify({
            "message": "המשתמש נרשם בהצלחה!",
            "user_id": new_user.id}), 201


    except Exception as e:
        # במקרה של תקלה לא צפויה (למשל בעיה בחיבור למסד הנתונים)
        return jsonify({"message": f"שגיאה ברישום המשתמש: {str(e)}"}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    נתיב להתחברות משתמש קיים.
    בודק האם האימייל קיים והאם הסיסמה שהוזנה תואמת למה ששמור (אחרי גיבוב).
    """
    data = request.get_json()

    # חיפוש המשתמש לפי האימייל
    user = User.query.filter_by(email=data.get('email')).first()

    # בדיקה כפולה: האם המשתמש קיים והאם פונקציית הבדיקה (check_password) מחזירה True
    if user and user.check_password(data.get('password')):
        # אם הכל תקין, נחזיר פרטי משתמש בסיסיים (בלי הסיסמה כמובן!)
        return jsonify({
            "message": f"ברוך הבא, {user.userName}!",
            "user": {
                "id": user.id,
                "userName": user.userName,
                "role": user.role
            }
        }), 200

    # אם אחד מהנתונים לא נכון, נחזיר קוד שגיאה 401 (Unauthorized)
    return jsonify({"message": "אימייל או סיסמה שגויים"}), 401

@auth_bp.route('/user-details/<int:user_id>', methods=['GET'])
def get_user_details(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "משתמש לא נמצא"}), 404
    return jsonify({
        "userName": user.userName,
        "email": user.email,
        "role": user.role,
        "is_approved": user.is_approved_uploader,
        "is_pending": user.is_pending_approval
    }), 200

#
@auth_bp.route('/request-upload-permission', methods=['POST'])
def request_permission():
    data = request.get_json()
    user_id = data.get('user_id')
    user = User.query.get(user_id)
    if user:
        user.is_pending_approval = True  # סימון שהבקשה ממתינה
        db.session.commit()
        return jsonify({"message": "בקשתך נשלחה למנהל"}), 200
    return jsonify({"message": "משתמש לא נמצא"}), 404

# נתיב למנהל לאשר משתמשים
@auth_bp.route('/approve-user/<int:user_id>', methods=['POST'])
def approve_user(user_id):
    # בדיקה שהמבצע הוא אדמין (לפי ה-Header ששלחנו)
    admin_id = request.headers.get('User-ID')
    admin = User.query.get(admin_id)
    if not admin or admin.role != 'Admin':
        return jsonify({"message": "רק מנהל יכול לאשר משתמשים"}), 403

    user = User.query.get(user_id)
    if user:
        user.role = 'Uploader'
        user.is_approved_uploader = True
        user.is_pending_approval = False  # הבקשה כבר לא ממתינה
        db.session.commit()
        return jsonify({"message": f"המשתמש {user.userName} אושר בהצלחה"}), 200
    return jsonify({"message": "משתמש לא נמצא"}), 404

@auth_bp.route('/pending-users', methods=['GET'])
def get_pending_users():
    # שולף רק משתמשים שהם Reader ושסימנו שהם מחכים לאישור
    pending = User.query.filter_by(role='Reader', is_pending_approval=True).all()
    output = []
    for u in pending:
        output.append({"id": u.id, "userName": u.userName, "email": u.email})
    return jsonify(output), 200

@auth_bp.route('/reject-user/<int:user_id>', methods=['POST'])
@login_required
def reject_user(user_id):
    admin_id = request.headers.get('User-ID')
    admin = User.query.get(admin_id)
    if not admin or admin.role != 'Admin':
        return jsonify({"message": "אין לך הרשאה לבצע פעולה זו"}), 403

    user = User.query.get(user_id)
    if user:
        user.is_pending_approval = False # פשוט מאפסים את הבקשה
        db.session.commit()
        return jsonify({"message": "הבקשה נדחתה"}), 200
    return jsonify({"message": "משתמש לא נמצא"}), 404