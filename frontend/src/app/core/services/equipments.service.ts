// src/app/features/portal/services/equipments.service.ts

import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from '../../core/services/api.service';
import { Equipment } from '../model/equipment.model';

@Injectable({
  providedIn: 'root'
})
export class EquipmentsService {
  constructor(private api: ApiService) {}

  listAll(): Observable<Equipment[]> {
    return this.api.get<Equipment[]>('equipments');
  }

  getById(id: number): Observable<Equipment> {
    return this.api.get<Equipment>(`equipments/${id}`);
  }

  create(equipment: Omit<Equipment, 'id'>): Observable<Equipment> {
    return this.api.post<Equipment>('equipments', equipment);
  }

  update(id: number, equipment: Partial<Equipment>): Observable<Equipment> {
    return this.api.put<Equipment>(`equipments/${id}`, equipment);
  }

  delete(id: number): Observable<void> {
    return this.api.delete<void>(`equipments/${id}`);
  }
}
