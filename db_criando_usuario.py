import sqlite3

# Criar conexão com o novo banco de usuários
conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

# Criar a tabela de usuários com a estrutura correta
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    matricula TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    permissao TEXT NOT NULL
)
''')

conn.commit()
conn.close()

print("Tabela 'usuario' criada com sucesso no banco usuarios.db!")

