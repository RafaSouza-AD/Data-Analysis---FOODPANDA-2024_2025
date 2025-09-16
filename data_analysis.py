import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns

df = pd.read_csv('manipulated_foodpanda_analysis_dataset.csv')

print('\n' + '=' * 50)
print('\nANALYTICAL OVERVIEW OF THE MANIPULATED DATASET')
print('\nThis section provides an analytical overview of the manipulated dataset, including correlational ' \
'information between various variables, with the aim of identifying relevant patterns and trends for data analysis.')
print('\n' + '=' * 50)

print("First 5 rows of the dataset:")
print(df.head())
print('-' * 50)
print("\nName of Coolumns in the dataset:")
print(df.columns)      
print('-' * 50)
print("\nDataset Information:")
print(df.info())
print('-' * 50) 
print("\nStatistical Summary:")
print(df[['quantity',
       'price', 'order_frequency', 'rating_date']].describe().to_string(float_format="%.2f")) 
print('-' * 50)
total_missing_values = df.isnull().sum().sum()
print(f"Total of Missing Values in the Dataset: {total_missing_values}")
print('-' * 50)
print("\nUnique Values in Each Column:")
print(df.nunique())
print('-' * 50)

print('=' * 50)
print("\nCORRELATIONAL ANALYSIS BETWEEN VARIABLES")
print('\n' + '=' * 50)

# 3. Use groupby() para uma análise por cidade
city_summary = df.groupby('city').agg(
    avg_rating=('rating', 'mean'),
    avg_order_freq=('order_frequency', 'mean'),
    total_amount_spent=('price', 'sum'),
    avg_price_per_order=('price', 'mean'),
    
    # Para as colunas categóricas mais populares, usamos uma função lambda
    most_popular_restaurant=('restaurant_name', lambda x: x.mode()[0]),
    most_popular_category=('category', lambda x: x.mode()[0]),
    most_popular_dish=('dish_name', lambda x: x.mode()[0]),
    most_popular_payment_method=('payment_method', lambda x: x.mode()[0])
)

print("\nCONSOLIDATED STATISTICAL ANALYSIS BY CITY")
print(city_summary) # Formata os floats para 2 casas decimais
print("="*50)

# Análise do Padrão de Pedidos por Mês
print("\nANALYSIS OF ORDER PATTERN BY MONTH")
monthly_orders = df['order_month'].value_counts()
print("\nMonthly Order Pattern:")
print(monthly_orders)
print('-'*50)

# Mês com maior e menor volume
busiest_month = monthly_orders.idxmax()
slowest_month = monthly_orders.idxmin()

print(f"\nPeak Performance:")
print(f"Busiest Month: {busiest_month} ({monthly_orders[busiest_month]:,} orders)")
print(f"Slowest Month: {slowest_month} ({monthly_orders[slowest_month]:,} orders)")
print(f"Difference: {monthly_orders[busiest_month] - monthly_orders[slowest_month]:,} orders")

print('=' * 50)

# Valor Médio gasto por Método de Pagamento
payment_spent = df.groupby('payment_method')['price'].mean().sort_values(ascending=False)
print("\nAVARAGE AMOUNT SPENT BY PAYMENT METHOD")    
print(payment_spent.to_string(float_format="%.2f")) # Formata os floats para 2 casas decimais
print('='*50)

# Média de gastos por genero
genre_spent = df.groupby('gender')['price'].mean().sort_values(ascending=False)
print("\nAVERAGE AMOUNT SPENT BY GENDER")    
print(genre_spent.to_string(float_format="%.2f")) # Formata os floats para 2 casas decimais
print('='*50)

# Stats by city
print("\nANALYSIS BY AGE RANGE")
ages = df['age'].unique()
for age in ages:
    age_data = df[df['age'] == age]
    num_costumers = age_data['age'].value_counts().sum().sum()
    num_dishes = age_data['dish_name'].nunique()
    num_categories = age_data['category'].nunique()
    avg_rating = age_data['rating'].mean()
    avg_order_freq = age_data['order_frequency'].mean()
    num_order_freq = age_data['order_frequency'].sum()
    avg_price = age_data['price'].mean()
    price_range = age_data['price'].sum()
    num_churned_inactive = (age_data['churned'] == 'Inactive').sum()
    num_chuerned_active = (age_data['churned'] == 'Active').sum()
    payment_methods_city = age_data['payment_method'].value_counts()
    num_cancellations = (age_data['delivery_status'] == 'Cancelled').sum()
    
    print(f"\nAge: {age}")
    print(f'Number of Costumers: {num_costumers}')
    print(f'Number of Inactive Customers: {num_churned_inactive}')
    print(f'Number of Active Customers: {num_chuerned_active}')
    print(f"Average Rating: {avg_rating:.1f}")
    print(f"Average Order Frequency: {avg_order_freq:.0f} orders")
    print(f'Total Amount Spent: {price_range: ,.2f} currency units')
    print(f'Average Price per Order: {avg_price: ,.2f} currency units')
    print('Principal Payment Methods: ', payment_methods_city.head(1).index[0])
    print('Most Popular Restaurant: ', age_data["restaurant_name"].value_counts().head(1).index[0])
    print(f'Most Popular Category: ', age_data["category"].value_counts().head(1).index[0])
    print(f'Most Popular Dish: ', age_data["dish_name"].value_counts().head(1).index[0])
    print(f'Total Number of Orders: {num_order_freq} orders')
    print(f'Number of Cancellations: {num_cancellations} cancellations')
   
    print('-'*30)
