import { Component } from '@angular/core';
import { Router, RouterLink } from "@angular/router";
import { AuthService } from '../../../../core/services/auth.service';

@Component({
  selector: 'app-portal-sidebar',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './portal-sidebar.component.html',
  styleUrl: './portal-sidebar.component.scss'
})
export class PortalSidebarComponent {

  constructor(private auth: AuthService, private router: Router) {}

  logout(): void {
    this.auth.logout();
    localStorage.removeItem('auth_token');
    this.router.navigate(['/login']);
  }
}
