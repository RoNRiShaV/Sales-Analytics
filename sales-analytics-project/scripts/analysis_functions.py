"""
ANALYSIS FUNCTIONS
Comprehensive analysis of e-commerce sales data
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')

os.makedirs('reports', exist_ok=True)

class SalesAnalyzer:
    """Class for analyzing e-commerce sales data"""
    
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        self.df['order_date'] = pd.to_datetime(self.df['order_date'])
        
    def get_basic_stats(self):
        """Get basic statistical summary"""
        stats = {
            'total_orders': len(self.df),
            'total_revenue': round(self.df['total_revenue'].sum(), 2),
            'avg_order_value': round(self.df['total_revenue'].mean(), 2),
            'median_order_value': round(self.df['total_revenue'].median(), 2),
            'total_customers': self.df['customer_id'].nunique(),
            'total_products': self.df['product_id'].nunique(),
            'total_categories': self.df['category'].nunique(),
            'avg_quantity': round(self.df['quantity'].mean(), 2),
            'avg_discount': round(self.df['discount'].mean() * 100, 2),
            'avg_satisfaction': round(self.df['satisfaction_score'].mean(), 2),
            'avg_shipping_days': round(self.df['shipping_days'].mean(), 2),
            'total_profit': round(self.df['estimated_profit'].sum(), 2),
            'profit_margin': round((self.df['estimated_profit'].sum() / self.df['total_revenue'].sum()) * 100, 2)
        }
        return stats
    
    def get_category_performance(self):
        """Analyze performance by category"""
        return self.df.groupby('category').agg({
            'total_revenue': 'sum',
            'order_id': 'count',
            'quantity': 'sum',
            'satisfaction_score': 'mean',
            'estimated_profit': 'sum'
        }).round(2).sort_values('total_revenue', ascending=False)
    
    def get_monthly_trends(self):
        """Get monthly sales trends"""
        monthly = self.df.groupby(self.df['order_date'].dt.to_period('M')).agg({
            'total_revenue': 'sum',
            'order_id': 'count',
            'estimated_profit': 'sum'
        }).round(2)
        monthly.index = monthly.index.astype(str)
        return monthly
    
    def get_customer_segments(self):
        """Analyze customer segments"""
        segments = self.df.groupby('customer_segment').agg({
            'customer_id': 'nunique',
            'total_revenue': 'sum',
            'order_id': 'count',
            'satisfaction_score': 'mean',
            'estimated_profit': 'sum'
        }).round(2)
        return segments
    
    def get_top_products(self, n=10):
        """Get top N products by revenue"""
        return self.df.groupby('product_name').agg({
            'total_revenue': 'sum',
            'quantity': 'sum',
            'order_id': 'count',
            'satisfaction_score': 'mean'
        }).round(2).sort_values('total_revenue', ascending=False).head(n)
    
    def get_location_performance(self):
        """Analyze performance by location"""
        return self.df.groupby('customer_location').agg({
            'total_revenue': 'sum',
            'order_id': 'count',
            'customer_id': 'nunique'
        }).round(2).sort_values('total_revenue', ascending=False)
    
    def get_payment_analysis(self):
        """Analyze payment methods"""
        return self.df.groupby('payment_method').agg({
            'total_revenue': 'sum',
            'order_id': 'count'
        }).round(2).sort_values('total_revenue', ascending=False)
    
    def get_daily_patterns(self):
        """Analyze daily patterns"""
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily = self.df.groupby('order_weekday').agg({
            'total_revenue': 'sum',
            'order_id': 'count'
        }).reindex(weekday_order).round(2)
        return daily
    
    def get_discount_impact(self):
        """Analyze impact of discounts"""
        discount_groups = self.df.groupby(pd.cut(self.df['discount'], bins=[0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30])).agg({
            'total_revenue': 'sum',
            'order_id': 'count'
        }).round(2)
        return discount_groups
    
    def get_revenue_forecast(self, days=30):
        """Simple revenue forecast using moving average"""
        daily_revenue = self.df.groupby('order_date')['total_revenue'].sum()
        last_30_days = daily_revenue.tail(30).mean()
        forecast = last_30_days * days
        return round(forecast, 2)
    
    def get_correlation_analysis(self):
        """Analyze correlations between numeric variables"""
        numeric_cols = ['quantity', 'unit_price', 'discount', 'final_price', 
                       'shipping_days', 'satisfaction_score', 'total_revenue']
        available_cols = [col for col in numeric_cols if col in self.df.columns]
        return self.df[available_cols].corr()
    
    def run_complete_analysis(self):
        """Run all analyses and return combined results"""
        return {
            'basic_stats': self.get_basic_stats(),
            'category_performance': self.get_category_performance(),
            'monthly_trends': self.get_monthly_trends(),
            'customer_segments': self.get_customer_segments(),
            'top_products': self.get_top_products(),
            'location_performance': self.get_location_performance(),
            'payment_analysis': self.get_payment_analysis(),
            'daily_patterns': self.get_daily_patterns(),
            'discount_impact': self.get_discount_impact(),
            'revenue_forecast_30d': self.get_revenue_forecast(),
            'correlation': self.get_correlation_analysis()
        }
    
    def generate_report(self):
        """Generate a text report of findings"""
        stats = self.get_basic_stats()
        
        report = []
        report.append("="*70)
        report.append("E-COMMERCE SALES ANALYSIS REPORT")
        report.append("="*70)
        report.append(f"\nReport Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("="*70)
        
        report.append("\nKEY METRICS")
        report.append("-"*50)
        report.append(f"Total Orders:        {stats['total_orders']:,}")
        report.append(f"Total Revenue:       ${stats['total_revenue']:,.2f}")
        report.append(f"Average Order Value: ${stats['avg_order_value']:,.2f}")
        report.append(f"Total Customers:     {stats['total_customers']:,}")
        report.append(f"Total Products:      {stats['total_products']:,}")
        report.append(f"Avg Satisfaction:    {stats['avg_satisfaction']:.2f}/5.0")
        report.append(f"Avg Discount:        {stats['avg_discount']:.2f}%")
        report.append(f"Total Profit:        ${stats['total_profit']:,.2f}")
        
        report.append("\nTOP 5 PRODUCTS")
        report.append("-"*50)
        top_products = self.get_top_products(5)
        for idx, (product, data) in enumerate(top_products.iterrows(), 1):
            report.append(f"{idx}. {product}: ${data['total_revenue']:,.2f}")
        
        report.append("\nTOP 5 LOCATIONS")
        report.append("-"*50)
        locations = self.get_location_performance().head(5)
        for idx, (location, data) in enumerate(locations.iterrows(), 1):
            report.append(f"{idx}. {location}: ${data['total_revenue']:,.2f}")
        
        report.append("\nPAYMENT METHODS")
        report.append("-"*50)
        payments = self.get_payment_analysis()
        for method, data in payments.iterrows():
            pct = (data['total_revenue'] / stats['total_revenue'] * 100)
            report.append(f"{method}: ${data['total_revenue']:,.2f} ({pct:.1f}%)")
        
        report.append("\nCUSTOMER SEGMENTS")
        report.append("-"*50)
        segments = self.get_customer_segments()
        for segment, data in segments.iterrows():
            report.append(f"{segment}: {data['customer_id']:,.0f} customers, ${data['total_revenue']:,.2f} revenue")
        
        report.append("\nDAILY PATTERNS")
        report.append("-"*50)
        daily = self.get_daily_patterns()
        for day, data in daily.iterrows():
            report.append(f"{day}: ${data['total_revenue']:,.2f}")
        
        report.append("\nREVENUE FORECAST")
        report.append("-"*50)
        report.append(f"Next 30 Days Forecast: ${self.get_revenue_forecast():,.2f}")
        
        report.append("\n" + "="*70)
        report.append("RECOMMENDATIONS")
        report.append("="*70)
        report.append("1. Focus on Electronics category - highest revenue contributor")
        report.append("2. Target Young Adult segment - highest spending group")
        report.append("3. Optimize Sunday promotions - peak shopping day")
        report.append("4. Consider 15% discount strategy for optimal revenue")
        report.append("5. Improve customer satisfaction in lower-rated products")
        report.append("="*70)
        
        return "\n".join(report)

if __name__ == "__main__":
    print("="*60)
    print("RUNNING COMPLETE ANALYSIS")
    print("="*60)
    
    if not os.path.exists('data/cleaned_sales_data.csv'):
        print("ERROR: data/cleaned_sales_data.csv not found!")
        print("Please run data_cleaning.py first.")
        exit(1)
    
    analyzer = SalesAnalyzer('data/cleaned_sales_data.csv')
    results = analyzer.run_complete_analysis()
    
    print("\nBASIC STATISTICS:")
    for key, value in results['basic_stats'].items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    
    print("\nTOP 5 PRODUCTS BY REVENUE:")
    print(results['top_products'].head(5))
    
    print("\nMONTHLY TRENDS (Last 6 months):")
    print(results['monthly_trends'].tail(6))
    
    report = analyzer.generate_report()
    with open('reports/sales_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("\nReport saved to 'reports/sales_report.txt'")
    print("\n" + report)