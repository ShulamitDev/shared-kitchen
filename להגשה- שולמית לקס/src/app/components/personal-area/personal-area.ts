import { Component, OnInit, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RecipeService } from '../../services/recipe';
import { Recipe } from '../../models/recipe.model';
import { RouterLink } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-personal-area',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './personal-area.html',
  styleUrl: './personal-area.css'
})
export class PersonalArea implements OnInit {
  private recipeService = inject(RecipeService);
  public serverUrl = this.recipeService.serverUrl;
  private http = inject(HttpClient);
  private cdr = inject(ChangeDetectorRef);


  myRecipes: Recipe[] = [];
  pendingUsers: any[] = []; // למשתמשים שממתינים לאישור

  userName: string = '';
  userId: string = '';
  userRole: string = '';
  userEmail: string = '';

  userUploadedCount: number = 0;
  isApproved: boolean = false;
  isPending: boolean = false; // האם המשתמש מחכה לאישור

  ngOnInit() {
    this.userId = localStorage.getItem('user_id') || '';
    this.userName = localStorage.getItem('user_name') || 'בשלן/ית';
    this.userRole = localStorage.getItem('user_role') || 'Reader';
    this.userEmail = localStorage.getItem('user_email') || '';

    if (this.userId) {
      this.loadMyRecipes();
      this.loadUserDetails()
      

      if (this.userRole === 'Admin') {
        this.loadPendingUsers();
      }
    }
  }

  // שליפת רשימת המשתמשים הממתינים - עבור המנהל
  loadPendingUsers() {
    this.http.get<any[]>(`/api/auth/pending-users`)
      .subscribe({
        next: (users) => {
          this.pendingUsers = users;
        },
        error: (err) => console.error('שגיאה בטעינת בקשות', err)
      });
  }

  // פונקציית האישור של המנהל
  approveUser(targetUserId: number) {
    //כתובת בשרת לאישור משתמש
    this.http.post(`/api/auth/approve-user/${targetUserId}`, {}, {
      // שולח את ה-ID של המנהל לאימות
      headers: { 'User-ID': this.userId } 
    }).subscribe({
      next: () => {
        alert('המשתמש אושר בהצלחה!');
        //this.cdr.detectChanges();
        this.pendingUsers = this.pendingUsers.filter(u => u.id !== targetUserId);
      },
      error: (err) => alert('שגיאה באישור המשתמש')
    });
  }

    rejectUser(targetUserId: number) {
    if (confirm('האם אתה בטוח שברצונך לדחות את בקשת המשתמש?')) {
      this.http.post(`/api/auth/reject-user/${targetUserId}`, {}, {
        headers: { 'User-ID': this.userId }
      }).subscribe({
        next: () => {
          alert('הבקשה נדחתה.');
          this.pendingUsers = this.pendingUsers.filter(u => u.id !== targetUserId);
        }
      });
    }
  }


  loadUserDetails() {
    // קריאה לשרת לקבלת פרטים נוספים כמו אימייל וסטטוס אישור
    this.http.get<any>(`/api/auth/user-details/${this.userId}`)
      .subscribe({
        next: (data: any) => {
          this.userEmail = data.email;
          this.isApproved = data.is_approved;
          this.userRole = data.role;
          this.isPending = data.is_pending;
        },
        error: (err) => console.error('שגיאה בטעינת פרטי משתמש', err)
      });
  }

  requestPermission() {
    // קריאה לשרת לשליחת בקשה
    this.http.post(`/api/auth/request-upload-permission`, { user_id: this.userId })
      .subscribe({
        next: () => {
          this.isPending = true;
          alert('בקשתך נשלחה בהצלחה למנהל המערכת!');
        },
        error: (err) => {
          console.error('שגיאה בשליחת בקשה', err);
          alert('חלה שגיאה בשליחת הבקשה. נסה שוב מאוחר יותר.');
        }
      });
  }


  loadMyRecipes() {
    this.recipeService.getAllRecipes().subscribe({
      next: (recipes) => {
        console.log("Recipes from server:", recipes); // בדיקה: האם לכל מתכון יש user_id?
        console.log("Current User ID from storage:", this.userId); // בדיקה: מה המזהה שלי?

        // המרה של שניהם למספרים כדי למנוע ספק
        const currentId = Number(this.userId);
        const isAdmin = localStorage.getItem('user_role') === 'Admin';

        // 1. חישוב המונה האמיתי (תמיד רק של המשתמש הנוכחי)
        this.userUploadedCount = recipes.filter(r => Number(r.user_id) === currentId).length;

        // 2. סינון הרשימה לתצוגה (אם אדמין - רואה הכל)
        this.myRecipes = recipes.filter(r => {
          const recipeOwnerId = Number(r.user_id);
          return recipeOwnerId === currentId || isAdmin;
        });


        console.log("Filtered recipes for user:", this.myRecipes);
      },
      error: (err) => console.error('Error loading recipes', err)
    })
  }

  deleteRecipe(id: number) {
    const userRole = localStorage.getItem('user_role') || 'Uploader';

    if (confirm('האם את בטוחה שברצונך למחוק את המתכון הזה לצמיתות?')) {
      this.recipeService.deleteRecipe(id, this.userId, userRole).subscribe({
        next: () => {
          // הסרת המתכון מהמערך המקומי כדי שהמשתמש יראה שהוא נעלם מיד
          this.myRecipes = this.myRecipes.filter(r => r.id !== id);
          alert('המתכון נמחק בהצלחה מהמערכת.');
        },
        error: (err) => {
          console.error('מחיקה נכשלה:', err);
          alert('שגיאה: לא ניתן למחוק את המתכון.');
        }
      });
    }
  }

  isAdmin(): string {
    if (localStorage.getItem('user_role') === 'Admin') {
      return 'ניהול כל המתכונים';
    } else {
      return 'המתכונים שלי';
    }
  }
}