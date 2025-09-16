import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Configuração da página
st.set_page_config(page_title="📊 Recomposição de Aprendizagem", layout="wide")

# Título do aplicativo
st.title("Recomposição de Aprendizagem")

# Dicionários com descrições das habilidades por avaliação e disciplina
DESCRICOES_HABILIDADES = {
    "CAED1_Matemática": {
        "H01": "Utilizar informações apresentadas em tabelas ou gráficos na resolução de problemas.",
        "H02": "Utilizar o princípio multiplicativo de contagem na resolução de problema.",
        "H03": "Utilizar probabilidade na resolução de problema.",
        "H04": "Utilizar proporcionalidade entre duas grandezas na resolução de problema.",
        "H05": "Corresponder pontos do plano a pares ordenados em um sistema de coordenadas cartesianas.",
        "H06": "Utilizar o cálculo de volumes/capacidade de prismas retos e de cilindros na resolução de problema.",
        "H07": "Utilizar perímetro de figuras bidimensionais na resolução de problema.",
        "H08": "Utilizar relações métricas de um triângulo retângulo na resolução de problema.",
        "H09": "Analisar regiões de crescimento/decrescimento, domínios de validade ou zeros de funções reais representadas graficamente.",
        "H10": "Utilizar função polinomial de 1º grau na resolução de problemas.",
        "H11": "Reconhecer a representação algébrica de uma função polinomial de 2º grau a partir dos dados apresentados em uma tabela.",
        "H12": "Utilizar a medida da área total e/ou lateral de um sólido na resolução de problema.",
        "H13": "Utilizar função exponencial na resolução de problemas.",
        "H14": "Utilizar função polinomial de 2º grau na resolução de problemas.",
        "H15": "Utilizar propriedades de progressões aritméticas ou geométricas na resolução de problemas.",
        "H16": "Utilizar equação polinomial de 2º grau na resolução de problema.",
        "H17": "Reconhecer a representação gráfica das funções trigonométricas (seno, cosseno e tangente).",
        "H18": "Resolver problemas que envolvam razões trigonométricas no triângulo retângulo.",
    },
    "CAED2_Matemática": {
        "H01": "Corresponder figuras tridimensionais às suas planificações.",
        "H02": "Utilizar informações apresentadas em tabelas ou gráficos na resolução de problemas",
        "H03": "Utilizar o principío multiplicativo de contagem na resolução de problema.",
        "H04": "Utilizar probabilidade na resolução de problema.",
        "H05": "Utilizar proporcionalidade entre duas grandezas na resolução de problema.",
        "H06": "Corresponder pontos do plano a pares ordenados em um sistema de coordenadas cartesianas.",
        "H07": "Utilizar o cálculo de volumes/capacidade de prismas retos e de cilindros na resolução de problema.",
        "H08": "Utilizar perímetro de figuras bidimensionais na resolução de problema.",
        "H09": "Utilizar porcentagem na resolução de problemas.",
        "H10": "Utilizar relações métricas de um triângulo retângulo na resolução de problema.",
        "H11": "Analisar regiões de crescimento/decrescimento, domínios de validade ou zeros de funções reais representadas graficamente.",
        "H12": "Corresponder a representação algébrica e gráfica de uma função polinomial de 1º grau.",
        "H13": "Utilizar função polinomial de 1º grau na resolução de problemas.",
        "H14": "Utilizar a medida da área total e/ou lateral de um sólido na resolução de problema.",
        "H15": "Utilizar função exponencial na resolução de problemas.",
        "H16": "Utilizar função polinomial de 2º grau na resolução de problemas.",
        "H17": "Utilizar propriedades de progressões aritméticas ou geométricas na resolução de problemas.",
        "H18": "Identificar a representação algébrica ou gráfica de uma função exponencial.",
        "H19": "Utilizar equação polinomial de 2º grau na resolução de problema.",
        "H20": "Relacionar as raízes de um polinômio com sua decomposição em fatores do 1º grau.",
        "H21": "Reconhecer a representação gráfica das funções trigonométricas (seno, cosseno e tangente).",
        "H22": "Resolver problemas que envolvam razões trigonométricas no triângulo retângulo."
    },
    "CAED1_Português": {
        "H01": "Reconhecer formas de tratar uma informação na comparação de textos que tratam do mesmo tema.",
        "H02": "Localizar informação explícita.",
        "H03": "Inferir informações em textos.",
        "H04": "Reconhecer efeito de humor ou de ironia em um texto.",
        "H05": "Distinguir ideias centrais de secundárias ou tópicos and subtópicos em um dado gênero textual.",
        "H06": "Identificar a tese de um texto.",
        "H07": "Reconhecer posições distintas relativas ao mesmo fato ou mesmo tema.",
        "H08": "Reconhecer as relações entre partes de um texto, identificando os recursos coesivos que contribuem para a sua continuidade.",
        "H09": "Distinguir um fato da opinião.",
        "H10": "Reconhecer o sentido das relações lógico-discursivas em um texto.",
        "H11": "Reconhecer o efeito de sentido decorrente da escolha de uma determinada palavra ou expressão.",
        "H12": "Estabelecer relação entre a tese e os argumentos oferecidos para sustentá-la.",
        "H13": "Estabelecer relação causa/consequência entre partes e elementos do texto.",
        "H14": "Reconhecer o efeito de sentido decorrente da exploração de recursos ortográficos e/ou morfossintáticos.",
        "H15": "Identificar as marcas linguísticas que evidenciam o locutor e o interlocutor de um texto.",
    },
    "CAED2_Português": {
        "H01": "Reconhecer formas de tratar uma informação na comparação de textos que tratam do mesmo tema.",
        "H02": "Localizar informação explícita.",
        "H03": "Inferir informações em textos.",
        "H04": "Reconhecer efeito de humor ou de ironia em um texto.",
        "H05": "Distinguir ideias centrais de secundárias ou tópicos and subtópicos em um dado gênero textual.",
        "H06": "Identificar a tese de um texto.",
        "H07": "Reconhecer posições distintas relativas ao mesmo fato ou mesmo tema.",
        "H08": "Reconhecer as relações entre partes de um texto, identificando os recursos coesivos que contribuem para a sua continuidade.",
        "H09": "Distinguir um fato da opinião.",
        "H10": "Reconhecer o sentido das relações lógico-discursivas em um texto.",
        "H11": "Reconhecer o efeito de sentido decorrente da escolha de uma determinada palavra ou expressão.",
        "H12": "Estabelecer relação entre a tese e os argumentos oferecidos para sustentá-la.",
        "H13": "Estabelecer relação causa/consequência entre partes e elementos do texto.",
        "H14": "Reconhecer o efeito de sentido decorrente da exploração de recursos ortográficos e/ou morfossintáticos.",
        "H15": "Identificar as marcas linguísticas que evidenciam o locutor e o interlocutor de um texto.",
    }
}

