import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Hder } from './hder/hder';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, Hder],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class App {
  protected readonly title = signal('front-downloader');
}
