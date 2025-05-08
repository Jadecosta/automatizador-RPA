import sqlite3

# Conectar ao banco historico.db
conn = sqlite3.connect('historico.db')
cursor = conn.cursor()

# Deletar a tabela usuario
cursor.execute("DROP TABLE IF EXISTS sqlite_sequence")

conn.commit()
conn.close()

print("Tabela 'usuario' deletada com sucesso do banco historico.db!")
