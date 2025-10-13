import { Component } from '@angular/core';
import { PortalSidebarComponent } from './layout/portal-sidebar/portal-sidebar.component';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from '../../shared/header/header.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { EquipmentsComponent } from './equipments/equipments.component';
import { UsersComponent } from './users/users.component';
import { SettingsComponent } from './settings/settings.component';

@Component({
  selector: 'app-portal',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    HeaderComponent,
    PortalSidebarComponent,
    DashboardComponent,
    EquipmentsComponent,
    UsersComponent,
    SettingsComponent
  ],
  templateUrl: './portal.component.html',
  styleUrl: './portal.component.scss'
})
export class PortalComponent {

}
