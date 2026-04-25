import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RecipeService } from '../../services/recipe';
import { RecipeCard } from '../recipe-card/recipe-card';
import { Recipe } from '../../models/recipe.model';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-recipes-list',
  standalone: true,
  imports: [CommonModule, RecipeCard, FormsModule],
  templateUrl: './recipes-list.html',
  styleUrl: './recipes-list.css'
})
export class RecipesList implements OnInit {
  private recipeService = inject(RecipeService);// הזרקת השירות שיצרנו

  recipes: Recipe[] = [];
  filteredRecipes: Recipe[] = [];

  // משתני סינון
  selectedType: string = 'הכל';
  sortBy: string = 'none';

  // פונקציית Lifecycle שרצה ברגע שהקומפוננטה עולה על המסך
  ngOnInit(): void {
    //בקשת קבלת כל המתכונים מהשרת
    this.recipeService.getAllRecipes()
      //המתנה לנתונים שיגיעו מהשרת
      .subscribe({
        //הצלחה, כאשר הנתונים חוזרים מהשרת=next
        next: (data) => {
          // שמירת הנתונים שהגיעו מהפייתון במערך המקומי
          // ושינוי אוטומטי של המסך בהתאם
          this.recipes = data;
          console.log('Recipes loaded:', data);
          this.filteredRecipes = data;
        },
        error: (err) => console.error('Error fetching recipes', err)
      });
  }
  applyFilters() {
    let temp = [...this.recipes];

    // סינון לפי סוג
    if (this.selectedType !== 'הכל') {
      temp = temp.filter(r => r.recipe_type === this.selectedType);
    }

    // מיון
    if (this.sortBy === 'time') {
      temp.sort((a, b) => (a.prep_time + a.cook_time) - (b.prep_time + b.cook_time));
    } else if (this.sortBy === 'servings') {
      temp.sort((a, b) => Number(b.servings) - Number(a.servings));
    }else if (this.sortBy === 'rating') {
    // מיון לפי דירוג מהגבוה לנמוך
    // temp.sort((a, b) => (b.rating || 0) - (a.rating || 0));
  }
    this.filteredRecipes = temp;
  }

}