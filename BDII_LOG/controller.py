import json
import psycopg2

def config_tabela(cur):
    cur.execute('DROP TABLE IF EXISTS tabela;')

    cur.execute('''
    CREATE TABLE tabela (
        id integer NOT NULL,
        a integer NOT NULL,
        b integer NOT NULL
    )
    ''')

    file = open('metadado.json', 'r')

    data = json.load(file)['INITIAL']
    tuples = list( zip(data['id'], data['A'], data['B']) )

    for tuple in tuples:

        tuple = [str(column) for column in tuple]

        values = ', '.join(tuple)

        insert_query = 'INSERT INTO tabela(id, a, b) VALUES (' + values + ')'
        cur.execute(insert_query)

    file.close()


def busca_commited(transactions):
    file = open('entradaLog.txt', 'r')
    linhas = file.readlines()
    for linha in linhas:
        linha = linha[1:-2]
        comando = linha.split()
        if len(comando) != 2:
            comando = linha.split(',')

        if comando[0] == 'start':
            transactions[comando[1]] = 1
        elif comando[0] == 'commit':
            transactions[comando[1]] = 0

    file.close

def realiza_mudancas(cur, transactions):
    vet_undo = []
    file = open('entradaLog.txt', 'r')
    linhas = file.readlines()
    for linha in linhas:
        linha = linha[1:-2]
        comando = linha.split()

        if len(comando) != 2:
            comando = linha.split(',')
            if(transactions[comando[0]] == 0):
                cur.execute(f"UPDATE tabela SET {comando[2]} = {comando[4]} where id = {comando[1]}")
            elif(transactions[comando[0]] == 1):
                vet_undo.append([comando[1], comando[2], comando[3]])
        
    for i in reversed(vet_undo):
        cur.execute(f"UPDATE tabela SET {i[1]} = {i[2]} where id = {i[0]}")

    file.close

def print_final(cur):
    cur.execute('SELECT * FROM tabela')
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    print(columns)
    for row in rows:
        print(row)

if __name__ == '__main__':

    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    config_tabela(cur)

    transactions = {}
    busca_commited(transactions)
    for i in transactions:
        if transactions[i] == 1:
            print(f'TRANSAÇÃO {i} REALIZOU UNDO')
        elif transactions[i] == 0:
            print(f'TRANSAÇÃO {i} REALIZOU REDO')

    realiza_mudancas(cur, transactions)

    print_final(cur)

    conn.commit()
    cur.close()
    conn.close()
