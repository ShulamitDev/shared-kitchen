import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root' // אומר לאנגולר: השירות הזה הוא "סינגלטון" (מופע יחיד) שזמין בכל האפליקציה
})
export class AuthService { // השם נשאר AuthService לצורך נוחות, הקובץ הוא auth.ts
  private http = inject(HttpClient); // הזרקת שירות ה-HTTP
  // אנגולר תדע להפנות את זה ל-http://127.0.0.1:5000/auth בזכות הגדרת ה-Proxy
  private apiUrl = '/api/auth';
  private currentUserSubject = new BehaviorSubject<any>(null);

  constructor() {
    // בדיקה אם הקוד רץ בדפדפן
    if (typeof window !== 'undefined' && window.localStorage) {
      const savedUser = localStorage.getItem('user');
      if (savedUser) {
        this.currentUserSubject.next(JSON.parse(savedUser));
      }
    }
  }

  // פונקציית התחברות
  // היא מקבלת אימייל וסיסמה כמחרוזות (string)
  // ומחזירה Observable - הבטחה שבעתיד יחזור מידע מהשרת
  login(email: string, password: string): Observable<any> {
    // שליחת בקשת POST לשרת. הגוף של הבקשה הוא אובייקט עם המידע.
    return this.http.post<any>(`${this.apiUrl}/login`, { email, password }).pipe(
      tap(user => {
        // שמירת פרטי המשתמש ב-Local Storage בדפדפן
        //!!localStorage.setItem('user', JSON.stringify(user));
        //!!this.currentUserSubject.next(user);
      })
    );
  }
  // פונקציית הרשמה
  // מקבלת אובייקטuserData (שיכול להכיל שם, אימייל, תפקיד וכו')
  register(userData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/register`, userData);
  }
}