
export interface Equipment {
  id: number;
  codigo: string;
  nome_posto: string;
  razao_uso?: string;
  vs_solucao: string;
  motivo_homologacao: string;
  data_limite_homologacao?: Date;  // ou tipo Date, dependendo do backend
  responsavel: string;
  status: string;
}
