import { Component, inject} from '@angular/core';
import { FormsModule } from '@angular/forms'; // חייב לייבא בשביל הטפסים
import { CommonModule } from '@angular/common'; // בשביל ngIf
import { AuthService } from '../../services/auth'; // השירות שבנינו
import { Router, RouterModule } from '@angular/router'; // בשביל לעבור דף אחרי ההצלחה



@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, CommonModule, RouterModule],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {
  // משתנים שמחוברים ל-HTML
  email = '';
  password = '';
  errorMessage = '';

  private authService = inject(AuthService); // הזרקת השירות
  private router = inject(Router); // הזרקת הנתב
 

  onLogin() {
    // קריאה לפונקציית ה-login בשירות
    this.authService.login(this.email, this.password).subscribe({
      next: (response) => {
          console.log('התחברות הצליחה!', response);
          // response.user מכיל את ה-id, userName ו-role כפי שהגדרת ב-auth.py
          localStorage.setItem('user_id', response.user.id);
          localStorage.setItem('user_role', response.user.role);
          localStorage.setItem('user_name', response.user.userName);
          localStorage.setItem('user_email', this.email);

          // אחרי התחברות מוצלחת, נעבור לדף הבית
          this.router.navigate(['/']);
      },
      error: (err) => {
        this.errorMessage = err.error?.message || 'חלה שגיאה בחיבור לשרת';

        console.error(err); 
    }
    });
  }

}
