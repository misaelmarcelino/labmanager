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
    console.log('🧩 Tipo de entidade recebido:', this.config.entityType);

    if (this.config.entityType === 'equipment') {
      this.form = new FormGroup({
        codigo: new FormControl(data.codigo ?? '', Validators.required),
        nome_do_posto: new FormControl(data.nome_do_posto ?? '', Validators.required),
        razao_uso: new FormControl(data.razao_uso ?? '', Validators.required),
        versao_solucao: new FormControl(data.versao_solucao ?? '', Validators.required),
        descricao: new FormControl(data.descricao ?? '', Validators.required),
        data_limite: new FormControl(data.data_limite ?? '', Validators.required),
        responsavel: new FormControl(data.responsavel ?? '', Validators.required),
        status: new FormControl(data.status ?? 'PENDENTE', Validators.required)
      });
    } else {
      this.form = new FormGroup({
        name: new FormControl(data.name ?? '', Validators.required),
        email: new FormControl(data.email ?? '', [Validators.required, Validators.email]),
        role: new FormControl((data.role ?? 'USER').toUpperCase())
      });
    }
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
