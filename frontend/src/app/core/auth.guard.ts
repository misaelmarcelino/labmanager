import { CanActivateFn } from '@angular/router';
import { inject } from '@angular/core';
import { AuthService } from './auth.service';
import { Router } from '@angular/router';

export const authGuard: CanActivateFn = (route, state) => {
  const auth = inject(AuthService);
  const router = inject(Router);

  if (!auth.isLoggedIn) {
    return router.createUrlTree(['/login']);
  }
  const requiredRole = route.data?.['role'] as string | undefined;
  if (requiredRole && !auth.hasRole(requiredRole)) {
    return router.createUrlTree(['/equipments']);
  }
  return true;
};
