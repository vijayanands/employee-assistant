import streamlit as st

from hr.hr_compliance_engagement_dashboard import \
    hr_engagement_and_compliance_dashboard
from hr.hr_overview_dashboard import hr_overview_dashboard
from hr.hr_demographics_dashboard import hr_demographics_dashboard
from hr.hr_recruitment_dashboard import hr_recruitment_dashboard
from hr.hr_training_dashboard import hr_training_dashboard


def show_hr_dashboard(nav_option):
    if nav_option == "Overview":
        hr_overview_dashboard()
    elif nav_option == "Engagement & Compliance":
        hr_engagement_and_compliance_dashboard()
    elif nav_option == "Recruitment":
        hr_recruitment_dashboard()
    elif nav_option == "Training":
        hr_training_dashboard()
    elif nav_option == "Demographics":
        hr_demographics_dashboard()
    else:
        st.write(f"Dashboard for {nav_option} is not implemented yet.")