# Mapeamento de arquivos CSV
ARQUIVOS_CSV = {
    "CAED1_Matemática": "CAED1_3_matematica.csv",
    "CAED2_Matemática": "CAED2_3_matematica.csv",
    "CAED1_Português": "CAED1_3_portugues.csv",
    "CAED2_Português": "CAED2_3_portugues.csv"
}

# Função para carregar dados
def carregar_dados(avaliacao_disciplina):
    """Carrega o arquivo CSV correspondente à avaliação e disciplina selecionadas"""
    try:
        nome_arquivo = ARQUIVOS_CSV.get(avaliacao_disciplina)
        if not nome_arquivo:
            st.error("Avaliação e disciplina não reconhecidas.")
            return None
        
        # Tenta encontrar o arquivo na mesma pasta do script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, nome_arquivo)
        
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
            return df
        else:
            st.error(f"Arquivo '{nome_arquivo}' não encontrado na pasta do script.")
            st.info(f"Certifique-se de que o arquivo '{nome_arquivo}' está na mesma pasta que este script.")
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
    else:
        return "✅ Domina Plenamente"

# Função para obter descrição da habilidade
def get_descricao_habilidade(codigo, avaliacao_disciplina):
    return DESCRICOES_HABILIDADES.get(avaliacao_disciplina, {}).get(codigo, "Descrição não disponível")

# Função segura para calcular porcentagem (evita divisão por zero)
def calcular_porcentagem(parte, total):
    if total == 0:
        return 0.0
    return (parte / total) * 100

# Sidebar para seleção de avaliação e disciplina
st.sidebar.header("🎯 Seleção de Dados")
avaliacao = st.sidebar.selectbox(
    "Selecione a avaliação:",
    [1, 2]
)

disciplina = st.sidebar.selectbox(
    "Selecione a disciplina:",
    ["Matemática", "Português"]
)

