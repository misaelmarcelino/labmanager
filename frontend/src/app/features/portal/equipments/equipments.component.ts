import { Component, OnInit } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { Equipment } from '../../../core/model/equipment.model';
import { EquipmentsService } from '../../../core/services/equipments.service';
import { AuthService } from '../../../core/services/auth.service';
import { ModalService } from '../../../core/services/modal.service';

@Component({
  selector: 'app-equipments',
  standalone: true,
  imports: [CommonModule, DatePipe],
  templateUrl: './equipments.component.html',
  styleUrls: ['./equipments.component.scss']
})
export class EquipmentsComponent implements OnInit {
  equipamentos: Equipment[] = [];
  errorMessage: string | null = null;
  userRole: string | null = null;

  constructor(
    private auth: AuthService,
    private equipmentService: EquipmentsService,
    private modalService: ModalService
  ) {}

  ngOnInit(): void {
    const user = this.auth.user;
    this.userRole = user ? user.role : null;
    this.loadEquipamentos();
  }

  /** 🔹 Carrega lista de equipamentos */
  loadEquipamentos(): void {
    this.equipmentService.listAll().subscribe({
      next: (eqs) => (this.equipamentos = eqs),
      error: (err) => {
        console.error('Erro ao buscar equipamentos:', err);
        this.errorMessage = 'Não foi possível carregar equipamentos.';
      }
    });
  }

  /** 🔹 Abre modal para criar novo equipamento */
  openCreateEquipmentModal(): void {
    this.modalService.open({
      title: 'Novo Equipamento',
      type: 'form',
      entityType: 'equipment',
      data: {}, // sem dados — novo registro
      onConfirm: (newEq) => this.createEquipment(newEq)
    });
  }

  /** 🔹 Cria novo equipamento */
  createEquipment(newEq: any): void {
    const payload = {
      ...newEq,
      status: newEq.status || 'Pendente'
    };

    this.equipmentService.create(payload).subscribe({
      next: () => {
        this.loadEquipamentos();
        this.modalService.open({
          title: 'Sucesso!',
          message: 'Equipamento cadastrado com sucesso!',
          type: 'info'
        });
      },
      error: (err) => {
        console.error('Erro ao criar equipamento:', err);
        this.errorMessage = 'Erro ao criar equipamento.';
      }
    });
  }

  /** 🔹 Abre modal para editar equipamento */
  editEquipment(equipment: Equipment): void {
    this.modalService.open({
      title: 'Editar Equipamento',
      type: 'form',
      entityType: 'equipment', // indica ao modal o tipo de formulário
      data: equipment,         // dados existentes — para preencher o form
      onConfirm: (updated) => this.updateEquipment(equipment.id, updated)
    });
  }

  /** 🔹 Atualiza equipamento */
  updateEquipment(id: number, data: any): void {
    this.equipmentService.update(id, data).subscribe({
      next: () => {
        this.loadEquipamentos();
        this.modalService.open({
          title: 'Sucesso!',
          message: 'Equipamento atualizado com sucesso!',
          type: 'info'
        });
      },
      error: (err) => {
        console.error('Erro ao atualizar equipamento:', err);
        this.errorMessage = 'Erro ao atualizar equipamento.';
      }
    });
  }

  /** 🔹 Confirma exclusão antes de deletar */
  confirmDelete(id: number): void {
    this.modalService.open({
      title: 'Excluir Equipamento',
      message: 'Deseja realmente excluir este equipamento?',
      type: 'confirm',
      onConfirm: () => this.deleteEquipment(id)
    });
  }

  /** 🔹 Exclui equipamento */
  deleteEquipment(id: number): void {
    this.equipmentService.delete(id).subscribe({
      next: () => this.loadEquipamentos(),
      error: (err) => {
        console.error('Erro ao excluir equipamento:', err);
        this.errorMessage = 'Erro ao excluir equipamento.';
      }
    });
  }

  /** 🔹 Verifica se é administrador */
  isAdmin(): boolean {
    return this.userRole?.toLowerCase() === 'admin';
  }
}
