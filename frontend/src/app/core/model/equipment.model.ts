import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { DashboardComponent } from '../../features/portal/dashboard/dashboard.component';
import { EquipmentsComponent } from '../../features/portal/equipments/equipments.component';
import { PortalSidebarComponent } from '../../features/portal/layout/portal-sidebar/portal-sidebar.component';
import { SettingsComponent } from '../../features/portal/settings/settings.component';
import { UsersComponent } from '../../features/portal/users/users.component';
import { HeaderComponent } from '../../shared/header/header.component';

export interface Equipment {
  id: number;
  codigo: string;
  nome_do_posto: string;
  razao_uso?: string;
  versao_solucao: string;
  descricao: string;
  data_limite?: Date;  // ou tipo Date, dependendo do backend
  responsavel: string;
  status: string;
}
