import { CanActivateFn } from '@angular/router';
import { inject } from '@angular/core';
import { AuthService } from './services/auth.service';
import { Router } from '@angular/router';

export const authGuard: CanActivateFn = (route, state) => {
  const auth = inject(AuthService);
  const router = inject(Router);

  if (!auth.isLoggedIn) {
    return router.createUrlTree(['/login']);
  }

  const requiredRole = route.data?.['role'] as string | undefined;
  if (requiredRole) {
    const userRole = auth.user?.role ?? '';
    if (userRole.toLowerCase() !== requiredRole.toLowerCase()) {
      return router.createUrlTree(['/home']);
    }
  }

  console.log('Guard: rota permitida');
  return true;
};


