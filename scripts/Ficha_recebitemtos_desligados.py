import pandas as pd
from database_utils import *

def buscar_dados(cur, mes, ano, tabelas):
    dfs = []
    for tabela in tabelas:
        consulta_sql = f"""
SELECT 
    E.SIGLA_EMPRESA, 
    F.CHAVE_FOLHA, 
    pdc.CPF_PESSOA, 
    pp.NOME,
    FF.COD_INSTITUCIONAL,
    FI.DATA_NOMEACAO,
    FD.DATA_DESLIGAMENTO,
    R.cod_rubrica_legado, 
    R.COD_RUBRICA, 
    R.NOME_RUBRICA, 
    FFR.VALOR_CALCULADO
FROM SW_cofir.FOLHA_FUNC FF
    LEFT JOIN SW_{tabela}.FOLHA F ON F.ID_FOLHA = FF.ID_FOLHA AND F.MES = {mes} AND F.ANO = {ano}
    LEFT JOIN SW_{tabela}.FOLHA_FUNC_RUBRICA FFR ON FFR.ID_FOLHA_FUNCIONARIO = FF.ID_FOLHA_FUNCIONARIO
    LEFT JOIN SW_PUBLICO.FOLHA_RUBRICA R ON R.ID_RUBRICA = FFR.ID_RUBRICA
    LEFT JOIN SW_PUBLICO.EMPRESA E ON E.SIGLA = '{tabela}'
    LEFT JOIN SW_PUBLICO.PESSOA_DOC_CPF pdc ON FF.ID_PESSOA_FUNCIONARIO = pdc.ID_PESSOA
    LEFT JOIN SW_PUBLICO.PESSOA pp ON pp.ID_PESSOA = FF.ID_PESSOA_FUNCIONARIO
    LEFT JOIN SW_{tabela}.FUNC_DESLIGAMENTO FD ON FD.ID_FUNCIONARIO = FF.ID_FUNCIONARIO
    LEFT JOIN SW_{tabela}.FUNCIONARIO_INGRESSO FI ON FI.ID_FUNCIONARIO = FF.ID_FUNCIONARIO
WHERE R.TIPO IN ('R') AND F.CHAVE_FOLHA IS NOT NULL AND FD.DATA_DESLIGAMENTO IS NOT NULL
ORDER BY F.CHAVE_FOLHA, pp.NOME
        """
        cur.execute(consulta_sql)
        results = cur.fetchall()
        colunas = [desc[0] for desc in cur.description]
        dfs.append(pd.DataFrame(results, columns=colunas))
    return pd.concat(dfs, ignore_index=True)


