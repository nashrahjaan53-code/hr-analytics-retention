import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.retention import attrition_by_department, performance_by_department, tenure_analysis
from src.performance import performance_distribution, salary_analysis, top_performers, identify_at_risk

st.set_page_config(page_title="HR Analytics", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .header {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data
df = pd.read_csv('data/employee_data.csv')

if df is not None and len(df) > 0:
    st.markdown('<div class="header"><h1>👥 HR Analytics & Employee Retention Dashboard</h1></div>', 
                unsafe_allow_html=True)
    
    # Calculate metrics
    total_employees = len(df)
    attrition_count = df['attrition'].sum()
    attrition_rate = (attrition_count / total_employees * 100)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Employees", total_employees)
    with col2:
        st.metric("Attrition Rate", f"{attrition_rate:.1f}%", delta=f"{int(attrition_count)} left")
    with col3:
        st.metric("Avg Salary", f"${df['salary'].mean():,.0f}")
    with col4:
        st.metric("Avg Performance", f"{df['performance_rating'].mean():.2f}/5.0")
    
    st.divider()
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "👨‍💼 Performance", "🚪 Attrition", "💰 Compensation", "⚠️ At-Risk"])
    
    # TAB 1: OVERVIEW
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Employee Distribution by Department (Pie)")
            dept_dist = df['department'].value_counts()
            fig_dept = px.pie(values=dept_dist.values, names=dept_dist.index,
                            title="Employee Count by Department",
                            color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig_dept, use_container_width=True)
        
        with col2:
            st.subheader("Employee Distribution by Role (Pie)")
            role_dist = df['job_role'].value_counts()
            fig_role = px.pie(values=role_dist.values, names=role_dist.index,
                            title="Employee Count by Job Role")
            st.plotly_chart(fig_role, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Tenure Distribution (Histogram)")
            fig_tenure = px.histogram(df, x='years_at_company', nbins=8,
                                    title="Tenure Distribution",
                                    labels={'years_at_company': 'Years at Company'},
                                    color_discrete_sequence=['#fa709a'])
            st.plotly_chart(fig_tenure, use_container_width=True)
        
        with col2:
            st.subheader("Performance Rating Distribution (Histogram)")
            fig_perf_dist = px.histogram(df, x='performance_rating', nbins=5,
                                        title="Performance Rating Distribution",
                                        color_discrete_sequence=['#fee140'])
            st.plotly_chart(fig_perf_dist, use_container_width=True)
    
    # TAB 2: PERFORMANCE
    with tab2:
        perf_dept = performance_by_department(df)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Avg Performance by Department (Bar)")
            fig_perf_dept = px.bar(x=perf_dept.index, y=perf_dept['performance_rating'],
                                  title="Average Performance Rating by Department",
                                  labels={'performance_rating': 'Avg Rating'},
                                  color=perf_dept['performance_rating'],
                                  color_continuous_scale='RdYlGn')
            st.plotly_chart(fig_perf_dept, use_container_width=True)
        
        with col2:
            st.subheader("Top Performers (Bar)")
            top_perf = top_performers(df, n=5)
            fig_top = px.bar(data_frame=top_perf, x='employee_id', y='performance_rating',
                           title="Top 5 Performers",
                           labels={'performance_rating': 'Rating'},
                           color='performance_rating',
                           color_continuous_scale='Greens')
            st.plotly_chart(fig_top, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Performance vs Tenure (Scatter)")
            fig_perf_tenure = px.scatter(df, x='years_at_company', y='performance_rating',
                                        color='department', size='salary',
                                        title="Performance Rating vs Years at Company",
                                        hover_name='employee_id')
            st.plotly_chart(fig_perf_tenure, use_container_width=True)
        
        with col2:
            st.subheader("Top Performers Table")
            st.dataframe(top_perf, use_container_width=True, hide_index=True)
    
    # TAB 3: ATTRITION
    with tab3:
        attrition_dept = attrition_by_department(df)
        attrition_dept['attrition_rate'] = (attrition_dept['left_company'] / attrition_dept['total_employees'] * 100).round(1)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Attrition Rate by Department (Bar)")
            fig_attr_rate = px.bar(x=attrition_dept.index, y=attrition_dept['attrition_rate'],
                                  title="Attrition Rate % by Department",
                                  labels={'attrition_rate': 'Attrition Rate (%)'},
                                  color=attrition_dept['attrition_rate'],
                                  color_continuous_scale='Reds')
            st.plotly_chart(fig_attr_rate, use_container_width=True)
        
        with col2:
            st.subheader("Left vs Stayed by Department")
            dept_status = pd.crosstab(df['department'], df['attrition'])
            fig_status = px.bar(dept_status, barmode='group',
                              title="Employee Status by Department",
                              labels={0: 'Active', 1: 'Left'},
                              color_discrete_map={0: '#2ecc71', 1: '#e74c3c'})
            st.plotly_chart(fig_status, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Tenure vs Attrition Risk (Heatmap)")
            df_copy = df.copy()
            df_copy['tenure_bucket'] = pd.cut(df_copy['years_at_company'], 
                                             bins=[0, 1, 3, 5, 10, 30],
                                             labels=['<1yr', '1-3yr', '3-5yr', '5-10yr', '10+yr'])
            tenure_attr = pd.crosstab(df_copy['tenure_bucket'], df_copy['attrition'])
            fig_tenure_heat = px.imshow(tenure_attr.T, labels=dict(x="Tenure", y="Status"),
                                       title="Attrition Heatmap by Tenure",
                                       color_continuous_scale='RdYlGn_r')
            st.plotly_chart(fig_tenure_heat, use_container_width=True)
        
        with col2:
            st.subheader("Attrition Summary Table")
            st.dataframe(attrition_dept, use_container_width=True, hide_index=True)
    
    # TAB 4: COMPENSATION
    with tab4:
        st.subheader("Salary Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Average Salary by Department (Bar)")
            dept_salary = df.groupby('department')['salary'].mean().sort_values(ascending=False)
            fig_dept_sal = px.bar(x=dept_salary.index, y=dept_salary.values,
                                 title="Average Salary by Department",
                                 labels={'y': 'Avg Salary ($)'},
                                 color=dept_salary.values,
                                 color_continuous_scale='Blues')
            st.plotly_chart(fig_dept_sal, use_container_width=True)
        
        with col2:
            st.subheader("Salary Distribution Box Plot")
            fig_salary_box = px.box(df, x='department', y='salary',
                                   color='department',
                                   title="Salary Distribution by Department")
            st.plotly_chart(fig_salary_box, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Salary vs Performance (Scatter)")
            fig_sal_perf = px.scatter(df, x='performance_rating', y='salary',
                                     color='department', size='years_at_company',
                                     title="Salary vs Performance Rating",
                                     hover_name='employee_id')
            st.plotly_chart(fig_sal_perf, use_container_width=True)
        
        with col2:
            st.subheader("Avg Salary by Job Role (Bar)")
            role_salary = df.groupby('job_role')['salary'].mean().sort_values(ascending=False)
            fig_role_sal = px.bar(x=role_salary.index, y=role_salary.values,
                                 title="Average Salary by Job Role",
                                 labels={'y': 'Avg Salary ($)'},
                                 color=role_salary.values,
                                 color_continuous_scale='Viridis')
            st.plotly_chart(fig_role_sal, use_container_width=True)
    
    # TAB 5: AT-RISK EMPLOYEES
    with tab5:
        st.subheader("⚠️ At-Risk Employee Analysis")
        
        at_risk = identify_at_risk(df)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(f"At-Risk Employees: {len(at_risk)}")
            if len(at_risk) > 0:
                fig_at_risk = px.scatter(at_risk.reset_index(), x='years_at_company', 
                                        y='performance_rating',
                                        color='department', size='employee_id',
                                        title="At-Risk Employee Profile",
                                        hover_name='employee_id')
                st.plotly_chart(fig_at_risk, use_container_width=True)
            else:
                st.success("✅ No at-risk employees detected!")
        
        with col2:
            st.subheader("Performance vs Tenure (All Employees)")
            fig_all = px.scatter(df, x='years_at_company', y='performance_rating',
                               color='attrition', size='salary',
                               title="All Employees: High Risk Areas",
                               hover_name='employee_id',
                               color_discrete_map={0: '#2ecc71', 1: '#e74c3c'})
            st.plotly_chart(fig_all, use_container_width=True)
        
        if len(at_risk) > 0:
            st.subheader("At-Risk Employees List")
            st.dataframe(at_risk, use_container_width=True, hide_index=True)
        
        csv = at_risk.to_csv(index=False) if len(at_risk) > 0 else ""
        if len(at_risk) > 0:
            st.download_button(
                label="📥 Download At-Risk Report",
                data=csv,
                file_name="at_risk_employees.csv",
                mime="text/csv"
            )
else:
    st.error("Unable to load data.")
