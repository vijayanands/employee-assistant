import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from ui.style import (apply_styled_dropdown_css, create_styled_metric,
                      create_styled_tabs)


# Create more comprehensive dummy data
def create_dummy_data():
    departments = ["Sales", "Marketing", "Engineering", "HR", "Finance"]
    time_periods = [
        "Last 30 days",
        "Last 90 days",
        "Last 6 months",
        "Last year",
        "All time",
    ]

    data = []
    for dept in departments:
        for period in time_periods:
            completion_rate = np.random.randint(60, 100)
            data.append(
                {
                    "department": dept,
                    "time_period": period,
                    "completionRate": completion_rate,
                }
            )

    return pd.DataFrame(data)


training_completion_data = create_dummy_data()

skills_inventory_data = pd.DataFrame(
    [
        {"skill": "Project Management", "availability": 75},
        {"skill": "Data Analysis", "availability": 60},
        {"skill": "Leadership", "availability": 55},
        {"skill": "Communication", "availability": 80},
        {"skill": "Technical Writing", "availability": 45},
    ]
)


def create_plotly_bar_chart(data, x_column, y_column, x_label, y_label):
    fig = go.Figure(
        data=[
            go.Bar(x=data[x_column], y=data[y_column], marker_color="rgb(55, 83, 109)")
        ]
    )
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        font=dict(
            family="Helvetica, Arial, sans-serif", size=14, color="rgb(55, 83, 109)"
        ),
    )
    return fig


def hr_training_dashboard():
    st.title("Training & Development Dashboard")

    # Apply styled dropdown CSS
    apply_styled_dropdown_css()

    # Filter dropdowns
    col1, col2 = st.columns(2)
    with col1:
        filter_option = st.selectbox(
            "Filter by:",
            ("All Departments", "Sales", "Marketing", "Engineering", "HR", "Finance"),
        )
    with col2:
        duration_option = st.selectbox(
            "Time period:",
            ("Last 30 days", "Last 90 days", "Last 6 months", "Last year", "All time"),
        )

    # Filter data based on user selection
    filtered_data = training_completion_data[
        training_completion_data["time_period"] == duration_option
    ]
    if filter_option != "All Departments":
        filtered_data = filtered_data[filtered_data["department"] == filter_option]

    # Calculate average completion rate for the filtered data
    avg_completion_rate = filtered_data["completionRate"].mean()

    # Create tabs
    tabs = create_styled_tabs(["Overview", "Training Completion", "Skills Inventory"])

    with tabs[0]:
        col1, col2 = st.columns(2)

        with col1:
            create_styled_metric(
                "Average Learning Hours per Employee", "24.5 hours", "📚"
            )

        with col2:
            create_styled_metric(
                "Training Effectiveness", f"{avg_completion_rate:.1f}%", "📈"
            )

        st.markdown(
            f"""
        <p>Training Effectiveness measures the impact of our training programs on employee performance and knowledge retention. 
        The score of {avg_completion_rate:.1f}% indicates the level of success in achieving learning objectives and applying new skills in the workplace.</p>
        """,
            unsafe_allow_html=True,
        )

    with tabs[1]:
        st.header("Training Completion Rates by Department")

        if filter_option == "All Departments":
            chart_data = (
                filtered_data.groupby("department")["completionRate"]
                .mean()
                .reset_index()
            )
        else:
            chart_data = filtered_data

        fig_completion = create_plotly_bar_chart(
            chart_data,
            "department",
            "completionRate",
            "Department",
            "Completion Rate (%)",
        )
        st.plotly_chart(fig_completion)

    with tabs[2]:
        st.header("Skills Inventory")

        # Color coding based on availability
        def get_skill_color(availability):
            if availability >= 75:
                return "#4CAF50"  # Green for high availability
            elif availability >= 50:
                return "#FFA500"  # Orange for medium availability
            else:
                return "#FF6347"  # Red for low availability

        for _, skill in skills_inventory_data.iterrows():
            col1, col2, col3 = st.columns([1, 3, 1])
            with col1:
                st.write(skill["skill"])
            with col2:
                color = get_skill_color(skill["availability"])
                st.markdown(
                    f'<div style="width: 100%; background-color: #e0e0e0; padding: 3px; border-radius: 3px;">'
                    f'<div style="width: {skill["availability"]}%; height: 24px; border-radius: 2px; background-color: {color};"></div>'
                    f"</div>",
                    unsafe_allow_html=True,
                )
            with col3:
                st.write(f"{skill['availability']}%")


if __name__ == "__main__":
    hr_training_dashboard()
