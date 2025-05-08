import pandas as pd
from datetime import datetime
import scripts.calculos as calculos

def calcular_dias_trabalhados(data_admissao_str, data_exoneracao_str):
    data_admissao = datetime.strptime(data_admissao_str, '%d/%m/%Y')
    data_exoneracao = datetime.strptime(data_exoneracao_str, '%d/%m/%Y')
    
    dias_trabalhados = (data_exoneracao - data_admissao).days + 1  # +1 para incluir o último dia
    return dias_trabalhados

def dias_trabalhados_13(data_exoneracao_str):
    data_exoneracao = datetime.strptime(data_exoneracao_str, '%d/%m/%Y')
    
    # Pega o ano da exoneração e monta o dia 01/01 daquele ano
    data_inicio = datetime(data_exoneracao.year, 1, 1)
    # ((data_exoneracao - data_admissao) + 1 ) * (recebimento_ultimo / 365)
    # Calcula os dias (inclusivo)
    dias_trabalhados_13 = (data_exoneracao - data_inicio).days + 1
    
    return dias_trabalhados_13

def dias_trabalhados_ferias(data_admissao_str, data_exoneracao_str):
    data_admissao = datetime.strptime(data_admissao_str, '%d/%m/%Y')
    data_exoneracao = datetime.strptime(data_exoneracao_str, '%d/%m/%Y')

    if data_admissao.month > data_exoneracao.month:
        ano_inicio = data_exoneracao.year - 1
    else:
        ano_inicio = data_exoneracao.year

    data_inicio = datetime(ano_inicio, data_admissao.month, data_admissao.day)
    dias_trabalhados_ferias = (data_exoneracao - data_inicio).days + 1

    return dias_trabalhados_ferias

def ferias_gozadas(base_calc, feriasGozadas):
    ferias_gozadas = (base_calc / 30) * (feriasGozadas)
    return ferias_gozadas

def calcular_13_proporcional(recebimento_ultimo, dias_trabalhados_13):
    return round((recebimento_ultimo / 365) * dias_trabalhados_13, 2)

def ferias_proporcionais(recebimento_ultimo, dias_trabalhados_ferias):
    return round((recebimento_ultimo / 365) * dias_trabalhados_ferias, 2)

def terco_ferias(ferias_proporcionais):
    return round(ferias_proporcionais / 3, 2)

def ferias_nao_gozadas(base_calc, cet_calc, dias_trabalhados_13):
    total_base = base_calc + cet_calc
    return round((total_base / 365) * dias_trabalhados_13, 2)

def indenizacao_total(valor_13, valor_ferias_proporcionais, valor_ferias_nao_gozadas, valor_terco_ferias):
    total = 0
    total += valor_13 if isinstance(valor_13, (int, float)) else 0
    total += valor_ferias_proporcionais if isinstance(valor_ferias_proporcionais, (int, float)) else 0
    total += valor_ferias_nao_gozadas if isinstance(valor_ferias_nao_gozadas, (int, float)) else 0
    total += valor_terco_ferias if isinstance(valor_terco_ferias, (int, float)) else 0
    return round(total, 2)



