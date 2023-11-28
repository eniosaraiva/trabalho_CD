#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 14:38:37 2023

@author: enio
"""
#Teste de normalidade usando o teste de Shapiro-Wilk:

from scipy.stats import shapiro
import scipy
from scipy.stats import f_oneway
import pandas as pd
import scipy.stats
#

# Variável contínua para teste de normalidade (exemplo: área desmatada)
area_desmatada = df3['desmatado']

# Realizar o teste de Shapiro-Wilk
stat, p_value = shapiro(area_desmatada)

# Verificar o resultado do teste
alpha = 0.05  # Nível de significância
if p_value > alpha:
    print("A variável segue uma distribuição normal")
else:
    print("A variável não segue uma distribuição normal")
   

# Selecionar as colunas relevantes para a análise
columns = ['ano', 'bioma', 'area_total', 'vegetacao_natural', 'nao_vegetacao_natural', 'hidrografia', 'sigla_uf', 'pib', 'va_agropecuaria', 'va_industria', 'va_servicos', 'va_adespss']

# Realizar a ANOVA para cada coluna em relação a 'desmatado'
for column in columns:
    groups = []
    for group_name, group_data in df3.groupby(column):
        groups.append(group_data['desmatado'])
    
    # Executar o teste de ANOVA
    f_value, p_value = f_oneway(*groups)
    print(f"Variável: {column}")
    print(f"F-value: {f_value}")
    print(f"P-value: {p_value}\n")
    
#Teste de correlação usando o coeficiente de correlação de Pearson:
# Variáveis para teste de correlação - desmatamento e PIB

# Remover linhas com valores NaN ou infinitos
df3_clean = df3.dropna(subset=['desmatado', 'pib'], axis=0)

# Converter as colunas para o tipo de dado correto, se necessário
df3_clean['desmatado'] = df3_clean['desmatado'].astype(float)
df3_clean['pib'] = df3_clean['pib'].astype(float)

# Calcular o coeficiente de correlação de Pearson
correlation_coef, p_value = scipy.stats.pearsonr(df3_clean['desmatado'], df3_clean['pib'])

# Verificar o resultado do teste
alpha = 0.05  # Nível de significância
if p_value < alpha:
    print("Existe uma correlação significativa entre as variáveis")
else:
    print("Não há uma correlação significativa entre as variáveis")
    
#Teste de diferença entre grupos usando ANOVA:

# Variável contínua para teste de diferença entre grupos
area_desmatada = df3['desmatado']

bioma = df3['bioma']

# Realizar o teste de ANOVA
stat, p_value = f_oneway(area_desmatada[bioma == 'Amazônia'],
                         area_desmatada[bioma == 'Cerrado'],
                         area_desmatada[bioma == 'Pantanal'],
                         area_desmatada[bioma == 'Pampa'],
                         area_desmatada[bioma == 'Caatinga'],
                         area_desmatada[bioma == 'Mata Atlântica'])

# Verificar o resultado do teste
alpha = 0.05  # Nível de significância
if p_value < alpha:
    print("Há diferenças significativas nas médias das variáveis entre os grupos")
else:
    print("Não há diferenças significativas nas médias das variáveis entre os grupos")