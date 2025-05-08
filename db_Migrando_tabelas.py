import pandas as pd
import sqlite3

# Conectar ao banco antigo (onde está a tabela atual)
conn_old = sqlite3.connect('historico.db')

# Conectar ao novo banco de usuários
conn_new = sqlite3.connect('usuarios.db')

# Ler os dados da tabela antiga
df_usuarios = pd.read_sql_query("SELECT * FROM usuario", conn_old)

# Selecionar apenas as colunas que existem na nova tabela
colunas_validas = ['id', 'nome', 'matricula', 'email', 'senha', 'permissao']
df_usuarios = df_usuarios[colunas_validas]

# Criar a tabela no novo banco com a estrutura correta
conn_new.execute('''
CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    matricula TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    permissao TEXT NOT NULL
)
''')

# Inserir os dados no novo banco
df_usuarios.to_sql('usuario', conn_new, if_exists='append', index=False)

# Fechar conexões
conn_old.close()
conn_new.close()

print("Migração concluída com sucesso!")
