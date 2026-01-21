import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { finalize } from 'rxjs/operators';

import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-reset-password',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './reset-password.component.html',
  styleUrls: ['./reset-password.component.scss']
})
export class ResetPasswordComponent implements OnInit {

  // ===== FORM FIELDS =====
  email = ''
  oldPassword = '';
  newPassword = '';
  confirmPassword = '';

  // ===== UI STATE =====
  loading = false;
  errorMessage: string | null = null;
  successMessage: string | null = null;

  // ===== FLOW CONTROL =====
  isFirstAccess = false;
  private token: string | null = null;

  constructor(
    private auth: AuthService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  // =========================================================
  // =============== LIFECYCLE ===============================
  // =========================================================
  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.token = params['token'] ?? null;
      this.isFirstAccess = params['first'] === 'true';
      this.email = params['email'] ?? '';
    });
  }

  // =========================================================
  // =============== FORM SUBMIT ==============================
  // =========================================================
  submit(): void {
    this.resetMessages();

    if (!this.isPasswordValid()) {
      return;
    }

    this.loading = true;

    if (this.isFirstAccess) {
      this.handleFirstAccess();
      return;
    }

    this.handleTokenReset();
  }

  // =========================================================
  // =============== FLOWS ===================================
  // =========================================================

  /**
   * Fluxo de primeiro acesso
   * Exige senha atual + nova senha
   */
  private handleFirstAccess(): void {
    if(!this.email) {
      this.errorMessage = 'Email inválido ou ausente.';
      this.loading = false;
      return;
    }

    if (!this.oldPassword) {
      this.errorMessage = 'Informe sua senha atual.';
      this.loading = false;
      return;
    }

    this.auth.firstAccess(this.email, this.oldPassword, this.newPassword)
      .pipe(finalize(() => (this.loading = false)))
      .subscribe({
        next: () => {
          this.successMessage = 'Senha definida com sucesso! Faça login.';
          this.redirectToLogin();
        },
        error: (err) => {
          this.errorMessage = err.error?.detail || 'Senha atual incorreta.';
        }
    });
  }

  /**
   * Fluxo de reset por token
   * Exige token + nova senha
   */
  private handleTokenReset(): void {
    if (!this.token) {
      this.errorMessage = 'Token inválido ou ausente.';
      this.loading = false;
      return;
    }

    this.auth.resetPassword(this.token, this.newPassword)
      .pipe(finalize(() => (this.loading = false)))
      .subscribe({
        next: () => {
          this.successMessage = 'Senha redefinida com sucesso! Faça login.';
          this.redirectToLogin();
        },
        error: (err) => {
          this.errorMessage = err.error?.detail || 'Erro ao redefinir senha.';
        }
      });
  }

  // =========================================================
  // =============== HELPERS =================================
  // =========================================================

  private isPasswordValid(): boolean {
    if (!this.newPassword || !this.confirmPassword) {
      this.errorMessage = 'Preencha todos os campos.';
      return false;
    }

    if (this.newPassword !== this.confirmPassword) {
      this.errorMessage = 'As senhas não conferem.';
      return false;
    }

    return true;
  }

  private resetMessages(): void {
    this.errorMessage = null;
    this.successMessage = null;
  }

  private redirectToLogin(): void {
    setTimeout(() => {
      this.router.navigate(['/login']);
    }, 2000);
  }
}
