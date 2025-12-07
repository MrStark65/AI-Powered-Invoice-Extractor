"""Output generation service for CSV, Excel, and charts."""

import csv
from pathlib import Path
from typing import List, Dict
from datetime import datetime
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict


class OutputGenerator:
    """Generates CSV, Excel, and chart outputs from extracted invoice data."""
    
    def generate_csv(self, data: List[Dict], output_dir: Path) -> Path:
        """Generate CSV file with extracted invoice data."""
        csv_path = output_dir / 'invoices.csv'
        
        if not data:
            headers = ['vendor_name', 'invoice_number', 'date', 'total_amount', 'currency', 'filename']
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
            return csv_path
        
        headers = list(data[0].keys())
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        
        return csv_path
    
    def generate_excel(self, data: List[Dict], output_dir: Path) -> Path:
        """Generate Excel dashboard with formatted data."""
        excel_path = output_dir / 'invoices_dashboard.xlsx'
        
        if not data:
            headers = ['vendor_name', 'invoice_number', 'date', 'total_amount', 'currency', 'filename']
            df = pd.DataFrame(columns=headers)
        else:
            df = pd.DataFrame(data)
        
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Invoices', index=False)
            
            worksheet = writer.sheets['Invoices']
            for idx, col in enumerate(df.columns):
                max_length = max(
                    df[col].astype(str).apply(len).max() if len(df) > 0 else 0,
                    len(col)
                ) + 2
                worksheet.column_dimensions[chr(65 + idx)].width = min(max_length, 50)
        
        return excel_path
    
    def generate_chart(self, data: List[Dict], output_dir: Path) -> Path:
        """Generate monthly spending chart visualization."""
        chart_path = output_dir / 'monthly_spending.png'
        
        if not data:
            plt.figure(figsize=(10, 6))
            plt.text(0.5, 0.5, 'No data available', ha='center', va='center')
            plt.savefig(chart_path)
            plt.close()
            return chart_path
        
        monthly_totals = defaultdict(float)
        for invoice in data:
            try:
                date_str = invoice.get('date', 'N/A')
                if date_str != 'N/A':
                    date = datetime.strptime(date_str, '%Y-%m-%d')
                    month_key = date.strftime('%Y-%m')
                    amount = float(invoice.get('total_amount', 0))
                    monthly_totals[month_key] += amount
            except (ValueError, TypeError):
                continue
        
        if not monthly_totals:
            plt.figure(figsize=(10, 6))
            plt.text(0.5, 0.5, 'No valid date data', ha='center', va='center')
            plt.savefig(chart_path)
            plt.close()
            return chart_path
        
        sorted_months = sorted(monthly_totals.items())
        months = [m[0] for m in sorted_months]
        amounts = [m[1] for m in sorted_months]
        
        plt.figure(figsize=(12, 6))
        plt.bar(months, amounts, color='steelblue')
        plt.xlabel('Month')
        plt.ylabel('Total Amount')
        plt.title('Monthly Spending')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(chart_path, dpi=300)
        plt.close()
        
        return chart_path
