# 🏷️ Censo Escolar Brasil (1995–2024): Pipeline de Limpeza e Estruturação de Dados

## 📘 Descrição Geral

Este projeto tem como objetivo padronizar, limpar e estruturar os microdados do Censo Escolar de 1995 a 2024, disponibilizados pelo INEP.

Devido à grande variação no formato dos arquivos ao longo dos anos, foi desenvolvido um pipeline em Python que:

- Faz o download automático dos arquivos originais (.zip);
- Extrai e organiza os dados brutos em pastas padronizadas;
- Limpa, tipa e consolida os CSVs principais;
- Armazena os resultados em um banco de dados SQLite (censo_escolar.db) para fácil consulta e análise posterior.

Este repositório é parte do meu portfólio em Engenharia de Dados, demonstrando habilidades em ETL, modelagem relacional, e automação de pipelines.

## 🧰 Stack Utilizada

- Python 3.13
    - pandas
    - sqlalchemy
    - zipfile / pathlib / os
    - tqdm 
- SQLite (banco leve, sem necessidade de instalação)
- SQLiteStudio (para visualização e checagem de schema)
- Jupyter Notebook / VS Code

## 🗂 Estrutura do Repositório
   ```bash
📂 Censo-Data-ETL-Pipeline/ 
    ├── 📂 data/ -> dados brutos e tratados 
    │    ├── 📂 raw/               # CSVs originais extraídos dos .zip 
    │    ├── 📂 processed/         # CSVs limpos e tratados 
    │    └── 🛢 censo_escolar.db    # Banco SQLite final
    ├── 📓 notebooks/              # notebooks de exploração e limpeza
    ├── 📂 src/ -> scripts Python reutilizáveis
    │    ├── 01_Data_Cleaning.ipynb  # Limpeza e Estruturação dos Dados
    ├── 📄 requirements.txt
    └── 📘 README.md -> documentação do projeto
   ```

## ⚙️ Etapas do Pipeline
### 1️⃣ Download & Extração

O script load_data.py percorre uma lista de links oficiais do INEP, faz o download dos .zip e extrai os arquivos automaticamente.

Arquivos CSV principais são enviados para data/raw/.

Arquivos de apoio (PDFs, dicionários, planilhas) são enviados para .dev/ (gitignored).

### 2️⃣ Limpeza e Padronização

Cada CSV é lido com o encoding correto (latin-1).

Nomes de colunas são padronizados.

Conversão automática:

float → int64

datas no formato %d%b%Y:%H:%M:%S → datetime64

Datasets de cada ano são unidos via concatenação incremental, respeitando diferenças de schema.

### 3️⃣ Armazenamento e Modelagem

Cada tabela é armazenada no SQLite como fato_censo_<ano>.

A tabela entidades contém todas as escolas (CO_ENTIDADE) e seus metadados.

CO_ENTIDADE foi definida como Primary Key via SQLiteStudio.



















## 🚀 Como Reproduzir
1. Clone este repositório:
   ```bash
   git clone https://github.com/rickcolettohub/Censo-Data-ETL-Pipeline.git

2. Instale as dependências:
    ```cmd
    pip install -r requirements.txt

3. Execute o script import_censo_data.py para baixar os dados brutos do Censo:
    ```cmd
    python src/import_censo_data.py

4. Execute os notebooks na pasta notebooks/.

## 📌 Fonte dos Dados

[Censo Escolar - INEP - gov.br](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar)
