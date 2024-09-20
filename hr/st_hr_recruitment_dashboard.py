import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from ui.style import create_styled_bar_chart, create_pie_chart, display_pie_chart, create_styled_tabs, create_styled_metric, create_styled_bullet_list, apply_styled_dropdown_css

# Dummy data (unchanged)
dummy_open_positions = pd.DataFrame([
    {"department": "Engineering", "count": 5, "date": "2024-09-01"},
    {"department": "Sales", "count": 3, "date": "2024-09-05"},
    {"department": "Marketing", "count": 2, "date": "2024-08-15"},
    {"department": "HR", "count": 1, "date": "2024-07-20"},
    {"department": "Finance", "count": 2, "date": "2024-08-30"},
])

dummy_time_to_fill = pd.DataFrame([
    {"position": "Software Engineer", "days": 45, "department": "Engineering", "date": "2024-09-10"},
    {"position": "Sales Manager", "days": 30, "department": "Sales", "date": "2024-08-25"},
    {"position": "Marketing Specialist", "days": 25, "department": "Marketing", "date": "2024-09-05"},
    {"position": "HR Coordinator", "days": 20, "department": "HR", "date": "2024-07-30"},
    {"position": "Financial Analyst", "days": 35, "department": "Finance", "date": "2024-08-15"},
])

dummy_candidate_pipeline = pd.DataFrame([
    {"stage": "Applied", "count": 200, "department": "Engineering", "date": "2024-09-15"},
    {"stage": "Screening", "count": 100, "department": "Sales", "date": "2024-09-12"},
    {"stage": "Interview", "count": 50, "department": "Marketing", "date": "2024-09-10"},
    {"stage": "Offer", "count": 10, "department": "HR", "date": "2024-09-08"},
    {"stage": "Hired", "count": 5, "department": "Finance", "date": "2024-09-05"},
])

dummy_source_effectiveness = pd.DataFrame([
    {"name": "Job Boards", "value": 40, "department": "Engineering", "date": "2024-09-01"},
    {"name": "Referrals", "value": 30, "department": "Sales", "date": "2024-08-20"},
    {"name": "Company Website", "value": 20, "department": "Marketing", "date": "2024-09-10"},
    {"name": "LinkedIn", "value": 10, "department": "HR", "date": "2024-07-15"},
])

# Convert date strings to datetime objects
for df in [dummy_open_positions, dummy_time_to_fill, dummy_candidate_pipeline, dummy_source_effectiveness]:
    df['date'] = pd.to_datetime(df['date'])

# New dummy data for upcoming interviews
today = datetime.now().date()
dummy_upcoming_interviews = pd.DataFrame([
    {"date": today, "time": "09:00 AM", "candidate": "John Doe", "position": "Software Engineer", "department": "Engineering"},
    {"date": today, "time": "11:30 AM", "candidate": "Jane Smith", "position": "Marketing Specialist", "department": "Marketing"},
    {"date": today, "time": "02:00 PM", "candidate": "Mike Johnson", "position": "Sales Manager", "department": "Sales"},
    {"date": today + timedelta(days=1), "time": "10:00 AM", "candidate": "Sarah Brown", "position": "HR Coordinator", "department": "HR"},
    {"date": today + timedelta(days=1), "time": "03:30 PM", "candidate": "Chris Lee", "position": "Software Engineer", "department": "Engineering"},
    {"date": today + timedelta(days=2), "time": "11:00 AM", "candidate": "Emily Chen", "position": "Data Analyst", "department": "Engineering"},
    {"date": today + timedelta(days=3), "time": "01:30 PM", "candidate": "David Wilson", "position": "Financial Analyst", "department": "Finance"},
])

# Convert date to datetime
dummy_upcoming_interviews['date'] = pd.to_datetime(dummy_upcoming_interviews['date'])

def filter_data(df, department, time_period):
    if department != "All Departments":
        df = df[df['department'] == department]
    
    end_date = pd.Timestamp.now()
    if time_period == "Last 30 days":
        start_date = end_date - pd.Timedelta(days=30)
    elif time_period == "Last 90 days":
        start_date = end_date - pd.Timedelta(days=90)
    elif time_period == "Last 6 months":
        start_date = end_date - pd.Timedelta(days=180)
    elif time_period == "Last year":
        start_date = end_date - pd.Timedelta(days=365)
    else:  # All time
        return df
    
    return df[(df['date'] >= start_date) & (df['date'] <= end_date)]

def hr_recruitment_dashboard():
    st.title("Recruitment Dashboard")
    apply_styled_dropdown_css()

    col1, col2 = st.columns(2)
    with col1:
        department_filter = st.selectbox(
            "Filter by:",
            ("All Departments", "Engineering", "Sales", "Marketing", "HR", "Finance")
        )
    with col2:
        time_filter = st.selectbox(
            "Time period:",
            ("Last 30 days", "Last 90 days", "Last 6 months", "Last year", "All time")
        )

    tabs = create_styled_tabs(["Overview", "Candidate Pipeline", "Upcoming Interviews"])

    with tabs[0]:
        col1, col2 = st.columns(2)

        filtered_open_positions = filter_data(dummy_open_positions, department_filter, time_filter)
        filtered_time_to_fill = filter_data(dummy_time_to_fill, department_filter, time_filter)

        with col1:
            create_styled_bar_chart(
                filtered_open_positions['department'].tolist(),
                filtered_open_positions['count'].tolist(),
                "Department",
                "Open Positions"
            )

        with col2:
            create_styled_bar_chart(
                filtered_time_to_fill['position'].tolist(),
                filtered_time_to_fill['days'].tolist(),
                "Position",
                "Days to Fill"
            )

        create_styled_metric("Average cost per hire", "$4,500", "💰")

    with tabs[1]:
        col1, col2 = st.columns(2)

        filtered_candidate_pipeline = filter_data(dummy_candidate_pipeline, department_filter, time_filter)
        filtered_source_effectiveness = filter_data(dummy_source_effectiveness, department_filter, time_filter)

        with col1:
            create_styled_bar_chart(
                filtered_candidate_pipeline['stage'].tolist(),
                filtered_candidate_pipeline['count'].tolist(),
                "Stage",
                "Number of Candidates"
            )

        with col2:
            fig_source_effectiveness = create_pie_chart(filtered_source_effectiveness, "name", "value", "Source Effectiveness")
            display_pie_chart(fig_source_effectiveness)

    with tabs[2]:
        st.subheader("Upcoming Interviews")

        filtered_interviews = dummy_upcoming_interviews[
            (dummy_upcoming_interviews['department'] == department_filter) | (department_filter == "All Departments")
        ]

        # Apply time filter to upcoming interviews
        filtered_interviews = filter_data(filtered_interviews, department_filter, time_filter)

        st.write(f"{len(filtered_interviews)} interviews scheduled")

        filtered_interviews['datetime'] = pd.to_datetime(filtered_interviews['date'].astype(str) + ' ' + filtered_interviews['time'])
        sorted_interviews = filtered_interviews.sort_values('datetime')

        st.table(sorted_interviews[['date', 'time', 'candidate', 'position', 'department']].style.format({'date': lambda x: x.strftime('%Y-%m-%d')}))

        if st.button("View Alert"):
            st.warning("2 positions have been open for more than 60 days. Consider revisiting the job requirements or expanding your search channels.")

        create_styled_bullet_list([
            "Review job descriptions for long-open positions",
            "Expand search to new job boards or platforms",
            "Consider internal candidates or employee referrals",
            "Evaluate compensation package competitiveness"
        ], "Action Items")

if __name__ == "__main__":
    hr_recruitment_dashboard()
