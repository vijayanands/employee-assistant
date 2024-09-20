import pandas as pd
import streamlit as st

from ui.style import (create_styled_bar_chart, create_styled_bullet_list,
                      create_styled_tabs)

# Anonymized engagement data
anonymized_engagement_data = [
    {
        "id": "EMP001",
        "workLifeBalance": 7,
        "jobSatisfaction": 8,
        "teamCollaboration": 9,
        "careerGrowth": 6,
    },
    {
        "id": "EMP002",
        "workLifeBalance": 6,
        "jobSatisfaction": 7,
        "teamCollaboration": 8,
        "careerGrowth": 7,
    },
    {
        "id": "EMP003",
        "workLifeBalance": 8,
        "jobSatisfaction": 6,
        "teamCollaboration": 7,
        "careerGrowth": 8,
    },
    {
        "id": "EMP004",
        "workLifeBalance": 5,
        "jobSatisfaction": 7,
        "teamCollaboration": 9,
        "careerGrowth": 6,
    },
    {
        "id": "EMP005",
        "workLifeBalance": 7,
        "jobSatisfaction": 8,
        "teamCollaboration": 6,
        "careerGrowth": 7,
    },
]

# Employee compliance data
employee_compliance_data = [
    {
        "name": "Alice",
        "safetyTraining": "compliant",
        "dataProtection": "compliant",
        "codeOfConduct": "compliant",
    },
    {
        "name": "Bob",
        "safetyTraining": "non-compliant",
        "dataProtection": "compliant",
        "codeOfConduct": "compliant",
    },
    {
        "name": "Charlie",
        "safetyTraining": "compliant",
        "dataProtection": "warning",
        "codeOfConduct": "compliant",
    },
    {
        "name": "Diana",
        "safetyTraining": "compliant",
        "dataProtection": "compliant",
        "codeOfConduct": "non-compliant",
    },
    {
        "name": "Ethan",
        "safetyTraining": "warning",
        "dataProtection": "compliant",
        "codeOfConduct": "compliant",
    },
]


def manager_engagement_and_compliance_dashboard():
    st.title("Team Engagement and Compliance Dashboard")

    # Create tabs
    tab1, tab2 = create_styled_tabs(["Engagement Metrics", "Compliance Status"])

    with tab1:
        display_engagement_metrics()
        display_engagement_action_items()

    with tab2:
        display_compliance_status()
        display_compliance_action_items()


def display_engagement_metrics():
    st.header("Anonymized Team Engagement Metrics")

    df = pd.DataFrame(anonymized_engagement_data)
    categories = [
        "workLifeBalance",
        "jobSatisfaction",
        "teamCollaboration",
        "careerGrowth",
    ]

    for category in categories:
        create_styled_bar_chart(
            df["id"],
            df[category],
            "Employee ID",
            f"{category} Score",
            # f"{category} Scores"
        )

    # Metric detail buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Work-Life Balance"):
            show_metric_details("workLifeBalance")
    with col2:
        if st.button("Job Satisfaction"):
            show_metric_details("jobSatisfaction")
    with col3:
        if st.button("Team Collaboration"):
            show_metric_details("teamCollaboration")
    with col4:
        if st.button("Career Growth"):
            show_metric_details("careerGrowth")


def show_metric_details(metric):
    st.subheader(f"{metric} Details")
    df = pd.DataFrame(anonymized_engagement_data)
    st.dataframe(df[["id", metric]])


def display_compliance_status():
    st.header("Team Compliance Status")

    df = pd.DataFrame(employee_compliance_data)

    # Function to color-code status
    def color_status(val):
        if val == "compliant":
            return "background-color: #90EE90"
        elif val == "non-compliant":
            return "background-color: #FFB6C1"
        elif val == "warning":
            return "background-color: #FFFFE0"
        return ""

    # Apply color-coding to the dataframe
    styled_df = df.style.applymap(
        color_status, subset=["safetyTraining", "dataProtection", "codeOfConduct"]
    )

    st.dataframe(styled_df, use_container_width=True)


def display_engagement_action_items():
    st.header("Engagement Action Items")
    engagement_action_items = [
        "Review work-life balance concerns with the team, particularly focusing on improving the lowest scores",
        "Schedule a team meeting to discuss ways to improve overall job satisfaction",
        "Implement team-building activities to enhance team collaboration",
        "Develop individual career growth plans for team members",
        "Conduct one-on-one meetings to address specific engagement concerns",
    ]
    create_styled_bullet_list(engagement_action_items, "Engagement Action Items")


def display_compliance_action_items():
    st.header("Compliance Action Items")
    compliance_action_items = [
        "Ensure Bob completes his safety training by the end of the week",
        "Follow up with Charlie regarding the data protection warning",
        "Review the code of conduct with Diana and provide necessary guidance",
        "Schedule a refresher course on safety procedures for Ethan",
        "Conduct a team-wide compliance awareness session",
    ]
    create_styled_bullet_list(compliance_action_items, "Compliance Action Items")


if __name__ == "__main__":
    manager_engagement_and_compliance_dashboard()
