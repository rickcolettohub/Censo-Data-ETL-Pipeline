# 🏷️ Censo Escolar Brasil (1995–2024): Pipeline de Limpeza e Estruturação de Dados

## 📘 Descrição Geral

Este projeto tem como objetivo **padronizar, limpar e estruturar** os microdados do **Censo Escolar Brasileiro** no período de **2007 a 2024**, disponibilizados pelo **INEP**.  

A partir de 2007, o Censo Escolar passou por uma **reformulação completa de metodologia**, incluindo alterações no formato dos microdados, nos códigos de variáveis e na estrutura de entidades.  
Por esse motivo, os dados de 2007 em diante são tratados como uma série homogênea, **adequada para integração, análise temporal e modelagem relacional**.  

Os dados anteriores a 2007 utilizavam outro padrão técnico e estão planejados para um **projeto separado** que tratará da integração histórica do Censo Escolar (1995–2006).


## 🧰 Stack Utilizada
- **Python 3.11+**
  - pandas  
  - sqlalchemy  
  - zipfile / pathlib / os  
  - tqdm  
- **SQLite** (banco leve, sem necessidade de instalação)
- **SQLiteStudio** (visualização e checagem de schema)
- **Jupyter Notebook / VS Code**



## 🧩 Estrutura do Repositório
   ```bash
📂 Censo-Data-ETL-Pipeline/ 
    ├── 📂 data/ 
    │    ├── 📂 raw/               # CSVs originais extraídos dos .zip 
    │    ├── 📂 processed/         # CSVs limpos e tratados 
    │    └── 🛢 censo_escolar.db    # Banco SQLite final - Gitignored
    │
    ├── 📓 notebooks/
    │    └── 01_Data_Cleaning.ipynb # notebooks de exploração e limpeza
    │
    ├── 📂 src/ 
    │    ├── create_sqldb.py        # Cria um .db limpo para receber os dados
    │    └── load_data.py           # Download dos dados brutos
    │
    ├── 📄 requirements.txt
    └── 📘 README.md 
   ```
    ‼️IMPORTANTE: O arquivo censo_escolar.db final estará disponivel para download em um link externo para analise e utilização em outros projetos.

## ⚙️ Etapas do Pipeline

### 1️⃣ Download & Extração
O script `load_data.py` percorre uma lista de links oficiais do INEP, faz o download dos arquivos `.zip` e extrai automaticamente.

Os **arquivos CSV principais** são armazenados em `data/raw/`, enquanto documentos auxiliares (PDFs, dicionários, planilhas) vão para `.dev/` (ignorada no Git).

### 2️⃣ Limpeza e Padronização
- Leitura com encoding adequado (`latin-1`);
- Padronização dos nomes das colunas;
- Conversões automáticas:
  - `float → int64`
  - Datas em formato `%d%b%Y:%H:%M:%S` → `datetime64`
- Consolidação dos CSVs de 2007–2024 via concatenação incremental.

### 3️⃣ Armazenamento e Modelagem
- Cada tabela é armazenada no SQLite como `fato_censo_<ano>`;
- A tabela `entidades` contém as escolas (CO_ENTIDADE) e seus metadados;
- `CO_ENTIDADE` foi definida como **Primary Key** via SQLiteStudio.

## 🧮 Exemplo de Query no SQLite
```sql
-- Número de escolas por estado em 2024
SELECT NO_UF, COUNT(*) AS total_escolas
FROM fato_censo_2024
GROUP BY NO_UF
ORDER BY total_escolas DESC;
```

## 📊 Próximos Passos

🔹 **Projeto 2:** Análise exploratória e indicadores de qualidade da educação (Power BI e Python);  
🔹 **Projeto 3:** Publicação dos dados limpos no Kaggle;  
🔹 **Projeto 4:** Pipeline histórico (1995–2006) com reconciliação de códigos e variáveis.

## 🧠 Conceitos Demonstrados

| Competência | Demonstração |
|--------------|--------------|
| ETL Pipeline | Download, extração, limpeza e carregamento dos dados |
| Engenharia de Dados | Padronização e consolidação de datasets heterogêneos |
| Modelagem Relacional | Definição de PK, tabelas de dimensão e fato |
| Otimização de Memória | Conversão de tipos e compressão |
| SQL | Criação de schema e consultas complexas |
| Documentação Técnica | Organização e reprodutibilidade do projeto |

## 💬 Instruções de Execução
1. Clone este repositório:
   ```bash
   git clone https://github.com/rickcolettohub/Censo-Data-ETL-Pipeline.git
    ```

2. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

3. Execute o script import_censo_data.py para baixar os dados brutos do Censo e a criação do arquivo censo_escolar.db:
    ```bash
    python src/import_censo_data.py
    python scripts/build_db.py
    ```

4. Execute o notebook na pasta notebooks/.

4. Consulte o banco via Jupyter:
   ```python
    import pandas as pd
    import sqlalchemy as sqla

    db_path = os.path.join('..','data', 'censo_escolar.db')
    sql_engine = sqla.create_engine(f'sqlite:///{db_path}', echo=True)
    query = pd.read_sql("SELECT * FROM fato_censo_2024 LIMIT 5", sql_engine)
    display(query)
   ```

## 🧾 Licença e Créditos
- Fonte dos dados: **[INEP / Ministério da Educação (MEC)](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar)**  
- Licença: Dados públicos (Acesso aberto)
- Autor: *Rick Coletto*

> 💡 Este repositório faz parte de uma série de projetos voltados ao Censo Escolar Brasileiro.  
> Os dados de 2007–2024 representam a fase metodológica atual, enquanto os dados de 1995–2006 serão tratados em um projeto futuro voltado à integração histórica.
