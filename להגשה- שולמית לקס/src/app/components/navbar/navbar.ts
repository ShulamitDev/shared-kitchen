import { Component, inject} from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { AuthService } from '../../services/auth';
import { PLATFORM_ID, Inject } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';

@Component({
  selector: 'app-navbar', // השם של התגית שבה נשתמש ב-HTML (למשל <app-navbar>)
  standalone: true,      // מציין שזהו רכיב עצמאי
  imports: [CommonModule, RouterModule], // חייב RouterModule בשביל routerLink
  templateUrl: './navbar.html',
  styleUrl: './navbar.css'
})
export class Navbar {
  private authService = inject(AuthService); // גישה לשירות האימות שבנינו מול הפייתון
  private router = inject(Router);        // גישה לנתב בשביל ניווט בין דפים


  constructor(@Inject(PLATFORM_ID) private platformId: Object) {}

  /*
      פונקציה לבדיקה האם המשתמש מחובר.
      מחזירה true אם קיים מזהה משתמש בזיכרון המקומי של הדפדפן.
     */
  isLoggedIn(): boolean {
    // כאן בעתיד נבדוק אם יש Token או User בזיכרון
    // כרגע נחזיר ערך פשוט כדי לראות שזה עובד
    if (typeof window !== 'undefined' && window.localStorage) {
    return !!localStorage.getItem('user_id');
    }
    return false;
  }

  /*
    פעולת התנתקות מהמערכת.
    מנקה את פרטי המשתמש מהדפדפן ומחזירה אותו לדף הכניסה.
   */
  logout() {
    localStorage.removeItem('user_name'); // מחיקת שם המשתמש מהזיכרון
    localStorage.removeItem('user_id'); // מחיקת ID מהזיכרון
    localStorage.removeItem('user_role'); // מחיקת התפקיד (Admin/Uploader וכו')
    this.router.navigate(['/login']); // חזרה לדף התחברות ללא רענון
  }

  getUserName(): string {
  const userName = localStorage.getItem('user_name') || 'אורח';
  return userName;
}

isUploader(): boolean {
  if (isPlatformBrowser(this.platformId)) {
  const role = localStorage.getItem('user_role');
  return role === 'Uploader' || role === 'Admin';
}
return false;
}
}

// לצורך הגרסה הראשונית LocalStorage -בחרנו כרגע להשתמש ב
// בגרסת הייצור הסופי HttpOnly Cookies-אך לטובת אבטחה נצטרך לעבור ל