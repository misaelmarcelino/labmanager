import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { AuthService } from '../../../core/services/auth.service';
import { UsersService } from '../../../core/services/users.service';
import { ModalService } from '../../../core/services/modal.service';

export interface User {
  id: number;
  name: string;
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
    private usersService: UsersService,
    private modalService: ModalService
  ) {}

  ngOnInit(): void {
    const user = this.auth.user;
    this.userRole = user ? user.role : null;
    this.loadUsers();
  }

  /** 🔹 Carrega todos os usuários */
  loadUsers(): void {
    this.usersService.listAll().subscribe({
      next: (usr) => (this.users = usr),
      error: (err) => {
        console.error('Erro ao buscar usuários:', err);
        this.errorMessage = 'Não foi possível carregar usuários.';
      }
    });
  }

  /** 🔹 Abrir modal para novo usuário */
  openCreateUserModal(): void {
    this.modalService.open({
      title: 'Novo Usuário',
      type: 'form',
      entityType: 'user', // 👈 define tipo
      data: {}, // vazio
      onConfirm: (newUser) => this.createUser(newUser)
    });
  }

  /** 🔹 Criar novo usuário */
  createUser(newUser: { name: string; email: string; role: string }): void {
    const payload = {
      ...newUser,
      role: newUser.role?.toUpperCase() || 'USER'
    };

    this.usersService.create(payload).subscribe({
      next: (response) => {
        console.log('✅ Usuário criado:', response);
        this.loadUsers();

        // Mensagem de sucesso
        this.modalService.open({
          title: 'Sucesso!',
          message: 'Usuário cadastrado com sucesso!',
          type: 'info'
        });
      },
      error: (err) => {
        console.error('Erro ao salvar usuário:', err);
        this.errorMessage = 'Erro ao salvar usuário.';
      }
    });
  }

  /** 🔹 Editar usuário existente */
  editUser(user: User): void {
    this.modalService.open({
      title: 'Editar Usuário',
      type: 'form',
      entityType: 'user', // 👈 define tipo
      data: user,
      onConfirm: (updated) => this.updateUser(user.id, updated)
    });
  }

  /** 🔹 Atualiza dados do usuário */
  updateUser(id: number, data: any): void {
    const payload = {
      ...data,
      role: data.role?.toUpperCase() || 'USER'
    };

    this.usersService.update(id, payload).subscribe({
      next: () => {
        console.log(`Usuário ${id} atualizado.`);
        this.loadUsers();
      },
      error: (err) => {
        console.error('Erro ao atualizar usuário:', err);
        this.errorMessage = 'Erro ao atualizar usuário.';
      }
    });
  }

  /** 🔹 Confirmar exclusão */
  confirmDelete(userId: number): void {
    this.modalService.open({
      title: 'Excluir Usuário',
      message: 'Tem certeza que deseja excluir este usuário?',
      type: 'confirm',
      onConfirm: () => this.deleteUser(userId)
    });
  }

  /** 🔹 Excluir usuário */
  deleteUser(id: number): void {
    this.usersService.delete(id).subscribe({
      next: () => this.loadUsers(),
      error: (err) => {
        console.error('Erro ao excluir usuário:', err);
        this.errorMessage = 'Erro ao excluir usuário.';
      }
    });
  }

  /** 🔹 Verifica se usuário logado é admin */
  isAdmin(): boolean {
    return this.userRole?.toLowerCase() === 'admin';
  }
}
