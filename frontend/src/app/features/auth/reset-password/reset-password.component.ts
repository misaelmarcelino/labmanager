import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-reset-password',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './reset-password.component.html',
  styleUrls: ['./reset-password.component.scss']
})
export class ResetPasswordComponent {
  oldPassword = ''; // 👈 senha antiga
  newPassword = '';
  confirmPassword = '';
  email = '';
  errorMessage: string | null = null;
  successMessage: string | null = null;
  loading = false;

  private token: string | null = null;
  private isFirstAccess = false;

  constructor(
    private auth: AuthService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
  this.route.queryParams.subscribe(params => {
    this.token = params['token'] || null;
    this.email = params['email'] || '';
    this.isFirstAccess = params['first'] === 'true';

    // 🔹 recupera senha antiga da sessão
    if (this.isFirstAccess) {
      this.oldPassword = sessionStorage.getItem('old_password') || '';
    }
  });
  }

  submit(): void {
    if (this.isFirstAccess) {
      if (!this.oldPassword) {
        this.errorMessage = 'Senha anterior não encontrada. Faça login novamente.';
        return;
      }

      this.auth.changePassword(this.oldPassword, this.newPassword).subscribe({
        next: () => {
          // limpa senha da sessão
          sessionStorage.removeItem('old_password');
          this.successMessage = 'Senha alterada com sucesso! Faça login novamente.';
          setTimeout(() => this.router.navigate(['/login']), 2000);
        },
        error: (err: any) => {
          console.error('Erro ao alterar senha:', err);
          this.errorMessage = err.error?.detail || 'Erro ao alterar senha.';
        },
        complete: () => (this.loading = false)
      });
    }
  }

}
