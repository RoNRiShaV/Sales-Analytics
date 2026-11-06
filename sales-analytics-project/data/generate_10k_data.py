"""
COMPLETE 10,000 ROW DATA GENERATOR
Generates data matching your exact format with derived columns
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Create data directory
os.makedirs('data', exist_ok=True)

def generate_ecommerce_data(n_rows=10000):
    """Generate complete e-commerce sales data matching your format"""
    
    np.random.seed(42)
    random.seed(42)
    
    # ===== PRODUCT CATALOG =====
    categories = {
        'Electronics': {
            'products': ['Laptop Pro', 'Smartphone X', 'Tablet Air', 'Wireless Headphones', 'Smartwatch Series', 
                        'Gaming Console', '4K TV', 'Bluetooth Speaker', 'Drone', 'Camera'],
            'price_range': (100, 2000)
        },
        'Clothing': {
            'products': ['Designer Jeans', 'Cotton T-Shirt', 'Leather Jacket', 'Running Shoes', 'Summer Dress',
                        'Winter Coat', 'Sweater', 'Hoodie', 'Formal Shirt', 'Polo T-Shirt'],
            'price_range': (15, 300)
        },
        'Books': {
            'products': ['Fiction Bestseller', 'Non-Fiction Guide', 'Textbook Edition', 'E-Book Collection', 'Audiobook Set',
                        'Biography', 'Self-Help Book', 'Cookbook', 'Children Book', 'Science Journal'],
            'price_range': (5, 100)
        },
        'Home & Garden': {
            'products': ['Modern Sofa', 'Decorative Lamp', 'Kitchen Blender', 'Garden Tool Set', 'Wall Art Print',
                        'Coffee Table', 'Bookshelf', 'Plant Pot', 'Floor Mat', 'Curtain Set'],
            'price_range': (20, 800)
        },
        'Sports': {
            'products': ['Yoga Mat', 'Dumbbell Set', 'Sports Shoes', 'Fitness Tracker', 'Water Bottle',
                        'Tennis Racket', 'Football', 'Basketball', 'Cycling Helmet', 'Gym Bag'],
            'price_range': (15, 250)
        }
    }
    
    # Generate product list with prices
    products = []
    for category, info in categories.items():
        for item in info['products']:
            price = round(np.random.uniform(info['price_range'][0], info['price_range'][1]), 2)
            products.append({
                'product_id': f"PRD{len(products)+1:04d}",
                'product_name': item,
                'category': category,
                'base_price': price
            })
    
    # Generate dates (last 365 days)
    end_date = datetime.now()
    
    # Locations
    locations = ['New York', 'California', 'Texas', 'Florida', 'Illinois', 
                 'Pennsylvania', 'Ohio', 'Georgia', 'North Carolina', 'Michigan',
                 'New Jersey', 'Virginia', 'Washington', 'Massachusetts', 'Arizona',
                 'Tennessee', 'Indiana', 'Missouri', 'Maryland', 'Wisconsin']
    
    # Payment methods
    payment_methods = ['Credit Card', 'PayPal', 'Debit Card', 'Net Banking', 'Gift Card']
    
    # Generate data
    data = []
    
    for order_id in range(1, n_rows + 1):
        # Select random product
        product = random.choice(products)
        
        # Generate date (last 365 days, weighted towards recent)
        days_ago = int(np.random.exponential(30))
        days_ago = min(days_ago, 365)
        order_date = end_date - timedelta(days=days_ago)
        
        # Quantity (1-5)
        quantity = random.choices([1, 2, 3, 4, 5], weights=[0.4, 0.3, 0.15, 0.1, 0.05])[0]
        
        # Discount (0-25%)
        discount = random.choices([0, 0.05, 0.10, 0.15, 0.20, 0.25], 
                                  weights=[0.3, 0.2, 0.2, 0.15, 0.1, 0.05])[0]
        
        # Calculate final price
        unit_price = product['base_price']
        final_price = unit_price * (1 - discount) * quantity
        
        # Customer data
        customer_id = f"CUST{random.randint(1000, 9999)}"
        gender = random.choices(['Male', 'Female'], weights=[0.48, 0.52])[0]
        age = int(np.random.normal(35, 12))
        age = max(18, min(65, age))
        location = random.choice(locations)
        
        # Payment method
        payment_method = random.choices(payment_methods, weights=[0.35, 0.25, 0.2, 0.15, 0.05])[0]
        
        # Satisfaction (1-5)
        satisfaction = min(5, max(1, int(np.random.normal(4.2, 0.8))))
        
        # Shipping days (1-7)
        shipping_days = random.choices([1, 2, 3, 4, 5, 6, 7], 
                                       weights=[0.1, 0.2, 0.25, 0.2, 0.15, 0.07, 0.03])[0]
        
        # Create row (matching your exact format)
        row = {
            'order_id': order_id,
            'order_date': order_date.strftime('%Y-%m-%d'),
            'customer_id': customer_id,
            'product_id': product['product_id'],
            'product_name': product['product_name'],
            'category': product['category'],
            'quantity': quantity,
            'unit_price': round(unit_price, 2),
            'discount': discount,
            'final_price': round(final_price, 2),
            'payment_method': payment_method,
            'customer_gender': gender,
            'customer_age': age,
            'customer_location': location,
            'shipping_days': shipping_days,
            'satisfaction_score': satisfaction
        }
        data.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    df['order_date'] = pd.to_datetime(df['order_date'])
    
    # ===== ADD DERIVED COLUMNS =====
    
    # Date components
    df['order_year'] = df['order_date'].dt.year
    df['order_month'] = df['order_date'].dt.month
    df['order_day'] = df['order_date'].dt.day
    df['order_weekday'] = df['order_date'].dt.day_name()
    df['order_quarter'] = df['order_date'].dt.quarter
    df['order_week'] = df['order_date'].dt.isocalendar().week
    
    # Customer segment
    df['customer_segment'] = pd.cut(
        df['customer_age'],
        bins=[0, 25, 35, 50, 100],
        labels=['Young (18-24)', 'Young Adult (25-34)', 
                'Middle Age (35-49)', 'Senior (50+)'],
        right=False
    )
    
    # Total revenue (same as final_price)
    df['total_revenue'] = df['final_price']
    
    # Estimated profit (30% margin)
    df['estimated_profit'] = df['total_revenue'] * 0.3
    
    # Discount percentage
    df['discount_percentage'] = df['discount'] * 100
    
    # Shipping speed
    df['shipping_speed'] = pd.cut(
        df['shipping_days'],
        bins=[0, 2, 4, 10],
        labels=['Fast (1-2 days)', 'Standard (3-4 days)', 'Slow (5+ days)']
    )
    
    return df

if __name__ == "__main__":
    print("="*70)
    print("GENERATING COMPLETE E-COMMERCE DATA (10,000 ROWS)")
    print("="*70)
    
    # Generate data
    df = generate_ecommerce_data(10000)
    
    # Save to CSV
    csv_path = 'data/ecommerce_sales.csv'
    df.to_csv(csv_path, index=False)
    
    print(f"\n[SUCCESS] Generated {len(df):,} rows")
    print(f"Data saved to: {csv_path}")
    
    print("\n" + "="*70)
    print("COLUMN INFORMATION")
    print("="*70)
    print(f"Total Columns: {len(df.columns)}")
    print("\nColumns:")
    for col in df.columns:
        print(f"  - {col}: {df[col].dtype}")
    
    print("\n" + "="*70)
    print("BASIC STATISTICS")
    print("="*70)
    print(df.describe())
    
    print("\n" + "="*70)
    print("CATEGORY DISTRIBUTION")
    print("="*70)
    print(df['category'].value_counts())
    
    print("\n" + "="*70)
    print("TOTAL REVENUE SUMMARY")
    print("="*70)
    print(f"Total Revenue: ${df['total_revenue'].sum():,.2f}")
    print(f"Average Order Value: ${df['total_revenue'].mean():,.2f}")
    print(f"Total Orders: {len(df):,}")
    print(f"Total Customers: {df['customer_id'].nunique():,}")
    print(f"Total Products: {df['product_id'].nunique():,}")
    print(f"Total Categories: {df['category'].nunique():,}")
    print(f"Average Satisfaction: {df['satisfaction_score'].mean():.2f}/5.0")
    print(f"Average Discount: {df['discount_percentage'].mean():.2f}%")
    
    print("\n" + "="*70)
    print("SAMPLE 10 ROWS")
    print("="*70)
    print(df.head(10).to_string())