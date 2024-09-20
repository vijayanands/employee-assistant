import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from ui.style import create_styled_metric, create_styled_tabs, create_pie_chart, display_pie_chart, create_multi_bar_chart, apply_styled_dropdown_css

# Full year of dummy data (same as before)
full_year_data = [
    {"month": "Jul", "voluntary": 2.1, "involuntary": 0.5, "actual": 95, "required": 100, "rate": 3.2},
    {"month": "Aug", "voluntary": 1.9, "involuntary": 0.6, "actual": 96, "required": 100, "rate": 3.3},
    {"month": "Sep", "voluntary": 2.0, "involuntary": 0.4, "actual": 97, "required": 100, "rate": 3.1},
    {"month": "Oct", "voluntary": 2.2, "involuntary": 0.5, "actual": 98, "required": 100, "rate": 3.0},
    {"month": "Nov", "voluntary": 1.8, "involuntary": 0.7, "actual": 99, "required": 100, "rate": 3.2},
    {"month": "Dec", "voluntary": 1.7, "involuntary": 0.6, "actual": 100, "required": 100, "rate": 3.4},
    {"month": "Jan", "voluntary": 2.1, "involuntary": 0.5, "actual": 95, "required": 100, "rate": 3.2},
    {"month": "Feb", "voluntary": 1.8, "involuntary": 0.7, "actual": 97, "required": 100, "rate": 3.5},
    {"month": "Mar", "voluntary": 2.3, "involuntary": 0.4, "actual": 98, "required": 100, "rate": 3.1},
    {"month": "Apr", "voluntary": 2.0, "involuntary": 0.6, "actual": 99, "required": 100, "rate": 2.9},
    {"month": "May", "voluntary": 1.9, "involuntary": 0.5, "actual": 101, "required": 100, "rate": 3.3},
    {"month": "Jun", "voluntary": 2.2, "involuntary": 0.3, "actual": 100, "required": 100, "rate": 3.0},
]

payroll_data = [
    {"category": "Base Salary", "value": 70, "description": "Regular wages paid to employees"},
    {"category": "Overtime", "value": 10, "description": "Additional pay for hours worked beyond regular schedule"},
    {"category": "Benefits", "value": 15, "description": "Health insurance, retirement plans, and other perks"},
    {"category": "Bonuses", "value": 5, "description": "Performance-based additional compensation"},
]

# Convert to DataFrame
df = pd.DataFrame(full_year_data)
payroll_df = pd.DataFrame(payroll_data)

def hr_overview_dashboard():
    st.title("HR Metrics Dashboard")

    # Apply styled dropdown CSS
    apply_styled_dropdown_css()

    # Time period selection
    time_period = st.selectbox(
        "Select time period",
        options=["Last Month", "Last 3 Months", "Last 6 Months", "Last Year"],
        index=2,
    )

    # Filter data based on time period
    if time_period == "Last Month":
        filtered_df = df.tail(1)
    elif time_period == "Last 3 Months":
        filtered_df = df.tail(3)
    elif time_period == "Last 6 Months":
        filtered_df = df.tail(6)
    else:
        filtered_df = df

    # Create styled tabs
    tab1, tab2, tab3, tab4 = create_styled_tabs(["Turnover Rates", "Staffing Levels", "Payroll Distribution", "Absenteeism Rates"])

    with tab1:
        st.subheader("Turnover Rates")
        fig = create_multi_bar_chart(
            filtered_df,
            x="month",
            y=["voluntary", "involuntary"],
            labels={"voluntary": "Voluntary Turnover", "involuntary": "Involuntary Turnover"},
            title="Turnover Rates Over Time"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.write("""
        This chart shows the voluntary and involuntary turnover rates over time. 
        - Voluntary turnover represents employees who choose to leave the company.
        - Involuntary turnover represents employees who are asked to leave the company.
        Higher rates may indicate issues with employee satisfaction or performance management.
        """)

    with tab2:
        st.subheader("Staffing Levels")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered_df['month'], y=filtered_df['actual'], mode='lines+markers', name='Actual Staffing'))
        fig.add_trace(go.Scatter(x=filtered_df['month'], y=filtered_df['required'], mode='lines+markers', name='Required Staffing'))
        fig.update_layout(xaxis_title="Month", yaxis_title="Staffing Level")
        st.plotly_chart(fig, use_container_width=True)

        st.write("""
        This chart compares actual staffing levels to required staffing levels over time.
        - Actual staffing represents the current number of employees.
        - Required staffing represents the target number of employees needed.
        Discrepancies between these two lines may indicate over- or under-staffing situations.
        """)

    with tab3:
        st.subheader("Payroll Distribution")
        fig = create_pie_chart(
            data=payroll_df,
            names="category",
            values="value",
            title="Payroll Distribution"
        )
        display_pie_chart(fig)

        st.subheader("Payroll Distribution Details")
        for _, row in payroll_df.iterrows():
            create_styled_metric(row['category'], f"{row['value']}%", "💰")
            st.write(row['description'])

        st.write("""
        The payroll distribution chart shows how the company's total payroll is allocated across different categories. 
        This breakdown helps in understanding the composition of employee compensation and can be useful for budgeting 
        and identifying areas where costs might be optimized.
        
        - **Base Salary** forms the largest portion, which is typical for most organizations.
        - **Benefits** are the second largest category, highlighting the company's investment in employee well-being.
        - **Overtime** costs may indicate high workload or potential understaffing in some areas.
        - **Bonuses** represent performance-based pay, which can be a tool for motivation and retention.
        
        Monitoring these distributions over time can reveal trends in compensation strategy and operational efficiency.
        """)

    with tab4:
        st.subheader("Absenteeism Rates")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered_df['month'], y=filtered_df['rate'], mode='lines+markers', name='Absenteeism Rate'))
        fig.update_layout(xaxis_title="Month", yaxis_title="Absenteeism Rate (%)")
        st.plotly_chart(fig, use_container_width=True)

        st.write("""
        This chart shows the percentage of employees absent from work each month. 
        The absenteeism rate is calculated as: (Number of absent days) / (Number of available workdays) x 100.
        A lower rate indicates better attendance. High absenteeism rates may signal issues with employee engagement, 
        health and safety concerns, or work-life balance problems that need to be addressed.
        """)

if __name__ == "__main__":
    hr_overview_dashboard()
