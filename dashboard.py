import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Dashboard Foodpanda - Análise de Dados",
    page_icon="🍕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Função para carregar os dados
@st.cache_data
def load_data():
    df = pd.read_csv('manipulated_foodpanda_analysis_dataset.csv')
    return df

# Função para calcular métricas gerais
def calculate_general_metrics(df):
    metrics = {
        'total_orders': len(df),
        'unique_cities': df['city'].nunique(),
        'unique_restaurants': df['restaurant_name'].nunique(),
        'unique_dishes': df['dish_name'].nunique(),
        'unique_categories': df['category'].nunique(),
        'avg_rating': df['rating'].mean(),
        'avg_order_frequency': df['order_frequency'].mean(),
        'total_revenue': df['price'].sum(),
        'avg_order_value': df['price'].mean()
    }
    return metrics

# Função para criar rankings
def create_ranking_chart(data, title, x_label, y_label, color_scheme='viridis'):
    """Cria gráfico de barras horizontais para rankings"""
    fig = px.bar(
        x=data.values,
        y=data.index,
        orientation='h',
        title=title,
        labels={'x': x_label, 'y': y_label},
        color=data.values,
        color_continuous_scale=color_scheme
    )
    fig.update_layout(
        height=400,
        showlegend=False,
        yaxis={'categoryorder': 'total ascending'}
    )
    return fig

# Carregamento dos dados
df = load_data()

# Título principal
st.title("🍕 Dashboard Foodpanda - Análise de Dados")
st.markdown("---")

# Sidebar para filtros
st.sidebar.header("Filtros")

# Filtros
cities = st.sidebar.multiselect(
    "Selecione as Cidades:",
    options=df['city'].unique(),
    default=df['city'].unique()
)

genders = st.sidebar.multiselect(
    "Selecione o Gênero:",
    options=df['gender'].unique(),
    default=df['gender'].unique()
)

ages = st.sidebar.multiselect(
    "Selecione a Faixa Etária:",
    options=df['age'].unique(),
    default=df['age'].unique()
)

payment_methods = st.sidebar.multiselect(
    "Selecione o Método de Pagamento:",
    options=df['payment_method'].unique(),
    default=df['payment_method'].unique()
)

delivery_status = st.sidebar.multiselect(
    "Selecione o Status de Entrega:",
    options=df['delivery_status'].unique(),
    default=df['delivery_status'].unique()
)

# Aplicar filtros
filtered_df = df[
    (df['city'].isin(cities)) &
    (df['gender'].isin(genders)) &
    (df['age'].isin(ages)) &
    (df['payment_method'].isin(payment_methods)) &
    (df['delivery_status'].isin(delivery_status))
]

# Verificar se há dados após filtros
if filtered_df.empty:
    st.error("Nenhum dado encontrado com os filtros selecionados. Por favor, ajuste os filtros.")
    st.stop()

# Calcular métricas
metrics = calculate_general_metrics(filtered_df)

# Seção de Métricas Principais
st.header("📊 Métricas Principais")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total de Pedidos", f"{metrics['total_orders']:,}")
with col2:
    st.metric("Cidades", metrics['unique_cities'])
with col3:
    st.metric("Restaurantes", metrics['unique_restaurants'])
with col4:
    st.metric("Avaliação Média", f"{metrics['avg_rating']:.2f}")
with col5:
    st.metric("Receita Total", f"R$ {metrics['total_revenue']:,.2f}")

st.markdown("---")

# Seção de Análise por Cidade
st.header("🏙️ Análise por Cidade")
col1, col2 = st.columns(2)

with col1:
    city_revenue = filtered_df.groupby('city')['price'].sum().sort_values(ascending=True)
    fig_city_revenue = px.bar(
        x=city_revenue.values,
        y=city_revenue.index,
        orientation='h',
        title="Receita Total por Cidade",
        labels={'x': 'Receita (R$)', 'y': 'Cidade'},
        color=city_revenue.values,
        color_continuous_scale='Blues'
    )
    fig_city_revenue.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_city_revenue, use_container_width=True)

