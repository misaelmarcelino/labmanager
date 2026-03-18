import { Routes } from '@angular/router'
import { authGuard } from './core/auth.guard'
import { PortalComponent } from './features/portal/portal.component'

export const routes: Routes = [

  // Launcher de aplicações
  {
    path: '',
    loadComponent: () =>
      import('./features/apps/apps.component').then(m => m.AppsComponent)
  },
  {
    path:'standin',
    loadComponent: () =>
      import('./features/upload/upload.component').then(m => m.UploadComponent)
  },
  // Login
  {
    path: 'login',
    loadComponent: () =>
      import('./features/auth/login/login.component').then(m => m.LoginComponent)
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

  // Área protegida
  {
    path: 'portal',
    component: PortalComponent,
    canActivate: [authGuard],
    children: [

      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },

      {
        path: 'dashboard',
        loadComponent: () =>
          import('./features/portal/dashboard/dashboard.component')
            .then(m => m.DashboardComponent)
      },

      {
        path: 'equipamentos',
        loadComponent: () =>
          import('./features/portal/equipments/equipments.component')
            .then(m => m.EquipmentsComponent)
      },

      {
        path: 'usuarios',
        loadComponent: () =>
          import('./features/portal/users/users.component')
            .then(m => m.UsersComponent)
      },

      {
        path: 'relatorios',
        loadComponent: () =>
          import('./features/portal/reports/reports.component')
            .then(m => m.ReportsComponent)
      },

      {
        path: 'configuracoes',
        loadComponent: () =>
          import('./features/portal/settings/settings.component')
            .then(m => m.SettingsComponent)
      }

    ]
  },

  {
    path: '**',
    redirectTo: ''
  }

]
