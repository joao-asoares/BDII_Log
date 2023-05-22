# BDII_Log
Trabalho de banco de dados II sobre LOG - Ciência da Computação UFFS/2023.1

NECESSÁRIO: instalar biblioteca do python psycopg2 (usada para acesso ao banco postgres)

Objetivo: implementar o mecanismo de log Redo/Undo sem checkpoint usando o SGBD.

Funcionamento: 
O código, escrito em Python, é capaz de ler o arquivo de log (entradaLog) e o arquivo de Metadado e validar as informações no banco de dados através do modelo REDO/UNDO. 
O código recebe como entrada o arquivo de metadados (dados salvos) e os dados da tabela que irá operar no banco de dados. 

Exemplo de Arquivo de Metadado (json): 
{  "table": {
	“id”:[1,2],
	"A": [20,20],
	"B": [55,30]
  }
}

Arquivo de log no formato <transação, “id da tupla”,”coluna”, “valor antigo”, “valor novo”>.

Saída: 
“Transação x realizou REDO/UNDO”, além de imprimir o valor das variáveis do banco no final
