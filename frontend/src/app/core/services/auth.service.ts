// src/app/core/auth.service.ts

import { Injectable, signal } from '@angular/core';
import { Router } from '@angular/router';
import { Observable, map, tap } from 'rxjs';
import { ApiService } from './api.service';
import { User } from '../model/user.model';
import { catchError, of } from 'rxjs';

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
    return this.api.post<{
      access_token: string;
      email: string;
      name: string;
      role: string;
      token_type: string;
      is_first_access: boolean;
    }>('auth/login', { email, password }).pipe(
      tap(response => {
        localStorage.setItem('auth_token', response.access_token);

        const user: User = {
          email: response.email,
          name: response.name,
          role: response.role,
          is_first_access: response.is_first_access
        };

        this._user.set(user);
      }),
      map(response => ({
        email: response.email,
        name: response.name,
        role: response.role,
        is_first_access: response.is_first_access
      }))
    );
  }


  logout(): void {
    this._user.set(null);
    localStorage.removeItem('auth_token');
  }

  hasRole(role: string): boolean {
    const u = this._user();
    return u ? u.role === role : false;
  }

  requestPasswordReset(email: string): Observable<any> {
    return this.api.post<any>('auth/forgot-password', { email });
  }

  resetPassword(token: string, newPassword: string): Observable<any> {
    return this.api.post<any>('auth/reset-password/confirm', {
      token,
      new_password: newPassword
    });
  }

  firstAccess(email: string, tempPassword: string, newPassword: string): Observable<any> {
    return this.api.post<any>('auth/first-access', {
      email,
      temp_password: tempPassword,
      new_password: newPassword
    });
  }

  loadCurrentUser(): Observable<User | null> {
    return this.api.get<any>('users/me').pipe(
      tap(user => {
        this._user.set({
          email: user.email,
          name: user.name,
          role: user.role,
          is_first_access: false
        });
      }),
      catchError(() => {
        this._user.set(null);
        return of(null);
      })
    );
  }



}
