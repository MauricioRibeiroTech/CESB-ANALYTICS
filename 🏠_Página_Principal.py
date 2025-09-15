import streamlit as st
import pandas as pd
import os

# Configurações da página
st.set_page_config(
    page_title="CESB Analytic - Recomposição da Aprendizagem",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
custom_css = """
<style>
    .main {
        background-color: #f8f9fa;
    }
    .header {
        background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%);
        padding: 3rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    .feature-card {
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        transition: transform 0.3s;
        background: gray;
        border-left: 4px solid #1E40AF;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .stats-card {
        text-align: center;
        padding: 1.5rem;
        border-radius: 10px;
        background: gray;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .stats-value {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .stats-label {
        font-size: 0.9rem;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
    h1, h2, h3 {
        color: #1E40AF;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Sidebar de navegação
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="font-size: 24px;">CESB Analytic</h1>
        <h2 style="font-size: 18px;">Decifrando Potenciais, Transformando Aprendizagens</h2>
    </div>
    """, unsafe_allow_html=True)
  
    # Verificar se existem dados
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <p style="font-size: 14px;">Colégio Estadual São Braz</p>
        <p style="font-size: 12px;">Recomposição da Aprendizagem</p>
    </div>
    """, unsafe_allow_html=True)

# Conteúdo principal
st.markdown("""
<div class="header">
    <h1 style="color: white; text-align: center; margin: 0;">CESB Analytic</h1>
    <h2 style="color: white; text-align: center; margin: 0;">Recomposição da Aprendizagem</h2>
</div>
""", unsafe_allow_html=True)

# Introdução
st.markdown("""
Mais do que uma plataforma, somos o seu parceiro estratégico na recomposição da aprendizagem. O CESB Analytic foi meticulosamente desenvolvido para oferecer um diagnóstico inteligente e profundamente direcionado, iluminando o caminho para o desenvolvimento das habilidades essenciais de cada estudante.
""")
# Seção de recursos
st.markdown("## ✨ Módulos Disponíveis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>🔍 Análise Individual</h3>
        <p>Visualize o desempenho individual de cada aluno com gráficos de radar e estatísticas detalhadas por habilidade.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>👥 Grupos por Habilidade</h3>
        <p>Agrupe alunos por nível de domínio em habilidades específicas para intervenções direcionadas.</p>
    </div>
    """, unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>⚖️ Grupos Balanceados</h3>
        <p>Forme grupos equilibrados automaticamente usando algoritmo de machine learning (K-Means).</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <h3>📊 Estatísticas Gerais</h3>
        <p>Visualize métricas gerais de desempenho e distribuição de habilidades entre os alunos.</p>
    </div>
    """, unsafe_allow_html=True)
# Como usar
st.markdown("## 📌 Como Utilizar")

st.markdown("""
1. **Navegue** entre os módulos usando o menu lateral
2. **Selecione** as turmas e habilidades desejadas
3. **Analise** os gráficos e estatísticas apresentados
4. **Forme** grupos de intervenção conforme necessário
5. **Exporte** os relatórios para uso pedagógico
""")

# Rodapé
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; font-size: 14px;">
    <p>Colégio Estadual São Braz - Recomposição da Aprendizagem</p>
    <p>© 2025 CESB Analytic - Todos os direitos reservados</p>
</div>
""", unsafe_allow_html=True)