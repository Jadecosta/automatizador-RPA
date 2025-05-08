import pandas as pd
from datetime import datetime

# Carregar o arquivo Excel
try:
    df = pd.read_excel('C:/Github/App_Program/dados_folha.xlsx', engine='openpyxl')
    print("Arquivo Excel carregado com sucesso!")
except Exception as e:
    print(f"Erro ao carregar o arquivo Excel: {e}")

# Garantir que VALOR_CALCULADO seja numérico
df['VALOR_CALCULADO'] = pd.to_numeric(df['VALOR_CALCULADO'], errors='coerce')

# Criar colunas auxiliares para MES e ANO
df['MES_ANO'] = df['CHAVE_FOLHA'].str[:7]  # Extrai os primeiros 7 caracteres (mes/ano)
df[['MES', 'ANO']] = df['MES_ANO'].str.split('/', expand=True)
df['MES'] = pd.to_numeric(df['MES'], errors='coerce')
df['ANO'] = pd.to_numeric(df['ANO'], errors='coerce')

# Filtrar por matrículas com DATA_DESLIGAMENTO preenchida
df_desligados = df[df['DATA_DESLIGAMENTO'].notna()]

# Função para calcular o 13º proporcional
def calcular_13_proporcional(row):
    # Filtrar apenas os dados do COD_INSTITUCIONAL atual
    matricula_df = df[
        (df['COD_INSTITUCIONAL'] == row['COD_INSTITUCIONAL']) & 
        (df['MES'] != 13)  # Excluir mês 13
    ]
    
    # Identificar o último mês válido
    matricula_df = matricula_df.sort_values(by=['ANO', 'MES'], ascending=[False, False])
    ultimo_mes_ano = matricula_df.iloc[0]['ANO']
    ultimo_mes_mes = matricula_df.iloc[0]['MES']

    # Filtrar todos os registros do último mês válido
    ultimo_mes_df = matricula_df[
        (matricula_df['ANO'] == ultimo_mes_ano) &
        (matricula_df['MES'] == ultimo_mes_mes)
    ]
    # Eliminar duplicatas baseando-se em COD_RUBRICA
    #ultimo_mes_df = ultimo_mes_df.drop_duplicates(subset=['COD_INSTITUCIONAL'])

    print(ultimo_mes_df)
    # Somar os valores de todas as rubricas do último mês
    valor_calculado_ultimo_mes = ultimo_mes_df['VALOR_CALCULADO'].sum()
    print(valor_calculado_ultimo_mes)
    # Calcular dias trabalhados
    desligamento_ano = row['DATA_DESLIGAMENTO'].year
    data_inicio = datetime.strptime(f"01/01/{desligamento_ano}", "%d/%m/%Y")
    data_final = row['DATA_DESLIGAMENTO']
    dias_trabalhados = (data_final - data_inicio).days #+ 1
    print(dias_trabalhados)
    # Calcular valor proporcional
    proporcional = (valor_calculado_ultimo_mes / 365 ) * (dias_trabalhados )
    print(proporcional)
    # Subtrair valor recebido referente à rubrica 116003
    valor_recebido = matricula_df[
        (matricula_df['COD_RUBRICA'] == 116003)
    ]['VALOR_CALCULADO'].sum()

    proporcional_final = max(proporcional - valor_recebido, 0)
    
    # Retornar todos os valores calculados
    return pd.Series([valor_calculado_ultimo_mes, dias_trabalhados, proporcional_final])

# Aplicar a função para calcular o 13º proporcional
df_desligados[['VALOR_ULTIMO_MES', 'DIAS_TRABALHADOS', '13_PROPORCIONAL']] = df_desligados.apply(calcular_13_proporcional, axis=1)



