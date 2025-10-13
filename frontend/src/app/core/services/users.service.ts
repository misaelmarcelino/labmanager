// src/app/features/portal/services/users.service.ts

import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';

export interface User {
  id: number;
  name: string;
  email: string;
  role: string;
}
export interface CreateUserResponse {
  message: string;
  user: User;
}

@Injectable({
  providedIn: 'root'
})
export class UsersService {
  constructor(private api: ApiService) {}

  listAll(): Observable<User[]> {
    return this.api.get<User[]>('users');
  }

  getById(id: number): Observable<User> {
    return this.api.get<User>(`users/${id}`);
  }

  create(user: Omit<User, 'id'>): Observable<CreateUserResponse> {
    return this.api.post<CreateUserResponse>('users', user);
  }

  update(id: number, user: Partial<User>): Observable<User> {
    return this.api.put<User>(`users/${id}`, user);
  }

  delete(id: number): Observable<void> {
    return this.api.delete<void>(`users/${id}`);
  }
}
