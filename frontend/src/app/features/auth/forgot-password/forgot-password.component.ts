// src/app/modules/forgot-password/forgot-password.component.ts

import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-forgot-password',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.scss'],
})
export class ForgotPasswordComponent {
  email = '';
  errorMessage: string | null = null;
  successMessage: string | null = null;
  loading = false;

  constructor(private auth: AuthService ) {}

  submit(): void {
    this.errorMessage = null;
    this.successMessage = null;

    const email = this.email.trim().toLowerCase();

    if (email) {
      this.errorMessage = 'Informe um email válido.';
      return;
    }

    this.loading = true;

    this.auth.requestPasswordReset(email).subscribe({
      next: () => {
        this.successMessage = 'Se esse email estiver cadastrado, você receberá instruções para redefinir sua senha.';
      },
      error: (err: any) => {
        console.error('Erro ao solicitar redefinição de senha:', err);
        this.errorMessage = 'Ocorreu um erro. Tente novamente mais tarde.';
      },
      complete: () => {
        this.loading = false;
      }
    });
  }
}
