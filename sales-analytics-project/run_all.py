"""
MASTER SCRIPT - Runs all components
"""

import subprocess
import os
import sys
import time

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def run_script(script_path, description):
    print_header(f"Running: {description}")
    try:
        result = subprocess.run([sys.executable, script_path], 
                               capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[SUCCESS] {description} completed")
            output_lines = result.stdout.split('\n')
            if len(output_lines) > 10:
                print('\n'.join(output_lines[-10:]))
            else:
                print(result.stdout)
            return True
        else:
            print(f"[ERROR] {description} failed")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"[ERROR] Exception: {e}")
        return False

def main():
    print_header("E-COMMERCE DATA ANALYTICS PROJECT")
    print("Starting full pipeline...")
    
    os.makedirs('data', exist_ok=True)
    os.makedirs('visualizations/charts', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    
    if not os.path.exists('data/ecommerce_sales.csv'):
        print("Generating new data...")
        if not run_script('data/generate_10k_data.py', 'Data Generation'):
            print("[ERROR] Project halted")
            return
    else:
        print("[SKIP] Data file already exists")
    
    time.sleep(1)
    
    if not run_script('scripts/data_cleaning.py', 'Data Cleaning'):
        print("[ERROR] Project halted")
        return
    
    time.sleep(1)
    
    if not run_script('scripts/analysis_functions.py', 'Data Analysis'):
        print("[ERROR] Project halted")
        return
    
    time.sleep(1)
    
    if not run_script('scripts/visualization.py', 'Visualization Creation'):
        print("[ERROR] Project halted")
        return
    
    print_header("PROJECT COMPLETED SUCCESSFULLY")
    print("\nOutput Files Generated:")
    print("  Data Files:")
    print("    - data/ecommerce_sales.csv (Raw data)")
    print("    - data/cleaned_sales_data.csv (Cleaned data)")
    print("\n  Visualizations:")
    print("    - visualizations/charts/ - Static charts (PNG)")
    print("\n  Reports:")
    print("    - reports/sales_report.txt - Analysis report")
    print("\n  Web Dashboard:")
    print("    - web_dashboard/index.html - Interactive dashboard")
    print("\nNext Steps:")
    print("  1. Open web_dashboard/index.html in your browser")
    print("  2. Check reports/sales_report.txt for insights")
    print("  3. View visualizations in the charts folder")
    print("\n" + "="*70)

if __name__ == "__main__":
    main()