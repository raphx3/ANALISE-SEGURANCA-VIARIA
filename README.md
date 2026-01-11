# Dashboard de Segurança Viária - Visão Zero Vitória
Este projeto é um painel de controle interativo (dashboard) construído com Streamlit para monitoramento e análise de segurança viária. O relatório simula a análise de sinistros de trânsito na Ilha de Vitória, Espírito Santo, focando na proteção de parceiros entregadores.

# O objetivo deste projeto é demonstrar proficiência em:

Geoprocessamento e Inteligência Espacial: Identificação de hotspots de acidentes e classificação de risco por eixos viários reais.

Machine Learning Aplicado: Uso do algoritmo K-Means para clusterização automática de zonas de perigo e definição de áreas prioritárias para auditoria.

Visualização de Dados Dinâmica: Uso de Folium e MarkerCluster para criar mapas interativos com controle de camadas (Layer Control).

Desenvolvimento de Dashboards Logísticos: Criação de uma ferramenta funcional para tomada de decisão baseada em dados viários.

# Funcionalidades do Dashboard
O painel apresenta uma análise integrada da malha viária urbana:

Métricas de Segurança (KPIs): Painel lateral com contagem em tempo real de acidentes Leves, Graves e Fatais.

Classificação de Vias: Visualização de rotas logísticas coloridas por nível de risco (Crítica, Atenção e Segura).

Área de Intervenção Prioritária: Um raio de 600m gerado automaticamente por IA sobre o cluster de maior gravidade para sugerir intervenções de infraestrutura.

Mapa de Calor e Clusters: Camadas alternáveis que mostram a densidade de ocorrências e agrupamentos de sinistros.

Tabela de Dados Inteligente: Listagem completa de sinistros com destaque visual (Style Map) em ocorrências graves para triagem operacional rápida.

# Como Executar o Projeto
Para rodar o projeto localmente, siga os passos abaixo:

1. Pré-requisitos
Certifique-se de ter o Python instalado (versão 3.9+ recomendada).

2. Instalação das Dependências
Crie o ambiente virtual:

Bash

python -m venv .venv
Ative o ambiente virtual:

Windows: .\.venv\Scripts\activate

Mac/Linux: source .venv/bin/activate

Instale as dependências:

Bash

pip install streamlit pandas folium streamlit-folium scikit-learn
3. Execução do Aplicativo
Execute o aplicativo com o comando do Streamlit:

Bash

streamlit run main.py
