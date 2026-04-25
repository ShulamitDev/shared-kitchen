import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { RecipeService } from '../../services/recipe';
import { Recipe } from '../../models/recipe.model';

@Component({
  selector: 'app-recipe-details',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './recipe-details.html',
  styleUrl: './recipe-details.css'
})
export class RecipeDetails implements OnInit {
  private route = inject(ActivatedRoute); // מאפשר לנו לקרוא פרמטרים מה-URL
  public recipeService = inject(RecipeService);

  recipe?: Recipe; // המתכון שנציג

  ngOnInit(): void {
    // שליפת ה-ID מהנתיב (למשל מתוך /recipe/1)
    const id = Number(this.route.snapshot.paramMap.get('id'));
    console.log('ID from URL:', id);
    if (id) {
      this.fetchRecipeFromServer(id);
    }
  }
  // פונקציה לשליפת פרטי המתכון מהשרת
  fetchRecipeFromServer(id: number) {
    this.recipeService.getRecipeById(id).subscribe({
      next: (data: Recipe) => {
        if (data.variations) {
          data.variations = data.variations.map(path => path.trim());
        }
        console.log('Data received from server:', data);
        this.recipe = data;
      },
      error: (err) => console.error('Error loading details', err)
    });
  }

  // תוספת לניהול גלריית תמונות
  currentImageIndex: number = 0;

  // פונקציה שתעזור לנו לקבל את כל התמונות (הראשית + הוריאציות) כמערך אחד
  get allImages(): string[] {
    if (!this.recipe) return [];
    const main = this.recipe.image_path;
    const variations = this.recipe.variations || [];
    return [main, ...variations];
  }

  // פונקציה להחזרת נתיב מלא (כדי שלא נכתוב את הלוגיקה הארוכה ב-HTML)
  getFullPath(path: string): string {
    if (!path) return '';
    if (path.includes('http')) return path;
    return `${this.recipeService.serverUrl}/${path.trim()}`;
  }

  // פונקציה למעבר לתמונה הבאה/הקודמת
  changeImage(step: number) {
    const total = this.allImages.length;
    this.currentImageIndex = (this.currentImageIndex + step + total) % total;
  }

}