with col2:
    city_rating = filtered_df.groupby('city')['rating'].mean().sort_values(ascending=True)
    fig_city_rating = px.bar(
        x=city_rating.values,
        y=city_rating.index,
        orientation='h',
        title="Avaliação Média por Cidade",
        labels={'x': 'Avaliação Média', 'y': 'Cidade'},
        color=city_rating.values,
        color_continuous_scale='Greens'
    )
    fig_city_rating.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_city_rating, use_container_width=True)

st.markdown("---")

# Seção de Padrões de Pedidos
st.header("📅 Padrões de Pedidos")
col1, col2 = st.columns(2)

with col1:
    monthly_orders = filtered_df.groupby('order_month').size().sort_index()
    fig_monthly = px.line(
        x=monthly_orders.index,
        y=monthly_orders.values,
        title="Pedidos por Mês",
        labels={'x': 'Mês', 'y': 'Número de Pedidos'},
        markers=True
    )
    fig_monthly.update_layout(height=400)
    st.plotly_chart(fig_monthly, use_container_width=True)

with col2:
    weekly_orders = filtered_df.groupby('order_day_of_week').size()
    fig_weekly = px.bar(
        x=weekly_orders.index,
        y=weekly_orders.values,
        title="Pedidos por Dia da Semana",
        labels={'x': 'Dia da Semana', 'y': 'Número de Pedidos'},
        color=weekly_orders.values,
        color_continuous_scale='Oranges'
    )
    fig_weekly.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_weekly, use_container_width=True)

st.markdown("---")

# Seção de Comportamento do Cliente
st.header("👥 Comportamento do Cliente")
col1, col2 = st.columns(2)

with col1:
    gender_spending = filtered_df.groupby('gender')['price'].mean().sort_values(ascending=True)
    fig_gender = px.bar(
        x=gender_spending.values,
        y=gender_spending.index,
        orientation='h',
        title="Gasto Médio por Gênero",
        labels={'x': 'Gasto Médio (R$)', 'y': 'Gênero'},
        color=gender_spending.values,
        color_continuous_scale='Purples'
    )
    fig_gender.update_layout(height=300, showlegend=False)
    st.plotly_chart(fig_gender, use_container_width=True)

