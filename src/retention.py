"""Employee retention analysis"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

def attrition_by_department(df):
    """Calculate attrition rate by department"""
    return df.groupby('department').agg({
        'employee_id': 'count',
        'attrition': 'sum'
    }).rename(columns={'employee_id': 'total_employees', 'attrition': 'left_company'})

def performance_by_department(df):
    """Analyze performance by department"""
    return df.groupby('department').agg({
        'performance_rating': 'mean',
        'salary': 'mean',
        'years_at_company': 'mean'
    }).round(2)

def tenure_analysis(df):
    """Analyze tenure patterns"""
    df['tenure_bucket'] = pd.cut(df['years_at_company'], 
                                bins=[0, 1, 3, 5, 10, 30],
                                labels=['<1yr', '1-3yr', '3-5yr', '5-10yr', '10+yr'])
    return df.groupby('tenure_bucket')['attrition'].agg(['count', 'sum', 'mean'])

def attrition_predictors(df):
    """Identify key predictors of attrition"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    correlations = df[numeric_cols].corrwith(df['attrition']).sort_values(ascending=False)
    return correlations.abs().head(10)
