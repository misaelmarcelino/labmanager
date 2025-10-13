import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-equipment-modal',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './equipment-modal.component.html',
  styleUrls: ['./equipment-modal.component.scss']
})
export class EquipmentModalComponent {
  @Output() onSave = new EventEmitter<any>();
  @Output() onCancel = new EventEmitter<void>();

  equipment = {
    codigo: '',
    nome_posto: '',
    razao_uso: '',
    vs_solucao: '',
    motivo_homologacao: '',
    data_limite_homologacao: '',
    responsavel: '',
    status_equip: 'Em homologação'
  };

  save() {
    this.onSave.emit(this.equipment);
  }

  cancel() {
    this.onCancel.emit();
  }
}
