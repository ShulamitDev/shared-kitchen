import { Component, Input, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { RecipeService } from '../../services/recipe';
import { Recipe } from '../../models/recipe.model';

@Component({
  selector: 'app-recipe-card',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './recipe-card.html',
  styleUrl: './recipe-card.css'
})
export class RecipeCard {
  public recipeService = inject(RecipeService);
  @Input() recipeData!: Recipe; 
  // מקבל את נתוני המתכון מהאבא (RecipesList)
  // @Input מאפשר לאבא (RecipesList) להעביר נתונים לתוך הילד הזה
}