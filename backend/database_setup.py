#!/usr/bin/env python3
"""
Database Setup for Executive Dashboard
PostgreSQL integration with real business data
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.db_url = os.getenv("DATABASE_URL", 
            "postgresql://postgres:password@localhost:5432/executive_dashboard")
    
    def connect(self):
        """Connect to PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(self.db_url)
            return True
        except Exception as e:
            print(f"Database connection failed: {e}")
            return False
    
    def create_tables(self):
        """Create necessary tables for business data"""
        if not self.connection:
            return False
            
        tables_sql = """
        -- Companies table
        CREATE TABLE IF NOT EXISTS companies (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            industry VARCHAR(100),
            size VARCHAR(50),
            location VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Financial data table
        CREATE TABLE IF NOT EXISTS financial_data (
            id SERIAL PRIMARY KEY,
            company_id INTEGER REFERENCES companies(id),
            date DATE NOT NULL,
            revenue DECIMAL(15,2),
            expenses DECIMAL(15,2),
            profit DECIMAL(15,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Customer data table
        CREATE TABLE IF NOT EXISTS customer_data (
            id SERIAL PRIMARY KEY,
            company_id INTEGER REFERENCES companies(id),
            customer_count INTEGER,
            new_customers INTEGER,
            churned_customers INTEGER,
            date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- KPI metrics table
        CREATE TABLE IF NOT EXISTS kpi_metrics (
            id SERIAL PRIMARY KEY,
            company_id INTEGER REFERENCES companies(id),
            metric_name VARCHAR(100) NOT NULL,
            metric_value DECIMAL(15,2),
            date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(tables_sql)
                self.connection.commit()
            return True
        except Exception as e:
            print(f"Table creation failed: {e}")
            return False
    
    def import_csv_data(self, file_path, table_name):
        """Import data from CSV file"""
        try:
            df = pd.read_csv(file_path)
            
            # Convert DataFrame to SQL
            with self.connection.cursor() as cursor:
                for _, row in df.iterrows():
                    columns = row.index.tolist()
                    values = row.values.tolist()
                    
                    placeholders = ', '.join(['%s'] * len(values))
                    sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
                    
                    cursor.execute(sql, values)
                
                self.connection.commit()
            return True
            
        except Exception as e:
            print(f"CSV import failed: {e}")
            return False
    
    def get_company_kpis(self, company_id, start_date=None, end_date=None):
        """Retrieve KPI data for a company"""
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                sql = """
                SELECT * FROM kpi_metrics 
                WHERE company_id = %s
                """
                params = [company_id]
                
                if start_date and end_date:
                    sql += " AND date BETWEEN %s AND %s"
                    params.extend([start_date, end_date])
                
                sql += " ORDER BY date DESC"
                
                cursor.execute(sql, params)
                return cursor.fetchall()
                
        except Exception as e:
            print(f"KPI retrieval failed: {e}")
            return []

if __name__ == "__main__":
    db = DatabaseManager()
    
    if db.connect():
        print("✅ Database connected successfully")
        
        if db.create_tables():
            print("✅ Tables created successfully")
        else:
            print("❌ Table creation failed")
    else:
        print("❌ Database connection failed")
