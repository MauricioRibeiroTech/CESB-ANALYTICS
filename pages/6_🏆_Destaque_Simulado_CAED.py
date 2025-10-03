import streamlit as st
import pandas as pd
import os
import re
import glob

# ==============================================================================
# Configuração da Página
# ==============================================================================
st.set_page_config(
    page_title="🌟 Destaques SAEB",
    layout="wide",
    page_icon="🌟"
)

# ==============================================================================
# Estilo CSS Personalizado
# ==============================================================================
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #6a11cb;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px #e0e0e0;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #2575fc;
        margin-top: 2.5rem;
        margin-bottom: 1.5rem;
        font-weight: bold;
        border-bottom: 3px solid #f0f2f6;
        padding-bottom: 0.5rem;
    }
    .superstar-card {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        text-align: center;
    }
    .superstar-card .name {
        font-size: 1.8rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .superstar-card .score {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .superstar-card .details {
        font-size: 1rem;
    }
    .champion-card {
        background: #FFFFFF;
        padding: 1.5rem;
        border-radius: 15px;
        color: #333;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border-left: 8px solid #FFD700;
    }
    .champion-card .name {
        font-size: 1.2rem;
        font-weight: bold;
        color: #6a11cb;
    }
    .champion-card .score {
        font-size: 2rem;
        font-weight: bold;
        color: #34A853;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# Funções de Processamento de Dados
# ==============================================================================

@st.cache_data
def processar_arquivo(caminho_arquivo):
    """Lê um arquivo CSV, extrai metadados e calcula o desempenho dos alunos."""
    try:
        nome_arquivo = os.path.basename(caminho_arquivo)
        partes = re.match(r"CAED(\d+)_(\d+)_(\w+)\.csv", nome_arquivo, re.IGNORECASE)
        if not partes: return None

        edicao = f"CAED {partes.group(1)}"
        serie = f"{partes.group(2)}º Ano"
        # Garante que 'matematica' e 'portugues' sejam padronizados
        disciplina = partes.group(3).capitalize().replace("ú", "u").replace("á", "a")

        df = pd.read_csv(caminho_arquivo, delimiter=';')
        df.columns = [col.strip() for col in df.columns]
        df = df.rename(columns={'Aluno': 'aluno', 'Turma': 'turma'})

        # Limpeza e padronização dos dados
        df['aluno'] = df['aluno'].str.strip().str.title()
        df['turma'] = df['turma'].str.strip()

        colunas_habilidade = [col for col in df.columns if col.upper().startswith('H')]
        if not colunas_habilidade: return None

        df['desempenho'] = df[colunas_habilidade].apply(lambda x: (x > 0).sum(), axis=1) / len(colunas_habilidade) * 100
        df['edicao'] = edicao
        df['disciplina'] = disciplina
        df['serie'] = serie
        return df[['aluno', 'turma', 'serie', 'edicao', 'disciplina', 'desempenho']]
    except Exception:
        return None

@st.cache_data
def carregar_e_unir_dados():
    """Carrega todos os arquivos CAED, processa e une os dados de Português e Matemática."""
    arquivos_csv = glob.glob("CAED*.csv")
    if not arquivos_csv: return pd.DataFrame()

    lista_dfs = [processar_arquivo(f) for f in arquivos_csv]
    df_completo = pd.concat([df for df in lista_dfs if df is not None], ignore_index=True)

    if df_completo.empty or 'disciplina' not in df_completo.columns: return pd.DataFrame()
    
    # Pivota a tabela para ter colunas de disciplina
    df_pivot = df_completo.pivot_table(
        index=['aluno', 'turma', 'serie', 'edicao'],
        columns='disciplina',
        values='desempenho'
    ).reset_index()

    # Filtra para alunos com notas em ambas as disciplinas e calcula a média
    if 'Portugues' in df_pivot.columns and 'Matematica' in df_pivot.columns:
        df_pivot = df_pivot.dropna(subset=['Portugues', 'Matematica'])
        df_pivot['Desempenho Geral'] = df_pivot[['Portugues', 'Matematica']].mean(axis=1)
        return df_pivot
    
    return pd.DataFrame()

# ==============================================================================
# Interface Principal da Aplicação
# ==============================================================================

st.markdown("<h1 class='main-header'>🌟 Destaques Combinados</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Análise dos alunos com melhor desempenho simultâneo em Português e Matemática.</p>", unsafe_allow_html=True)

df_final = carregar_e_unir_dados()

if df_final.empty:
    st.error("❌ Nenhum dado de aluno com desempenho em ambas as disciplinas foi encontrado. Verifique os arquivos CSV.")
else:
    # --- Barra Lateral com Filtro de Edição ---
    st.sidebar.header("🔍 Filtro de Avaliação")
    edicao_unica = sorted(df_final['edicao'].unique())
    edicao_selecionada = st.sidebar.selectbox(
        'Selecione a Edição da Prova:',
        options=edicao_unica
    )

    df_filtrado = df_final[df_final['edicao'] == edicao_selecionada].copy()

    # --- Destaques Globais (9º e 3º Ano) ---
    st.markdown("<h2 class='sub-header'>🏆 Super Destaques da Avaliação</h2>", unsafe_allow_html=True)
    
    df_9ano = df_filtrado[df_filtrado['serie'] == '9º Ano']
    df_3ano = df_filtrado[df_filtrado['serie'] == '3º Ano']

    destaque_9ano = df_9ano.loc[df_9ano['Desempenho Geral'].idxmax()] if not df_9ano.empty else None
    destaque_3ano = df_3ano.loc[df_3ano['Desempenho Geral'].idxmax()] if not df_3ano.empty else None

    col1, col2 = st.columns(2)
    with col1:
        if destaque_9ano is not None:
            st.markdown(f"""
            <div class="superstar-card">
                <div style="font-size: 1.2rem;">Destaque Global - 9º Ano</div>
                <div class="name">🚀 {destaque_9ano['aluno']}</div>
                <div class="score">{destaque_9ano['Desempenho Geral']:.2f}%</div>
                <div class="details">
                    Turma: {destaque_9ano['turma']} <br>
                    (Port: {destaque_9ano['Portugues']:.1f}% | Mat: {destaque_9ano['Matematica']:.1f}%)
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Nenhum destaque encontrado para o 9º Ano.")

    with col2:
        if destaque_3ano is not None:
            st.markdown(f"""
            <div class="superstar-card">
                <div style="font-size: 1.2rem;">Destaque Global - 3º Ano</div>
                <div class="name">🌠 {destaque_3ano['aluno']}</div>
                <div class="score">{destaque_3ano['Desempenho Geral']:.2f}%</div>
                <div class="details">
                    Turma: {destaque_3ano['turma']} <br>
                    (Port: {destaque_3ano['Portugues']:.1f}% | Mat: {destaque_3ano['Matematica']:.1f}%)
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Nenhum destaque encontrado para o 3º Ano.")

    # --- Destaques por Turma ---
    st.markdown("<h2 class='sub-header'>🥇 Campeões de Cada Turma</h2>", unsafe_allow_html=True)

    idx_campeoes_turma = df_filtrado.groupby('turma')['Desempenho Geral'].idxmax()
    df_campeoes = df_filtrado.loc[idx_campeoes_turma].sort_values('turma')

    if df_campeoes.empty:
        st.warning("Nenhum campeão de turma encontrado para a edição selecionada.")
    else:
        num_cols = min(3, len(df_campeoes))
        cols = st.columns(num_cols)
        
        for i, row in enumerate(df_campeoes.itertuples()):
            with cols[i % num_cols]:
                st.markdown(f"""
                <div class="champion-card">
                    <div class="name">Turma {row.turma}</div>
                    <p style="font-size: 1.1rem; margin-top: 5px;"><strong>{row.aluno}</strong></p>
                    <div class="score">{row._7:.2f}%</div>
                    <div class="details">
                        Port: {row.Portugues:.1f}% | Mat: {row.Matematica:.1f}%
                    </div>
                </div>
                """, unsafe_allow_html=True)  
