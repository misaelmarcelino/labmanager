import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { UsersService } from '../../../core/services/users.service';
import { EquipmentsService } from '../../../core/services/equipments.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  totalUsers = 0;
  totalEquipments = 0;
  approvedCount = 0;
  pendingCount = 0;
  rejectedCount = 0;

  loading = true;
  errorMessage: string | null = null;

  constructor(
    private usersService: UsersService,
    private equipmentsService: EquipmentsService
  ) {}

  ngOnInit(): void {
    this.loadDashboardData();
  }

  /** 🔹 Carrega todos os dados do dashboard */
  loadDashboardData() {
    this.loading = true;

    Promise.all([
      this.usersService.listAll().toPromise(),
      this.equipmentsService.listAll().toPromise()
    ])
      .then(([users, equipments]) => {
        this.totalUsers = users!.length;
        this.totalEquipments = equipments!.length;

        // Contagem por status
        this.approvedCount = equipments!.filter(eq => eq.status === 'APROVADO').length;
        this.pendingCount = equipments!.filter(eq => eq.status === 'PENDENTE').length;
        this.rejectedCount = equipments!.filter(eq => eq.status === 'REPROVADO').length;
      })
      .catch(err => {
        console.error('Erro ao carregar dashboard:', err);
        this.errorMessage = 'Não foi possível carregar os dados do dashboard.';
      })
      .finally(() => {
        this.loading = false;
      });
  }
}
