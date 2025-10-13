import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { AuthService } from '../../../core/services/auth.service';
import { UsersService } from '../../../core/services/users.service';
import { UserModalComponent } from '../../../shared/modal/user-modal/user-modal.component';
import { ModalComponent } from '../../../shared/modal/modal.component';
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
  imports: [CommonModule, RouterModule, UserModalComponent,],
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.scss']
})
export class UsersComponent implements OnInit {
  users: User[] = [];
  errorMessage: string | null = null;
  userRole: string | null = null;
  showUserModal = false;

  constructor(
    private auth: AuthService,
    private usersService: UsersService,
    private modalService: ModalService
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


  // createUser(newUser: { name: string; email: string; role: string }): void {
  //   this.usersService.create(newUser).subscribe({
  //     next: (response) => {
  //       console.log('Usuário criado:', response);
  //       this.showUserModal = false;
  //       this.loadUsers();
  //       alert('✅ Usuário cadastrado com sucesso!');
  //     },
  //     error: (err) => {
  //       console.error('Erro ao salvar usuário:', err);
  //       this.errorMessage = 'Erro ao salvar usuário.';
  //     }
  //   });
  // }
  openCreateUserModal() {
    this.modalService.open({
      title: 'Novo Usuário',
      type: 'form',
      data: {}, // formulário vazio
      onConfirm: (newUser) => this.createUser(newUser)
    });
  }

  /** 🔹 Cria novo usuário */
  createUser(newUser: { name: string; email: string; role: string }): void {
    const payload = {
      ...newUser,
      role: newUser.role?.toUpperCase() || 'USER' // garante padrão válido
    };

    this.usersService.create(payload).subscribe({
      next: (response) => {
        console.log('✅ Usuário criado:', response);
        this.loadUsers();
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


  editUser(user: any) {
    this.modalService.open({
      title: 'Editar Usuário',
      type: 'form',
      data: user, // 👈 importante!
      onConfirm: (updated) => this.updateUser(user.id, updated)
    });
  }

  updateUser(id: number, data: any) {
    console.log(`Usuário ${id} atualizado:`, data);
    const index = this.users.findIndex(u => u.id === id);
    if (index !== -1) this.users[index] = { ...this.users[index], ...data };
  }

  isAdmin(): boolean {
    return this.userRole?.toLowerCase() === 'admin';
  }

  confirmDelete(userId: number) {
    this.modalService.open({
      title: 'Excluir Usuário',
      message: 'Tem certeza que deseja excluir este usuário?',
      type: 'confirm',
      onConfirm: () => this.deleteUser(userId)
    });
  }
  deleteUser(id: number) {
    console.log('🗑️ Usuário excluído:', id);
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

  showInfo() {
    this.modalService.open({
      title: 'Informação',
      message: 'Usuário criado com sucesso!',
      type: 'info'
    });
  }
}
