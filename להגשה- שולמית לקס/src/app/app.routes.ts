// src/app/app.routes.ts- "מרכזיית הטלפונים" של האתר
import { Routes } from '@angular/router';
import { Login } from './components/login/login';
import { Register } from './components/register/register';
import { RecipesList } from './components/recipes-list/recipes-list';
import { RecipeDetails } from './components/recipe-details/recipe-details';
import { PersonalArea } from './components/personal-area/personal-area';
import { Home } from './components/home/home';
import { AddRecipe } from './components/add-recipe/add-recipe';
import { RecipeSearch } from './components/recipe-search/recipe-search';

export const routes: Routes = [
  { path: '',component:Home },
  { path: 'login', component:Login},
  { path: 'register', component: Register },
  { path: 'recipes', component: RecipesList },
  { path: 'recipe/:id', component: RecipeDetails }, // נתיב עם פרמטר ID
  { path: 'personal', component: PersonalArea },
  { path: 'add-recipe', component: AddRecipe },
  { path: 'search', component: RecipeSearch },
  { path: '**', redirectTo: '' } // נתיב לשגיאות (דף לא נמצא)
];