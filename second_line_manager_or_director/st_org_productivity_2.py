import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
from ui.style import (
    create_styled_metric, create_styled_bullet_list, create_styled_tabs,
    create_pie_chart, display_pie_chart,
    apply_styled_dropdown_css, create_styled_bar_chart
)

# Generate dummy data
def generate_dummy_data():
    # Productivity data
    productivity_data = pd.DataFrame([
        {"department": "Engineering", "productivity": 85},
        {"department": "Marketing", "productivity": 78},
        {"department": "Sales", "productivity": 92},
        {"department": "Customer Support", "productivity": 88},
        {"department": "HR", "productivity": 76},
    ])

    # Projects data
    projects_data = pd.DataFrame([
        {"id": 1, "name": "Website Redesign", "completion": 75, "status": "on-track", "risk": "low"},
        {"id": 2, "name": "Mobile App Development", "completion": 40, "status": "delayed", "risk": "medium"},
        {"id": 3, "name": "CRM Integration", "completion": 90, "status": "on-track", "risk": "low"},
        {"id": 4, "name": "Data Migration", "completion": 60, "status": "on-track", "risk": "high"},
        {"id": 5, "name": "Security Audit", "completion": 30, "status": "delayed", "risk": "medium"},
    ])

    # Generate time series data for productivity trends
    departments = productivity_data['department'].tolist()
    date_range = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    productivity_trends = pd.DataFrame(index=date_range)

    for dept in departments:
        base_productivity = productivity_data[productivity_data['department'] == dept]['productivity'].values[0]
        trend = [base_productivity + random.uniform(-5, 5) for _ in range(len(date_range))]
        productivity_trends[dept] = trend

    return productivity_data, projects_data, productivity_trends

def director_productivity_dashboard():
    st.title("Productivity & Projects Dashboard")
    apply_styled_dropdown_css()

    # Generate dummy data
    productivity_data, projects_data, productivity_trends = generate_dummy_data()

    # Use styled tabs
    tabs = create_styled_tabs(["Overview", "Project Status", "Productivity Trends", "Risk Assessment"])

    with tabs[0]:
        overview_tab(productivity_data, projects_data)

    with tabs[1]:
        project_status_tab(projects_data)

    with tabs[2]:
        productivity_trends_tab(productivity_trends)

    with tabs[3]:
        risk_assessment_tab(projects_data)

def overview_tab(productivity_data, projects_data):
    st.header("Productivity Overview")

    # Key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        create_styled_metric("Total Projects", len(projects_data), "📊")
    with col2:
        on_track_count = len(projects_data[projects_data['status'] == 'on-track'])
        on_track_percentage = (on_track_count / len(projects_data)) * 100
        create_styled_metric("On-Track Projects", f"{on_track_count} ({on_track_percentage:.0f}%)", "✅")
    with col3:
        avg_completion = projects_data['completion'].mean()
        create_styled_metric("Average Completion", f"{avg_completion:.1f}%", "🏁")

    # Productivity heatmap
    st.subheader("Departmental Productivity")
    fig = px.imshow(
        [productivity_data['productivity']], 
        x=productivity_data['department'], 
        y=['Productivity Score'], 
        color_continuous_scale='RdYlGn',
        text_auto=True,
        aspect="auto",
        title="Team Productivity Heatmap"
    )
    fig.update_layout(height=200)
    st.plotly_chart(fig, use_container_width=True)

    # Department productivity bar chart
    create_styled_bar_chart(
        productivity_data['department'],
        productivity_data['productivity'],
        "Department",
        "Productivity Score"
    )

def project_status_tab(projects_data):
    st.header("Project Status")

    # Project selection
    selected_project = st.selectbox("Select a project", projects_data['name'])
    project = projects_data[projects_data['name'] == selected_project].iloc[0]

    # Project details
    col1, col2 = st.columns(2)
    with col1:
        status_color = "green" if project['status'] == 'on-track' else "orange"
        st.markdown(f"**Status:** <span style='color:{status_color};'>●</span> {project['status'].capitalize()}", unsafe_allow_html=True)
        
        risk_color = {"low": "green", "medium": "orange", "high": "red"}[project['risk']]
        st.markdown(f"**Risk:** <span style='color:{risk_color};'>●</span> {project['risk'].capitalize()}", unsafe_allow_html=True)

    with col2:
        st.metric("Completion", f"{project['completion']}%")
        st.progress(project['completion'] / 100)

    # All projects overview
    st.subheader("All Projects Overview")
    fig = go.Figure()
    for _, proj in projects_data.iterrows():
        fig.add_trace(go.Bar(
            x=[proj['name']],
            y=[proj['completion']],
            name=proj['name'],
            marker_color='green' if proj['status'] == 'on-track' else 'orange'
        ))
    fig.update_layout(
        title="Project Completion Status",
        xaxis_title="Project",
        yaxis_title="Completion (%)",
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

def productivity_trends_tab(productivity_trends):
    st.header("Productivity Trends")

    # Department selection
    departments = productivity_trends.columns.tolist()
    selected_dept = st.selectbox("Select Department", departments)

    # Date range selection
    date_range = st.date_input(
        "Select Date Range",
        value=(productivity_trends.index.min(), productivity_trends.index.max()),
        min_value=productivity_trends.index.min(),
        max_value=productivity_trends.index.max()
    )

    # Filter data based on selection
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered_data = productivity_trends.loc[start_date:end_date, selected_dept]

    # Create line chart
    fig = px.line(
        filtered_data,
        x=filtered_data.index,
        y=filtered_data.values,
        title=f"{selected_dept} Productivity Trend"
    )
    fig.update_layout(xaxis_title="Date", yaxis_title="Productivity Score")
    st.plotly_chart(fig, use_container_width=True)

    # Calculate and display metrics
    avg_productivity = filtered_data.mean()
    max_productivity = filtered_data.max()
    min_productivity = filtered_data.min()

    col1, col2, col3 = st.columns(3)
    with col1:
        create_styled_metric("Average Productivity", f"{avg_productivity:.2f}", "📊")
    with col2:
        create_styled_metric("Max Productivity", f"{max_productivity:.2f}", "🔼")
    with col3:
        create_styled_metric("Min Productivity", f"{min_productivity:.2f}", "🔽")

def risk_assessment_tab(projects_data):
    st.header("Risk Assessment")

    # Count projects by risk level
    risk_counts = projects_data['risk'].value_counts()

    # Create pie chart
    fig = create_pie_chart(
        risk_counts,
        names=risk_counts.index,
        values=risk_counts.values,
        title="Project Risk Distribution",
        color_sequence=['green', 'orange', 'red']
    )
    display_pie_chart(fig)

    # List high-risk projects
    high_risk_projects = projects_data[projects_data['risk'] == 'high']
    if not high_risk_projects.empty:
        st.subheader("High Risk Projects")
        for project in high_risk_projects['name'].tolist():
            st.write(f". {project}")
    else:
        st.info("No high-risk projects at the moment.")

    # Risk mitigation strategies
    st.subheader("Risk Mitigation Strategies")
    strategies = [
        "Conduct regular risk assessment meetings",
        "Implement robust testing procedures",
        "Maintain open communication channels with stakeholders",
        "Develop contingency plans for high-risk areas",
        "Provide additional resources to high-risk projects"
    ]
    for strategy in strategies:
        st.write(f"• {strategy}")
if __name__ == "__main__":
    director_productivity_dashboard()
