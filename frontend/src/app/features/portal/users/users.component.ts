import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { AuthService } from '../../../core/services/auth.service';
import { UsersService } from '../../../core/services/users.service';

export interface User {
  id: number;
  username: string;
  email: string;
  role: string;
}

@Component({
  selector: 'app-users',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.scss']
})
export class UsersComponent implements OnInit {
  users: User[] = [];
  errorMessage: string | null = null;
  userRole: string | null = null;

  constructor(
    private auth: AuthService,
    private usersService: UsersService
  ) {}

  ngOnInit(): void {
    const u = this.auth.user;
    this.userRole = u ? u.role : null;
    this.loadUsers();
  }

  loadUsers(): void {
    this.usersService.listAll().subscribe({
      next: (usr) => {
        this.users = usr;
      },
      error: (err) => {
        console.error('Erro ao buscar usuários:', err);
        this.errorMessage = 'Não foi possível carregar usuários.';
      }
    });
  }
  newUser(): void {
    // Lógica para navegar para a página de criação de usuário
    // Por exemplo, usando o Router do Angular
    // this.router.navigate(['/portal/usuarios/novo']);
  }

  editUser(id: number): void {
    // Lógica para navegar para a página de edição de usuário
    // Por exemplo, usando o Router do Angular
    // this.router.navigate(['/portal/usuario/editar', id]);
  }

  isAdmin(): boolean {
    return this.userRole?.toLowerCase() === 'admin';
  }

  deleteUser(id: number): void {
    if (!confirm('Deseja realmente excluir este usuário?')) {
      return;
    }
    this.usersService.delete(id).subscribe({
      next: () => {
        this.loadUsers();
      },
      error: (err) => {
        console.error('Erro ao excluir usuário:', err);
        this.errorMessage = 'Erro ao excluir usuário.';
      }
    });
  }
}
