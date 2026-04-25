import { Component, signal } from '@angular/core';
import { RouterOutlet, RouterLinkWithHref } from '@angular/router';
import { Navbar } from './components/navbar/navbar';

@Component({
  selector: 'app-root', // התגית הראשית שמופיעה ב-index.html
  imports: [RouterOutlet, Navbar, RouterLinkWithHref],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('client');
}
