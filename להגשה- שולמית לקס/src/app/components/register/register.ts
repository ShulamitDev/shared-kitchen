import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-register',
  standalone: true,
  // ייבוא FormsModule חיוני כדי להשתמש ב-[(ngModel)] בטופס
  imports: [FormsModule, CommonModule, RouterModule],
  templateUrl: './register.html',
  styleUrl: './register.css'
})
export class Register {
  // הגדרת משתנים שיאחסנו את נתוני הטופס (מחוברים ל-HTML)
  userName = '';
  email = '';
  password = '';
  errorMessage = ''; // להצגת הודעות שגיאה למשתמש
  successMessage = ''; // להצגת הודעת הצלחה

  private authService = inject(AuthService); // הזרקת שירות האימות
  private router = inject(Router);           // הזרקת הנתב למעבר בין דפים

  /**
   * פונקציה הנקראת בעת שליחת הטופס.
   */
  onRegister() {
    // יצירת אובייקט עם השדות שהפייתון מצפה לקבל (userName, email, password)
    const userData = {
      userName: this.userName,
      email: this.email,
      password: this.password
    };
    // Flaskל (userData)מתוך השירות, ושליחת הנתונים שהמשתמש מילא (AuthService) הפעלת פונקציית הרישום
    this.authService.register(userData).subscribe({
      // 'next' פועל כאשר השרת מחזיר תשובה תקינה (קוד 200/201)
      next: (response) => {

        // בדיקה: האם השרת (Flask) שלח סטטוס 'exists' (המשתמש כבר רשום במערכת)
        if (response.status === 'exists') {
          // הצגת הודעת שגיאה למשתמש
          this.errorMessage = response.message;
          // המתנה של 2 שניות והעברה לדף ההתחברות
          setTimeout(() => this.router.navigate(['/login']), 2000);
        } else {
          // שמירת הנתונים בזיכרון המקומי כדי שהמשתמש ייחשב "מחובר" מיד
          localStorage.setItem('user_id', response.user_id); // וודאי שבפייתון את מחזירה את ה-ID ברישום
          localStorage.setItem('user_role', 'Reader'); // ברישום חדש התפקיד הוא תמיד Reader אצלך
          localStorage.setItem('user_name', this.userName);
          localStorage.setItem('user_email', this.email); // שמירת האימייל מהטופס


          this.successMessage = 'נרשמת בהצלחה! ברוך הבא...';

          setTimeout(() => this.router.navigate(['/recipes']), 1500);
        }
      },
      // 'error' פועל במקרה של תקשורת לקויה או שגיאת שרת (קוד 400 ומעלה)
      error: (err) => {
        // טיפול בשגיאת שרת (500) או שגיאה כללית אחרת
        this.errorMessage = 'חלה שגיאה ברישום. נסה שוב מאוחר יותר.';
        console.error(err);
        console.log('Full Error Object:', err); // הדפסת האובייקט המלא
        this.errorMessage = `שגיאה: ${err.status} - ${err.statusText}`;
      }
    });
  }
}