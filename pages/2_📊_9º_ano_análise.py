import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from PIL import Image

# Configuração da página
st.set_page_config(page_title="📊 Recomposição de Aprendizagem", layout="wide")

# Título do aplicativo
st.title("Recomposição de Aprendizagem")

# Dicionários com descrições das habilidades por disciplina
DESCRICOES_HABILIDADES = {
    "Portugues": {
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
    },
    "Matematica": {
        "H01": "Corresponder figuras tridimensionais às suas planificações.",
        "H02": "Utilizar informações apresentadas em tabelas ou gráficos na resolução de problemas.",
        "H03": "Utilizar área de figuras bidimensionais na resolução de problema.",
        "H04": "Identificar frações equivalentes.",
        "H05": "Utilizar conversão entre unidades de medida, na resolução de problema.",
        "H06": "Utilizar o princípio multiplicativo de contagem na resolução de problema.",
        "H07": "Utilizar proporcionalidade entre duas grandezas na resolução de problema.",
        "H08": "Classificar quadriláteros por meio de suas propriedades.",
        "H09": "Classificar triângulos por meio de suas propriedades.",
        "H10": "Corresponder diferentes representações de um número racional.",
        "H11": "Utilizar o cálculo de volumes/capacidade de prismas retos e de cilindros na resolução de problema.",
        "H12": "Utilizar perímetro de figuras bidimensionais na resolução de problema.",
        "H13": "Utilizar porcentagem na resolução de problemas.",
        "H14": "Identificar a expressão algébrica that expressa uma regularidade observada em sequência de números ou figuras (padrões).",
        "H15": "Executar cálculos com números reais.",
        "H16": "Utilizar o cálculo do valor numérico de expressões algébricas na resolução de problemas.",
        "H17": "Utilizar relações métricas de um triângulo retângulo na resolução de problema.",
        "H18": "Utilizar equação polinomial de 2º grau na resolução de problema.",
        "H19": "Utilizar números racionais, envolvendo diferentes significados das operações, na resolução de problemas.",
        "H20": "Identificar uma equação ou inequação do 1º grau que expressa um problema."
    }
}

# Função para carregar dados
def carregar_dados(disciplina, prova):
    """Carrega o arquivo CSV correspondente à disciplina e prova selecionadas"""
    try:
        # Construir o nome do arquivo
        nome_arquivo = f"CAED{prova}_9_{disciplina.lower()}.csv"
        
        # Tenta encontrar o arquivo na mesma pasta
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
def get_nivel_descricao(valor, disciplina):
    if disciplina == "Portugues":
        if valor == 0:
            return "❌ Não Domina"
        elif valor == 1:
            return "⚠️ Domina"
        elif valor == 2:
            return "✅ Domina Plenamente"
        else:  # valor == 3
            return "🏆 Completamente Dominado"
    else:  # Matematica
        if valor == 0:
            return "❌ Não Domina"
        elif valor == 1:
            return "⚠️ Domina"
        else:
            return "✅ Domina Plenamente"

# Função para obter descrição da habilidade
def get_descricao_habilidade(codigo, disciplina):
    return DESCRICOES_HABILIDADES[disciplina].get(codigo, "Descrição não disponível")

# Função para obter pontuação máxima
def get_pontuacao_maxima(disciplina):
    return 3 if disciplina == "Portugues" else 2

# Sidebar com seleção de disciplina e prova
st.sidebar.header("🔧 Configurações")

prova = st.sidebar.selectbox(
    "Selecione a prova:",
    [1, 2]
)

disciplina = st.sidebar.selectbox(
    "Selecione a disciplina:",
    ["Portugues", "Matematica"]
)

# Carregar dados automaticamente
df = carregar_dados(disciplina, prova)

