import { Component, OnInit } from '@angular/core';
import { Equipment } from '../../core/model/equipment.model';
import { EquipmentsService } from '../../core/services/equipments.service';
import { AuthService } from '../../core/services/auth.service';
import { CommonModule, DatePipe } from '@angular/common';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, DatePipe],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  equipamentos: Equipment[] = [];
  errorMessage: string | null = null;
  userRole: string | null = null;

  constructor(
    private auth: AuthService,
    private equipmentService: EquipmentsService
  ) {}

  ngOnInit(): void {
    const user = this.auth.user;
    this.userRole = user ? user.role : null;
    this.loadEquipamentos();
  }

  loadEquipamentos(): void {
    this.equipmentService.listAll().subscribe({
      next: eq => {
        this.equipamentos = eq;
      },
      error: err => {
        console.error('Erro ao buscar equipamentos:', err);
        this.errorMessage = 'Não foi possível carregar equipamentos';
      }
    });
  }

  isAdmin(): boolean {
    return this.userRole?.toLowerCase() === 'admin';
  }

  deleteEquipment(id: number): void {
    if (!confirm('Deseja realmente excluir este equipamento?')) {
      return;
    }
    this.equipmentService.delete(id).subscribe({
      next: () => this.loadEquipamentos(),
      error: err => {
        console.error('Erro ao excluir equipamento:', err);
        this.errorMessage = 'Erro ao excluir equipamento';
      }
    });
  }
}
