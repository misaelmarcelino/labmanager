import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-user-modal',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './user-modal.component.html',
  styleUrls: ['./user-modal.component.scss']
})
export class UserModalComponent {
  @Output() onSave = new EventEmitter<any>();
  @Output() onCancel = new EventEmitter<void>();

  user = {
    name: '',
    email: '',
    role: 'USER'
  };

  save() {
    this.onSave.emit({
      name: this.user.name,
      email: this.user.email,
      role: this.user.role.toUpperCase()
    });
  }

  cancel() {
    this.onCancel.emit();
  }
}
