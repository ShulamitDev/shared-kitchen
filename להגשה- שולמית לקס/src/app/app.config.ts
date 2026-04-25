import { ApplicationConfig, provideZoneChangeDetection} from '@angular/core';//provideZoneChangeDetection 
import { provideRouter} from '@angular/router';
import { provideHttpClient, withFetch } from '@angular/common/http'; // הוספה עבור תקשורת שרת
import { routes } from './app.routes';
// import { provideClientHydration} from '@angular/platform-browser';

export const appConfig: ApplicationConfig = {
  providers: [
    // provideBrowserGlobalErrorListeners(),
    // provideZonelessChangeDetection(),
    // provideZoneChangeDetection({ eventCoalescing: true}),
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideHttpClient(withFetch()) // מאפשר שימוש ב-HttpClient בכל האפליקציה
    // provideClientHydration() //withEventReplay()
  ]
};
