"""
DATA CLEANING SCRIPT
Cleans and preprocesses e-commerce sales data
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')

os.makedirs('data', exist_ok=True)
os.makedirs('logs', exist_ok=True)

class DataCleaner:
    """Class for cleaning and preprocessing e-commerce data"""
    
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        self.df['order_date'] = pd.to_datetime(self.df['order_date'])
        self.original_shape = self.df.shape
        self.cleaning_log = []
        self.outliers_removed = {}
        
    def clean_data(self):
        """Perform all cleaning operations"""
        self.log("STARTING DATA CLEANING...")
        self.log(f"Original shape: {self.df.shape}")
        
        # 1. Handle missing values
        self.handle_missing_values()
        
        # 2. Remove duplicates
        self.remove_duplicates()
        
        # 3. Fix data types
        self.fix_data_types()
        
        # 4. Handle outliers
        self.handle_outliers()
        
        # 5. Add derived columns
        self.add_derived_columns()
        
        # 6. Final validation
        self.validate_data()
        
        self.log(f"CLEANING COMPLETE. Final shape: {self.df.shape}")
        return self.df
    
    def handle_missing_values(self):
        """Handle missing values in the dataset"""
        missing_before = self.df.isnull().sum().sum()
        
        # Fill missing values with appropriate defaults
        if 'customer_gender' in self.df.columns:
            self.df['customer_gender'] = self.df['customer_gender'].fillna('Unknown')
        if 'customer_age' in self.df.columns:
            self.df['customer_age'] = self.df['customer_age'].fillna(self.df['customer_age'].median())
        if 'satisfaction_score' in self.df.columns:
            self.df['satisfaction_score'] = self.df['satisfaction_score'].fillna(3)
        if 'shipping_days' in self.df.columns:
            self.df['shipping_days'] = self.df['shipping_days'].fillna(3)
        
        missing_after = self.df.isnull().sum().sum()
        self.log(f"Missing values: {missing_before} -> {missing_after}")
    
    def remove_duplicates(self):
        """Remove duplicate rows"""
        duplicates = self.df.duplicated().sum()
        if duplicates > 0:
            self.df = self.df.drop_duplicates()
            self.log(f"Removed {duplicates} duplicate rows")
        else:
            self.log("No duplicate rows found")
    
    def fix_data_types(self):
        """Fix incorrect data types"""
        if 'order_date' in self.df.columns:
            self.df['order_date'] = pd.to_datetime(self.df['order_date'])
        if 'discount' in self.df.columns:
            self.df['discount'] = pd.to_numeric(self.df['discount'], errors='coerce')
        if 'final_price' in self.df.columns:
            self.df['final_price'] = pd.to_numeric(self.df['final_price'], errors='coerce')
        
        self.log("Data types fixed")
    
    def handle_outliers(self):
        """Handle outliers using IQR method"""
        numeric_cols = ['final_price', 'quantity', 'shipping_days']
        
        for col in numeric_cols:
            if col in self.df.columns:
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)]
                if len(outliers) > 0:
                    self.df = self.df[(self.df[col] >= lower_bound) & (self.df[col] <= upper_bound)]
                    self.outliers_removed[col] = len(outliers)
                    self.log(f"Removed {len(outliers)} outliers from {col}")
    
    def add_derived_columns(self):
        """Add useful derived columns for analysis"""
        if 'order_date' in self.df.columns:
            self.df['order_year'] = self.df['order_date'].dt.year
            self.df['order_month'] = self.df['order_date'].dt.month
            self.df['order_day'] = self.df['order_date'].dt.day
            self.df['order_weekday'] = self.df['order_date'].dt.day_name()
            self.df['order_quarter'] = self.df['order_date'].dt.quarter
            self.df['order_week'] = self.df['order_date'].dt.isocalendar().week
        
        if 'customer_age' in self.df.columns:
            self.df['customer_segment'] = pd.cut(
                self.df['customer_age'],
                bins=[0, 25, 35, 50, 100],
                labels=['Young (18-24)', 'Young Adult (25-34)', 
                        'Middle Age (35-49)', 'Senior (50+)'],
                right=False
            )
        
        if 'final_price' in self.df.columns:
            self.df['total_revenue'] = self.df['final_price']
            self.df['estimated_profit'] = self.df['total_revenue'] * 0.3
        
        if 'discount' in self.df.columns:
            self.df['discount_percentage'] = self.df['discount'] * 100
        
        if 'shipping_days' in self.df.columns:
            self.df['shipping_speed'] = pd.cut(
                self.df['shipping_days'],
                bins=[0, 2, 4, 10],
                labels=['Fast (1-2 days)', 'Standard (3-4 days)', 'Slow (5+ days)']
            )
        
        self.log("Added derived columns")
    
    def validate_data(self):
        """Validate the cleaned data"""
        if 'final_price' in self.df.columns:
            negative_prices = (self.df['final_price'] < 0).sum()
            if negative_prices > 0:
                self.log(f"WARNING: {negative_prices} negative prices found")
        
        missing = self.df.isnull().sum()
        if missing.sum() > 0:
            self.log(f"WARNING: {missing.sum()} missing values remain")
        else:
            self.log("No missing values remain")
    
    def log(self, message):
        """Add message to cleaning log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cleaning_log.append(f"[{timestamp}] {message}")
    
    def get_cleaning_summary(self):
        """Get summary of cleaning operations"""
        summary = {
            'original_rows': self.original_shape[0],
            'final_rows': self.df.shape[0],
            'original_columns': self.original_shape[1],
            'final_columns': self.df.shape[1],
            'outliers_removed': self.outliers_removed,
            'cleaning_log': self.cleaning_log[-5:]
        }
        return summary

if __name__ == "__main__":
    print("="*60)
    print("DATA CLEANING PROCESS")
    print("="*60)
    
    if not os.path.exists('data/ecommerce_sales.csv'):
        print("ERROR: data/ecommerce_sales.csv not found!")
        print("Please run generate_10k_data.py first.")
        exit(1)
    
    cleaner = DataCleaner('data/ecommerce_sales.csv')
    cleaned_df = cleaner.clean_data()
    
    cleaned_df.to_csv('data/cleaned_sales_data.csv', index=False)
    
    print("\n" + "="*60)
    print("CLEANING SUMMARY")
    print("="*60)
    summary = cleaner.get_cleaning_summary()
    print(f"Original Rows: {summary['original_rows']:,}")
    print(f"Final Rows: {summary['final_rows']:,}")
    print(f"Original Columns: {summary['original_columns']}")
    print(f"Final Columns: {summary['final_columns']}")
    if summary['outliers_removed']:
        print("\nOutliers Removed:")
        for col, count in summary['outliers_removed'].items():
            print(f"  - {col}: {count}")
    
    print("\nCleaned data saved to 'data/cleaned_sales_data.csv'")
    print("\nSample of cleaned data:")
    print(cleaned_df.head())