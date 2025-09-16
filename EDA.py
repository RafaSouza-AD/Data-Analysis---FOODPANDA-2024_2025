import pandas as pd
import numpy as np


df = pd.read_csv('manipulated_foodpanda_analysis_dataset.csv')

# Stats for the entire dataset
print('='*50)
print("\nOVERALL DATASET STATS")
unique_cities = df['city'].nunique()
list_cities = df['city'].unique()   
print(f"\nNumber of Unique Cities: {unique_cities} cities {list_cities}")
unique_restaurants = df['restaurant_name'].nunique()
list_restaurants = df['restaurant_name'].unique()
print(f"\nNumber of Unique Restaurants: {unique_restaurants} restaurants {list_restaurants}")
unique_dishes = df['dish_name'].nunique()
list_dishes = df['dish_name'].unique()
print(f"\nNumber of Unique Dishes: {unique_dishes} dishes {list_dishes}")
unique_categories = df['category'].nunique()
list_categories = df['category'].unique()
print(f"\nNumber of Unique Categories: {unique_categories} categories {list_categories}")
average_rating = df['rating'].mean()
print(f"\nOverall Average Rating (between 0-5): {average_rating:.2f}")
average_order_frequency = df['order_frequency'].mean()
print(f"\nOveral Average Order Frequency: {average_order_frequency:.1f} orders")
payment_methods = df['payment_method'].value_counts()
print(f"\nMost Used Payment Methods:\n{payment_methods}")
print('='*50)

# Stats by city
print("\nSTATS BY CITY")
cities = df['city'].unique()
for city in cities:
    city_data = df[df['city'] == city]
    num_restaurants = city_data['restaurant_name'].nunique()
    num_dishes = city_data['dish_name'].nunique()
    num_categories = city_data['category'].nunique()
    avg_rating = city_data['rating'].mean()
    avg_order_freq = city_data['order_frequency'].mean()
    avg_price = city_data['price'].mean()
    price_range = city_data['price'].sum()
    payment_methods_city = city_data['payment_method'].value_counts()
    
    print(f"\nCity: {city}")
    print(f"Average Rating: {avg_rating:.1f}")
    print(f"Average Order Frequency: {avg_order_freq:.0f} orders")
    print(f'Total Amount Spent: {price_range: ,.2f} currency units')
    print(f'Average Price per Order: {avg_price: ,.2f} currency units')
    print('Principal Payment Methods: ', payment_methods_city.head(1).index[0])
    print(f"Number of Unique Restaurants: {num_restaurants} restaurants")
    print('Most Popular Restaurant: ', city_data["restaurant_name"].value_counts().head(1).index[0])
    print(f'Most Popular Category: ', city_data["category"].value_counts().head(1).index[0])
    print(f'Most Popular Dish: ', city_data["dish_name"].value_counts().head(1).index[0])
   
    print('-'*30)
print('='*50)


