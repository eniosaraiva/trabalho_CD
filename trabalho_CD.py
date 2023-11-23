# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# """
# Desmatamento 2000-2022

# """

import basedosdados as bd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import zipfile
import urllib.request
import os
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist


df = bd.read_table(dataset_id='br_inpe_prodes',
table_id='municipio_bioma',
billing_project_id="bases-jud")

df2 = bd.read_table(dataset_id='br_geobr_mapas',
table_id='municipio',
billing_project_id="bases-jud")

df3 = pd.merge(df, df2, on='id_municipio')

df3 = df3.drop("geometria", axis=1)

df3['nome_municipio'] = ''

url = 'https://geoftp.ibge.gov.br/organizacao_do_territorio/estrutura_territorial/divisao_territorial/2022/DTB_2022.zip'
xls_filename = 'RELATORIO_DTB_BRASIL_MUNICIPIO.xls'
urllib.request.urlretrieve(url, 'DTB_2022.zip')
with zipfile.ZipFile('DTB_2022.zip', 'r') as zip_ref:
    zip_ref.extractall()
df4 = pd.read_excel(xls_filename, header=7, usecols=[11, 12], names=['id_municipio', 'nome_municipio'])

arquivos_descompactados = [f for f in os.listdir('.') if f.endswith('.xls')]
for arquivo in arquivos_descompactados:
    os.remove(arquivo)
    
arquivos_descompactados = [f for f in os.listdir('.') if f.endswith('.ods')]
for arquivo in arquivos_descompactados:
    os.remove(arquivo)

arquivos_descompactados = [f for f in os.listdir('.') if f.endswith('.zip')]
for arquivo in arquivos_descompactados:
    os.remove(arquivo)
    
map_dict = df4.set_index('id_municipio')['nome_municipio'].to_dict()

df3['nome_municipio'] = df4['id_municipio'].map(map_dict).fillna(df3['nome_municipio'])

df = bd.read_table(dataset_id='br_ibge_pib',
table_id='municipio',
billing_project_id="bases-jud")

df3 = pd.merge(df3, df[['ano', 'id_municipio', 'pib', 'va_agropecuaria', 'va_industria', 'va_servicos', 'va_adespss']], on=['ano', 'id_municipio'], how='left')

df.to_csv('df3.csv', index=False)

#df3 = pd.read_csv('df3.csv')

print(df3.columns)

df_relevante = df3[['ano', 'bioma', 'desmatado', 'area_total',
       'vegetacao_natural', 'nao_vegetacao_natural', 'hidrografia', 'sigla_uf',
       'pib', 'va_agropecuaria', 'va_industria',
       'va_servicos', 'va_adespss', 'id_municipio']]

df_agrupado = df_relevante.groupby(['ano', 'bioma']).sum().reset_index()

biomas = df_agrupado['bioma'].unique()

for bioma in biomas:
    df_bioma = df_agrupado[df_agrupado['bioma'] == bioma]
    plt.plot(df_bioma['ano'], df_bioma['desmatado'], label=bioma)

plt.xlabel('Ano')
plt.ylabel('Área Desmatada (km²)')
plt.title('Evolução do Desmatamento por Bioma')
plt.legend()
plt.savefig('evolucao_desmatamento.png')
plt.show()

df_agrupado = df_relevante.groupby(['ano', 'sigla_uf']).sum().reset_index()

biomas = df_agrupado['sigla_uf'].unique()

for bioma in biomas:
    df_bioma = df_agrupado[df_agrupado['sigla_uf'] == bioma]
    plt.plot(df_bioma['ano'], df_bioma['desmatado'], label=bioma)

plt.xlabel('Ano')
plt.ylabel('Área Desmatada (km²)')
plt.title('Evolução do Desmatamento por UF')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
plt.savefig('evolucao_desmatamento.png', bbox_inches='tight')
plt.show()

desmatamento_por_bioma = df3.groupby('bioma')['desmatado'].sum()
desmatamento_por_bioma.plot(kind='bar', xlabel='Bioma', ylabel='Área Desmatada (km²)')
plt.title('Distribuição do Desmatamento por Bioma')
plt.tight_layout() 
for i, valor in enumerate(desmatamento_por_bioma):
    plt.annotate(f'{valor:.2f}', (i, valor), ha='center', va='bottom')

plt.savefig('desmatamento_por_bioma.png', dpi = 300)
plt.show()

tendencias_temporais = df3.groupby('ano')['desmatado'].sum()
tendencias_temporais.plot(kind='line', xlabel='Ano', ylabel='Área Desmatada (km²)')
plt.title('Tendências Temporais de Desmatamento')
plt.savefig('tendencia_geral.png')
plt.show()

correlacoes = df3.corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlacoes, annot=True, cmap='coolwarm', ax=ax)
plt.title('Correlações entre as Variáveis')
plt.tight_layout()
plt.savefig('correlacoes.png', dpi=300)
plt.show()

df_2022 = df3[df3['ano'] == 2022]

df_relevante = df_2022.groupby('sigla_uf')['desmatado'].mean().reset_index()

dist_matrix = pdist(df_relevante['desmatado'].values.reshape(-1, 1))

Z = linkage(dist_matrix, method='ward')

plt.figure(figsize=(10, 6))
dendro = dendrogram(Z, labels=df_relevante['sigla_uf'].tolist(), orientation='top')
plt.title('Dendrograma do Desmatamento (2022)')
plt.xlabel('Sigla UF')
plt.ylabel('Distância')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig('dendrograma.png')
plt.show()