'''
# Cálculo de 1/3 de Férias Proporcionais
def calcular_terco_ferias_proporcionais(row):
    data_desligamento = datetime.strptime(row['DATA_DESLIGAMENTO'], '%d/%m/%Y')
    dia = row['DATA_NOMEACAO'].day
    mes = row['DATA_NOMEACAO'].month
    ano = row['DATA_DESLIGAMENTO'].year - 1

    periodo = f"{dia:02d}/{mes:02d}/{ano}"

    dias_trabalhados = (row['DATA_DESLIGAMENTO'] - periodo + 1 )
    salario_base = row['VALOR_CALCULADO']  # na verdade deve ser o somatorios dos Valor_calculado das rubricas que entram para o calculo
    
    # Verificar se já recebeu rubrica 111051
    recebeu_ferias = not df[(df['COD_RUBRICA'] == 111051) & (df['COD_INSTITUCIONAL'] == row['COD_INSTITUCIONAL'])].empty
    if recebeu_ferias:
        return 0

    return ((salario_base / 365) * dias_trabalhados) / 3

df_desligados['TERCO_FERIAS_PROPORCIONAIS'] = df_desligados.apply(calcular_terco_ferias_proporcionais, axis=1)

# Cálculo de Férias Indenizatórias
def calcular_ult_periodo_ferias_proporcionais(row):
    #data_desligamento = datetime.strptime(row['DATA_DESLIGAMENTO'], '%d/%m/%Y')
    dia = row['DATA_NOMEACAO'].day
    mes = row['DATA_NOMEACAO'].month
    ano = row['DATA_DESLIGAMENTO'].year - 1

    periodo = f"{dia:02d}/{mes:02d}/{ano}"
    dias_trabalhados = (row['DATA_DESLIGAMENTO'] - periodo + 1)
    salario_base = row['VALOR_CALCULADO']  # na verdade deve ser o somatorios dos Valor_calculado das rubricas que entram para o calculo
    return (salario_base / 365) * dias_trabalhados

df_desligados['FERIAS_PROPORCIONAIS_ULTIMO_PERIODO'] = df_desligados.apply(calcular_ult_periodo_ferias_proporcionais, axis=1)

# Cálculo de Férias Indenizatórias
def calcular_penult_periodo_ferias_proporcionais(row):
    dia = row['DATA_NOMEACAO'].day - 1 
    dia2 = row['DATA_NOMEACAO'].day
    mes = row['DATA_NOMEACAO'].month
    ano = row['DATA_DESLIGAMENTO'].year - 1
    ano2 = row['DATA_DESLIGAMENTO'].year - 2
    periodo = f"{dia:02d}/{mes:02d}/{ano}"
    periodo2 = f"{dia2:02d}/{mes:02d}/{ano2}"
    
    dias_trabalhados = (periodo - periodo2 + 1)
    salario_base = row['VALOR_CALCULADO']  # na verdade deve ser o somatorios dos Valor_calculado das rubricas que entram para o calculo
    return (salario_base / 365 ) * dias_trabalhados

df_desligados['FERIAS_PROPORCIONAIS_PENULTIMO_PERIODO'] = df_desligados.apply(calcular_penult_periodo_ferias_proporcionais, axis=1)
'''
# Agrupar por COD_INSTITUCIONAL e consolidar os dados
resultados = (
    df_desligados
    .groupby(['COD_INSTITUCIONAL', 'DATA_NOMEACAO', 'DATA_DESLIGAMENTO'], as_index=False)
    .agg({
        'DIAS_TRABALHADOS': 'mean',  # Média dos dias trabalhados (deve ser único por matrícula)
        'VALOR_ULTIMO_MES': 'sum',  # Somatório do valor do último mês por matrícula
        '13_PROPORCIONAL': 'sum',   # Somatório do 13º proporcional por matrícula
        #'TERCO_FERIAS_PROPORCIONAIS': 'sum',
        #'FERIAS_PROPORCIONAIS_ULTIMO_PERIODO': 'sum',
        #'FERIAS_PROPORCIONAIS_PENULTIMO_PERIODO': 'sum'
    })
)



# Arredondar os valores para 2 casas decimais
resultados = resultados.round(2)

print(resultados)

# Salvar resultados em CSV
resultados.to_csv('calculos_rescisao.csv', index=False)