if df is not None:
    try:
        # Limpar nomes das colunas
        df.columns = df.columns.str.strip()
        
        # Determinar o número máximo de habilidades com base na disciplina
        max_habilidades = 15 if disciplina == "Portugues" else 20
        
        # Filtrar apenas as colunas de H01 a H(max_habilidades)
        habilidades_cols = [col for col in df.columns if col.startswith('H ') and int(col.split()[1]) <= max_habilidades]
        
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
            
            # Layout das colunas baseado na disciplina
            if disciplina == "Portugues":
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.subheader("❌ Não Domina")
                    nao_domina = []
                    for hab in nome_habilidades.values():
                        if aluno_data[hab] == 0:
                            nao_domina.append(hab)
                    if nao_domina:
                        for hab in sorted(nao_domina):
                            st.write(f"• **{hab}**: {get_descricao_habilidade(hab, disciplina)}")
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
                            st.write(f"• **{hab}**: {get_descricao_habilidade(hab, disciplina)}")
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
                            st.write(f"• **{hab}**: {get_descricao_habilidade(hab, disciplina)}")
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
                            st.write(f"• **{hab}**: {get_descricao_habilidade(hab, disciplina)}")
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
                    pontuacao_maxima = len(nome_habilidades) * get_pontuacao_maxima(disciplina)
                    st.metric("Pontuação Total", f"{pontuacao_total}/{pontuacao_maxima}", f"{pontuacao_total/pontuacao_maxima*100:.1f}%")
                
            else:  # Matematica
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.subheader("❌ Não Domina")
                    nao_domina = []
                    for hab in nome_habilidades.values():
                        if aluno_data[hab] == 0:
                            nao_domina.append(hab)
                    if nao_domina:
                        for hab in sorted(nao_domina):
                            st.write(f"• **{hab}**: {get_descricao_habilidade(hab, disciplina)}")
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
                            st.write(f"• **{hab}**: {get_descricao_habilidade(hab, disciplina)}")
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
                            st.write(f"• **{hab}**: {get_descricao_habilidade(hab, disciplina)}")
                    else:
                        st.write("Nenhuma habilidade neste nível")
                
                # Estatísticas do aluno
                st.subheader("📊 Estatísticas do Aluno")
                col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
                
                with col_stats1:
                    st.metric("Não Domina", f"{len(nao_domina)}", f"{len(nao_domina)/len(nome_habilidades)*100:.1f}%")
                with col_stats2:
                    st.metric("Domina", f"{len(domina)}", f"{len(domina)/len(nome_habilidades)*100:.1f}%")
                with col_stats3:
                    st.metric("Domina Plenamente", f"{len(domina_plenamente)}", f"{len(domina_plenamente)/len(nome_habilidades)*100:.1f}%")
                with col_stats4:
                    pontuacao_total = sum([aluno_data[hab] for hab in nome_habilidades.values()])
                    pontuacao_maxima = len(nome_habilidades) * get_pontuacao_maxima(disciplina)
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
                else:  # valor == 3 (apenas Português)
                    cores.append('#4D96FF')  # Azul para completamente dominado

            # Criar gráfico de radar
            fig = go.Figure()

            fig.add_trace(go.Scatterpolar(
                r=valores,
                theta=habilidades,
                fill='toself',
                fillcolor='rgba(77, 150, 255, 0.2)',
                line=dict(color='rgba(77, 150, 255, 0.8)', width=2),
                marker=dict(size=8, color=cores, line=dict(width=1, color='DarkSlateGrey')),
                name=aluno_selecionado
            ))

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, get_pontuacao_maxima(disciplina)],
                        tickvals=list(range(get_pontuacao_maxima(disciplina)+1)),
                        ticktext=[get_nivel_descricao(i, disciplina).split()[-1] for i in range(get_pontuacao_maxima(disciplina)+1)]
                    )
                ),
                showlegend=False,
                title=f"Perfil de Habilidades de {aluno_selecionado}",
                height=500
            )

            st.plotly_chart(fig, use_container_width=True)
            
        elif tipo_analise == "Ver Grupos por Habilidade":
            st.header("👥 Grupos por Habilidade")
            
            # Selecionar habilidade
            habilidade_selecionada = st.selectbox(
                "Selecione a habilidade:",
                sorted(nome_habilidades.values())
            )
            
            # Descrição da habilidade
            st.info(f"**Descrição:** {get_descricao_habilidade(habilidade_selecionada, disciplina)}")
            
            # Agrupar alunos por nível de domínio
            grupos = {
                "❌ Não Domina": alunos_filtrados[alunos_filtrados[habilidade_selecionada] == 0],
                "⚠️ Domina": alunos_filtrados[alunos_filtrados[habilidade_selecionada] == 1],
                "✅ Domina Plenamente": alunos_filtrados[alunos_filtrados[habilidade_selecionada] == 2]
            }
            
            if disciplina == "Portugues":
                grupos["🏆 Completamente Dominado"] = alunos_filtrados[alunos_filtrados[habilidade_selecionada] == 3]
            
            # Layout com abas para cada grupo
            tabs = st.tabs(list(grupos.keys()))
            
            for i, (nivel, grupo) in enumerate(grupos.items()):
                with tabs[i]:
                    st.subheader(f"{nivel} ({len(grupo)} alunos)")
                    
                    if len(grupo) > 0:
                        # Mostrar alunos em colunas
                        col_count = 3
                        cols = st.columns(col_count)
                        
                        for idx, (_, aluno) in enumerate(grupo.iterrows()):
                            with cols[idx % col_count]:
                                st.write(f"**{aluno['Aluno']}** (Turma {aluno['Turma']})")
                    else:
                        st.info("Nenhum aluno neste grupo")
            
            # Gráfico de distribuição
            st.subheader("📊 Distribuição por Nível de Domínio")
            
            # Contar alunos por nível
            contagem_niveis = {nivel: len(grupo) for nivel, grupo in grupos.items()}
            
            # Criar gráfico de pizza
            fig = px.pie(
                values=list(contagem_niveis.values()),
                names=list(contagem_niveis.keys()),
                title=f"Distribuição de alunos por nível de domínio - {habilidade_selecionada}",
                color=list(contagem_niveis.keys()),
                color_discrete_map={
                    "❌ Não Domina": "#FF6B6B",
                    "⚠️ Domina": "#FFD93D",
                    "✅ Domina Plenamente": "#6BCB77",
                    "🏆 Completamente Dominado": "#4D96FF"
                }
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        elif tipo_analise == "Visão Geral dos Grupos":
            st.header("📋 Visão Geral dos Grupos")
            
            # Definir níveis baseado na disciplina
            niveis = ["❌ Não Domina", "⚠️ Domina", "✅ Domina Plenamente"]
            if disciplina == "Portugues":
                niveis.append("🏆 Completamente Dominado")
            
            # Selecionar nível
            nivel_selecionado = st.selectbox("Selecione o nível:", niveis)
            
            # Mapear nível para valor numérico
            nivel_para_valor = {
                "❌ Não Domina": 0,
                "⚠️ Domina": 1,
                "✅ Domina Plenamente": 2,
                "🏆 Completamente Dominado": 3
            }
            
            valor_nivel = nivel_para_valor[nivel_selecionado]
            
            # Encontrar alunos que estão no nível selecionado para pelo menos uma habilidade
            alunos_no_nivel = []
            
            for _, aluno in alunos_filtrados.iterrows():
                habilidades_no_nivel = []
                for hab in nome_habilidades.values():
                    if aluno[hab] == valor_nivel:
                        habilidades_no_nivel.append(hab)
                
                if habilidades_no_nivel:
                    alunos_no_nivel.append({
                        "Aluno": aluno["Aluno"],
                        "Turma": aluno["Turma"],
                        "Habilidades": ", ".join(sorted(habilidades_no_nivel)),
                        "Quantidade": len(habilidades_no_nivel)
                    })
            
            # Converter para DataFrame
            df_nivel = pd.DataFrame(alunos_no_nivel)
            
            if len(df_nivel) > 0:
                # Ordenar por quantidade (decrescente)
                df_nivel = df_nivel.sort_values("Quantidade", ascending=False)
                
                # Mostrar tabela
                st.subheader(f"Alunos que {nivel_selecionado.split()[-1]} pelo menos uma habilidade")
                st.dataframe(
                    df_nivel,
                    column_config={
                        "Aluno": "Aluno",
                        "Turma": "Turma",
                        "Habilidades": "Habilidades",
                        "Quantidade": st.column_config.NumberColumn(
                            "Quantidade",
                            help="Número de habilidades neste nível",
                            format="%d"
                        )
                    },
                    hide_index=True,
                    use_container_width=True
                )
                
                # Estatísticas
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total de Alunos", len(df_nivel))
                with col2:
                    st.metric("Média de Habilidades", f"{df_nivel['Quantidade'].mean():.1f}")
                with col3:
                    st.metric("Habilidade mais comum", df_nivel['Habilidades'].str.split(', ').explode().mode().iloc[0] if not df_nivel.empty else "N/A")
                
                # Gráfico de distribuição
                st.subheader("Distribuição por Quantidade de Habilidades")
                
                # Contar alunos por quantidade de habilidades no nível
                contagem_quantidade = df_nivel['Quantidade'].value_counts().sort_index()
                
                fig = px.bar(
                    x=contagem_quantidade.index,
                    y=contagem_quantidade.values,
                    labels={'x': 'Quantidade de Habilidades', 'y': 'Número de Alunos'},
                    title=f"Distribuição de alunos por quantidade de habilidades que {nivel_selecionado.split()[-1]}"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
            else:
                st.info(f"Nenhum aluno {nivel_selecionado.split()[-1]} nenhuma habilidade")
                
        elif tipo_analise == "Estatísticas Gerais":
            st.header("📈 Estatísticas Gerais")
            
            # Estatísticas por turma
            st.subheader("Estatísticas por Turma")
            
            # Calcular estatísticas para cada turma
            estatisticas_turmas = []
            
            for turma in turmas_disponiveis:
                if turma in turma_selecionada:
                    alunos_turma = alunos_filtrados[alunos_filtrados['Turma'] == turma]
                    
                    # Calcular pontuação média por habilidade
                    pontuacao_media = alunos_turma[nome_habilidades.values()].mean().mean()
                    
                    # Calcular percentual de domínio (pontuação > 0)
                    dominio_geral = (alunos_turma[nome_habilidades.values()] > 0).mean().mean() * 100
                    
                    # Calcular percentual de domínio pleno (pontuação máxima)
                    if disciplina == "Portugues":
                        dominio_pleno = (alunos_turma[nome_habilidades.values()] == 3).mean().mean() * 100
                    else:
                        dominio_pleno = (alunos_turma[nome_habilidades.values()] == 2).mean().mean() * 100
                    
                    estatisticas_turmas.append({
                        "Turma": turma,
                        "Alunos": len(alunos_turma),
                        "Pontuação Média": pontuacao_media,
                        "Domínio Geral (%)": dominio_geral,
                        "Domínio Pleno (%)": dominio_pleno
                    })
            
            # Exibir estatísticas das turmas
            if estatisticas_turmas:
                df_estatisticas = pd.DataFrame(estatisticas_turmas)
                st.dataframe(
                    df_estatisticas,
                    column_config={
                        "Turma": "Turma",
                        "Alunos": "Nº de Alunos",
                        "Pontuação Média": st.column_config.NumberColumn(
                            "Pontuação Média",
                            format="%.2f"
                        ),
                        "Domínio Geral (%)": st.column_config.NumberColumn(
                            "Domínio Geral (%)",
                            format="%.1f%%"
                        ),
                        "Domínio Pleno (%)": st.column_config.NumberColumn(
                            "Domínio Pleno (%)",
                            format="%.1f%%"
                        )
                    },
                    hide_index=True,
                    use_container_width=True
                )
            
            # Habilidades com maior e menor domínio
            st.subheader("Habilidades com Maior e Menor Domínio")
            
            # Calcular percentual de domínio por habilidade
            dominio_por_habilidade = []
            
            for hab in nome_habilidades.values():
                dominio = (alunos_filtrados[hab] > 0).mean() * 100
                dominio_por_habilidade.append({
                    "Habilidade": hab,
                    "Domínio (%)": dominio,
                    "Descrição": get_descricao_habilidade(hab, disciplina)
                })
            
            df_dominio = pd.DataFrame(dominio_por_habilidade).sort_values("Domínio (%)", ascending=False)
            
            # Mostrar as 5 melhores e 5 piores habilidades
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Top 5 - Maior Domínio**")
                st.dataframe(
                    df_dominio.head(5),
                    column_config={
                        "Habilidade": "Habilidade",
                        "Domínio (%)": st.column_config.NumberColumn(
                            "Domínio (%)",
                            format="%.1f%%"
                        ),
                        "Descrição": "Descrição"
                    },
                    hide_index=True,
                    use_container_width=True
                )
            
            with col2:
                st.write("**Top 5 - Menor Domínio**")
                st.dataframe(
                    df_dominio.tail(5).sort_values("Domínio (%)", ascending=True),
                    column_config={
                        "Habilidade": "Habilidade",
                        "Domínio (%)": st.column_config.NumberColumn(
                            "Domínio (%)",
                            format="%.1f%%"
                        ),
                        "Descrição": "Descrição"
                    },
                    hide_index=True,
                    use_container_width=True
                )
            
            # Gráfico de calor das habilidades
            st.subheader("Mapa de Calor das Habilidades")
            
            # Calcular percentual de domínio por turma e habilidade
            heatmap_data = []
            
            for turma in turma_selecionada:
                alunos_turma = alunos_filtrados[alunos_filtrados['Turma'] == turma]
                
                for hab in nome_habilidades.values():
                    dominio = (alunos_turma[hab] > 0).mean() * 100
                    heatmap_data.append({
                        "Turma": turma,
                        "Habilidade": hab,
                        "Domínio (%)": dominio
                    })
            
            df_heatmap = pd.DataFrame(heatmap_data)
            
            # Criar heatmap
            fig = px.imshow(
                df_heatmap.pivot(index="Habilidade", columns="Turma", values="Domínio (%)"),
                labels=dict(x="Turma", y="Habilidade", color="Domínio (%)"),
                color_continuous_scale="RdYlGn",
                range_color=[0, 100],
                title="Percentual de Domínio por Habilidade e Turma"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        # Adicionar informações sobre a disciplina e prova
        st.sidebar.header("ℹ️ Informações")
        st.sidebar.write(f"**Disciplina:** {disciplina}")
        st.sidebar.write(f"**Prova:** CAED {prova}")
        st.sidebar.write(f"**Habilidades analisadas:** {len(nome_habilidades)}")
        
    except Exception as e:
        st.error(f"Erro ao processar os dados: {e}")
        st.info("Verifique se o formato do arquivo CSV está correto.")
else:
    st.info("💡 Para começar, faça o upload de um arquivo CSV ou verifique se o arquivo está na pasta correta.")


st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; font-size: 14px;">
    <p>Colégio Estadual São Braz - Recomposição da Aprendizagem</p>
    <p>© 2025 - Todos os direitos reservados</p>
    <p>© Desenvolvido por Mauricio A. Ribeiro</p>
</div>""", unsafe_allow_html=True)