with col2:
    payment_dist = filtered_df['payment_method'].value_counts()
    fig_payment = px.pie(
        values=payment_dist.values,
        names=payment_dist.index,
        title="Distribuição dos Métodos de Pagamento"
    )
    fig_payment.update_layout(height=300)
    st.plotly_chart(fig_payment, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    churned_status = filtered_df['churned'].value_counts()
    churned_labels = ['Ativo' if x == 0 else 'Inativo' for x in churned_status.index]
    fig_status = px.pie(
        values=churned_status.values,
        names=churned_labels,
        title="Clientes Ativos vs Inativos"
    )
    fig_status.update_layout(height=300)
    st.plotly_chart(fig_status, use_container_width=True)

with col4:
    age_spending = filtered_df.groupby('age')['price'].mean().sort_values(ascending=True)
    fig_age = px.bar(
        x=age_spending.values,
        y=age_spending.index,
        orientation='h',
        title="Gasto Médio por Faixa Etária",
        labels={'x': 'Gasto Médio (R$)', 'y': 'Faixa Etária'},
        color=age_spending.values,
        color_continuous_scale='Reds'
    )
    fig_age.update_layout(height=300, showlegend=False)
    st.plotly_chart(fig_age, use_container_width=True)

st.markdown("---")

# Seção de Análise de Cancelamentos
st.header("❌ Análise de Cancelamentos")
col1, col2 = st.columns(2)

with col1:
    # Taxa de cancelamento por faixa etária
    cancellation_by_age = filtered_df.groupby('age').apply(
        lambda x: (x['delivery_status'] == 'Cancelled').mean() * 100
    ).sort_values(ascending=True)
    
    fig_cancel_age = px.bar(
        x=cancellation_by_age.values,
        y=cancellation_by_age.index,
        orientation='h',
        title="Taxa de Cancelamento por Faixa Etária (%)",
        labels={'x': 'Taxa de Cancelamento (%)', 'y': 'Faixa Etária'},
        color=cancellation_by_age.values,
        color_continuous_scale='Reds'
    )
    fig_cancel_age.update_layout(height=300, showlegend=False)
    st.plotly_chart(fig_cancel_age, use_container_width=True)

with col2:
    # Heatmap de correlação entre status de entrega e churned
    status_churned = pd.crosstab(
        filtered_df['delivery_status'], 
        filtered_df['churned'], 
        normalize='columns'
    ) * 100
    
    # Renomear as colunas para melhor visualização
    status_churned.columns = ['Ativo', 'Inativo']
    
    fig_heatmap = px.imshow(
        status_churned.values,
        x=status_churned.columns,
        y=status_churned.index,
        title="Relação Status de Entrega vs Inatividade (%)",
        color_continuous_scale='RdYlBu_r',
        text_auto=True
    )
    fig_heatmap.update_layout(height=300)
    st.plotly_chart(fig_heatmap, use_container_width=True)

st.markdown("---")

# NOVA SEÇÃO: Rankings e Top Performers
st.header("🏆 Rankings e Top Performers")

# Criar abas para diferentes tipos de rankings
tab1, tab2, tab3, tab4 = st.tabs(["📊 Por Volume", "💰 Por Receita", "🍽️ Produtos", "📅 Temporal"])

with tab1:
    st.subheader("Rankings por Volume de Pedidos")
    col1, col2 = st.columns(2)
    
    with col1:
        # Top categorias por volume
        top_categories = filtered_df['category'].value_counts().head(5)
        fig_cat_vol = create_ranking_chart(
            top_categories, 
            "Top 5 Categorias Mais Pedidas",
            "Número de Pedidos",
            "Categoria",
            'viridis'
        )
        st.plotly_chart(fig_cat_vol, use_container_width=True)
    
    with col2:
        # Top cidades por volume
        top_cities_vol = filtered_df['city'].value_counts().head(5)
        fig_cities_vol = create_ranking_chart(
            top_cities_vol,
            "Top 5 Cidades com Mais Pedidos",
            "Número de Pedidos", 
            "Cidade",
            'plasma'
        )
        st.plotly_chart(fig_cities_vol, use_container_width=True)
    
    # Top pratos por volume
    st.subheader("Top 10 Pratos Mais Pedidos")
    top_dishes_vol = filtered_df['dish_name'].value_counts().head(10)
    fig_dishes_vol = create_ranking_chart(
        top_dishes_vol,
        "Pratos Mais Populares por Volume",
        "Número de Pedidos",
        "Prato",
        'cividis'
    )
    st.plotly_chart(fig_dishes_vol, use_container_width=True)

with tab2:
    st.subheader("Rankings por Receita Total")
    col1, col2 = st.columns(2)
    
    with col1:
        # Top faixas etárias por receita
        top_age_revenue = filtered_df.groupby('age')['price'].sum().sort_values(ascending=False).head(5)
        fig_age_rev = create_ranking_chart(
            top_age_revenue,
            "Top Faixas Etárias por Receita",
            "Receita Total (R$)",
            "Faixa Etária",
            'blues'
        )
        st.plotly_chart(fig_age_rev, use_container_width=True)
    
    with col2:
        # Top cidades por receita
        top_cities_revenue = filtered_df.groupby('city')['price'].sum().sort_values(ascending=False).head(5)
        fig_cities_rev = create_ranking_chart(
            top_cities_revenue,
            "Top 5 Cidades por Receita",
            "Receita Total (R$)",
            "Cidade", 
            'greens'
        )
        st.plotly_chart(fig_cities_rev, use_container_width=True)
    
    # Top restaurantes por receita
    st.subheader("Top 10 Restaurantes por Receita")
    top_restaurants_revenue = filtered_df.groupby('restaurant_name')['price'].sum().sort_values(ascending=False).head(10)
    fig_rest_rev = create_ranking_chart(
        top_restaurants_revenue,
        "Restaurantes com Maior Receita",
        "Receita Total (R$)",
        "Restaurante",
        'oranges'
    )
    st.plotly_chart(fig_rest_rev, use_container_width=True)

with tab3:
    st.subheader("Rankings de Produtos")
    
    # Top pratos por receita
    st.subheader("Top 10 Pratos por Receita")
    top_dishes_revenue = filtered_df.groupby('dish_name')['price'].sum().sort_values(ascending=False).head(10)
    fig_dishes_rev = create_ranking_chart(
        top_dishes_revenue,
        "Pratos com Maior Receita",
        "Receita Total (R$)",
        "Prato",
        'reds'
    )
    st.plotly_chart(fig_dishes_rev, use_container_width=True)
    
    # Comparação volume vs receita para categorias
    col1, col2 = st.columns(2)
    with col1:
        cat_volume = filtered_df['category'].value_counts().head(5)
        fig_cat_comp1 = px.bar(
            x=cat_volume.index,
            y=cat_volume.values,
            title="Categorias: Volume de Pedidos",
            labels={'x': 'Categoria', 'y': 'Pedidos'},
            color=cat_volume.values,
            color_continuous_scale='viridis'
        )
        fig_cat_comp1.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_cat_comp1, use_container_width=True)
    
    with col2:
        cat_revenue = filtered_df.groupby('category')['price'].sum().sort_values(ascending=False).head(5)
        fig_cat_comp2 = px.bar(
            x=cat_revenue.index,
            y=cat_revenue.values,
            title="Categorias: Receita Total",
            labels={'x': 'Categoria', 'y': 'Receita (R$)'},
            color=cat_revenue.values,
            color_continuous_scale='plasma'
        )
        fig_cat_comp2.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_cat_comp2, use_container_width=True)

