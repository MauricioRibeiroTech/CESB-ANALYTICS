import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="🌟 Destaques Prova Paraná",
    layout="wide",
    page_icon="🌟"
)

# CSS personalizado para melhorar a aparência
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #2e86ab;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .highlight-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .gold-card {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 6px 20px rgba(255,215,0,0.3);
        border: 3px solid #FFD700;
    }
    .diamond-card {
        background: linear-gradient(135deg, #B9F2FF 0%, #0077B6 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(0,119,182,0.4);
        border: 4px solid #B9F2FF;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    .edition-badge {
        background: #ff6b6b;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 1rem;
    }
    .turma-section {
        background: #6395EE;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #4ecdc4;
    }
    .global-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<div class="main-header">🏆 Alunos em Destaque por Edição Prova Paraná</div>', unsafe_allow_html=True)

# Função para carregar dados
@st.cache_data
def carregar_dados():
    """Carrega todos os arquivos CSV da pasta"""
    dados = {}
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Lista todos os arquivos CSV na pasta
    arquivos_csv = [f for f in os.listdir(script_dir) if f.endswith('.csv')]
    
    for arquivo in arquivos_csv:
        try:
            caminho_arquivo = os.path.join(script_dir, arquivo)
            # Tentar diferentes encodings e separadores
            try:
                df = pd.read_csv(caminho_arquivo, sep=';', encoding='utf-8', decimal=',')
            except:
                try:
                    df = pd.read_csv(caminho_arquivo, sep=';', encoding='latin-1', decimal=',')
                except:
                    df = pd.read_csv(caminho_arquivo, sep=',', encoding='utf-8')
            
            # Limpar nomes das colunas
            df.columns = df.columns.str.strip()
            
            # Adicionar coluna de turma baseada no nome do arquivo
            turma = arquivo.split('_')[0]
            df['Turma'] = turma
            
            # Adicionar coluna de edição
            if '_1ED' in arquivo:
                edicao = '1ED'
            elif '_2ED' in arquivo:
                edicao = '2ED'
            else:
                edicao = 'OUTRA'
            df['Edição'] = edicao
            
            # Adicionar coluna de série (9º ou 3º ano)
            if turma.startswith('9'):
                df['Série'] = '9º Ano'
            elif turma.startswith('3'):
                df['Série'] = '3º Ano'
            else:
                df['Série'] = 'Outra'
            
            # Converter coluna de porcentagem para numérico
            if 'percAcertosAluno' in df.columns:
                # Remover possíveis vírgulas e converter para float
                df['percAcertosAluno'] = pd.to_numeric(
                    df['percAcertosAluno'].astype(str).str.replace(',', '.'), 
                    errors='coerce'
                )
            
            dados[arquivo] = df
            
        except Exception as e:
            st.warning(f"Erro ao carregar {arquivo}: {e}")
    
    return dados

# Função para encontrar alunos destaque
def encontrar_alunos_destaque(dados):
    """Encontra os alunos com melhor desempenho em cada edição"""
    alunos_destaque = []
    
    for nome_arquivo, df in dados.items():
        try:
            # Verificar se a coluna de porcentagem de acertos existe
            if 'percAcertosAluno' in df.columns and not df['percAcertosAluno'].isna().all():
                # Remover linhas com valores NaN
                df_clean = df.dropna(subset=['percAcertosAluno'])
                
                if not df_clean.empty:
                    # Encontrar aluno com maior porcentagem de acertos
                    idx_max = df_clean['percAcertosAluno'].idxmax()
                    aluno_destaque = df_clean.loc[idx_max].copy()
                    
                    # Adicionar informações adicionais
                    aluno_destaque['Arquivo'] = nome_arquivo
                    aluno_destaque['Posição'] = 1
                    
                    alunos_destaque.append(aluno_destaque)
                
        except Exception as e:
            st.warning(f"Erro ao processar {nome_arquivo}: {e}")
    
    if alunos_destaque:
        return pd.DataFrame(alunos_destaque)
    else:
        return pd.DataFrame()

# Função para encontrar alunos destaque por turma na 2ª edição
def encontrar_destaque_por_turma_2ed(dados):
    """Encontra o aluno destaque de cada turma específica na 2ª edição"""
    turmas_2ed = ['9A_2ED', '9B_2ED', '3A_2ED', '3B_2ED', '3C_2ED']
    destaque_turmas = []
    
    for nome_arquivo, df in dados.items():
        # Verificar se é um arquivo da 2ª edição das turmas específicas
        if any(turma in nome_arquivo for turma in turmas_2ed):
            try:
                if 'percAcertosAluno' in df.columns and not df['percAcertosAluno'].isna().all():
                    # Remover linhas com valores NaN
                    df_clean = df.dropna(subset=['percAcertosAluno'])
                    
                    if not df_clean.empty:
                        # Encontrar aluno com maior porcentagem de acertos
                        idx_max = df_clean['percAcertosAluno'].idxmax()
                        aluno_destaque = df_clean.loc[idx_max].copy()
                        
                        aluno_destaque['Arquivo'] = nome_arquivo
                        aluno_destaque['Categoria'] = 'Destaque da Turma - 2ª Edição'
                        destaque_turmas.append(aluno_destaque)
                        
            except Exception as e:
                st.warning(f"Erro ao processar {nome_arquivo}: {e}")
    
    if destaque_turmas:
        return pd.DataFrame(destaque_turmas)
    else:
        return pd.DataFrame()

# Função para encontrar alunos destaque globais por série
def encontrar_destaque_global_por_serie(dados):
    """Encontra os alunos com melhor desempenho global por série"""
    todos_alunos = []
    
    for nome_arquivo, df in dados.items():
        try:
            if 'percAcertosAluno' in df.columns and not df['percAcertosAluno'].isna().all():
                df_clean = df.dropna(subset=['percAcertosAluno'])
                if not df_clean.empty:
                    # Adicionar todos os alunos à lista
                    for idx, aluno in df_clean.iterrows():
                        aluno_copy = aluno.copy()
                        aluno_copy['Arquivo'] = nome_arquivo
                        # Garantir que temos uma cópia independente
                        aluno_dict = {}
                        for col in aluno_copy.index:
                            aluno_dict[col] = aluno_copy[col]
                        todos_alunos.append(aluno_dict)
        except Exception as e:
            st.warning(f"Erro ao processar {nome_arquivo}: {e}")
    
    if todos_alunos:
        df_todos = pd.DataFrame(todos_alunos)
        
        # Encontrar destaque global do 9º ano
        alunos_9ano = df_todos[df_todos['Série'] == '9º Ano']
        if not alunos_9ano.empty:
            idx_melhor_9ano = alunos_9ano['percAcertosAluno'].idxmax()
            destaque_9ano = alunos_9ano.loc[idx_melhor_9ano]
            # Criar uma cópia independente
            destaque_9ano_dict = {}
            for col in destaque_9ano.index:
                destaque_9ano_dict[col] = destaque_9ano[col]
            destaque_9ano_dict['Categoria'] = 'Destaque Global - 9º Ano'
        else:
            destaque_9ano_dict = None
        
        # Encontrar destaque global do 3º ano
        alunos_3ano = df_todos[df_todos['Série'] == '3º Ano']
        if not alunos_3ano.empty:
            idx_melhor_3ano = alunos_3ano['percAcertosAluno'].idxmax()
            destaque_3ano = alunos_3ano.loc[idx_melhor_3ano]
            # Criar uma cópia independente
            destaque_3ano_dict = {}
            for col in destaque_3ano.index:
                destaque_3ano_dict[col] = destaque_3ano[col]
            destaque_3ano_dict['Categoria'] = 'Destaque Global - 3º Ano'
        else:
            destaque_3ano_dict = None
        
        return destaque_9ano_dict, destaque_3ano_dict
    else:
        return None, None

# Função para extrair valor numérico seguro
def get_valor_seguro(aluno, campo, padrao=0.0):
    """Extrai valor numérico de forma segura de um dicionário ou Series"""
    try:
        if campo in aluno and pd.notna(aluno[campo]):
            if hasattr(aluno[campo], 'iloc'):
                # É uma Series, pegar o primeiro valor
                return float(aluno[campo].iloc[0])
            else:
                # É um valor único
                return float(aluno[campo])
        return padrao
    except (ValueError, TypeError):
        return padrao

# Função para extrair texto seguro
def get_texto_seguro(aluno, campo, padrao='N/A'):
    """Extrai texto de forma segura de um dicionário ou Series"""
    try:
        if campo in aluno and pd.notna(aluno[campo]):
            if hasattr(aluno[campo], 'iloc'):
                # É uma Series, pegar o primeiro valor
                return str(aluno[campo].iloc[0])
            else:
                # É um valor único
                return str(aluno[campo])
        return padrao
    except (ValueError, TypeError):
        return padrao

# Função para criar card de aluno destaque
def criar_card_aluno(aluno, cor="#667eea", destaque_geral=False, destaque_global=False):
    """Cria um card visualmente atrativo para cada aluno destaque"""
    
    # Extrair valores de forma segura
    nome_aluno = get_texto_seguro(aluno, 'nomeAluno', 'Nome não disponível')
    turma = get_texto_seguro(aluno, 'Turma', 'N/A')
    edicao = get_texto_seguro(aluno, 'Edição', 'N/A')
    serie = get_texto_seguro(aluno, 'Série', 'N/A')
    desempenho = get_valor_seguro(aluno, 'percAcertosAluno')
    
    if destaque_global:
        template = f"""
        <div class="diamond-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h1 style="margin: 0; color: white;">💎 {nome_aluno}</h1>
                    <p style="margin: 0.5rem 0; color: white; font-size: 1.4rem;">
                        <strong>Série:</strong> {serie} | 
                        <strong>Turma:</strong> {turma} | 
                        <strong>Edição:</strong> {edicao}
                    </p>
                    <p style="margin: 0; color: white; font-size: 1.2rem;">
                        <strong>🏆 DESTAQUE GLOBAL</strong>
                    </p>
                </div>
                <div style="text-align: right;">
                    <h1 style="margin: 0; color: white; font-size: 4rem;">
                        {desempenho:.1f}%
                    </h1>
                    <p style="margin: 0; color: white; font-size: 1.4rem;">Melhor Desempenho</p>
                </div>
            </div>
        </div>
        """
    elif destaque_geral:
        template = f"""
        <div class="gold-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h2 style="margin: 0; color: white;">👑 {nome_aluno}</h2>
                    <p style="margin: 0.5rem 0; color: white; font-size: 1.2rem;">
                        <strong>Turma:</strong> {turma} | 
                        <strong>Edição:</strong> {edicao}
                    </p>
                    <p style="margin: 0; color: white; font-size: 1rem;">
                        <strong>🏆 Destaque Geral da Turma</strong>
                    </p>
                </div>
                <div style="text-align: right;">
                    <h1 style="margin: 0; color: white; font-size: 3rem;">
                        {desempenho:.1f}%
                    </h1>
                    <p style="margin: 0; color: white; font-size: 1.2rem;">Melhor Desempenho</p>
                </div>
            </div>
        </div>
        """
    else:
        template = f"""
        <div class="highlight-card" style="background: linear-gradient(135deg, {cor} 0%, {cor}88 100%);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3 style="margin: 0; color: white;">🎓 {nome_aluno}</h3>
                    <p style="margin: 0.5rem 0; color: white; font-size: 1.1rem;">
                        <strong>Turma:</strong> {turma} | 
                        <strong>Edição:</strong> {edicao}
                    </p>
                </div>
                <div style="text-align: right;">
                    <h2 style="margin: 0; color: white; font-size: 2.5rem;">
                        {desempenho:.1f}%
                    </h2>
                    <p style="margin: 0; color: white;">Acertos</p>
                </div>
            </div>
        </div>
        """
    
    st.markdown(template, unsafe_allow_html=True)

# Carregar dados
with st.spinner('📊 Carregando dados...'):
    dados = carregar_dados()

if not dados:
    st.error("❌ Nenhum arquivo CSV encontrado na pasta do script.")
    st.info("💡 Certifique-se de que os arquivos CSV estão na mesma pasta que este script.")
else:
    # Encontrar alunos destaque
    alunos_destaque = encontrar_alunos_destaque(dados)
    alunos_destaque_turmas_2ed = encontrar_destaque_por_turma_2ed(dados)
    destaque_9ano, destaque_3ano = encontrar_destaque_global_por_serie(dados)
    
    # DEBUG: Mostrar informações sobre os dados carregados
    st.sidebar.markdown("### 🔍 Informações dos Dados")
    st.sidebar.write(f"Arquivos CSV carregados: {len(dados)}")
    if not alunos_destaque.empty:
        st.sidebar.write(f"Alunos destaque encontrados: {len(alunos_destaque)}")
    if destaque_9ano:
        st.sidebar.write("✅ Destaque 9º Ano encontrado")
    if destaque_3ano:
        st.sidebar.write("✅ Destaque 3º Ano encontrado")
    
    # SEÇÃO: DESTAQUES GLOBAIS POR SÉRIE
    if destaque_9ano is not None or destaque_3ano is not None:
        st.markdown("---")
        st.markdown('<div class="sub-header">💎 Destaques Globais por Série</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if destaque_9ano is not None:
                st.markdown("### 🎯 Destaque Global - 9º Ano")
                criar_card_aluno(destaque_9ano, destaque_global=True)
                # Mostrar informações detalhadas
                with st.expander("📊 Detalhes do Destaque 9º Ano"):
                    st.write(f"**Nome:** {get_texto_seguro(destaque_9ano, 'nomeAluno')}")
                    st.write(f"**Turma:** {get_texto_seguro(destaque_9ano, 'Turma')}")
                    st.write(f"**Edição:** {get_texto_seguro(destaque_9ano, 'Edição')}")
                    st.write(f"**Desempenho:** {get_valor_seguro(destaque_9ano, 'percAcertosAluno'):.1f}%")
                    st.write(f"**CGM:** {get_texto_seguro(destaque_9ano, 'cgm', 'N/A')}")
            else:
                st.info("📊 Nenhum aluno do 9º ano encontrado para análise")
        
        with col2:
            if destaque_3ano is not None:
                st.markdown("### 🎯 Destaque Global - 3º Ano")
                criar_card_aluno(destaque_3ano, destaque_global=True)
                # Mostrar informações detalhadas
                with st.expander("📊 Detalhes do Destaque 3º Ano"):
                    st.write(f"**Nome:** {get_texto_seguro(destaque_3ano, 'nomeAluno')}")
                    st.write(f"**Turma:** {get_texto_seguro(destaque_3ano, 'Turma')}")
                    st.write(f"**Edição:** {get_texto_seguro(destaque_3ano, 'Edição')}")
                    st.write(f"**Desempenho:** {get_valor_seguro(destaque_3ano, 'percAcertosAluno'):.1f}%")
                    st.write(f"**CGM:** {get_texto_seguro(destaque_3ano, 'cgm', 'N/A')}")
            else:
                st.info("📊 Nenhum aluno do 3º ano encontrado para análise")
    
    if not alunos_destaque.empty:
        # Separar por edições
        alunos_1ed = alunos_destaque[alunos_destaque['Edição'] == '1ED']
        alunos_2ed = alunos_destaque[alunos_destaque['Edição'] == '2ED']
        
        # Layout principal - Destaques por Edição
        st.markdown("---")
        st.markdown('<div class="sub-header">🎯 Destaques por Edição</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div style="font-size: 1.5rem; color: #ff6b6b; margin-bottom: 1rem;">📚 1ª Edição - Alunos Destaque</div>', unsafe_allow_html=True)
            if not alunos_1ed.empty:
                for idx, aluno in alunos_1ed.iterrows():
                    criar_card_aluno(aluno, "#ff6b6b")
            else:
                st.info("📝 Nenhum aluno destaque encontrado para a 1ª edição")
        
        with col2:
            st.markdown('<div style="font-size: 1.5rem; color: #4ecdc4; margin-bottom: 1rem;">📚 2ª Edição - Alunos Destaque</div>', unsafe_allow_html=True)
            if not alunos_2ed.empty:
                for idx, aluno in alunos_2ed.iterrows():
                    criar_card_aluno(aluno, "#4ecdc4")
            else:
                st.info("📝 Nenhum aluno destaque encontrado para a 2ª edição")
        
        # Destaques Gerais por Turma - 2ª Edição
        st.markdown("---")
        st.markdown('<div class="sub-header">👑 Destaques Gerais por Turma - 2ª Edição</div>', unsafe_allow_html=True)
        
        if not alunos_destaque_turmas_2ed.empty:
            # Agrupar por turma
            turmas_especificas = ['9A', '9B', '3A', '3B', '3C']
            
            for turma in turmas_especificas:
                alunos_turma = alunos_destaque_turmas_2ed[alunos_destaque_turmas_2ed['Turma'] == turma]
                
                if not alunos_turma.empty:
                    st.markdown(f'<div class="turma-section"><h3>🏫 Turma {turma}</h3></div>', unsafe_allow_html=True)
                    
                    # Encontrar o melhor aluno da turma
                    idx_melhor = alunos_turma['percAcertosAluno'].idxmax()
                    melhor_aluno_turma = alunos_turma.loc[idx_melhor]
                    
                    # Card do destaque geral da turma
                    criar_card_aluno(melhor_aluno_turma, "#FFD700", destaque_geral=True)
        
        # Estatísticas gerais
        st.markdown("---")
        st.markdown('<div class="sub-header">📈 Estatísticas Gerais</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total de Alunos Destaque", 
                len(alunos_destaque),
                help="Número total de alunos em destaque considerando todas as turmas e edições"
            )
        
        with col2:
            if not alunos_1ed.empty:
                media_1ed = alunos_1ed['percAcertosAluno'].mean()
                st.metric(
                    "Média 1ª Edição", 
                    f"{media_1ed:.1f}%",
                    help="Média de acertos dos alunos destaque na 1ª edição"
                )
            else:
                st.metric("Média 1ª Edição", "0.0%")
        
        with col3:
            if not alunos_2ed.empty:
                media_2ed = alunos_2ed['percAcertosAluno'].mean()
                st.metric(
                    "Média 2ª Edição", 
                    f"{media_2ed:.1f}%",
                    help="Média de acertos dos alunos destaque na 2ª edição"
                )
            else:
                st.metric("Média 2ª Edição", "0.0%")
        
        with col4:
            if len(alunos_destaque) > 0:
                melhor_desempenho = alunos_destaque['percAcertosAluno'].max()
                st.metric(
                    "Melhor Desempenho Geral", 
                    f"{melhor_desempenho:.1f}%",
                    help="Melhor desempenho entre todos os alunos destaque"
                )
            else:
                st.metric("Melhor Desempenho Geral", "0.0%")
        
        # Tabela detalhada
        st.markdown("---")
        st.markdown('<div class="sub-header">📋 Detalhes dos Alunos Destaque</div>', unsafe_allow_html=True)
        
        # Combinar todos os dados para a tabela
        todos_alunos_destaque = pd.concat([alunos_destaque, alunos_destaque_turmas_2ed], ignore_index=True)
        
        # Adicionar destaques globais se existirem
        if destaque_9ano is not None:
            # Converter o dicionário para DataFrame
            destaque_9ano_df = pd.DataFrame([destaque_9ano])
            todos_alunos_destaque = pd.concat([todos_alunos_destaque, destaque_9ano_df], ignore_index=True)
        
        if destaque_3ano is not None:
            # Converter o dicionário para DataFrame
            destaque_3ano_df = pd.DataFrame([destaque_3ano])
            todos_alunos_destaque = pd.concat([todos_alunos_destaque, destaque_3ano_df], ignore_index=True)
        
        # Preparar dados para tabela
        dados_tabela = []
        for idx, aluno in todos_alunos_destaque.iterrows():
            nome_aluno = get_texto_seguro(aluno, 'nomeAluno')
            turma = get_texto_seguro(aluno, 'Turma')
            edicao = get_texto_seguro(aluno, 'Edição')
            serie = get_texto_seguro(aluno, 'Série', 'N/A')
            desempenho = get_valor_seguro(aluno, 'percAcertosAluno')
            cgm = get_texto_seguro(aluno, 'cgm', 'N/A')
            presenca = get_texto_seguro(aluno, 'presenca', 'N/A')
            categoria = get_texto_seguro(aluno, 'Categoria', 'Destaque por Arquivo')
            
            dados_tabela.append({
                'Aluno': nome_aluno,
                'Série': serie,
                'Turma': turma,
                'Edição': edicao,
                'Desempenho (%)': f"{desempenho:.1f}%",
                'CGM': cgm,
                'Presença': presenca,
                'Categoria': categoria
            })
        
        df_tabela = pd.DataFrame(dados_tabela)
        
        # Ordenar por desempenho (decrescente)
        df_tabela['Desempenho_Num'] = df_tabela['Desempenho (%)'].str.replace('%', '').astype(float)
        df_tabela = df_tabela.sort_values('Desempenho_Num', ascending=False)
        df_tabela = df_tabela.drop('Desempenho_Num', axis=1)
        
        st.dataframe(
            df_tabela,
            use_container_width=True,
            hide_index=True,
            column_config={
                'Aluno': 'Aluno',
                'Série': 'Série',
                'Turma': 'Turma',
                'Edição': 'Edição',
                'Desempenho (%)': st.column_config.NumberColumn(
                    'Desempenho (%)',
                    help="Porcentagem de acertos do aluno"
                ),
                'CGM': 'CGM',
                'Presença': 'Presença',
                'Categoria': 'Categoria'
            }
        )
        
    else:
        st.warning("⚠️ Não foi possível identificar alunos destaque nos arquivos carregados.")
        st.info("💡 Verifique se os arquivos CSV possuem a coluna 'percAcertosAluno'")

# Rodapé
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; font-size: 14px; padding: 2rem;">
    <p>🏆 <strong>Sistema de Análise de Alunos Destaque</strong></p>
    <p>Desenvolvido para identificar e celebrar a excelência acadêmica</p>
    <p>© 2025 - Todos os direitos reservados</p>
</div>
""", unsafe_allow_html=True)