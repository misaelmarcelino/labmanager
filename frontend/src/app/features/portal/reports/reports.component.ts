import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormGroup, FormControl } from '@angular/forms';
import { EquipmentsService } from '../../../core/services/equipments.service';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-reports',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './reports.component.html',
  styleUrls: ['./reports.component.scss'],
  providers: [DatePipe]
})
export class ReportsComponent implements OnInit {
  reportForm!: FormGroup;
  equipamentos: any[] = [];
  loading = false;
  total = 0;
  errorMessage: string | null = null;

  constructor(
    private equipmentsService: EquipmentsService,
    private datePipe: DatePipe
  ) {}

  ngOnInit(): void {
    this.reportForm = new FormGroup({
      status: new FormControl(''),
      responsavel: new FormControl(''),
      startDate: new FormControl(''),
      endDate: new FormControl('')
    });
  }

  /** 🔹 Gerar relatório filtrado */
  generateReport(): void {
    this.loading = true;
    this.errorMessage = null;

    const filters = this.reportForm.value;
    this.equipmentsService.listAll().subscribe({
      next: (data) => {
        let filtered = data;

        // 🔹 Aplicar filtros locais
        if (filters.status) {
          filtered = filtered.filter(eq => eq.status === filters.status);
        }
        if (filters.responsavel) {
          filtered = filtered.filter(eq => eq.responsavel?.toLowerCase().includes(filters.responsavel.toLowerCase()));
        }
        if (filters.startDate && filters.endDate) {
          const start = new Date(filters.startDate);
          const end = new Date(filters.endDate);
          filtered = filtered.filter(
            eq => eq.data_limite && new Date(eq.data_limite) >= start && new Date(eq.data_limite) <= end
          );


        }

        this.equipamentos = filtered;
        this.total = filtered.length;
        this.loading = false;
      },
      error: (err) => {
        console.error('Erro ao carregar relatório:', err);
        this.errorMessage = 'Erro ao gerar relatório.';
        this.loading = false;
      }
    });
  }

  /** 🔹 Exportar CSV */
  exportToCSV(): void {
    const csvData = this.equipamentos.map(e => ({
      Código: e.codigo,
      Posto: e.nome_do_posto,
      Razão_de_Uso: e.razao_uso,
      Versão: e.versao_solucao,
      Descrição: e.descricao,
      Responsável: e.responsavel,
      Status: e.status,
      Data_Limite: this.datePipe.transform(e.data_limite, 'dd/MM/yyyy')
    }));

    const csv = [
      Object.keys(csvData[0]).join(';'),
      ...csvData.map(row => Object.values(row).join(';'))
    ].join('\n');

    const blob = new Blob(["\uFEFF" + csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = url;
    link.download = `relatorio_equipamentos_${Date.now()}.csv`;
    link.click();
  }
}
