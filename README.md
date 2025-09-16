# Dashboard Foodpanda - Análise de Dados

## Descrição
Este dashboard interativo foi desenvolvido com base na análise dos scripts Python fornecidos (`data_analysis.py`, `data_stats.py` e `EDA.py`) e apresenta insights detalhados sobre os dados do Foodpanda de forma visual e interativa.

## Funcionalidades

### 📊 Métricas Principais
- Total de pedidos
- Número de cidades, restaurantes e categorias
- Avaliação média geral
- Receita total

### 🏙️ Análise por Cidade
- Receita total por cidade
- Avaliação média por cidade
- Comparação visual entre diferentes cidades

### 📅 Padrões de Pedidos
- Análise temporal por mês
- Distribuição por dia da semana
- Identificação de picos e tendências

### 👥 Comportamento do Cliente
- Gastos médios por gênero e faixa etária
- Distribuição dos métodos de pagamento
- Análise de clientes ativos vs inativos

### ❌ Análise de Cancelamentos
- Taxa de cancelamento por faixa etária
- Relação entre status de entrega e inatividade do cliente
- Heatmap de correlações

### 🔍 Filtros Interativos
- **Cidades**: Peshawar, Multan, Lahore, Karachi, Islamabad
- **Gênero**: Male, Female, Other
- **Faixa Etária**: Adult, Senior, Teenager
- **Método de Pagamento**: Cash, Wallet, Card
- **Status de Entrega**: Delivered, Delayed, Cancelled

### 📋 Dados Detalhados
- Tabela resumo por cidade
- Opção de download dos dados filtrados em CSV

### 🏆 Seção de Rankings e Top Performers
- 📊 Por Volume: Rankings baseados em quantidade de pedidos
- 💰 Por Receita: Rankings baseados em receita gerada
- 🍽️ Produtos: Rankings de pratos e categorias mais populares
- 📅 Temporal: Rankings por períodos temporais
  
### 📈 Visualizações dos Rankings:
- Top 5 Categorias Mais Pedidas
- Top 5 Cidades com Mais Pedidos
- Top 10 Pratos Mais Pedidos
- Rankings dinâmicos que se atualizam com os filtros

## Como Executar

### Pré-requisitos
```bash
pip install streamlit pandas plotly numpy
```

### Execução
```bash
streamlit run dashboard.py
```

**Nota:** Se você encontrar um erro relacionado a `width='stretch'` em `st.dataframe`, por favor, atualize seu Streamlit ou use `use_container_width=True` para essa função, pois o comportamento pode variar entre as versões.

O dashboard estará disponível em: `http://localhost:8501`

## Estrutura dos Dados
O dashboard utiliza o arquivo `manipulated_foodpanda_analysis_dataset.csv` que contém as seguintes colunas principais:
- Informações do cliente (ID, gênero, idade, cidade)
- Dados do pedido (ID, data, restaurante, prato, categoria)
- Métricas (quantidade, preço, avaliação, frequência)
- Status (entrega, pagamento, atividade do cliente)

## Insights Principais Evidenciados

### Análises Implementadas
1. **Visão Geral**: Estatísticas descritivas e métricas chave
2. **Segmentação Geográfica**: Performance por cidade
3. **Padrões Temporais**: Sazonalidade e tendências
4. **Comportamento do Cliente**: Preferências e gastos
5. **Análise de Churn**: Cancelamentos e inatividade

### Visualizações
- Gráficos de barras para comparações
- Gráficos de linha para tendências temporais
- Gráficos de pizza para distribuições
- Heatmaps para correlações
- Métricas em cards para KPIs

## Tecnologias Utilizadas
- **Streamlit**: Framework para criação do dashboard
- **Plotly**: Biblioteca para visualizações interativas
- **Pandas**: Manipulação e análise de dados
- **NumPy**: Operações numéricas

## Características Técnicas
- Interface responsiva e intuitiva
- Filtros dinâmicos que atualizam todas as visualizações
- Gráficos interativos com opções de zoom, pan e download
- Cache de dados para melhor performance
- Validação de filtros para evitar datasets vazios

Este dashboard consolida todas as análises realizadas nos scripts originais em uma interface única, permitindo exploração interativa dos dados e descoberta de insights de forma visual e intuitiva.

