import { Component, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormGroup, FormControl, Validators } from '@angular/forms';
import { ModalService, ModalConfig } from './../../core/services/modal.service';

@Component({
  selector: 'app-modal',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './modal.component.html',
  styleUrls: ['./modal.component.scss']
})
export class ModalComponent {
  visible = false;
  config: ModalConfig = {};
  form: FormGroup = new FormGroup({}); // garante existência do form (sem undefined)

  constructor(
    private modalService: ModalService,
    private cdr: ChangeDetectorRef
  ) {
    this.modalService.modalState$.subscribe(cfg => {
      cfg ? this.open(cfg) : this.close();
    });
  }

  /** 🔹 Abre o modal e inicializa o conteúdo */
  private open(cfg: ModalConfig): void {
    this.config = cfg;
    this.visible = true;

    if (cfg.type === 'form') {
      this.initializeForm(cfg.data);
    }

    // força renderização do Angular
    this.cdr.detectChanges();
  }

  /** 🔹 Fecha o modal */
  private close(): void {
    this.visible = false;
    this.form.reset(); // limpa campos, mas mantém estrutura do FormGroup
  }

  /** 🔹 Inicializa o formulário com dados de edição */
  private initializeForm(data: any = {}): void {
    this.form = new FormGroup({
      name: new FormControl(data.name ?? '', Validators.required),
      email: new FormControl(data.email ?? '', [Validators.required, Validators.email]),
      role: new FormControl(data.role ?? '', Validators.required)
    });

    // 🔹 aplica os valores dinamicamente (preenche campos)
    if (data) {
      this.form.patchValue({
        name: data.name ?? '',
        email: data.email ?? '',
        role: data.role.toUpperCase() ?? ''
      });
    }

    // 🔹 força o Angular a detectar os novos valores na view
    this.cdr.detectChanges();
  }

  /** 🔹 Confirma a ação (envia dados se for form) */
  confirm(): void {
    if (this.config.type === 'form' && this.form.valid) {
      this.config.onConfirm?.(this.form.value);

    } else {
      this.config.onConfirm?.();
    }
    this.modalService.close();
  }

  /** 🔹 Cancela e fecha o modal */
  cancel(): void {
    this.config.onCancel?.();
    this.modalService.close();
  }
}
