import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from ui.style import create_styled_metric, create_styled_bar_chart, apply_styled_dropdown_css


def set_page_style():
    # Custom CSS to improve the look
    st.markdown("""
    <style>
    .main > div {
        padding-top: 2rem;
    }
    .plot-container {
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-radius: 5px;
        padding: 1rem;
        background-color: white;
    }
    .dataframe {
        font-size: 0.8rem;
    }
    .stAlert {
        border-radius: 5px;
    }
    h1 {
        color: #1E3A8A;
        padding-bottom: 1rem;
        border-bottom: 2px solid #E5E7EB;
    }
    h3 {
        color: #1E3A8A;
        margin-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

def generate_dummy_data(num_teams, duration):
    teams = [f"Team {i}" for i in range(1, num_teams + 1)]
    dates = pd.date_range(end=datetime.now(), periods=duration, freq='D')
    
    data = []
    for team in teams:
        for date in dates:
            data.append({
                'Team': team,
                'Date': date,
                'Task Completion Rate': np.random.uniform(0.6, 1),
                'Communication Efficiency Rate': np.random.uniform(0.7, 1),
                'Knowledge Contributions': np.random.randint(0, 10),
                'Meeting Effectiveness': np.random.uniform(0.5, 1),
                'Average Meeting Duration': np.random.uniform(30, 120),
                'Percentage Time in Meetings': np.random.uniform(0.1, 0.4),
                'Action Items per Meeting': np.random.uniform(1, 5),
                'Resolutions per Meeting': np.random.uniform(0.5, 3)
            })
    
    return pd.DataFrame(data)

def manager_productivity_dashboard():
    set_page_style()
    apply_styled_dropdown_css()
    st.title("Team Productivity Dashboard")

    # Dummy data
    df = generate_dummy_data(num_teams=5, duration=365)

    # Filters in the main window
    col1, col2 = st.columns(2)
    with col1:
        duration = st.selectbox("Select Duration", ["Month", "Quarter", "Half Year", "Year"])
    with col2:
        team = st.selectbox("Select Team", ["All Teams"] + df['Team'].unique().tolist())

    # Filter data based on selection
    end_date = df['Date'].max()
    if duration == "Month":
        start_date = end_date - timedelta(days=30)
    elif duration == "Quarter":
        start_date = end_date - timedelta(days=90)
    elif duration == "Half Year":
        start_date = end_date - timedelta(days=180)
    else:
        start_date = end_date - timedelta(days=365)

    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    if team != "All Teams":
        filtered_df = filtered_df[filtered_df['Team'] == team]

    # Aggregate data
    agg_df = filtered_df.groupby('Team').agg({
        'Task Completion Rate': 'mean',
        'Communication Efficiency Rate': 'mean',
        'Knowledge Contributions': 'sum',
        'Meeting Effectiveness': 'mean',
        'Average Meeting Duration': 'mean',
        'Percentage Time in Meetings': 'mean',
        'Action Items per Meeting': 'mean',
        'Resolutions per Meeting': 'mean'
    }).reset_index()

    # Create visualizations
    st.subheader("Team Performance Metrics")

    create_styled_bar_chart(
        agg_df['Team'],
        agg_df['Task Completion Rate'],
        "Team",
        "Completion Rate",
        # "Team Level Task Completion Rate"
    )

    create_styled_bar_chart(
        agg_df['Team'],
        agg_df['Communication Efficiency Rate'],
        "Team",
        "Efficiency Rate",
        # "Team Level Communication Efficiency Rate"
    )

    create_styled_bar_chart(
        agg_df['Team'],
        agg_df['Knowledge Contributions'],
        "Team",
        "Number of Contributions",
        # "Team Level Knowledge Contributions"
    )

    # Split tables
    st.subheader("Meeting Productivity Analysis Table")
    meeting_df = agg_df[['Team', 'Meeting Effectiveness', 'Average Meeting Duration', 'Percentage Time in Meetings', 'Action Items per Meeting', 'Resolutions per Meeting']]
    st.dataframe(meeting_df.set_index('Team').style.format({
        'Meeting Effectiveness': '{:.2%}',
        'Average Meeting Duration': '{:.0f} min',
        'Percentage Time in Meetings': '{:.2%}',
        'Action Items per Meeting': '{:.1f}',
        'Resolutions per Meeting': '{:.1f}'
    }), height=220)

    st.subheader("Other Productivity Metrics Table")
    other_df = agg_df[['Team', 'Task Completion Rate', 'Communication Efficiency Rate', 'Knowledge Contributions']]
    st.dataframe(other_df.set_index('Team').style.format({
        'Task Completion Rate': '{:.2%}',
        'Communication Efficiency Rate': '{:.2%}',
        'Knowledge Contributions': '{:.0f}'
    }), height=220)

    # Attention Required section
    st.subheader("Attention Required")
    attention_required = False
    for _, row in agg_df.iterrows():
        if row['Task Completion Rate'] < 0.7:
            create_styled_metric(
                f"{row['Team']} Task Completion",
                f"{row['Task Completion Rate']:.2%}",
                "⚠️"
            )
            st.warning(f"{row['Team']}'s task completion rate is below 70%. Consider scheduling a review to address any blockers.")
            attention_required = True
        if row['Communication Efficiency Rate'] < 0.75:
            create_styled_metric(
                f"{row['Team']} Communication Efficiency",
                f"{row['Communication Efficiency Rate']:.2%}",
                "⚠️"
            )
            st.warning(f"{row['Team']}'s communication efficiency rate is below 75% ({row['Communication Efficiency Rate']:.2%}). Consider implementing team communication improvement strategies.")
            attention_required = True
        if row['Knowledge Contributions'] < 10:
            create_styled_metric(
                f"{row['Team']} Knowledge Contributions",
                f"{row['Knowledge Contributions']:.2%}",
                "ℹ️"
            )
            st.info(f"{row['Team']} has made fewer than 10 knowledge contributions ({row['Knowledge Contributions']}). Encourage more knowledge sharing within the team.")
            attention_required = True
    
    if not attention_required:
        create_styled_metric("Team Performance", "All Good", "🎉")
        st.success("All teams are performing well. No immediate attention required.")

if __name__ == "__main__":
    manager_productivity_dashboard()
