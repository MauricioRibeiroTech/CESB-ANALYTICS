import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from PIL import Image

# Configuração da página
st.set_page_config(page_title="CESB-Recomposição de Aprendizagem", layout="wide")

# Título do aplicativo
st.title("Lingua Portuguesa- Primeira Prova Diagnóstica- CAED - 9º Ano")

# Dicionário com descrições das habilidades
DESCRICOES_HABILIDADES = {
    "H01": "Identificar a finalidade de textos de diferentes gêneros.",
    "H02": "Localizar informação explícita.",
    "H03": "Inferir informações em textos.",
    "H04": "Reconhecer efeito de humor ou de ironia em um texto.",
    "H05": "Distinguir ideias centrais de secundárias ou tópicos e subtópicos em um dado gênero textual.",
    "H06": "Reconhecer os elementos que compõem uma narrativa e o conflito gerador.",
    "H07": "Identificar a tese de um texto.",
    "H08": "Reconhecer posições distintas relativas ao mesmo fato ou mesmo tema.",
    "H09": "Reconhecer as relações entre partes de um texto, identificando os recursos coesivos que contribuem para a sua continuidade.",
    "H10": "Distinguir um fato da opinião.",
    "H11": "Reconhecer o sentido das relações lógico-discursivas em um texto.",
    "H12": "Reconhecer o efeito de sentido decorrente da escolha de uma determinada palavra ou expressão.",
    "H13": "Estabelecer relação entre a tese e os argumentos oferecidos para sustentá-la.",
    "H14": "Reconhecer o efeito de sentido decorrente da exploração de recursos ortográficos e/ou morfossintáticos.",
    "H15": "Identificar as marcas linguísticas que evidenciam o locutor e o interlocutor de um texto.",
}

# Função para carregar dados
def carregar_dados():
    """Carrega o arquivo dados.csv da mesma pasta do script"""
    try:
        # Tenta encontrar o arquivo na mesma pasta
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, 'CAED1_9_portugues.csv')
        
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
            return df
        else:
            # Se não encontrar, tenta na pasta atual de trabalho
            csv_path = 'dados.csv'
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
                return df
            else:
                st.error("Arquivo 'dados.csv' não encontrado na pasta do script.")
                st.info("Certifique-se de que o arquivo 'dados.csv' está na mesma pasta que este script.")
                return None
                
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return None

# Função para obter descrição do nível
def get_nivel_descricao(valor):
    if valor == 0:
        return "❌ Não Domina"
    elif valor == 1:
        return "⚠️ Domina"
    elif valor == 2:
        return "✅ Domina Plenamente"
    else:  # valor == 3
        return "🏆 Completamente Dominado"

# Função para obter descrição da habilidade
def get_descricao_habilidade(codigo):
    return DESCRICOES_HABILIDADES.get(codigo, "Descrição não disponível")

# Carregar dados automaticamente
df = carregar_dados()

