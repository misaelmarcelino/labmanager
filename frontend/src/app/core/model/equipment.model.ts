
export interface Equipment {
  id: number;
  codigo: string;
  nome_do_posto: string;
  razao_uso?: string;
  versao_solucao: string;
  descricao: string;
  data_limite?: Date;  // ou tipo Date, dependendo do backend
  responsavel: string;
  status: string;
}
