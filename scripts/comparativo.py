import pandas as pd
from database_utils import *

def buscar_dados(cur, mes, ano, tabelas):
    dfs = []
    tabelas_validas = [t for t in tabelas if t != "TODOS"]  # Remove "TODOS" da lista
    for tabela in tabelas_validas:
        consulta_sql = f"""
            SELECT 
                E.SIGLA_EMPRESA, 
                F.CHAVE_FOLHA, 
                pdc.CPF_PESSOA, 
                pp.NOME,
                FF.COD_INSTITUCIONAL, 
                R.cod_rubrica_legado, 
                R.COD_RUBRICA, 
                R.NOME_RUBRICA, 
                FFR.VALOR_CALCULADO
            FROM SW_{tabela}.FOLHA_FUNC FF
                JOIN SW_{tabela}.FOLHA F ON F.ID_FOLHA = FF.ID_FOLHA AND F.MES = {mes} AND F.ANO = {ano}
                JOIN SW_{tabela}.FOLHA_FUNC_RUBRICA FFR ON FFR.ID_FOLHA_FUNCIONARIO = FF.ID_FOLHA_FUNCIONARIO
                JOIN SW_PUBLICO.FOLHA_RUBRICA R ON R.ID_RUBRICA = FFR.ID_RUBRICA
                JOIN SW_PUBLICO.EMPRESA E ON E.SIGLA = '{tabela}'
                JOIN SW_PUBLICO.PESSOA_DOC_CPF pdc ON FF.ID_PESSOA_FUNCIONARIO = pdc.ID_PESSOA
                JOIN SW_PUBLICO.PESSOA pp ON pp.ID_PESSOA = FF.ID_PESSOA_FUNCIONARIO
            WHERE R.TIPO IN ('R', 'D')
        """
        cur.execute(consulta_sql)
        results = cur.fetchall()
        colunas = [desc[0] for desc in cur.description]
        dfs.append(pd.DataFrame(results, columns=colunas))
    return pd.concat(dfs, ignore_index=True)

def gerar_comparativos(cur, mes, ano, tabelas):
    df_corrente = buscar_dados(cur, mes, ano, tabelas)
    mes_anterior = 12 if mes == 1 else mes - 1
    ano_anterior = ano - 1 if mes == 1 else ano
    df_anterior = buscar_dados(cur, mes_anterior, ano_anterior, tabelas)

    df_aba1 = df_corrente.merge(
        df_anterior[['COD_INSTITUCIONAL', 'CPF_PESSOA', 'COD_RUBRICA', 'VALOR_CALCULADO']],
        on=['COD_INSTITUCIONAL', 'CPF_PESSOA', 'COD_RUBRICA'],
        suffixes=('', '_mes_anterior'), how='left'
    )
    df_aba1['Comparativo'] = df_aba1['VALOR_CALCULADO'] - df_aba1['VALOR_CALCULADO_mes_anterior']

    df_aba2 = df_anterior.merge(
        df_corrente[['COD_INSTITUCIONAL', 'CPF_PESSOA', 'COD_RUBRICA', 'VALOR_CALCULADO']],
        on=['COD_INSTITUCIONAL', 'CPF_PESSOA', 'COD_RUBRICA'],
        suffixes=('_mes_anterior', '_corrente'), how='left'
    )
    df_aba2['Comparativo'] = df_aba2['VALOR_CALCULADO_corrente'] - df_aba2['VALOR_CALCULADO_mes_anterior']

    df_aba3 = df_corrente.groupby(['SIGLA_EMPRESA', 'COD_RUBRICA', 'NOME_RUBRICA']).sum().reset_index()
    df_aba4 = df_corrente.groupby(['COD_RUBRICA', 'NOME_RUBRICA']).sum().reset_index()

    return df_aba1, df_aba2, df_aba3, df_aba4
