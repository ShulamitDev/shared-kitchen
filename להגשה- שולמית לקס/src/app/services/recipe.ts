import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Recipe, SearchResult } from '../models/recipe.model'; // ודאי שהנתיב נכון


@Injectable({
  providedIn: 'root'
})
export class RecipeService {
  private http = inject(HttpClient);
  // private apiUrl = '/api/recipes'; // ה-Proxy יפנה ל-http://127.0.0.1:5000/recipes
  //הוספה: כתובת השרת עבור תמונות
  public readonly serverUrl = 'http://127.0.0.1:5000';
  private apiUrl = '/api/recipes';

  // שליפת כל המתכונים במערך
  getAllRecipes(): Observable<Recipe[]> {
    return this.http.get<Recipe[]>(`${this.apiUrl}/all`);
  }

  // שליחת רשימת מצרכים לשרת וקבלת תוצאות ממוינות לפי Score
  searchByIngredients(ingredients: string[]): Observable<SearchResult[]> {
    return this.http.post<SearchResult[]>(`${this.apiUrl}/search`, { ingredients });
  }

  // שליפת מתכון בודד לפי ID (לדף הפרטים)
  getRecipeById(id: number): Observable<Recipe> {
    // בשרת שלך כרגע אין Endpoint למתכון בודד, נצטרך להוסיף או לסנן מהרשימה
    return this.http.get<Recipe>(`${this.apiUrl}/details/${id}`);
  }


  // פונקציה לשליחת המתכון החדש לשרת
  createRecipe(formData: FormData, userId: string, userRole: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/add`, formData, {
      headers: {
        // השרת (ב-Decorator @login_required) מצפה לקבל את ה-ID של המשתמש בתוך ה-Header
        'User-ID': userId,
        'User-Role': userRole
      }
    });
  }

  // מחיקת מתכון
  deleteRecipe(id: number, userId: string, userRole: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/delete/${id}`, {
      headers: {
        'User-ID': userId,
        'User-Role': userRole
      }
    });
  }

}