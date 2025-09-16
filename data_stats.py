import pandas as pd

pd.set_option('display.max_columns', None)  # Mostrar todas as colunas
pd.set_option('display.width', None)        # Ajustar a largura do display


# 1. Carregue o dataset
try:
    df = pd.read_csv('manipulated_foodpanda_analysis_dataset.csv')
except FileNotFoundError:
    print("Erro: O arquivo 'manipulated_foodpanda_analysis_dataset.csv' não foi encontrado.")
    exit()

# 2. Análise Estatística Geral com describe()
print("="*50)
print("ANÁLISE ESTATÍSTICA DESCRITIVA GERAL")
print(df.describe().to_string(float_format="%.2f"))  # Formata os floats para 2 casas decimais
print("="*50)

# 3. Use groupby() para uma análise por cidade
city_summary = df.groupby('city').agg(
    num_restaurants=('restaurant_name', 'nunique'),
    num_dishes=('dish_name', 'nunique'),
    num_categories=('category', 'nunique'),
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

# 4. Imprima o resultado de forma concisa e organizada
print("\nANÁLISE ESTATÍSTICA CONSOLIDADA POR CIDADE")
print(city_summary.to_string(float_format="%.2f")) # Formata os floats para 2 casas decimais

# Valor médio de cada prato
print("\nVALOR MÉDIO DE CADA PRATO")
print(df.groupby('dish_name')['price'].mean().sort_values(ascending=False).to_string(float_format="%.2f")) # Formata os floats para 2 casas decimais
print('='*50)

# Valor Médio de cada pedido
print("\nVALOR MÉDIO DE CADA PEDIDO")

# Calcule o valor médio de cada pedido e armazene em uma nova Série
avg_order_price = df.groupby('order_id')['price'].mean()

# Calcule os quartis (Q1, Q2 - Mediana, Q3)
q1 = avg_order_price.quantile(0.25)
median = avg_order_price.quantile(0.50)
q3 = avg_order_price.quantile(0.75)

# Crie faixas de preço usando a função categorize_price
def categorize_price(price):
    if price <= q1:
        return 'Baixo (Q1)'
    elif price <= median:
        return 'Médio-Baixo (Q2)'
    elif price <= q3:
        return 'Médio-Alto (Q3)'
    else:
        return 'Alto (Q4)'

# Crie uma nova Série com as categorias, uma para cada pedido único
order_price_category = avg_order_price.apply(categorize_price)

# Agrupe a Série de preços médios usando as novas categorias e calcule as estatísticas
# O count() aqui será sobre o número de pedidos únicos
price_summary = avg_order_price.groupby(order_price_category).agg(['mean', 'sum'])

print("\nRESUMO CORRIGIDO DO NÚMERO DE PEDIDOS POR FAIXA DE PREÇO:")
print(f"\nDetalhes das Faixas de Preço:")
print(f"Baixo (Q1): Pedidos com valor menor ou igual a {q1:.2f}")
print(f"Médio-Baixo (Q2): Pedidos entre {q1:.2f} e {median:.2f}")
print(f"Médio-Alto (Q3): Pedidos entre {median:.2f} e {q3:.2f}")
print(f"Alto (Q4): Pedidos com valor maior que {q3:.2f}\n")

print(price_summary.to_string(float_format="%.2f"))
print('='*50)

# Valor Médio gasto por Faixa Etária
age_spent = df.groupby('age')['price'].mean().sort_values(ascending=False)
print("\nVALOR MÉDIO GASTO POR FAIXA ETÁRIA")       
print(age_spent.to_string(float_format="%.2f")) # Formata os floats para 2 casas decimais
print('='*50)

# Número de Operações por Método de Pagamento
print("\nFREQUÊNCIA DOS MÉTODOS DE PAGAMENTO")
print(df['payment_method'].value_counts())
print('='*50)

# Numero de Clientes ativos vs Inativos
print("\nNÚMERO DE CLIENTES ATIVOS VS INATIVOS")
print(df['churned'].value_counts()) 
print('='*50)   

# Relação entre status do pedido e clientes inativos
print("\nRELATIONSHIP BETWEEN CANCELLED ORDERS AND INACTIVE CUSTOMERS")

# Criar tabela de contingência
contingency_table = pd.crosstab(df['delivery_status'], df['churned'])
print("Contingency Table:")
print(contingency_table)

# Calcular proporções
print(f"\nProportions:")
proportions = contingency_table.div(contingency_table.sum(axis=1), axis=0)
print(proportions.round(4))

# Foco nos cancelamentos
cancelled_inactive = len(df[(df['delivery_status'] == 'Cancelled') & (df['churned'] == 'Inactive')])
total_cancelled = len(df[df['delivery_status'] == 'Cancelled'])
total_inactive = len(df[df['churned'] == 'Inactive'])

print(f"\nKey Metrics:")
print(f"Total cancelled orders: {total_cancelled}")
print(f"Cancelled orders with inactive customers: {cancelled_inactive}")
print(f"% of cancelled orders that are inactive: {(cancelled_inactive/total_cancelled)*100:.2f}%")
print(f"% of inactive customers with cancelled orders: {(cancelled_inactive/total_inactive)*100:.2f}%")

print('='*50)

# Relação entre dias da semana e número de pedidos
print("\nRELATIONSHIP DAYS AND ORDERS")

# Definir a ordem dos dias da semana
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Contar pedidos por dia da semana (ordenado)
if 'order_day_of_week' in df.columns:
    day_column = 'order_day_of_week'
else:
    # Verificar outros possíveis nomes de coluna
    possible_names = [col for col in df.columns if 'day' in col.lower()]
    if possible_names:
        day_column = possible_names[0]
        print(f"Using column: {day_column}")
    else:
        print("No day column found!")
        print('='*50)
        exit()

# Reindexar para manter a ordem dos dias
orders_by_day = df[day_column].value_counts()
if all(day in orders_by_day.index for day in day_order):
    orders_by_day = orders_by_day.reindex(day_order)

print("Orders by day of week:")
print(orders_by_day)

# Análise detalhada
print(f"\nDetailed Analysis:")
total_orders = len(df)

for day in orders_by_day.index:
    count = orders_by_day[day]
    percentage = (count / total_orders) * 100
    print(f"{day}: {count:,} orders ({percentage:.2f}%)")

# Comparação com média
avg_orders = orders_by_day.mean()
print(f"\nComparison with average ({avg_orders:.1f} orders/day):")
for day in orders_by_day.index:
    count = orders_by_day[day]
    diff = count - avg_orders
    if diff > 0:
        print(f"{day}: +{diff:.1f} above average")
    else:
        print(f"{day}: {diff:.1f} below average")

# Análise por status de entrega (se desejado)
print(f"\nOrders by day and delivery status:")
day_status_analysis = pd.crosstab(df[day_column], df['delivery_status'], margins=True)
print(day_status_analysis)

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

# Comparação com taxa média de cancelamento
total_cancelled = len(df[df['delivery_status'] == 'Cancelled'])
overall_cancellation_rate = (total_cancelled / total_orders) * 100

print(f"\nComparison with overall cancellation rate ({overall_cancellation_rate:.2f}%):")
for age_range in orders_by_age.index:
    if pd.notna(age_range):
        total_age_orders = orders_by_age[age_range]
        cancelled_age_orders = cancelled_by_age.get(age_range, 0)
        age_cancellation_rate = (cancelled_age_orders / total_age_orders) * 100
        
        diff = age_cancellation_rate - overall_cancellation_rate
        if diff > 0:
            print(f"{age_range}: +{diff:.2f}% above average")
        else:
            print(f"{age_range}: {diff:.2f}% below average")

# Identificar faixas etárias com maior e menor cancelamento
if len(cancelled_by_age) > 0:
    highest_cancellation_age = cancelled_by_age.idxmax()
    lowest_cancellation_age = cancelled_by_age.idxmin()
    
    print(f"\nAge Range Performance:")
    print(f"Highest cancellations: {highest_cancellation_age} ({cancelled_by_age[highest_cancellation_age]:,} orders)")
    print(f"Lowest cancellations: {lowest_cancellation_age} ({cancelled_by_age[lowest_cancellation_age]:,} orders)")

# Análise completa por status de entrega
print(f"\nComplete analysis by age and delivery status:")
age_status_crosstab = pd.crosstab(df[age_col_to_use], df['delivery_status'], margins=True)
print(age_status_crosstab)

# Percentual por faixa etária
print(f"\nPercentage distribution by delivery status within each age range:")
age_status_pct = pd.crosstab(df[age_col_to_use], df['delivery_status'], normalize='index') * 100
print(age_status_pct.round(2))

print('='*50)