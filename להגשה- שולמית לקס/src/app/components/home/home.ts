import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-home',
  imports: [RouterLink, CommonModule],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home {
  canUploadRecipe(): boolean {
    const role = localStorage.getItem('user_role');
    return role === 'Uploader' || role === 'Admin';
  }

}
