# CESB Analytics: Plataforma de Análise Pedagógica e Formação de Grupos

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-red?style=for-the-badge&logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-purple?style=for-the-badge&logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-5.15%2B-blue?style=for-the-badge&logo=plotly)
[![Plataforma](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com)
[![Licença](https://img.shields.io/badge/Licen%C3%A7a-MIT-green.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

Uma plataforma de análise de dados educacionais desenvolvida para apoiar o programa de **Recomposição da Aprendizagem** no Colégio Estadual São Braz (CESB). A ferramenta transforma dados brutos das avaliações do CAED em insights visuais e interativos, além de oferecer uma solução inteligente para a formação de grupos de estudo heterogêneos.

---
## ✨ Funcionalidades Principais

Este projeto é composto por três módulos principais, acessíveis através de um menu de navegação intuitivo:

### 📊 Dashboards de Desempenho (3º Ano do Ensino Médio e 9º Ano do Ensino Fundamental)

Análises detalhadas e interativas do desempenho dos alunos, permitindo uma visão macro e micro dos resultados.
- **Visão Geral da Turma:** Métricas agregadas de domínio por habilidade.
- **Análise por Habilidade:** Gráficos que mostram o percentual de alunos que dominam, dominam parcialmente ou não dominam cada competência avaliada.
- **Filtros Dinâmicos:** Filtre os dados por avaliação (CAED1, CAED2), disciplina (Matemática, Português) e turma.
- **Heatmaps Visuais:** Identifique rapidamente os pontos de maior atenção em diferentes turmas e habilidades.
- **Análise Individual:** Pesquise por um aluno específico para ver seu desempenho detalhado.

### 👥 Ferramenta de Formação de Grupos

Um assistente inteligente para professores criarem grupos de trabalho heterogêneos de forma estratégica e pedagógica.
- **Seleção de Foco:** Escolha a turma e as habilidades específicas que serão o foco do trabalho em grupo.
- **Algoritmo de Equilíbrio:** Utiliza um método de **distribuição estratificada** para garantir que cada grupo tenha um mix equilibrado de alunos com diferentes níveis de domínio ("Não Domina", "Domina" e "Domina Plenamente").
- **Visualização Clara:** Os grupos são apresentados em cards elegantes, listando os integrantes e exibindo um gráfico de desempenho médio do grupo nas habilidades selecionadas.
- **Insights Pedagógicos:** Cada card de grupo destaca os "Pontos Fortes" e "Pontos de Atenção", auxiliando o professor no direcionamento das atividades.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python
- **Interface e Visualização:** Streamlit, Plotly
- **Manipulação de Dados:** Pandas, NumPy

---

## 🚀 Instalação e Uso

Para executar este projeto localmente, siga os passos abaixo.

### Pré-requisitos
- Python 3.10 ou superior
- `pip` e `venv`

### Passos

1.  **Clone o repositório:**
    ```sh
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    cd seu-repositorio
    ```

2.  **Crie e ative um ambiente virtual:**
    ```sh
    # Para Windows
    python -m venv env
    .\env\Scripts\activate

    # Para macOS/Linux
    python3 -m venv env
    source env/bin/activate
    ```

3.  **Instale as dependências:**
    Crie um arquivo `requirements.txt` com o conteúdo abaixo e execute o comando `pip install`.
    
    **`requirements.txt`:**
    ```
    streamlit
    pandas
    numpy
    plotly
    ```

    **Comando de instalação:**
    ```sh
    pip install -r requirements.txt
    ```
    
4.  **Estrutura de arquivos:**
    Certifique-se de que os seus arquivos de dados `.csv` e os scripts Python estejam organizados na estrutura de múltiplas páginas do Streamlit:
    ```
    seu-repositorio/
    ├── 🏠_Pagina_Principal.py
    ├── pages/
    │   ├── 1_📊_3º_ano_análise.py
    │   ├── 2_📊_9º_ano_análise.py
    │   └── 3_👥_Gerador_de_Grupos.py
    ├── dados/  (Opcional, para organizar os CSVs)
    │   ├── CAED1_3_matematica.csv
    │   └── ...
    └── .streamlit/
        └── config.toml
    ```

5.  **Execute o aplicativo:**
    ```sh
    streamlit run 🏠_Pagina_Principal.py
    ```
    O aplicativo será aberto automaticamente no seu navegador.

---

## 🧠 Lógica do Formador de Grupos

A ferramenta de formação de grupos não é aleatória. Ela segue uma lógica de **distribuição estratificada** para maximizar o potencial de aprendizagem colaborativa:
1.  **Pontuação:** Calcula a pontuação média de cada aluno com base nas habilidades selecionadas pelo professor.
2.  **Categorização:** Classifica os alunos em três níveis: "Não Domina", "Domina" e "Domina Plenamente".
3.  **Distribuição Equilibrada:** Cria os grupos e os preenche de forma cíclica, distribuindo primeiro os alunos de maior domínio para garantir que eles fiquem em grupos diferentes, e depois preenchendo com os demais níveis. O resultado são equipes heterogêneas prontas para colaborar.

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 👨‍💻 Autor

Desenvolvido por **Mauricio A. Ribeiro**.
