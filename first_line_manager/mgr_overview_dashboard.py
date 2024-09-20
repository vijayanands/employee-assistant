from datetime import datetime

import pandas as pd
import streamlit as st

from ui.style import (create_multi_bar_chart, create_pie_chart,
                      create_styled_bar_chart, create_styled_metric,
                      create_styled_tabs)


def manager_overview_dashboard():
    # Set page config
    st.title("Management Dashboard")

    # Dummy data
    resource_allocation_data = pd.DataFrame(
        [
            {"name": "Project X", "allocation": 80},
            {"name": "Project Y", "allocation": 20},
        ]
    )

    compensation_data = pd.DataFrame(
        [
            {"name": "Salaries", "current": 850000, "budgeted": 900000},
            {"name": "Bonuses", "current": 50000, "budgeted": 100000},
        ]
    )

    upcoming_learning_opportunities = pd.DataFrame(
        [
            {"name": "AI Conference", "date": "2024-10-15"},
            {"name": "Leadership Workshop", "date": "2024-11-01"},
            {"name": "Advanced React Course", "date": "2024-11-15"},
        ]
    )

    employee_recognitions = pd.DataFrame(
        [
            {"name": "Alice Johnson", "award": "Employee of the Month"},
            {"name": "Bob Smith", "award": "Innovation Award"},
        ]
    )

    # Quick Stats
    st.subheader("Quick Stats")
    col_stats1, col_stats2, col_stats3 = st.columns(3)
    with col_stats1:
        create_styled_metric("Total Projects", "2", "📊")
    with col_stats2:
        create_styled_metric("Team Members", "10", "👥")
    with col_stats3:
        create_styled_metric("Budget Utilization", "95%", "💰")

    # Main content
    tab1, tab2, tab3, tab4 = create_styled_tabs(
        [
            "Resource & Compensation",
            "Employee Development",
            "Feedback & Recognition",
            "Upcoming Check-ins",
        ]
    )

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Resource Allocation")
            fig = create_pie_chart(
                resource_allocation_data,
                names="name",
                values="allocation",
                title="Resource Allocation",
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Compensation Review")
            fig = create_multi_bar_chart(
                compensation_data,
                x="name",
                y=["current", "budgeted"],
                labels={"current": "Current", "budgeted": "Budgeted"},
                title="Compensation Comparison",
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Employee Development")
        st.write("Upcoming Learning Opportunities")
        for _, opportunity in upcoming_learning_opportunities.iterrows():
            st.info(f"📚 {opportunity['name']} - {opportunity['date']}")

        if st.button("Add New Learning Opportunity"):
            st.write("Form to add new learning opportunity would appear here.")

    with tab3:
        st.subheader("Feedback and Recognition")
        st.write("Recent Recognitions")
        for _, recognition in employee_recognitions.iterrows():
            st.success(f"🏆 {recognition['name']} - {recognition['award']}")

        if st.button("Give Recognition"):
            st.write("Form to give new recognition would appear here.")

    with tab4:
        st.subheader("Upcoming Check-ins")
        col_date, col_checkins = st.columns([1, 2])

        with col_date:
            selected_date = st.date_input("Select Date", datetime.now())

        with col_checkins:
            st.write("Scheduled for", selected_date.strftime("%B %d, %Y"))
            st.info("👥 Team Meeting - 10:00 AM")
            st.info("👤 1-on-1 with Alice - 2:00 PM")

        if st.button("Schedule New Check-in"):
            st.write("Form to schedule new check-in would appear here.")

    # Footer
    st.write("---")
    col_refresh, col_export = st.columns(2)
    with col_refresh:
        if st.button("Refresh Data"):
            st.write("Data refreshed!")
    with col_export:
        if st.button("Export Report"):
            st.write("Report exported!")


if __name__ == "__main__":
    manager_overview_dashboard()
