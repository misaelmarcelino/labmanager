import { Routes } from '@angular/router';
import { authGuard } from './core/auth.guard';
import { PortalComponent } from './features/portal/portal.component';


export const routes: Routes = [
  {
    path: 'login',
    loadComponent: () =>
      import('./features/auth/login/login.component').then(m => m.LoginComponent),
  },
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full'
  },
  {
      path: 'esqueci-senha',
      loadComponent: () =>
      import('./features/auth/forgot-password/forgot-password.component')
            .then(m => m.ForgotPasswordComponent)
  },
  {
      path: 'redefinir-senha',
      loadComponent: () =>
      import('./features/auth/reset-password/reset-password.component')
            .then(m => m.ResetPasswordComponent)
  },
  {
    path: 'portal',
    component: PortalComponent,
    canActivate: [authGuard],
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      { path: 'dashboard', loadComponent: () => import('./features/portal/dashboard/dashboard.component').then(m => m.DashboardComponent) },
      { path: 'equipamentos', loadComponent: () => import('./features/portal/equipments/equipments.component').then(m => m.EquipmentsComponent) },
      { path: 'usuarios', loadComponent: () => import('./features/portal/users/users.component').then(m => m.UsersComponent) },
      { path: 'relatorios', loadComponent: () => import('./features/portal/reports/reports.component').then(m => m.ReportsComponent) },
      { path: 'configuracoes', loadComponent: () => import('./features/portal/settings/settings.component').then(m => m.SettingsComponent) },
      { path: '', redirectTo: 'portal', pathMatch: 'full' }
    ]
  },
  {
    path: 'home',
    loadComponent: () =>
      import('./features/home/home.component').then(m => m.HomeComponent),
    // canActivate: [authGuard]
  },
  {
    path: '**',
    redirectTo: 'login'
  }
];
