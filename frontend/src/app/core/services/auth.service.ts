// src/app/core/auth.service.ts

import { Injectable, signal } from '@angular/core';
import { Router } from '@angular/router';
import { Observable, map, tap } from 'rxjs';
import { ApiService } from './api.service';
import { User } from '../model/user.model';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private _user = signal<User | null>(null);

  get user(): User | null {
    return this._user();
  }

  get isLoggedIn(): boolean {
    return !!this._user();
  }

  constructor(private api: ApiService, private router: Router) {}

  login(email: string, password: string): Observable<User> {
    // usar ApiService.post para chamar “auth/login”
    return this.api.post<{
      access_token: string;
      email: string;
      name: string;
      role: string;
      token_type: string;
    }>('auth/login', { email, password }).pipe(
      tap(response => {
        localStorage.setItem('auth_token', response.access_token);
        const user: User = {
          email: response.email,
          name: response.name,
          role: response.role
        };
        this._user.set(user);
      }),
      map(response => ({
        email: response.email,
        name: response.name,
        role: response.role
      }))
    );
  }

  logout(): void {
    this._user.set(null);
    localStorage.removeItem('auth_token');
    this.router.navigate(['/login']);
  }

  hasRole(role: string): boolean {
    const u = this._user();
    return u ? u.role === role : false;
  }

  requestPasswordReset(email: string): Observable<any> {
    return this.api.post<any>('auth/forgot-password', { email });
  }

  resetPassword(token: string, newPassword: string): Observable<any> {
    return this.api.post<any>('auth/reset-password', {
      token,
      new_password: newPassword
    });
  }
}
