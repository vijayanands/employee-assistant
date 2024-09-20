import streamlit as st

from first_line_manager.st_1st_line_engagement_compliance import manager_engagement_and_compliance_dashboard
from first_line_manager.st_mgr1_performance_metrics import manager_performance_dashboard
from first_line_manager.st_mgr_dashboard import manager_overview_dashboard
from first_line_manager.combined_productivity_dashboard import productivity_dashboard


def show_first_line_manager_dashboard(nav_option):
    if nav_option == "Overview":
        manager_overview_dashboard()
    elif nav_option == "Productivity":
        productivity_dashboard()
    elif nav_option == "Performance & Career":
        manager_performance_dashboard()
    elif nav_option == "Learning & Skills":
        st.write("Dashboard for Learning is not implemented yet.")
    elif nav_option == "Engagement & Compliance":
        manager_engagement_and_compliance_dashboard()
    else:
        st.write(f"Dashboard for {nav_option} is not implemented yet.")