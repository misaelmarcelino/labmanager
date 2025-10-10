import { Routes } from '@angular/router';
import { authGuard } from './core/auth.guard';

export const routes: Routes = [
  {
    path: 'login',
    loadComponent: () => import('./modules/login/login.component').then(m => m.LoginComponent)
  },
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full'
  },
  {
    path: 'dashboard',
    loadComponent: () => import('./modules/dashboard/dashboard.component').then(m => m.DashboardComponent),
    canActivate: [authGuard],
    data: { role: 'admin' }
  },
  {
    path: 'equipments',
    loadComponent: () => import('./modules/home/home.component').then(m => m.HomeComponent),
    canActivate: [authGuard]
  },
  // opcional: rota de “not-found” ou “acesso negado”
  {
    path: '**',
    redirectTo: 'login'
  }
];
