"""Main analysis script for HR Analytics"""
import pandas as pd
from src.retention import attrition_by_department, performance_by_department, tenure_analysis, attrition_predictors
from src.performance import performance_distribution, salary_analysis, top_performers, identify_at_risk

def main():
    print("=" * 60)
    print("HR ANALYTICS & EMPLOYEE RETENTION ANALYSIS")
    print("=" * 60)
    
    # Load data
    df = pd.read_csv('data/employee_data.csv')
    
    # Overall metrics
    total_employees = len(df)
    attrition_count = df['attrition'].sum()
    attrition_rate = (attrition_count / total_employees * 100)
    
    print(f"\n📊 OVERALL METRICS:")
    print(f"  Total Employees: {total_employees}")
    print(f"  Employees Left: {attrition_count}")
    print(f"  Attrition Rate: {attrition_rate:.2f}%")
    print(f"  Average Salary: ${df['salary'].mean():,.2f}")
    print(f"  Average Performance: {df['performance_rating'].mean():.2f}/5.0")
    
    # Attrition by department
    print("\n👥 ATTRITION BY DEPARTMENT:")
    attrition_dept = attrition_by_department(df)
    attrition_dept['attrition_rate'] = (attrition_dept['left_company'] / attrition_dept['total_employees'] * 100).round(2)
    print(attrition_dept)
    
    # Performance by department
    print("\n📈 PERFORMANCE BY DEPARTMENT:")
    print(performance_by_department(df))
    
    # Tenure analysis
    print("\n📅 TENURE ANALYSIS:")
    print(tenure_analysis(df))
    
    # Top performers
    print("\n⭐ TOP PERFORMERS:")
    print(top_performers(df, n=5))
    
    # At-risk employees
    print("\n⚠️  AT-RISK EMPLOYEES:")
    at_risk = identify_at_risk(df)
    if len(at_risk) > 0:
        print(at_risk)
    else:
        print("  No at-risk employees identified")
    
    print("\n✅ Analysis complete!")

if __name__ == "__main__":
    main()
