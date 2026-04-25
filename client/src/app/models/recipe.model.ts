export interface Ingredient {
  product: string;
  amount: string;
  unit: string;
  section_name?: string; // שדה אופציונלי לשם הסעיף במתכון
}  

// מודל הנתונים של מתכון
export interface Recipe {
  id: number;
  user_id: number;
  author_name: string;
  title: string;
  description: string;
  instructions: string;
  image_path: string;
  prep_time: number;
  cook_time: number;
  servings: string;
  recipe_type: string;     // בשרי/חלבי/פרווה
  difficulty: string;      // קל/בינוני/מאתגר
  ingredients: Ingredient[];
  variations: string[];
 }
 
// שימוש ב"הורשה" (Inheritance) - מודל מיוחד לתוצאות חיפוש הכולל ציון התאמה
export interface SearchResult extends Recipe {
  score: number;
}
