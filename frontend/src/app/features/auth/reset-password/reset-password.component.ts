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
  styleUrl: './reset-password.component.scss'
})
export class ResetPasswordComponent {
  newPassword = '';
  confirmPassword = '';
  errorMessage: string | null = null;
  successMessage: string | null = null;
  loading = false;

  private token: string | null = null;

  constructor(
    private auth: AuthService,
    private route: ActivatedRoute,
    private router: Router
  ) {
    // Recupera o token da URL, se for passado como parâmetro de rota ou query
    this.route.queryParams.subscribe(params => {
      this.token = params['token'] || null;
    });
  }

  submit(): void {
    this.errorMessage = null;
    this.successMessage = null;

    if (!this.newPassword || !this.confirmPassword) {
      this.errorMessage = 'Por favor, preencha todos os campos.';
      return;
    }
    if (this.newPassword !== this.confirmPassword) {
      this.errorMessage = 'As senhas não coincidem.';
      return;
    }
    if (!this.token) {
      this.errorMessage = 'Token inválido ou expirado.';
      return;
    }

    this.loading = true;

    this.auth.resetPassword(this.token, this.newPassword).subscribe({
      next: () => {
        this.successMessage = 'Senha redefinida com sucesso! Você será redirecionado para o login.';
        // opcional: aguardar alguns segundos antes de redirecionar
        setTimeout(() => {
          this.router.navigate(['/login']);
        }, 3000);
      },
      error: (err: any) => {
        console.error('Erro ao redefinir senha:', err);
        this.errorMessage = 'Erro ao redefinir senha. Tente novamente mais tarde.';
      },
      complete: () => {
        this.loading = false;
      }
    });
  }
}
