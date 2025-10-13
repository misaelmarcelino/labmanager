import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

export interface ModalConfig {
  title?: string;
  message?: string;
  type?: 'info' | 'confirm' | 'form';
  data?: any;
  onConfirm?: (data?: any) => void;
  onCancel?: () => void;
}


@Injectable({ providedIn: 'root' })
export class ModalService {
  private modalState = new Subject<ModalConfig | null>();
  modalState$ = this.modalState.asObservable();

  open(config: ModalConfig) {
    this.modalState.next(config);
  }

  close() {
    this.modalState.next(null);
  }
}
