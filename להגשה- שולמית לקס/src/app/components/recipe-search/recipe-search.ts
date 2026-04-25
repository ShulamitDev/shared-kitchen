import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RecipeService } from '../../services/recipe';
import { SearchResult } from '../../models/recipe.model';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-recipe-search',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './recipe-search.html',
  styleUrl: './recipe-search.css'
})
export class RecipeSearch  {
  private recipeService = inject(RecipeService);
  public serverUrl = this.recipeService.serverUrl;

  ingredientInput: string = ''; // קלט מהמשתמש
  ingredientsToSearch: string[] = []; // רשימת המצרכים לחיפוש
  results: SearchResult[] = []; // תוצאות מהשרת
  hasSearched: boolean = false; // האם בוצע חיפוש

  // הוספת מצרך לרשימה
  addIngredient() {
    if (this.ingredientInput.trim()) {
      this.ingredientsToSearch.push(this.ingredientInput.trim());
      this.ingredientInput = ''; // איפוס השדה
    }
  }

  // הסרת מצרך מהרשימה
  removeIngredient(index: number) {
    this.ingredientsToSearch.splice(index, 1);
  }

  // שליחת הרשימה לשרת לקבלת תוצאות מדורגות לפי Score
  onSearch() {
    if (this.ingredientsToSearch.length === 0) return;

    this.recipeService.searchByIngredients(this.ingredientsToSearch).subscribe({
      next: (data) => {
        this.results = data; // השרת כבר מחזיר אותם ממוינים לפי Score
        this.hasSearched = true;
      },
      error: (err) => console.error('Search failed', err)
    });
  }
}