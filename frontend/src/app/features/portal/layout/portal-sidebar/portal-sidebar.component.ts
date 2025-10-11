import { Component } from '@angular/core';
import { RouterLink } from "@angular/router";

@Component({
  selector: 'app-portal-sidebar',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './portal-sidebar.component.html',
  styleUrl: './portal-sidebar.component.scss'
})
export class PortalSidebarComponent {

  logout(): void {
    // lógica de logout
  }
}
