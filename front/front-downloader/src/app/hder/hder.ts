import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
// 1. Importamos NgbCollapseModule
import { NgbCollapseModule } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-hder',
  standalone: true,
  // 2. Lo agregamos a los imports (junto con RouterLinkActive)
  imports: [RouterLink, RouterLinkActive, NgbCollapseModule],
  templateUrl: './hder.html',
  styleUrls: ['./hder.css'],
})
export class Hder {
  // 3. Variable para controlar el estado del menú (cerrado por defecto)
  isMenuCollapsed = true;
}
