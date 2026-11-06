"""
VISUALIZATION SCRIPT
Creates comprehensive visualizations for e-commerce data
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

os.makedirs('visualizations/charts', exist_ok=True)

class SalesVisualizer:
    """Class for creating sales visualizations"""
    
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        self.df['order_date'] = pd.to_datetime(self.df['order_date'])
        plt.style.use('default')
        sns.set_palette("husl")
        
    def create_all_visualizations(self):
        """Create all visualizations"""
        print("Creating visualizations...")
        
        self.plot_revenue_trend()
        self.plot_category_distribution()
        self.plot_top_products()
        self.plot_monthly_sales()
        self.plot_customer_segments()
        self.plot_location_revenue()
        self.plot_payment_methods()
        self.plot_satisfaction_distribution()
        self.plot_discount_impact()
        self.plot_daily_sales_pattern()
        self.plot_correlation_heatmap()
        
        print("All visualizations saved to 'visualizations/charts/'")
    
    def plot_revenue_trend(self):
        fig, ax = plt.subplots(figsize=(14, 6))
        daily_revenue = self.df.groupby('order_date')['total_revenue'].sum()
        daily_revenue.plot(ax=ax, color='#4f46e5', linewidth=2, alpha=0.7)
        
        for window, color, label in [(7, '#10b981', '7-Day MA'), (30, '#f59e0b', '30-Day MA')]:
            if len(daily_revenue) >= window:
                rolling = daily_revenue.rolling(window=window).mean()
                rolling.plot(ax=ax, color=color, linestyle='--', linewidth=1.5, label=label)
        
        ax.set_title('Daily Revenue Trend with Moving Averages', fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Revenue ($)', fontsize=12)
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('visualizations/charts/revenue_trend.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  - Revenue trend chart created")
    
    def plot_category_distribution(self):
        category_revenue = self.df.groupby('category')['total_revenue'].sum().sort_values(ascending=True)
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = sns.color_palette("viridis", len(category_revenue))
        bars = ax.barh(category_revenue.index, category_revenue.values, color=colors)
        
        for bar in bars:
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2, 
                   f'${width:,.0f}', ha='left', va='center', fontsize=10, fontweight='bold')
        
        ax.set_title('Revenue by Category', fontsize=16, fontweight='bold')
        ax.set_xlabel('Revenue ($)', fontsize=12)
        ax.grid(True, alpha=0.3, axis='x')
        plt.tight_layout()
        plt.savefig('visualizations/charts/category_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  - Category distribution chart created")
    
    def plot_top_products(self):
        top_products = self.df.groupby('product_name')['total_revenue'].sum().sort_values(ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(12, 7))
        colors = sns.color_palette("rocket", len(top_products))
        bars = ax.bar(range(len(top_products)), top_products.values, color=colors)
        
        ax.set_xticks(range(len(top_products)))
        ax.set_xticklabels(top_products.index, rotation=45, ha='right')
        ax.set_title('Top 10 Products by Revenue', fontsize=16, fontweight='bold')
        ax.set_xlabel('Product', fontsize=12)
        ax.set_ylabel('Revenue ($)', fontsize=12)
        
        for bar, value in zip(bars, top_products.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100,
                   f'${value:,.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig('visualizations/charts/top_products.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  - Top products chart created")
    
    def plot_monthly_sales(self):
        monthly = self.df.groupby(self.df['order_date'].dt.to_period('M')).agg({
            'total_revenue': 'sum',
            'order_id': 'count'
        }).reset_index()
        monthly['order_date'] = monthly['order_date'].astype(str)
        
        fig, ax1 = plt.subplots(figsize=(14, 6))
        color = '#4f46e5'
        ax1.set_xlabel('Month', fontsize=12)
        ax1.set_ylabel('Revenue ($)', color=color, fontsize=12)
        ax1.plot(monthly['order_date'], monthly['total_revenue'], color=color, 
                marker='o', linewidth=2.5, markersize=8)
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.tick_params(axis='x', rotation=45)
        
        ax2 = ax1.twinx()
        color = '#10b981'
        ax2.set_ylabel('Number of Orders', color=color, fontsize=12)
        ax2.plot(monthly['order_date'], monthly['order_id'], color=color, 
                marker='s', linestyle='--', linewidth=2, markersize=8)
        ax2.tick_params(axis='y', labelcolor=color)
        
        ax1.set_title('Monthly Revenue and Orders', fontsize=16, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('visualizations/charts/monthly_sales.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  - Monthly sales chart created")
    
    def plot_customer_segments(self):
        segments = self.df.groupby('customer_segment').agg({
            'total_revenue': 'sum',
            'customer_id': 'nunique'
        }).reset_index()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        colors = sns.color_palette("viridis", len(segments))
        bars = ax1.bar(segments['customer_segment'], segments['total_revenue'], color=colors)
        ax1.set_title('Revenue by Customer Segment', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Segment', fontsize=11)
        ax1.set_ylabel('Revenue ($)', fontsize=11)
        
        bars2 = ax2.bar(segments['customer_segment'], segments['customer_id'], color=colors)
        ax2.set_title('Customer Count by Segment', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Segment', fontsize=11)
        ax2.set_ylabel('Number of Customers', fontsize=11)
        
        for bar, value in zip(bars, segments['total_revenue']):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500,
                    f'${value:,.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        for bar, value in zip(bars2, segments['customer_id']):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                    f'{value}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        ax1.grid(True, alpha=0.3, axis='y')
        ax2.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig('visualizations/charts/customer_segments.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  - Customer segments chart created")
    
    def plot_location_revenue(self):
        location_revenue = self.df.groupby('customer_location')['total_revenue'].sum().sort_values(ascending=False).head(8)
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = sns.color_palette("plasma", len(location_revenue))
        bars = ax.bar(location_revenue.index, location_revenue.values, color=colors)
        
        ax.set_title('Revenue by Location', fontsize=16, fontweight='bold')
        ax.set_xlabel('Location', fontsize=12)
        ax.set_ylabel('Revenue ($)', fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        
        for bar, value in zip(bars, location_revenue.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500,
                   f'${value:,.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig('visualizations/charts/location_revenue.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  - Location revenue chart created")
    
    def plot_payment_methods(self):
        payment_data = self.df.groupby('payment_method').agg({
            'total_revenue': 'sum',
            'order_id': 'count'
        }).reset_index()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        colors = sns.color_palette("pastel", len(payment_data))
        ax1.pie(payment_data['total_revenue'], labels=payment_data['payment_method'],
                autopct='%1.1f%%', colors=colors)
        ax1.set_title('Revenue Distribution by Payment Method', fontsize=14, fontweight='bold')
        
        colors2 = sns.color_palette("Set3", len(payment_data))
        bars = ax2.bar(payment_data['payment_method'], payment_data['order_id'], color=colors2)
        ax2.set_title('Order Count by Payment Method', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Payment Method', fontsize=11)
        ax2.set_ylabel('Number of Orders', fontsize=11)
        ax2.tick_params(axis='x', rotation=15)
        ax2.grid(True, alpha=0.3, axis='y')
        
        for bar, value in zip(bars, payment_data['order_id']):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                    f'{value}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('visualizations/charts/payment_methods.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  - Payment methods chart created")
    
    def plot_satisfaction_distribution(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        satisfaction_counts = self.df['satisfaction_score'].value_counts().sort_index()
        colors = sns.color_palette("RdYlGn", len(satisfaction_counts))
        bars = ax.bar(satisfaction_counts.index, satisfaction_counts.values, color=colors)
        
        ax.set_title('Customer Satisfaction Score Distribution', fontsize=16, fontweight='bold')
        ax.set_xlabel('Satisfaction Score', fontsize=12)
        ax.set_ylabel('Number of Customers', fontsize=12)
        ax.set_xticks(range(1, 6))
        ax.grid(True, alpha=0.3, axis='y')
        
        total = satisfaction_counts.sum()
        for bar, value in zip(bars, satisfaction_counts.values):
            pct = (value / total) * 100
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                   f'{value}\n({pct:.1f}%)', ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        plt.savefig('visualizations/charts/satisfaction_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  - Satisfaction distribution chart created")
    
    def plot_discount_impact(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        discount_groups = self.df.groupby(pd.cut(self.df['discount'], bins=[0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30])).agg({
            'total_revenue': 'sum',
            'order_id': 'count'
        }).reset_index()
        
        discount_groups['discount_range'] = discount_groups['discount'].astype(str)
        discount_groups['discount_range'] = discount_groups['discount_range'].str.replace('(', '').str.replace(']', '')
        
        ax1.bar(discount_groups['discount_range'], discount_groups['total_revenue'], 
                color='lightcoral', edgecolor='darkred', linewidth=1.5)
        ax1.set_title('Revenue by Discount Range', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Discount Range', fontsize=11)
        ax1.set_ylabel('Revenue ($)', fontsize=11)
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, alpha=0.3, axis='y')
        
        ax2.bar(discount_groups['discount_range'], discount_groups['order_id'], 
                color='lightblue', edgecolor='navy', linewidth=1.5)
        ax2.set_title('Order Count by Discount Range', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Discount Range', fontsize=11)
        ax2.set_ylabel('Number of Orders', fontsize=11)
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('visualizations/charts/discount_impact.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  - Discount impact chart created")
    
    def plot_daily_sales_pattern(self):
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday_revenue = self.df.groupby('order_weekday')['total_revenue'].sum().reindex(weekday_order)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#FF6B6B' if day in ['Saturday', 'Sunday'] else '#4ECDC4' for day in weekday_order]
        bars = ax.bar(weekday_order, weekday_revenue.values, color=colors, edgecolor='black', linewidth=0.5)
        ax.set_title('Revenue by Day of Week', fontsize=16, fontweight='bold')
        ax.set_xlabel('Day of Week', fontsize=12)
        ax.set_ylabel('Revenue ($)', fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')
        
        for bar, value in zip(bars, weekday_revenue.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1000,
                   f'${value:,.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('visualizations/charts/daily_sales_pattern.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  - Daily sales pattern chart created")
    
    def plot_correlation_heatmap(self):
        numeric_cols = ['quantity', 'unit_price', 'discount', 'final_price', 
                       'shipping_days', 'satisfaction_score', 'total_revenue']
        available_cols = [col for col in numeric_cols if col in self.df.columns]
        
        if len(available_cols) >= 2:
            corr = self.df[available_cols].corr()
            fig, ax = plt.subplots(figsize=(10, 8))
            mask = np.triu(np.ones_like(corr, dtype=bool))
            sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='coolwarm',
                       square=True, linewidths=1, ax=ax)
            ax.set_title('Correlation Heatmap', fontsize=16, fontweight='bold')
            plt.tight_layout()
            plt.savefig('visualizations/charts/correlation_heatmap.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("  - Correlation heatmap created")
        else:
            print("  - Not enough columns for correlation heatmap")

if __name__ == "__main__":
    print("="*60)
    print("CREATING VISUALIZATIONS")
    print("="*60)
    
    if not os.path.exists('data/cleaned_sales_data.csv'):
        print("ERROR: data/cleaned_sales_data.csv not found!")
        print("Please run data_cleaning.py first.")
        exit(1)
    
    visualizer = SalesVisualizer('data/cleaned_sales_data.csv')
    visualizer.create_all_visualizations()
    
    print("\nAll visualizations saved!")
    print("Check the 'visualizations/charts/' folder for all outputs")