with tab4:
    st.subheader("Rankings Temporais")
    col1, col2 = st.columns(2)
    
    with col1:
        # Top meses por pedidos
        top_months = filtered_df['order_month'].value_counts().sort_values(ascending=False).head(5)
        fig_months = px.bar(
            x=top_months.index,
            y=top_months.values,
            title="Top 5 Meses com Mais Pedidos",
            labels={'x': 'Mês', 'y': 'Número de Pedidos'},
            color=top_months.values,
            color_continuous_scale='turbo'
        )
        fig_months.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_months, use_container_width=True)
    
    with col2:
        # Top meses por receita
        top_months_revenue = filtered_df.groupby('order_month')['price'].sum().sort_values(ascending=False).head(5)
        fig_months_rev = px.bar(
            x=top_months_revenue.index,
            y=top_months_revenue.values,
            title="Top 5 Meses por Receita",
            labels={'x': 'Mês', 'y': 'Receita (R$)'},
            color=top_months_revenue.values,
            color_continuous_scale='inferno'
        )
        fig_months_rev.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_months_rev, use_container_width=True)

st.markdown("---")

# Seção de Dados Detalhados
st.header("📋 Dados Detalhados")
st.subheader("Estatísticas por Cidade")

# Criar resumo por cidade
city_summary = filtered_df.groupby('city').agg({
    'rating': 'mean',
    'order_frequency': 'mean',
    'price': ['sum', 'mean'],
    'restaurant_name': lambda x: x.mode().iloc[0] if not x.mode().empty else 'N/A',
    'category': lambda x: x.mode().iloc[0] if not x.mode().empty else 'N/A',
    'payment_method': lambda x: x.mode().iloc[0] if not x.mode().empty else 'N/A'
}).round(2)

# Achatar as colunas multi-nível
city_summary.columns = ['Avaliação Média', 'Freq. Pedidos Média', 'Receita Total', 'Preço Médio', 
                       'Restaurante Popular', 'Categoria Popular', 'Método Pagamento Popular']

st.dataframe(city_summary, use_container_width=True) # Revertendo para use_container_width=True para st.dataframe

# Opção para baixar os dados filtrados
st.subheader("Download dos Dados Filtrados")
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="📥 Baixar dados filtrados como CSV",
    data=csv,
    file_name='foodpanda_dados_filtrados.csv',
    mime='text/csv'
)

st.markdown("---")
st.markdown("**Dashboard criado com base nas análises dos scripts Python fornecidos**")
st.markdown("_Dados: Foodpanda Analysis Dataset_")