if df is not None:
    try:
        # Limpar nomes das colunas
        df.columns = df.columns.str.strip()
        
        # Filtrar apenas as colunas de H01 a H20
        habilidades_cols = [col for col in df.columns if col.startswith('H ') and int(col.split()[1]) <= 15]
        
        # Renomear colunas para formato mais amigável
        nome_habilidades = {col: f'H{int(col.split()[1]):02d}' for col in habilidades_cols}
        df_renomeado = df.rename(columns=nome_habilidades)
        
        # Dados dos alunos com habilidades
        alunos_habilidades = df_renomeado[['Aluno', 'Turma'] + list(nome_habilidades.values())]
        
        # Sidebar com informações
        st.sidebar.header("Colégio Estadual São Braz")
        st.sidebar.write("Recomposição da Aprendizagem")
        st.sidebar.header("📊 Informações Gerais")
        st.sidebar.write(f"**Total de Alunos:** {len(alunos_habilidades)}")
        st.sidebar.write(f"**Total de Habilidades:** {len(nome_habilidades)}")
        
        # Filtro por turma no sidebar
        st.sidebar.header("🎯 Filtros")
        turmas_disponiveis = sorted(alunos_habilidades['Turma'].unique())
        turma_selecionada = st.sidebar.multiselect(
            "Selecionar Turma(s):",
            options=turmas_disponiveis,
            default=turmas_disponiveis,
            help="Selecione uma ou mais turmas para filtrar"
        )
        
        # Aplicar filtro de turma
        if turma_selecionada:
            alunos_filtrados = alunos_habilidades[alunos_habilidades['Turma'].isin(turma_selecionada)]
            st.sidebar.write(f"**Turmas selecionadas:** {', '.join(map(str, turma_selecionada))}")
            st.sidebar.write(f"**Alunos filtrados:** {len(alunos_filtrados)}")
        else:
            alunos_filtrados = alunos_habilidades
            st.sidebar.write("**Mostrando todas as turmas**")
        
        # Menu principal
        st.sidebar.header("🔧 Navegação")
        tipo_analise = st.sidebar.radio(
            "Selecione o tipo de análise:",
            ["Buscar Aluno Específico", "Ver Grupos por Habilidade", "Visão Geral dos Grupos", "Estatísticas Gerais"]
        )
        
        if tipo_analise == "Buscar Aluno Específico":
            st.header("🔍 Análise Individual por Aluno")
            
            # Selecionar aluno apenas da turma filtrada
            alunos_disponiveis = sorted(alunos_filtrados['Aluno'].tolist())
            aluno_selecionado = st.selectbox(
                "Selecione um aluno:",
                alunos_disponiveis
            )
            
            # Dados do aluno selecionado
            aluno_data = alunos_filtrados[alunos_filtrados['Aluno'] == aluno_selecionado].iloc[0]
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.subheader("❌ Não Domina")
                nao_domina = []
                for hab in nome_habilidades.values():
                    if aluno_data[hab] == 0:
                        nao_domina.append(hab)
                if nao_domina:
                    for hab in sorted(nao_domina):
                        st.write(f"• **{hab}**: {get_descricao_habilidade(hab)}")
                else:
                    st.success("🎉 Nenhuma habilidade não dominada!")
            
            with col2:
                st.subheader("⚠️ Domina")
                domina = []
                for hab in nome_habilidades.values():
                    if aluno_data[hab] == 1:
                        domina.append(hab)
                if domina:
                    for hab in sorted(domina):
                        st.write(f"• **{hab}**: {get_descricao_habilidade(hab)}")
                else:
                    st.write("Nenhuma habilidade neste nível")
            
            with col3:
                st.subheader("✅ Domina Plenamente")
                domina_plenamente = []
                for hab in nome_habilidades.values():
                    if aluno_data[hab] == 2:
                        domina_plenamente.append(hab)
                if domina_plenamente:
                    for hab in sorted(domina_plenamente):
                        st.write(f"• **{hab}**: {get_descricao_habilidade(hab)}")
                else:
                    st.write("Nenhuma habilidade neste nível")
                    
            with col4:
                st.subheader("🏆 Completamente Dominado")
                completamente_dominado = []
                for hab in nome_habilidades.values():
                    if aluno_data[hab] == 3:
                        completamente_dominado.append(hab)
                if completamente_dominado:
                    for hab in sorted(completamente_dominado):
                        st.write(f"• **{hab}**: {get_descricao_habilidade(hab)}")
                else:
                    st.write("Nenhuma habilidade neste nível")
            
            # Estatísticas do aluno
            st.subheader("📊 Estatísticas do Aluno")
            col_stats1, col_stats2, col_stats3, col_stats4, col_stats5 = st.columns(5)
            
            with col_stats1:
                st.metric("Não Domina", f"{len(nao_domina)}", f"{len(nao_domina)/len(nome_habilidades)*100:.1f}%")
            with col_stats2:
                st.metric("Domina", f"{len(domina)}", f"{len(domina)/len(nome_habilidades)*100:.1f}%")
            with col_stats3:
                st.metric("Domina Plenamente", f"{len(domina_plenamente)}", f"{len(domina_plenamente)/len(nome_habilidades)*100:.1f}%")
            with col_stats4:
                st.metric("Completamente Dominado", f"{len(completamente_dominado)}", f"{len(completamente_dominado)/len(nome_habilidades)*100:.1f}%")
            with col_stats5:
                pontuacao_total = sum([aluno_data[hab] for hab in nome_habilidades.values()])
                pontuacao_maxima = len(nome_habilidades) * 3
                st.metric("Pontuação Total", f"{pontuacao_total}/{pontuacao_maxima}", f"{pontuacao_total/pontuacao_maxima*100:.1f}%")
                        
            # Gráfico de Radar Elegante
            st.subheader("📊 Perfil de Habilidades - Radar")

            # Dados para o radar
            habilidades = list(nome_habilidades.values())
            valores = [aluno_data[hab] for hab in nome_habilidades.values()]

            # Cores baseadas nos valores
            cores = []
            for valor in valores:
                if valor == 0:
                    cores.append('#FF6B6B')  # Vermelho para não domina
                elif valor == 1:
                    cores.append('#FFD93D')  # Amarelo para domina
                elif valor == 2:
                    cores.append('#6BCB77')  # Verde para domina plenamente
                else:  # valor == 3
                    cores.append('#4D96FF')  # Azul para completamente dominado

            # Criar gráfico de radar
            fig = go.Figure()

            fig.add_trace(go.Scatterpolar(
                r=valores,
                theta=habilidades,
                fill='toself',
                fillcolor='rgba(77, 150, 255, 0.2)',
                line=dict(color='#4D96FF', width=2),
                marker=dict(color=cores, size=8, line=dict(color='white', width=1)),
                name=aluno_selecionado,
                hovertemplate='<b>%{theta}</b><br>Nível: %{r}<br>%{customdata}<extra></extra>',
                customdata=[get_descricao_habilidade(hab) for hab in habilidades]
            ))

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 3],
                        tickvals=[0, 1, 2, 3],
                        ticktext=['Não Domina', 'Domina', 'Domina<br>Plenamente', 'Completamente<br>Dominado'],
                        tickfont=dict(size=10),
                        gridwidth=1
                    ),
                    angularaxis=dict(
                        gridcolor='lightgray',
                        gridwidth=1,
                        linecolor='gray',
                        rotation=90
                    ),
                    bgcolor='rgba(245, 245, 245, 0.1)'
                ),
                title=dict(
                    text=f'<b>Perfil de Habilidades - {aluno_selecionado}</b>',
                    x=0.5,
                    font=dict(size=16)
                ),
                showlegend=False,
                height=500,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Arial, sans-serif")
            )

            st.plotly_chart(fig, use_container_width=True)

            # Legenda de cores
            st.caption("""
            🎨 **Legenda:** 
            <span style='color:#4D96FF; font-weight:bold'>● Completamente Dominado (3)</span> | 
            <span style='color:#6BCB77; font-weight:bold'>● Domina Plenamente (2)</span> | 
            <span style='color:#FFD93D; font-weight:bold'>● Domina (1)</span> | 
            <span style='color:#FF6B6B; font-weight:bold'>● Não Domina (0)</span>
            """, unsafe_allow_html=True)
        
        elif tipo_analise == "Ver Grupos por Habilidade":
            st.header("👥 Grupos de Alunos por Habilidade e Nível")
            
            col_hab, col_nivel = st.columns(2)
            
            with col_hab:
                habilidade_selecionada = st.selectbox(
                    "Selecione a habilidade:",
                    sorted(nome_habilidades.values()),
                    format_func=lambda x: f"{x} - {get_descricao_habilidade(x)}"
                )
            
            with col_nivel:
                nivel_selecionado = st.selectbox(
                    "Selecione o nível:",
                    ["❌ Não Domina (0)", "⚠️ Domina (1)", "✅ Domina Plenamente (2)", "🏆 Completamente Dominado (3)"]
                )
            
            # Mostrar descrição completa da habilidade
            st.info(f"{habilidade_selecionada}: {get_descricao_habilidade(habilidade_selecionada)}")
            
            # Mapeamento correto do nível
            mapeamento_niveis = {
                "❌ Não Domina (0)": 0,
                "⚠️ Domina (1)": 1, 
                "✅ Domina Plenamente (2)": 2,
                "🏆 Completamente Dominado (3)": 3
            }
            nivel_valor = mapeamento_niveis[nivel_selecionado]
            
            # Filtrar alunos (aplicando também o filtro de turma)
            alunos_grupo = alunos_filtrados[alunos_filtrados[habilidade_selecionada] == nivel_valor]
            
            nivel_desc = get_nivel_descricao(nivel_valor).replace('❌ ', '').replace('⚠️ ', '').replace('✅ ', '').replace('🏆 ', '')
            st.subheader(f"Alunos que {nivel_desc} a {habilidade_selecionada}")
            
            if not alunos_grupo.empty:
                st.write(f"**Total: {len(alunos_grupo)} alunos ({len(alunos_grupo)/len(alunos_filtrados)*100:.1f}% das turmas selecionadas)**")
                
                # Mostrar lista de alunos
                for _, aluno in alunos_grupo.iterrows():
                    st.write(f"{aluno['Aluno']} - Turma {aluno['Turma']}")
                
                # Distribuição por turma
                if len(alunos_grupo['Turma'].unique()) > 1:
                    st.subheader("📊 Distribuição por Turma")
                    dist_turma = alunos_grupo['Turma'].value_counts()
                    fig = px.pie(
                        values=dist_turma.values,
                        names=dist_turma.index,
                        title=f"Distribuição por Turma - {habilidade_selecionada} Nível {nivel_valor}"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
            else:
                st.warning(f"Nenhum aluno encontrado no grupo selecionado.")
        
        elif tipo_analise == "Visão Geral dos Grupos":
            st.header("📋 Visão Geral de Todos os Grupos")
            
            # Criar dataframe longo para análise
            grupos_data = []
            
            for _, aluno in alunos_filtrados.iterrows():
                for habilidade in nome_habilidades.values():
                    nivel = aluno[habilidade]
                    grupos_data.append({
                        'Aluno': aluno['Aluno'],
                        'Turma': aluno['Turma'],
                        'Habilidade': habilidade,
                        'Descrição': get_descricao_habilidade(habilidade),
                        'Nível': nivel,
                        'Grupo': get_nivel_descricao(nivel)
                    })
            
            grupos_df = pd.DataFrame(grupos_data)
            
            # Tabela interativa
            st.subheader("Tabela de Agrupamentos")
            
            col_filtro1, col_filtro2 = st.columns(2)
            
            with col_filtro1:
                habilidades_filtro = st.multiselect(
                    "Filtrar por habilidades:",
                    sorted(nome_habilidades.values()),
                    default=sorted(nome_habilidades.values())[:3],
                    format_func=lambda x: f"{x} - {get_descricao_habilidade(x)}"
                )
            
            with col_filtro2:
                grupos_filtro = st.multiselect(
                    "Filtrar por grupos:",
                    ["❌ Não Domina", "⚠️ Domina", "✅ Domina Plenamente", "🏆 Completamente Dominado"],
                    default=["❌ Não Domina", "⚠️ Domina", "✅ Domina Plenamente", "🏆 Completamente Dominado"]
                )
            
            # Aplicar filtros
            grupos_filtrados = grupos_df
            if habilidades_filtro:
                grupos_filtrados = grupos_filtrados[grupos_filtrados['Habilidade'].isin(habilidades_filtro)]
            if grupos_filtro:
                grupos_filtrados = grupos_filtrados[grupos_filtrados['Grupo'].isin(grupos_filtro)]
            
            st.dataframe(
                grupos_filtrados[['Aluno', 'Turma', 'Habilidade', 'Descrição', 'Grupo']],
                hide_index=True,
                use_container_width=True,
                height=400
            )
        
        else:  # Estatísticas Gerais
            st.header("📈 Estatísticas Gerais")
            
            # Calcular estatísticas por habilidade (apenas para turmas selecionadas)
            stats_data = []
            for habilidade in nome_habilidades.values():
                contagem = alunos_filtrados[habilidade].value_counts().reindex([0, 1, 2, 3], fill_value=0)
                stats_data.append({
                    'Habilidade': habilidade,
                    'Descrição': get_descricao_habilidade(habilidade),
                    'Não Domina (0)': contagem[0],
                    'Domina (1)': contagem[1],
                    'Domina Plenamente (2)': contagem[2],
                    'Completamente Dominado (3)': contagem[3],
                    '% Não Domina': (contagem[0] / len(alunos_filtrados) * 100).round(1),
                    '% Domina': (contagem[1] / len(alunos_filtrados) * 100).round(1),
                    '% Domina Plenamente': (contagem[2] / len(alunos_filtrados) * 100).round(1),
                    '% Completamente Dominado': (contagem[3] / len(alunos_filtrados) * 100).round(1)
                })
            
            stats_df = pd.DataFrame(stats_data)
            
            st.subheader("Estatísticas por Habilidade")
            st.write(f"**Turmas selecionadas:** {', '.join(map(str, turma_selecionada))}")
            st.dataframe(stats_df, use_container_width=True)
            
            # Heatmap de desempenho
            st.subheader("🎨 Heatmap de Desempenho")
            heatmap_data = stats_df.set_index('Habilidade')[['% Não Domina', '% Domina', '% Domina Plenamente', '% Completamente Dominado']]
            fig = px.imshow(
                heatmap_data.T,
                labels=dict(x="Habilidade", y="Nível", color="Percentual"),
                title=f"Distribuição Percentual por Habilidade e Nível - Turmas: {', '.join(map(str, turma_selecionada))}",
                aspect="auto"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Download dos dados filtrados
        st.sidebar.header("💾 Exportar Dados")
        
        if st.sidebar.button("📥 Gerar Relatório Completo"):
            relatorio_data = []
            for _, aluno in alunos_filtrados.iterrows():
                for habilidade in nome_habilidades.values():
                    relatorio_data.append({
                        'Aluno': aluno['Aluno'],
                        'Turma': aluno['Turma'],
                        'Habilidade': habilidade,
                        'Descrição': get_descricao_habilidade(habilidade),
                        'Nível': aluno[habilidade],
                        'Grupo': get_nivel_descricao(aluno[habilidade])
                    })
            
            relatorio_df = pd.DataFrame(relatorio_data)
            csv = relatorio_df.to_csv(index=False, encoding='utf-8-sig')
            
            st.sidebar.download_button(
                label="Baixar CSV Completo",
                data=csv,
                file_name="agrupamento_alunos_habilidades.csv",
                mime="text/csv"
            )
        
    except Exception as e:
        st.error(f"Erro ao processar os dados: {e}")
        st.write("Verifique se o formato do arquivo está correto.")

else:
    st.info("📂 Aguardando carregamento do arquivo 'dados.csv'...")
    st.write("""
    **Certifique-se de que:**
    1. O arquivo 'dados.csv' está na mesma pasta que este script
    2. O arquivo tem o formato correto com separador ';'
    3. As colunas seguem o padrão: Aluno;Turma;H 01;H 02;...;H 20
    """)