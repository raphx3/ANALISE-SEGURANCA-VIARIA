import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap, MarkerCluster
from sklearn.cluster import KMeans

# 1. Configurações Iniciais
st.set_page_config(page_title="Dashboard Segurança Viária", layout="wide")

# Estilização para a tabela
def highlight_graves(val):
    color = 'orange' if val == 'Grave' else ''
    return f'background-color: {color}'

# 2. Sidebar - KPIs Detalhados
st.sidebar.title("Métricas de Segurança")

# Dados Simulados
data_vix = {
    'latitude': [-20.2950, -20.3050, -20.3120, -20.3110, -20.3105, -20.2895, -20.2980, -20.3040, -20.3140, -20.3080],
    'longitude': [-40.3045, -40.3030, -40.3020, -40.3180, -40.3100, -40.3031, -40.3000, -40.2970, -40.3025, -40.3150],
    'gravidade': ['Fatal', 'Grave', 'Grave', 'Grave', 'Leve', 'Leve', 'Leve', 'Leve', 'Grave', 'Leve']
}
df = pd.DataFrame(data_vix)

# Cálculo de Métricas
st.sidebar.metric("Acidentes Leves", len(df[df['gravidade'] == 'Leve']))
st.sidebar.metric("Acidentes Graves", len(df[df['gravidade'] == 'Grave']))
st.sidebar.metric("Acidentes Fatais", len(df[df['gravidade'] == 'Fatal']))

st.sidebar.markdown("---")
st.sidebar.write("**Autor:** Raphael Alvarenga da Silva")
st.sidebar.write("**Foco:** Segurança Viária & Análise Geográfica")

# 3. Cabeçalho e Texto Estratégico
col1, col2 = st.columns([2, 1])

with col1:
    st.title("Projeto Segurança Viária: Vitória-ES")
    st.markdown("""
    ### Objetivo do Projeto
    Este dashboard foi desenvolvido para demonstrar competências técnicas em **Análise de Dados e Geoprocessamento** aplicadas à segurança de parceiros. O foco é a redução de acidentes graves e fatais através da identificação de *Hotspots* e classificação de risco por vias.
    
    ### Como este projeto atende à vaga:
    1.  **Visão de Negócio:** Classificação de vias (Crítica, Atenção, Segura) para priorizar investimentos em segurança e treinamentos.
    2.  **Machine Learning:** Uso de **K-Means** para clusterização automática de áreas com alta densidade de sinistros.
    3.  **Tecnologia SIG:** Domínio de bibliotecas geoespaciais (`Folium`, `Leaflet`) para visualização de dados complexos.
    """)

with col2:
    st.info("""
    **Metodologia Utilizada:**
    - **Coleta:** Dados simulados de sinistros na Ilha de Vitória.
    - **Processamento:** Clusterização para identificar zonas de auditoria prioritária.
    - **Saída:** Mapa dinâmico com rotas logísticas e níveis de criticidade.
    """)

# IA: K-Means para encontrar a área prioritária
X = df[['latitude', 'longitude']]
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X)
df['cluster'] = kmeans.labels_

# Seleção do cluster mais crítico (maior soma de graves e fatais)
cluster_prioritario = df[df['gravidade'].isin(['Grave', 'Fatal'])]['cluster'].value_counts().idxmax()
centroide = df[df['cluster'] == cluster_prioritario][['latitude', 'longitude']].mean().values

# 4. Mapa Interativo
st.divider()
st.subheader("Análise Espacial e Hotspots")

m = folium.Map(location=[-20.302, -40.305], zoom_start=14, tiles='CartoDB dark_matter')
m.add_child(folium.LatLngPopup())

# Grupos de Camadas
fg_rotas = folium.FeatureGroup(name="Classificação de Vias (Rotas)").add_to(m)
fg_raio = folium.FeatureGroup(name="Área Prioritária (Raio)").add_to(m)
fg_calor = folium.FeatureGroup(name="Mapa de Calor", show=False).add_to(m)
mc = MarkerCluster(name="Ocorrências Individuais").add_to(m)

# Rotas
folium.PolyLine([[-20.2922, -40.3051], [-20.3152, -40.3018]], color="#FF4B4B", weight=8, opacity=0.9, tooltip="CRÍTICA: Leitão da Silva").add_to(fg_rotas)
folium.PolyLine([[-20.3115, -40.3197], [-20.3099, -40.3088]], color="#F1C40F", weight=8, opacity=0.8, tooltip="ATENÇÃO: Av. Vitória").add_to(fg_rotas)
folium.PolyLine([[-20.2882, -40.3040], [-20.3085, -40.2957]], color="#2EB82E", weight=8, opacity=0.8, tooltip="SEGURA: Reta da Penha").add_to(fg_rotas)

# Raio Prioritário
folium.Circle(
    location=[centroide[0], centroide[1]],
    radius=600,
    color="white",
    weight=2,
    fill=True,
    fill_opacity=0.2,
    popup="Zona de Intervenção Prioritária"
).add_to(fg_raio)

# Calor e Marcadores
HeatMap([[r['latitude'], r['longitude']] for i, r in df.iterrows()], radius=30, blur=20).add_to(fg_calor)

for i, row in df.iterrows():
    color = 'black' if row['gravidade'] == 'Fatal' else 'red' if row['gravidade'] == 'Grave' else 'orange'
    icon = 'skull' if row['gravidade'] == 'Fatal' else 'exclamation-triangle' if row['gravidade'] == 'Grave' else 'info-circle'
    folium.Marker([row['latitude'], row['longitude']], 
                  icon=folium.Icon(color=color, icon=icon, prefix='fa'),
                  popup=f"Gravidade: {row['gravidade']}").add_to(mc)

folium.LayerControl(collapsed=False).add_to(m)

st_folium(m, width=1400, height=600)

# 5. Tabela de Dados
st.divider()
st.subheader("Base de Dados de Sinistros")
st.write("Abaixo, a tabela destaca automaticamente os acidentes **Graves** para facilitar a triagem operacional.")

# Aplicando destaques
st.dataframe(df.style.map(highlight_graves, subset=['gravidade']), width='stretch')

# Rodapé
st.markdown("---")
st.caption("Dashboard desenvolvido para fins de demonstração técnica de análise de dados.")
st.caption("LinkedIn: https://www.linkedin.com/in/raphaelalvarengadasilva/")


