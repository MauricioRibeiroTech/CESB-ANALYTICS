import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

# --- Configuração da Página ---
st.set_page_config(
    page_title="Análise de Desempenho em avaliações diagnósticas CESB",
    page_icon="📊",
    layout="wide"
)

# --- Estilo CSS Aprimorado para Alto Contraste ---
st.markdown("""
<style>
    /* Estilo geral */
    body {
        color: #333;
    }
    
    /* Cabeçalho Principal */
    .main-header {
        font-size: 2.8rem;
        color: white;
        text-align: center;
        font-weight: 700;
        padding: 1.5rem;
        background: linear-gradient(135deg, #005f73 0%, #0a9396 100%);
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }

    /* Cabeçalhos de Seção */
    .section-header {
        font-size: 1.8rem;
        color: #005f73;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #94d2bd;
        font-weight: 600;
    }

    /* Cartões de Métricas */
    .metric-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        text-align: center;
    }
    .metric-card h3 {
        font-size: 1.2rem;
        color: #555;
        margin-bottom: 0.5rem;
    }
    .metric-card p {
        font-size: 2rem;
        font-weight: 700;
        color: #0a9396;
    }

    /* Caixa de Destaque para Classificação do Aluno */
    .highlight-box {
        background-color: #000000;
        border-left: 8px solid;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .highlight-box h4 {
        margin-top: 0;
        font-size: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)


# --- Carregamento e Processamento dos Dados ---
@st.cache_data
def load_data(filepath):
    """
    Carrega e processa os dados do arquivo CSV.
    """
    try:
        # Carrega o CSV com o separador correto
        df = pd.read_csv(filepath, sep=';')
        
        # Limpa os nomes das colunas e dos alunos
        df.columns = df.columns.str.strip()
        df['Alunos'] = df['Alunos'].str.strip()

        # Converte colunas de notas para numérico, tratando erros
        score_cols = ['CAED1', 'CAED2', 'impulso']
        for col in score_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove linhas com dados numéricos ausentes
        df.dropna(subset=score_cols, inplace=True)

        # Calcula o total e o percentual (assumindo nota máxima de 74, como no script original)
        # Se a nota máxima for outra, ajuste o valor 74.
        max_score = 74 
        df['Total'] = df[score_cols].sum(axis=1)
        df['Percentual_Total'] = (df['Total'] / max_score * 100).round(1)

        # Calcula o percentil de cada aluno
        df['Percentil'] = df['Total'].rank(pct=True) * 100

        # Classifica os alunos com base no percentil
        def classify_student(percentile):
            if percentile >= 90:
                return "Excelente"
            elif percentile >= 70:
                return "Acima da Média"
            elif percentile >= 50:
                return "Na Média"
            elif percentile >= 30:
                return "Abaixo da Média"
            else:
                return "Precisa de Apoio"
        
        df['Classificação'] = df['Percentil'].apply(classify_student)
        return df.sort_values(by='Alunos').reset_index(drop=True)

    except FileNotFoundError:
        st.error(f"Erro: O arquivo '{filepath}' não foi encontrado. Verifique se ele está na mesma pasta do script.")
        return pd.DataFrame()

# Carrega os dados
data = load_data('1_dados.csv')

if data.empty:
    st.stop()


# --- Título Principal ---
st.markdown('<h1 class="main-header">Desempenho em avaliações diagnósticas CESB</h1>', unsafe_allow_html=True)

# --- Barra Lateral para Seleção ---
st.sidebar.title("Filtros")
st.sidebar.markdown("Selecione um aluno para uma análise detalhada.")

# Selecionar aluno da lista
student_list = data['Alunos'].unique()
selected_student = st.sidebar.selectbox(
    'Selecione o Aluno:',
    options=student_list
)

# --- Layout em Abas ---
tab1, tab2 = st.tabs(["Visão Geral da Turma", "Análise Individual do Aluno"])

# --- Aba 1: Visão Geral da Turma ---
with tab1:
    st.markdown('<h2 class="section-header">Desempenho Geral da Turma</h2>', unsafe_allow_html=True)

    # Métricas gerais
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Nº de Alunos</h3>
            <p>{len(data)}</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Média da Turma</h3>
            <p>{data['Total'].mean():.1f}</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Mediana da Turma</h3>
            <p>{data['Total'].median():.1f}</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Melhor Pontuação</h3>
            <p>{data['Total'].max()}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    col1_main, col2_main = st.columns(2)

    with col1_main:
        # Gráfico de Distribuição das Notas Totais
        st.markdown("<h4>Distribuição das Pontuações Totais</h4>", unsafe_allow_html=True)
        fig_dist = px.histogram(
            data, 
            x='Total',
            nbins=15,
            title='Frequência de Pontuações na Turma',
            labels={'Total': 'Pontuação Total', 'count': 'Número de Alunos'},
            color_discrete_sequence=['#0a9396']
        )
        fig_dist.update_layout(bargap=0.1, template='plotly_white')
        st.plotly_chart(fig_dist, use_container_width=True)

    with col2_main:
        # Gráfico de Classificação de Desempenho
        st.markdown("<h4>Distribuição por Classificação</h4>", unsafe_allow_html=True)
        classification_counts = data['Classificação'].value_counts().reindex(
            ["Excelente", "Acima da Média", "Na Média", "Abaixo da Média", "Precisa de Apoio"]
        )
        # Mapeamento de cores de alto contraste
        color_map = {
            "Excelente": "#2a9d8f",
            "Acima da Média": "#264653",
            "Na Média": "#e9c46a",
            "Abaixo da Média": "#f4a261",
            "Precisa de Apoio": "#e76f51"
        }
        fig_pie = px.pie(
            values=classification_counts.values, 
            names=classification_counts.index, 
            title='Percentual de Alunos por Nível de Desempenho',
            color=classification_counts.index,
            color_discrete_map=color_map
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# --- Aba 2: Análise Individual ---
with tab2:
    st.markdown(f'<h2 class="section-header">Análise de Desempenho de {selected_student}</h2>', unsafe_allow_html=True)

    # Obter dados do aluno selecionado
    student_data = data[data['Alunos'] == selected_student].iloc[0]

    # --- Cartão de Classificação com Cores de Alto Contraste ---
    classification = student_data['Classificação']
    color_map_css = {
        "Excelente": "#2a9d8f",       # Verde escuro
        "Acima da Média": "#264653", # Azul petróleo
        "Na Média": "#e9c46a",         # Amarelo mostarda
        "Abaixo da Média": "#f4a261", # Laranja claro
        "Precisa de Apoio": "#e76f51"   # Vermelho queimado
    }
    
    st.markdown(f"""
    <div class="highlight-box" style="border-color: {color_map_css.get(classification, '#000')};">
        <h4>Classificação: <span style="color: {color_map_css.get(classification, '#333')}">{classification}</span></h4>
        <p>O(A) aluno(a) está entre os <strong>{student_data['Percentil']:.1f}%</strong> melhores da turma.</p>
        <p>Nota final: <strong>{student_data['Total']}/74</strong> ({student_data['Percentual_Total']:.1f}%)</p>
        <p>Média da turma: <strong>{data['Total'].mean():.1f}/74</strong> ({(data['Total'].mean()/74*100):.1f}%)</p>
    </div>
    """, unsafe_allow_html=True)

    col1_ind, col2_ind = st.columns([0.6, 0.4])

    with col1_ind:
        # Gráfico de distribuição com destaque para o aluno
        st.markdown("<h4>Posição na Turma</h4>", unsafe_allow_html=True)
        fig_dist_highlight = px.histogram(
            data, 
            x='Total',
            nbins=20,
            title=f'Posição de {selected_student} na Distribuição da Turma',
            labels={'Total': 'Pontuação Total', 'count': 'Número de Alunos'},
            color_discrete_sequence=['#94d2bd']
        )
        
        # Adiciona linha vertical para o aluno selecionado
        fig_dist_highlight.add_vline(
            x=student_data['Total'], 
            line_dash="dash", 
            line_color="#e76f51", 
            line_width=3,
            annotation_text=f" {selected_student}",
            annotation_position="top right"
        )
        fig_dist_highlight.update_layout(template='plotly_white')
        st.plotly_chart(fig_dist_highlight, use_container_width=True)

    with col2_ind:
        # Comparação com a média da turma (Radar Chart)
        st.markdown("<h4>Comparativo de Notas</h4>", unsafe_allow_html=True)
        
        score_cols = ['CAED1', 'CAED2', 'impulso']
        student_scores = student_data[score_cols].values
        class_avg_scores = data[score_cols].mean().values

        fig_radar = go.Figure()

        # Radar para o aluno
        fig_radar.add_trace(go.Scatterpolar(
            r=student_scores,
            theta=score_cols,
            fill='toself',
            name=selected_student,
            marker_color='#0a9396'
        ))

        # Radar para a média da turma
        fig_radar.add_trace(go.Scatterpolar(
            r=class_avg_scores,
            theta=score_cols,
            fill='toself',
            name='Média da Turma',
            marker_color='#ee9b00',
            opacity=0.6
        ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(data[score_cols].max().max(), student_scores.max()) + 2]
                )
            ),
            title=f'{selected_student} vs. Média da Turma',
            showlegend=True,
            template='plotly_white'
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        # Footer informativo
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #94a3b8; padding: 25px;">
  <p> Desenvolvido por: Mauricio A. Ribeiro</p>
</div>
""", unsafe_allow_html=True)