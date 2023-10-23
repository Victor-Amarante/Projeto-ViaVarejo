import os
import pandas as pd
import numpy as np
from janitor import clean_names
from datetime import datetime, timedelta
pd.set_option("display.max_columns", None)

# preparacao do ambiente
BASE_DIR = os.getcwd()
DATA_DIR = os.path.join(BASE_DIR, "data")

# importar a base geral
if os.path.exists("data"):
    lista_arquivos = os.listdir(DATA_DIR)
    if lista_arquivos is not None:
        for arquivo in lista_arquivos:
            nome_arquivo = arquivo.split(".")[0]
            if nome_arquivo == "BASE GERAL - TAREFAS":
                caminho_arquivo = os.path.join(DATA_DIR, nome_arquivo)
                df_base_geral = pd.read_excel(f"{caminho_arquivo}.xlsx", engine="openpyxl")
                df_base_geral = clean_names(df_base_geral)

# excluir na coluna Escritorio tudo o que não for QCA
df_base_geral = df_base_geral[df_base_geral["escritorio_"] == "QUEIROZ CAVALCANTI ADVOGADOS"]


# adicionar 4 novas colunas (nomes no pop)
colunas_para_adicionar = ["NUCLEO", "BAIXA_ATE", "ITAPEVA", "STATUS"]
df_base_geral = df_base_geral.assign(**{coluna: "" for coluna in colunas_para_adicionar})

# coluna Nucleo -> PROCV base geral com base subtipo tarefas para pegar os nucleos
if os.path.exists("data"):
    lista_arquivos = os.listdir(DATA_DIR)
    if lista_arquivos is not None:
        for arquivo in lista_arquivos:
            nome_arquivo = arquivo.split(".")[0]
            if nome_arquivo == "BASE - SUBTIPO TAREFAS":
                caminho_arquivo = os.path.join(DATA_DIR, nome_arquivo)
                df_subtipo_tarefas = pd.read_excel(f"{caminho_arquivo}.xlsx", engine="openpyxl")
                df_subtipo_tarefas = clean_names(df_subtipo_tarefas)

df_subtipo_tarefas = df_subtipo_tarefas.drop_duplicates(subset=["tipo"])
procv1 = pd.merge(df_base_geral, df_subtipo_tarefas, how="left", left_on="sub_tipo", right_on="tipo", indicator=True)
procv1["NUCLEO"] = procv1["nucleo"]
procv1 = procv1.drop(['tipo', 'nucleo', '_merge'], axis=1)

# coluna Baixa-ate colocar os horarios atraves da coluna na mesma base Prazo(SLA)
def diminuir_uma_hora(horario_atual):
    novo_horario = horario_atual - timedelta(hours=1)
    novo_horario = novo_horario.strftime("%H:%M")
    return novo_horario

procv1["prazo_sla_"] = pd.to_datetime(procv1["prazo_sla_"])

procv1['BAIXA_ATE'] = procv1['prazo_sla_'].apply(diminuir_uma_hora)

now = pd.Timestamp.now()
cutoff_time = now.replace(hour=8, minute=0, second=0, microsecond=0)

# Adiciona um "-" onde o tempo é anterior ao tempo de corte
procv1['ATRASO'] = procv1['prazo_sla_'].apply(lambda x: '-' if x <= cutoff_time else '')


# coluna Itapeva -> PROCV base geral com base itapeva para pegar o NPC
if os.path.exists("data"):
    lista_arquivos = os.listdir(DATA_DIR)
    if lista_arquivos is not None:
        for arquivo in lista_arquivos:
            nome_arquivo = arquivo.split(".")[0]
            if nome_arquivo == "BASE - ITAPEVA":
                caminho_arquivo = os.path.join(DATA_DIR, nome_arquivo)
                df_subtipo_tarefas = pd.read_excel(f"{caminho_arquivo}.xlsx", engine="openpyxl", sheet_name="BASE")
                df_subtipo_tarefas = clean_names(df_subtipo_tarefas)
                df_subtipo_tarefas = df_subtipo_tarefas['npc']

procv2 = pd.merge(procv1, df_subtipo_tarefas, how="left", left_on="_processo_id", right_on="npc", indicator=True)
procv2 = procv2.drop(['_merge'], axis=1)

# coluna Status - > PROCV base geral com a base de impossibilidade e cancelamento
if os.path.exists("data"):
    lista_arquivos = os.listdir(DATA_DIR)
    if lista_arquivos is not None:
        for arquivo in lista_arquivos:
            nome_arquivo = arquivo.split(".")[0]
            if nome_arquivo == "BASE - IMPOSSIBILIDADE E CANCELAMENTO":
                caminho_arquivo = os.path.join(DATA_DIR, nome_arquivo)
                df_impossibilidade = pd.read_excel(f"{caminho_arquivo}.xlsx", engine="openpyxl")
                df_impossibilidade = clean_names(df_impossibilidade)
                df_impossibilidade = df_impossibilidade[["id_da_tarefa_", "status"]]

procv3 = pd.merge(procv2, df_impossibilidade, how='left', left_on="id_da_tarefa_", right_on="id_da_tarefa_", indicator=True)
procv3['STATUS'] = procv3['status_y']
procv3 = procv3.drop(['status_y', '_merge'], axis=1)
procv3.rename(columns={"status_x": "status", "npc": "NPC"}, inplace=True)


procv3.loc[(procv3["STATUS"].isna()) & (procv3['ATRASO'] == '-'), 'STATUS'] = "ATRASO - DEVE SER JUSTIFICADO!"

procv3.to_excel("teste_final_2.xlsx", index=False)

