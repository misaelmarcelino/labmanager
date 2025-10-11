import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

import { AuthService } from '../../../core/services/auth.service';
import { User } from '../../../core/model/user.model';
import { HeaderComponent } from '../../../shared/header/header.component';

@Component({
  selector: 'app-login',
  standalone: true,
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
  imports: [CommonModule, FormsModule, HeaderComponent]
})
export class LoginComponent {
  email = '';
  password = '';
  errorMessage: string | null = null;

  constructor(private auth: AuthService, private router: Router) {}

  login(): void {
    this.errorMessage = null;

    this.auth.login(this.email, this.password).subscribe({
      next: (user: User) => {

        const destino = user.role === 'ADMIN' ? '/portal' : '/home';

        this.router.navigate([destino]);
      },
      error: (err: any) => {
        this.errorMessage = 'Usuário ou senha incorretos.';
      }
    });
  }
}
