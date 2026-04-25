import { Component, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, FormArray, Validators } from '@angular/forms';
import { RecipeService } from '../../services/recipe';
import { Router } from '@angular/router';

@Component({
  selector: 'app-add-recipe',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './add-recipe.html',
  styleUrl: './add-recipe.css'
})
export class AddRecipe {
  private fb = inject(FormBuilder);
  private recipeService = inject(RecipeService);
  private router = inject(Router);

  message: string | null = null;
  isError: boolean = false;
  recipeForm: FormGroup;
  selectedFile: File | null = null;
  imagePreview: string | null = null;



  constructor() {
    this.recipeForm = this.fb.group({
      title: ['', [Validators.required, Validators.minLength(3)]],
      description: [''],//, Validators.required
      instructions: ['', Validators.required],
      prep_time: ['', [Validators.required, Validators.min(0)]],
      cook_time: [],//Validators.min(0)
      servings: ['', [Validators.required, Validators.min(0)]], // שונה לברירת מחדל של מחרוזת
      recipe_type: [''],
      difficulty: [''],
      is_anonymous: [false],
      ingredients: this.fb.array([])
    });

    this.addIngredient();
  }

  get ingredients() {
    return this.recipeForm.get('ingredients') as FormArray;
  }

  addIngredient() {
    this.ingredients.push(this.fb.group({
      product: ['', Validators.required],
      amount: [''],
      unit: [''],
    }));
  }

  removeIngredient(index: number) {
    this.ingredients.removeAt(index);
  }

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile = file;
      const reader = new FileReader();

      reader.onload = () =>{ 
        this.imagePreview = reader.result as string;
      };
      reader.readAsDataURL(file);
    }
  }

  onSubmit() {
    // 1. בדיקת תקינות בסיסית של הטופס והתמונה
    if (this.recipeForm.invalid || !this.selectedFile) {
      this.recipeForm.markAllAsTouched();
      this.message = 'נא למלא את כל השדות ולבחור תמונה';
      this.isError = true;
      return;
    }

    // 2. שליפת נתוני זיהוי מה-LocalStorage
    const userId = localStorage.getItem('user_id') || '1';
    const userRole = localStorage.getItem('user_role') || 'Admin';

    // 3. בניית אובייקט ה-FormData
    const formData = new FormData();

    // שדות טקסט והמרות למספרים (כדי שה-int() בפייתון לא ייכשל)
    formData.append('title', this.recipeForm.value.title);
    formData.append('description', this.recipeForm.value.description);
    formData.append('instructions', this.recipeForm.value.instructions);
    
    // וידוא שהערכים הם מחרוזות של מספרים שלמים
    formData.append('prep_time', Math.floor(Number(this.recipeForm.value.prep_time)).toString());
    formData.append('cook_time', Math.floor(Number(this.recipeForm.value.cook_time)).toString());
    formData.append('servings', Math.floor(Number(this.recipeForm.value.servings)).toString());

    // חשוב: הפייתון מצפה ל-'type' ולא ל-'recipe_type'
    formData.append('type', this.recipeForm.value.recipe_type);
    formData.append('difficulty', this.recipeForm.value.difficulty);
    
    // המרה לבוליאני כפי שהפייתון מצפה (בדיקת 'true' במחרוזת)
    formData.append('is_anonymous', this.recipeForm.value.is_anonymous ? 'true' : 'false');

    // 4. עיבוד רשימת המצרכים (מניעת NaN או מחרוזות ריקות ב-amount)
    const cleanedIngredients = this.recipeForm.value.ingredients.map((ing: any) => {
      let amountValue = 0;
      // בדיקה אם ה-amount הוא מספר תקין ולא ריק
      if (ing.amount !== null && ing.amount !== '' && !isNaN(Number(ing.amount))) {
        amountValue = parseFloat(ing.amount);
      }

      return {
        product: ing.product,
        amount: amountValue,
        unit: ing.unit || ''
      };
    });

    formData.append('ingredients', JSON.stringify(cleanedIngredients));

    // 5. הוספת הקובץ
    formData.append('image', this.selectedFile);

    // 6. שליחה ל-Service
    this.recipeService.createRecipe(formData, userId, userRole).subscribe({
      next: (res) => {
        this.message = 'המתכון נוסף בהצלחה! מעביר אותך לדף המתכונים...';
        this.isError = false;
        setTimeout(() => this.router.navigate(['/recipes']), 2000);
      },
      error: (err) => {
        // הדפסת הודעת השגיאה המדויקת מהשרת לדיבג
        console.error("Server Response Error:", err);
        this.message = err.error?.message || 'שגיאה בשמירת המתכון. בדקי את הטרמינל של השרת.';
        this.isError = true;
      }
    });
  }
}