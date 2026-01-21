import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { UsersService } from '../../../core/services/users.service';
import { AuthService } from '../../../core/services/auth.service';
@Component({
  selector: 'app-settings',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss']
})
export class SettingsComponent implements OnInit {

  user: any = {
    name: '',
    email: '',
    role: ''
  };

  oldPassword = '';
  newPassword = '';
  confirmPassword = '';

  isLoading = false;

  constructor(private userService: UsersService, private authService: AuthService) {}

  ngOnInit(): void {
    this.loadProfile();
  }

  loadProfile() {
    this.userService.getProfile().subscribe({
      next: (data) => (this.user = data),
      error: () => console.error('Erro ao carregar perfil')
    });
  }

  saveProfile() {
    this.isLoading = true;
    this.userService.updateProfile(this.user).subscribe({
      next: () => {
        alert('Perfil atualizado com sucesso!');
        this.isLoading = false;
      },
      error: () => {
        alert('Erro ao atualizar perfil.');
        this.isLoading = false;
      }
    });
  }

  changePassword() {
    if (this.newPassword !== this.confirmPassword) {
      alert('As senhas não coincidem!');
      return;
    }

    this.authService.resetPassword(this.oldPassword, this.newPassword).subscribe({
      next: () => {
        alert('Senha alterada com sucesso!');
        this.oldPassword = '';
        this.newPassword = '';
        this.confirmPassword = '';
      },
      error: () => alert('Erro ao alterar senha.')
    });
  }
}
