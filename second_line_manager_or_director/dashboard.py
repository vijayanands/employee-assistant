import streamlit as st

from second_line_manager_or_director.org_productivity_dashboard import \
    org_productivity_dashboard
from second_line_manager_or_director.org_engagement_and_compliance_dashboard import \
    director_engagement_compliance_dashboard
from second_line_manager_or_director.org_project_and_portfolio_dashboard import \
    director_project_portfolio_dashboard
from second_line_manager_or_director.org_executive_summary import \
    director_executive_summary_dashboard
from second_line_manager_or_director.org_performance_dashboard import \
    director_performance_dashboard


def show_director_dashboard(nav_option):
    if nav_option == "Executive Summary":
        director_executive_summary_dashboard()
    elif nav_option == "Productivity":
        org_productivity_dashboard()
    elif nav_option == "Performance":
        director_performance_dashboard()
    elif nav_option == "Projects and Portfolio":
        director_project_portfolio_dashboard()
    elif nav_option == "Learning & Skills":
        st.write("Dashboard for Learning is not implemented yet.")
    elif nav_option == "Engagement & Compliance":
        director_engagement_compliance_dashboard()
    else:
        st.write(f"Dashboard for {nav_option} is not implemented yet.")
