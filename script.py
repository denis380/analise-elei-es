import pandas as pd

# Carregar o CSV original
caminho_do_arquivo = 'votacao_secao_2020_MG/votos_contagem.csv'
try:
    dados = pd.read_csv(caminho_do_arquivo, encoding='utf-8', delimiter=',')
except:
    try:
        dados = pd.read_csv(caminho_do_arquivo, encoding='ISO-8859-1', delimiter=',')
    except:
        dados = pd.read_csv(caminho_do_arquivo, encoding='cp1252', delimiter=',')

# Filtrar apenas os registros onde DS_CARGO é 'Vereador'
df_filtrado = dados[dados['DS_CARGO'] == 'Vereador']

# Exportar o DataFrame filtrado para um novo arquivo CSV
caminho_do_arquivo_filtrado = 'votacao_secao_2020_MG/votos_contagem_vereadores.csv'
df_filtrado.to_csv(caminho_do_arquivo_filtrado, index=False, encoding='utf-8')

print(f"Arquivo CSV filtrado exportado para {caminho_do_arquivo_filtrado}")
