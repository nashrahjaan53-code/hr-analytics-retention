"""Employee performance analysis"""
import pandas as pd

def performance_distribution(df):
    """Analyze performance rating distribution"""
    return df['performance_rating'].describe().round(2)

def salary_analysis(df):
    """Analyze salary by role and department"""
    return df.groupby(['department', 'job_role']).agg({
        'salary': ['mean', 'min', 'max', 'count']
    }).round(2)

def top_performers(df, n=10):
    """Identify top performers"""
    return df.nlargest(n, 'performance_rating')[['employee_id', 'job_role', 'department', 'performance_rating', 'salary']]

def identify_at_risk(df):
    """Identify at-risk employees (low performance + long tenure)"""
    at_risk = df[(df['performance_rating'] < 3) & (df['years_at_company'] > 3)]
    return at_risk[['employee_id', 'job_role', 'department', 'performance_rating', 'years_at_company']]
