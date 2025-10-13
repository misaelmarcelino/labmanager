import { Component } from '@angular/core';
import { RouterLink } from "@angular/router";
import { AuthService } from '../../../../core/services/auth.service';

@Component({
  selector: 'app-portal-sidebar',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './portal-sidebar.component.html',
  styleUrl: './portal-sidebar.component.scss'
})
export class PortalSidebarComponent {

  constructor(private auth: AuthService) {}

  logout(): void {
    this.auth.logout();
  }
}