# Converter o número da avaliação para o formato CAED
avaliacao_str = f"CAED{avaliacao}"
avaliacao_disciplina = f"{avaliacao_str}_{disciplina}"

# Carregar dados automaticamente
df = carregar_dados(avaliacao_disciplina)

if df is not None:
    try:
        # Limpar nomes das colunas
        df.columns = df.columns.str.strip()
        
        # Determinar o número máximo de habilidades com base na seleção
        if avaliacao_disciplina == "CAED1_Matemática":
            max_hab = 18
        elif avaliacao_disciplina == "CAED2_Matemática":
            max_hab = 22
        else:  # Português (CAED1 ou CAED2)
            max_hab = 15
        
        # Filtrar apenas as colunas de habilidades
        if avaliacao_disciplina in ["CAED1_Matemática", "CAED2_Matemática"]:
            habilidades_cols = [col for col in df.columns if col.startswith('H ') and int(col.split()[1]) <= max_hab]
            # Renomear colunas para formato mais amigável
            nome_habilidades = {col: f'H{int(col.split()[1]):02d}' for col in habilidades_cols}
        else:  # Português
            habilidades_cols = [col for col in df.columns if col.startswith('H') and col[1:].isdigit() and int(col[1:]) <= max_hab]
            # Renomear colunas para formato mais amigável
            nome_habilidades = {col: f'H{int(col[1:]):02d}' for col in habilidades_cols}
        
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
            
            # Verificar se há alunos filtrados
            if len(alunos_filtrados) == 0:
                st.warning("Nenhum aluno encontrado com os filtros aplicados.")
            else:
                # Selecionar aluno apenas da turma filtrada
                alunos_disponiveis = sorted(alunos_filtrados['Aluno'].tolist())
                aluno_selecionado = st.selectbox(
                    "Selecione um aluno:",
                    alunos_disponiveis
                )
                
                # Dados do aluno selecionado
                aluno_data = alunos_filtrados[alunos_filtrados['Aluno'] == aluno_selecionado].iloc[0]
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.subheader("❌ Não Domina")
                    nao_domina = []
                    for hab in nome_habilidades.values():
                        if aluno_data[hab] == 0:
                            nao_domina.append(hab)
                    if nao_domina:
                        for hab in sorted(nao_domina):
                            st.write(f"• **{hab}**: {get_descricao_habilidade(hab, avaliacao_disciplina)}")
                    else:
                        st.success("🎉 Domina todas as habilidades!")
                
                with col2:
                    st.subheader("⚠️ Domina")
                    domina = []
                    for hab in nome_habilidades.values():
                        if aluno_data[hab] == 1:
                            domina.append(hab)
                    if domina:
                        for hab in sorted(domina):
                            st.write(f"• **{hab}**: {get_descricao_habilidade(hab, avaliacao_disciplina)}")
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
                            st.write(f"• **{hab}**: {get_descricao_habilidade(hab, avaliacao_disciplina)}")
                    else:
                        st.write("Nenhuma habilidade neste nível")
                
                # Estatísticas do aluno
                st.subheader("📊 Estatísticas do Aluno")
                col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
                
                with col_stats1:
                    st.metric("Não Domina", f"{len(nao_domina)}", f"{calcular_porcentagem(len(nao_domina), len(nome_habilidades)):.1f}%")
                with col_stats2:
                    st.metric("Domina", f"{len(domina)}", f"{calcular_porcentagem(len(domina), len(nome_habilidades)):.1f}%")
                with col_stats3:
                    st.metric("Domina Plenamente", f"{len(domina_plenamente)}", f"{calcular_porcentagem(len(domina_plenamente), len(nome_habilidades)):.1f}%")
                with col_stats4:
                    st.metric("Total Habilidades", len(nome_habilidades))
        
        elif tipo_analise == "Ver Grupos por Habilidade":
            st.header("👥 Grupos por Habilidade")
            
            # Verificar se há alunos filtrados
            if len(alunos_filtrados) == 0:
                st.warning("Nenhum aluno encontrado com os filtros aplicados.")
            else:
                # Selecionar habilidade para análise
                habilidade_selecionada = st.selectbox(
                    "Selecione uma habilidade:",
                    sorted(nome_habilidades.values())
                )
                
                # Descrição da habilidade
                st.info(f"**Descrição:** {get_descricao_habilidade(habilidade_selecionada, avaliacao_disciplina)}")
                
                # Filtrar alunos por nível de domínio na habilidade selecionada
                nao_domina = alunos_filtrados[alunos_filtrados[habilidade_selecionada] == 0]
                domina = alunos_filtrados[alunos_filtrados[habilidade_selecionada] == 1]
                domina_plenamente = alunos_filtrados[alunos_filtrados[habilidade_selecionada] == 2]
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.subheader(f"❌ Não Domina ({len(nao_domina)})")
                    if not nao_domina.empty:
                        for _, aluno in nao_domina.iterrows():
                            st.write(f"• {aluno['Aluno']} - Turma {aluno['Turma']}")
                    else:
                        st.success("🎉 Todos dominam esta habilidade!")
                
                with col2:
                    st.subheader(f"⚠️ Domina ({len(domina)})")
                    if not domina.empty:
                        for _, aluno in domina.iterrows():
                            st.write(f"• {aluno['Aluno']} - Turma {aluno['Turma']}")
                    else:
                        st.write("Nenhum aluno neste nível")
                
                with col3:
                    st.subheader(f"✅ Domina Plenamente ({len(domina_plenamente)})")
                    if not domina_plenamente.empty:
                        for _, aluno in domina_plenamente.iterrows():
                            st.write(f"• {aluno['Aluno']} - Turma {aluno['Turma']}")
                    else:
                        st.write("Nenhum aluno neste nível")
                
                # Gráfico de distribuição
                st.subheader("📊 Distribuição por Nível de Domínio")
                fig = px.pie(
                    names=["Não Domina", "Domina", "Domina Plenamente"],
                    values=[len(nao_domina), len(domina), len(domina_plenamente)],
                    color=["Não Domina", "Domina", "Domina Plenamente"],
                    color_discrete_map={
                        "Não Domina": "red",
                        "Domina": "orange",
                        "Domina Plenamente": "green"
                    }
                )
                st.plotly_chart(fig, use_container_width=True)
        
        elif tipo_analise == "Visão Geral dos Grupos":
            st.header("📋 Visão Geral dos Grupos")
            
            # Verificar se há alunos filtrados
            if len(alunos_filtrados) == 0:
                st.warning("Nenhum aluno encontrado com os filtros aplicados.")
            else:
                # Tabela com contagem de alunos por nível para cada habilidade
                st.subheader("📈 Estatísticas por Habilidade")
                
                # Calcular estatísticas para cada habilidade
                stats_data = []
                for hab in sorted(nome_habilidades.values()):
                    total = len(alunos_filtrados)
                    nao_domina_count = len(alunos_filtrados[alunos_filtrados[hab] == 0])
                    domina_count = len(alunos_filtrados[alunos_filtrados[hab] == 1])
                    domina_plenamente_count = len(alunos_filtrados[alunos_filtrados[hab] == 2])
                    
                    stats_data.append({
                        "Habilidade": hab,
                        "Descrição": get_descricao_habilidade(hab, avaliacao_disciplina),
                        "Não Domina": nao_domina_count,
                        "Domina": domina_count,
                        "Domina Plenamente": domina_plenamente_count,
                        "% Não Domina": f"{calcular_porcentagem(nao_domina_count, total):.1f}%",
                        "% Domina": f"{calcular_porcentagem(domina_count, total):.1f}%",
                        "% Domina Plenamente": f"{calcular_porcentagem(domina_plenamente_count, total):.1f}%"
                    })
                
                stats_df = pd.DataFrame(stats_data)
                
                # Mostrar tabela com estatísticas
                st.dataframe(
                    stats_df,
                    column_config={
                        "Habilidade": st.column_config.TextColumn("Habilidade", width="small"),
                        "Descrição": st.column_config.TextColumn("Descrição", width="large"),
                        "Não Domina": st.column_config.NumberColumn("Não Domina", format="%d"),
                        "Domina": st.column_config.NumberColumn("Domina", format="%d"),
                        "Domina Plenamente": st.column_config.NumberColumn("Domina Plenamente", format="%d"),
                        "% Não Domina": st.column_config.TextColumn("% Não Domina"),
                        "% Domina": st.column_config.TextColumn("% Domina"),
                        "% Domina Plenamente": st.column_config.TextColumn("% Domina Plenamente")
                    },
                    hide_index=True,
                    use_container_width=True
                )
                
                # Gráfico de barras com as habilidades mais problemáticas
                st.subheader("📊 Habilidades com Maior Dificuldade")
                
                # Ordenar por % de "Não Domina"
                stats_df_sorted = stats_df.sort_values("Não Domina", ascending=False)
                
                fig = px.bar(
                    stats_df_sorted.head(10),
                    x="Habilidade",
                    y="Não Domina",
                    color="Não Domina",
                    color_continuous_scale="reds",
                    title="Top 10 Habilidades com Maior Número de Alunos que Não Dominam"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        elif tipo_analise == "Estatísticas Gerais":
            st.header("📊 Estatísticas Gerais")
            
            # Verificar se há alunos filtrados
            if len(alunos_filtrados) == 0:
                st.warning("Nenhum aluno encontrado com os filtros aplicados.")
            else:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # Calcular total de alunos
                    total_alunos = len(alunos_filtrados)
                    st.metric("Total de Alunos", total_alunos)
                
                with col2:
                    # Calcular média de habilidades dominadas plenamente por aluno
                    habilidades_dominadas = alunos_filtrados[list(nome_habilidades.values())].apply(
                        lambda row: sum(row == 2), axis=1
                    )
                    media_dominadas = habilidades_dominadas.mean()
                    st.metric("Média de Habilidades Dominadas Plenamente", f"{media_dominadas:.1f}")
                
                with col3:
                    # Calcular média de habilidades não dominadas por aluno
                    habilidades_nao_dominadas = alunos_filtrados[list(nome_habilidades.values())].apply(
                        lambda row: sum(row == 0), axis=1
                    )
                    media_nao_dominadas = habilidades_nao_dominadas.mean()
                    st.metric("Média de Habilidades Não Dominadas", f"{media_nao_dominadas:.1f}")
                
                # Distribuição geral de domínio
                st.subheader("📈 Distribuição Geral de Domínio")
                
                total_habilidades = len(nome_habilidades) * total_alunos
                total_nao_domina = (alunos_filtrados[list(nome_habilidades.values())] == 0).sum().sum()
                total_domina = (alunos_filtrados[list(nome_habilidades.values())] == 1).sum().sum()
                total_domina_plenamente = (alunos_filtrados[list(nome_habilidades.values())] == 2).sum().sum()
                
                fig = px.pie(
                    names=["Não Domina", "Domina", "Domina Plenamente"],
                    values=[total_nao_domina, total_domina, total_domina_plenamente],
                    color=["Não Domina", "Domina", "Domina Plenamente"],
                    color_discrete_map={
                        "Não Domina": "red",
                        "Domina": "orange",
                        "Domina Plenamente": "green"
                    },
                    title="Distribuição Geral dos Níveis de Domínio"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Mapa de calor das habilidades
                st.subheader("🌡️ Mapa de Calor das Habilidades")
                
                # Calcular a porcentagem de alunos que não dominam cada habilidade
                heatmap_data = []
                for hab in sorted(nome_habilidades.values()):
                    nao_domina_count = len(alunos_filtrados[alunos_filtrados[hab] == 0])
                    porcentagem_nao_domina = calcular_porcentagem(nao_domina_count, total_alunos)
                    heatmap_data.append(porcentagem_nao_domina)
                
                # Criar o heatmap
                fig = go.Figure(data=go.Heatmap(
                    z=[heatmap_data],
                    x=sorted(nome_habilidades.values()),
                    y=["% Não Domina"],
                    colorscale='reds',
                    hoverongaps=False,
                    colorbar=dict(title="% Não Domina")
                ))
                
                fig.update_layout(
                    title="Porcentagem de Alunos que Não Dominam cada Habilidade",
                    xaxis_title="Habilidades",
                    yaxis_title=""
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        # Informações sobre a avaliação e disciplina
        st.sidebar.header("ℹ️ Informações")
        st.sidebar.write(f"Avaliação: {avaliacao_str}")
        st.sidebar.write(f"Disciplina: {disciplina}")
        st.sidebar.write(f"Habilidades: {len(nome_habilidades)}")
        
    except Exception as e:
        st.error(f"Erro ao processar os dados: {e}")
        st.info("Verifique se a estrutura do arquivo CSV está correta.")
else:
    st.info("Por favor, faça o upload dos arquivos CSV necessários ou coloque-os na mesma pasta do script.")


# Rodapé
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; font-size: 14px;">
    <p>Colégio Estadual São Braz - Recomposição da Aprendizagem</p>
    <p>© 2025 - Todos os direitos reservados</p>
    <p>© Desenvolvido por Mauricio A. Ribeiro</p>
</div>
""", unsafe_allow_html=True)