print('='*50)

# Relação entre status do pedido e clientes inativos
print("\nRELATIONSHIP BETWEEN CANCELLED ORDERS AND INACTIVE CUSTOMERS") 

# Tabela cruzada entre delivery_status e churned
# crosstab é usado para cruzar duas colunas da tabela e gerar uma vizualização mais clara e objetiva
cross_tab = pd.crosstab(df['delivery_status'], df['churned'], margins=True)
print("Cross-tabulation:")
print(cross_tab)

# Percentuais por linha (mostra a distribuição de churned para cada status)
cross_tab_pct = pd.crosstab(df['delivery_status'], df['churned'], normalize='index') * 100
print(f"\nPercentages (%) by delivery status:")
print(f'{cross_tab_pct.round(0)}')

print('='*50)

# Relação entre dias da semana e número de pedidos
print("\nRELATIONSHIP DAYS AND ORDERS")

# Usar o nome correto da coluna
day_col = 'order_day_of_week'  # Ajuste conforme necessário

# Análise básica
orders_by_day = df[day_col].value_counts()
print("Orders by day of week:")
print(orders_by_day.sort_index())

# Identificar padrões
weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
weekends = ['Saturday', 'Sunday']

if all(day in df[day_col].values for day in weekdays + weekends):
    weekday_orders = df[df[day_col].isin(weekdays)].shape[0]
    weekend_orders = df[df[day_col].isin(weekends)].shape[0]
    
    print(f"\nWeekday vs Weekend Analysis:")
    print(f"Weekday orders (Mon-Fri): {weekday_orders:,}")
    print(f"Weekend orders (Sat-Sun): {weekend_orders:,}")
    print(f"Weekday average per day: {weekday_orders/5:.1f}")
    print(f"Weekend average per day: {weekend_orders/2:.1f}")

# Dia com maior e menor volume
busiest_day = orders_by_day.idxmax()
slowest_day = orders_by_day.idxmin()

print(f"\nPeak Performance:")
print(f"Busiest day: {busiest_day} ({orders_by_day[busiest_day]:,} orders)")
print(f"Slowest day: {slowest_day} ({orders_by_day[slowest_day]:,} orders)")
print(f"Difference: {orders_by_day[busiest_day] - orders_by_day[slowest_day]:,} orders")

print('='*50)

# Número de Cancelamentos por faixa etária
print("\nCANCELLATIONS BY AGE RANGE")

# Verificar se existe coluna de idade
if 'age' in df.columns:
    age_column = 'age'
else:
    # Verificar outros possíveis nomes de coluna de idade
    possible_names = [col for col in df.columns if 'age' in col.lower()]
    if possible_names:
        age_column = possible_names[0]
        print(f"Using column: {age_column}")
    else:
        print("No age column found!")
        print('='*50)
        exit()

# Criar faixas etárias se necessário (caso a idade seja numérica)
if df[age_column].dtype in ['int64', 'float64']:
    # Criar bins de idade
    df['age_range'] = pd.cut(df[age_column], 
                            bins=[0, 18, 25, 35, 45, 55, 65, 100], 
                            labels=['<18', '18-24', '25-34', '35-44', '45-54', '55-64', '65+'])
    age_col_to_use = 'age_range'
else:
    age_col_to_use = age_column

# Análise geral por faixa etária
orders_by_age = df[age_col_to_use].value_counts().sort_index()
print("Total orders by age range:")
print(orders_by_age)

# Análise específica de cancelamentos
cancelled_by_age = df[df['delivery_status'] == 'Cancelled'][age_col_to_use].value_counts().sort_index()
print(f"\nCancelled orders by age range:")
print(cancelled_by_age)

# Calcular taxa de cancelamento por faixa etária
print(f"\nCancellation rate by age range:")
total_orders = len(df)

for age_range in orders_by_age.index:
    if pd.notna(age_range):  # Verificar se não é NaN
        total_age_orders = orders_by_age[age_range]
        cancelled_age_orders = cancelled_by_age.get(age_range, 0)
        cancellation_rate = (cancelled_age_orders / total_age_orders) * 100
        
        print(f"{age_range}:")
        print(f"  Total orders: {total_age_orders:,}")
        print(f"  Cancelled orders: {cancelled_age_orders:,}")
        print(f"  Cancellation rate: {cancellation_rate:.2f}%")

# Identificar faixas etárias com maior e menor cancelamento
if len(cancelled_by_age) > 0:
    highest_cancellation_age = cancelled_by_age.idxmax()
    lowest_cancellation_age = cancelled_by_age.idxmin()
    
    print(f"\nAge Range Performance:")
    print(f"Highest cancellations: {highest_cancellation_age} ({cancelled_by_age[highest_cancellation_age]:,} orders)")
    print(f"Lowest cancellations: {lowest_cancellation_age} ({cancelled_by_age[lowest_cancellation_age]:,} orders)")

print('='*50)