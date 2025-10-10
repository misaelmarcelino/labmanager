// src/app/core/auth.service.ts
import { Injectable, signal } from '@angular/core';
import { Router } from '@angular/router';
import { User } from './model/user.model';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private _user = signal<User | null>(null);

  get user() {
    return this._user();
  }

  get isLoggedIn(): boolean {
    return !!this._user();
  }

  login(username: string, password: string): void {
    // Aqui você chamaria seu backend e obteria token + papel
    // Por enquanto, simulação:
    const fakeUser: User = {
      username,
      role: username === 'admin' ? 'admin' : 'user'
    };
    this._user.set(fakeUser);
  }

  logout(): void {
    this._user.set(null);
    this.router.navigate(['/login']);
  }

  hasRole(role: string): boolean {
    const u = this._user();
    return u ? u.role === role : false;
  }

  constructor(private router: Router) {}
}
