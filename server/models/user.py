"""
מודל User – מייצג משתמש במערכת.

כולל:
- אימייל
- סיסמה
- תפקיד
- אישור העלאת מתכונים
"""

from database import db
from models.base_model import BaseModel
# הכל תקין, השגיאות בשורה הבאה באות סתם והכל עובד כראוי
from werkzeug.security import generate_password_hash, check_password_hash

class User(BaseModel): #מחלקת משתמש

    # שם משתמש
    userName = db.Column(db.String(50), nullable=False)
    # כתובת מייל – חייבת להיות ייחודית
    email = db.Column(db.String(120), unique=True, nullable=False)
    # סימה מוצפנת
    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), default="Reader")     # תפקיד המשתמש: קורא (Reader), מעלה מתכונים (Uploader) או מנהל (Admin)
    is_approved_uploader = db.Column(db.Boolean, default=False) # אישור מנהל להעלאה
    is_pending_approval = db.Column(db.Boolean, default=False) #

    recipes = db.relationship('Recipe', backref='author', lazy=True)#

    def set_password(self, password):
        """הופכת סיסמה רגילה לקוד מוצפן ושומרת אותו"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """בודקת אם הסיסמה שהמשתמש הקיש תואמת לקוד המוצפן"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.userName}>'
