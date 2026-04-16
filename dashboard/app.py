"""👔 HR ANALYTICS - EMPLOYEE RETENTION DASHBOARD"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

st.set_page_config(page_title="HR Analytics", layout="wide")

C1, C2, C3, C4 = "#1a237e", "#00d9ff", "#ff5722", "#4caf50"

st.markdown(f"""<style>
.header {{background: linear-gradient(135deg, {C1} 0%, {C2} 100%); padding: 40px; border-radius: 15px; color: white; margin-bottom: 30px;}}
.risk-high {{background: #ffebee; border-left: 5px solid #d32f2f; padding: 15px; border-radius: 8px; margin: 8px 0;}}
.risk-medium {{background: #fff3e0; border-left: 5px solid #f57c00; padding: 15px; border-radius: 8px; margin: 8px 0;}}
.risk-low {{background: #e8f5e9; border-left: 5px solid #388e3c; padding: 15px; border-radius: 8px; margin: 8px 0;}}
.kpi-box {{background: linear-gradient(135deg, #0d47a1 0%, #1565c0 100%); padding: 30px; border-radius: 12px; color: white; text-align: center; margin: 10px 0;}}
</style>""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('data/employee_data.csv')
    df['risk_score'] = (
        (df['performance_rating'] <= 2.5) * 40 +
        (df['tenure_years'] <= 1) * 30 +
        (df['salary'] < df['salary'].median()) * 20 +
        (df['status'] == 'Exited') * 50
    )
    return df

df = load_data()
st.markdown(f'<div class="header"><h1>👥 HR Risk Assessment Dashboard</h1><p>Employee Retention Intelligence & Churn Prevention</p></div>', unsafe_allow_html=True)

# KPIs
total_emp = len(df)
at_risk = len(df[df['risk_score'] >= 60])
high_performers = len(df[(df['performance_rating'] >= 4) & (df['status'] == 'Active')])
churn_rate = len(df[df['status'] == 'Exited']) / total_emp * 100

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="kpi-box"><p>⚠️ AT-RISK EMPLOYEES</p><h2>{at_risk}</h2><p>{at_risk/total_emp*100:.1f}% of workforce</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="kpi-box"><p>⭐ RETENTION STARS</p><h2>{high_performers}</h2><p>{high_performers/total_emp*100:.1f}% of workforce</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="kpi-box"><p>📊 ATTRITION RATE</p><h2>{churn_rate:.1f}%</h2><p>{len(df[df["status"]=="Exited"])} employees exited</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="kpi-box"><p>📈 AVG TENURE</p><h2>{df["tenure_years"].mean():.1f} yrs</h2><p>Avg across company</p></div>', unsafe_allow_html=True)

st.divider()

# MAIN SECTION: EMPLOYEE RISK TABLE
st.subheader("🚨 EMPLOYEE RISK ASSESSMENT TABLE")
risk_df = df[['employee_id', 'job_title', 'department', 'salary', 'tenure_years', 'performance_rating', 'status', 'risk_score']].copy()
risk_df = risk_df.sort_values('risk_score', ascending=False)

# Display with color coding
st.dataframe(risk_df, use_container_width=True, hide_index=True)

st.divider()

# VISUALIZATIONS
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Risk Distribution by Department")
    dept_risk = df.groupby('department')['risk_score'].mean().sort_values(ascending=False)
    fig = px.bar(
        x=dept_risk.index,
        y=dept_risk.values,
        color=dept_risk.values,
        color_continuous_scale='Reds',
        labels={'y': 'Average Risk Score', 'x': 'Department'},
        title="Average Employee Risk by Department"
    )
    fig.update_layout(height=400, plot_bgcolor='rgba(0,0,0,.05)')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("💰 Tenure vs Salary (colored by Risk)")
    fig = px.scatter(
        df,
        x='tenure_years',
        y='salary',
        color='risk_score',
        size='performance_rating',
        hover_name='employee_id',
        color_continuous_scale='RdYlGn_r',
        labels={'tenure_years': 'Tenure (Years)', 'salary': 'Salary ($)', 'risk_score': 'Risk Score'},
        title="Tenure vs Salary Analysis"
    )
    fig.update_layout(height=400, plot_bgcolor='rgba(0,0,0,.05)')
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# HIGH RISK EMPLOYEES
st.subheader("⛔ HIGHEST RISK EMPLOYEES (Action Required)")
high_risk = df[df['risk_score'] >= 60].sort_values('risk_score', ascending=False).head(10)

for idx, row in high_risk.iterrows():
    if row['risk_score'] >= 80:
        risk_class = "risk-high"
        emoji = "🔴"
    elif row['risk_score'] >= 60:
        risk_class = "risk-medium"
        emoji = "🟠"
    else:
        risk_class = "risk-low"
        emoji = "🟡"
    
    st.markdown(f"""<div class="{risk_class}">
    <strong>{emoji} {row['employee_id']} | {row['job_title']} | {row['department']}</strong><br/>
    Risk Score: {row['risk_score']:.0f} | Tenure: {row['tenure_years']:.1f} yrs | Performance: {row['performance_rating']:.1f}/5 | Salary: ${row['salary']:,.0f}
    </div>""", unsafe_allow_html=True)

st.divider()
csv = risk_df.to_csv(index=False)
st.download_button("📥 Download Employee Risk Report", csv, "hr_risk_report.csv", "text/csv")
