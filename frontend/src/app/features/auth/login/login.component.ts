import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { HeaderComponent } from '../../../shared/header/header.component';

@Component({
  selector: 'app-login',
  standalone: true,
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
  imports: [CommonModule, FormsModule, RouterLink]
})
export class LoginComponent {
  email = '';
  password = '';
  errorMessage: string | null = null;
  loading = false;

  constructor(private auth: AuthService, private router: Router) {}

  login(): void {
    this.loading = true;
    this.errorMessage = null;

    const email = this.email.trim().toLowerCase();

    this.auth.login(email, this.password).subscribe({
      next: (response) => {
        this.loading = false;

        if (response.is_first_access) {
          this.router.navigate(['/redefinir-senha'], {
            queryParams: { email: email, first: true },
          });
        } else {
          const destino = response.role === 'ADMIN' ? '/portal' : '/home';
          this.router.navigate([destino]);
        }
      },
      error: () => {
        this.loading = false;
        this.errorMessage = 'Usuário ou senha incorretos.';
      }
    });
  }
}
