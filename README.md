# 📊 Censo Escolar — Construção e Padronização de Séries Históricas (1995–2024)

## 🎯 Objetivo

- Unificar os arquivos brutos de 30 anos.
- Padronizar nomes de colunas, tipos e categorias.
- Tratar valores ausentes, inconsistências e duplicatas.
- Gerar datasets limpos e documentados prontos para uso em análise.

## 📌 Principais Perguntas de Negócio (KPIs)

1. sacac
2. asc
3. ascasas
4. ascasca
5. ascasc

## 🗂 Estrutura do Repositório
> Censo-Data-ETL-Pipeline/ <br />
> ├── data/ -> dados brutos e tratados <br />
> ├── notebooks/ -> notebooks de exploração, limpeza e análise <br />
> ├── src/ -> scripts Python reutilizáveis <br />
> ├── reports/ -> visualizações e dashboard Power BI <br />
> └── README.md -> documentação do projeto <br />

## 🔧 Tecnologias Usadas
- Python
- Pandas
- Power BI
- Jupyter Notebook

## 📊 Resultados Principais

### 1. Quais são as categorias mais vendidas? 
- Pasc
- ascascs
<img src="reports/figures/categorias_00.png" alt="Description of image">

### 2. Qual é o ticket médio por cliente?
- Éascascac
- ascascacs
<img src="reports/figures/ticket_medio_00.png" alt="Description of image">

### 3. Como está a evolução de vendas ao longo do tempo?
- ascascasc
<img src="reports/figures/evolucao_vendas_00.png" alt="Description of image">

### 4. Qual a distribuição geográfica dos clientes?
- ascascasc
- ascasca
<img src="reports/figures/distribuicao_geografica_00.png" alt="Description of image">

### 5. Existem padrões de sazonalidade nas vendas?
- ascascac
- ascacas

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
