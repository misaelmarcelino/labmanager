import { Component, OnInit } from '@angular/core';
import { Router, RouterLink } from "@angular/router";
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss'
})
export class HeaderComponent implements OnInit {

    user = {
    name: '',
    email: '',
    role: ''
  };

  constructor(private auth: AuthService, private router: Router) {}

  ngOnInit(): void {
    const authUser = this.auth.user;

    if (authUser) {
      this.user = authUser;
    } else {
      const token = localStorage.getItem('auth_token');
      if (token) {
        const storedUser = localStorage.getItem('user_data');
        if (storedUser) {
          this.user = JSON.parse(storedUser);
        }
      }
    }
  }

  logout(): void {
    this.auth.logout();
    localStorage.removeItem('auth_token');
    this.router.navigate(['/login']);
  }


}
