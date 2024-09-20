from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import streamlit as st

from ui.style import (apply_styled_dropdown_css, create_styled_bar_chart,
                      create_styled_bullet_list, create_styled_line_chart,
                      create_styled_metric, create_styled_tabs)


# Helper functions and data generation
def generate_random_data(min_val, max_val, decimals=0):
    return round(np.random.uniform(min_val, max_val), decimals)


def generate_data(time_period):
    end_date = datetime.now()
    if time_period == "Last Month":
        start_date = end_date - timedelta(days=30)
        date_range = pd.date_range(start=start_date, end=end_date, freq="D")
    elif time_period == "Last 3 Months":
        start_date = end_date - timedelta(days=90)
        date_range = pd.date_range(start=start_date, end=end_date, freq="W")
    elif time_period == "Last 6 Months":
        start_date = end_date - timedelta(days=180)
        date_range = pd.date_range(start=start_date, end=end_date, freq="2W")
    else:  # Last Year
        start_date = end_date - timedelta(days=365)
        date_range = pd.date_range(start=start_date, end=end_date, freq="M")

    data = []
    for date in date_range:
        data.append(
            {
                "date": date,
                "turnover": generate_random_data(1, 3, 1),
                "engagement": generate_random_data(7, 8.5, 1),
            }
        )

    df = pd.DataFrame(data)

    # Calculate the last period's values for KPIs
    last_period = df.iloc[-1]
    kpi_data = {
        "productivityScore": f"{generate_random_data(80, 95)}%",
        "performanceIndex": generate_random_data(7, 8.5, 1),
        "turnoverRate": f"{last_period['turnover']}%",
        "engagementScore": last_period["engagement"],
        "staffingLevels": f"{generate_random_data(90, 100)}%",
        "payrollOverview": f"${generate_random_data(1, 1.5, 1)}M",
    }

    return df, kpi_data


# Team data
team_data = {
    "Overall Productivity Score": [
        {"team": "Engineering", "score": 87},
        {"team": "Marketing", "score": 82},
        {"team": "Sales", "score": 90},
        {"team": "Customer Support", "score": 85},
    ],
    "Performance Index": [
        {"team": "Engineering", "score": 7.9},
        {"team": "Marketing", "score": 7.6},
        {"team": "Sales", "score": 8.2},
        {"team": "Customer Support", "score": 7.7},
    ],
    "Turnover Rate": [
        {"team": "Engineering", "score": "2.1%"},
        {"team": "Marketing", "score": "2.5%"},
        {"team": "Sales", "score": "2.8%"},
        {"team": "Customer Support", "score": "2.3%"},
    ],
    "Engagement Score": [
        {"team": "Engineering", "score": 7.8},
        {"team": "Marketing", "score": 7.5},
        {"team": "Sales", "score": 8.1},
        {"team": "Customer Support", "score": 7.9},
    ],
}


def director_executive_summary_dashboard():
    st.title("Executive Summary Dashboard")

    # Apply styled dropdown CSS
    apply_styled_dropdown_css()

    # Time period selector using styled dropdown
    time_period = st.selectbox(
        "Select time period",
        ["Last Month", "Last 3 Months", "Last 6 Months", "Last Year"],
        key="time_period",
    )

    # Generate data based on selected time period
    df, kpi_data = generate_data(time_period)

    # KPI tiles using styled metrics
    st.header("Key Performance Indicators")
    col1, col2, col3 = st.columns(3)
    with col1:
        create_styled_metric(
            "Overall Productivity Score", kpi_data["productivityScore"], "📈"
        )
        create_styled_metric("Turnover Rate", kpi_data["turnoverRate"], "🔄")
    with col2:
        create_styled_metric(
            "Performance Index", str(kpi_data["performanceIndex"]), "🎯"
        )
        create_styled_metric("Engagement Score", str(kpi_data["engagementScore"]), "😊")
    with col3:
        create_styled_metric("Staffing Levels", kpi_data["staffingLevels"], "👥")
        create_styled_metric("Payroll Overview", kpi_data["payrollOverview"], "💰")

    # Tabs for different sections using styled tabs
    tabs = create_styled_tabs(["Trends", "Team Breakdown", "Risk Assessment"])

    with tabs[0]:
        st.header("Trend Analysis")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Turnover Rate Trend")
            create_styled_line_chart(
                df["turnover"].tolist(), "Date", "Turnover Rate (%)"
            )
            trend_info = [
                "The Turnover Rate graph shows the percentage of employees leaving the company over time.",
                "A lower turnover rate is generally better, indicating higher employee retention.",
            ]
            create_styled_bullet_list(trend_info, "Turnover Rate Interpretation")

        with col2:
            st.subheader("Engagement Score Trend")
            create_styled_line_chart(
                df["engagement"].tolist(), "Date", "Engagement Score"
            )
            engagement_info = [
                "The Engagement Score graph represents employee satisfaction and involvement on a scale of 1-10.",
                "A higher engagement score indicates more satisfied and productive employees.",
            ]
            create_styled_bullet_list(
                engagement_info, "Engagement Score Interpretation"
            )

    with tabs[1]:
        st.header("Team Breakdown")
        selected_kpi = st.selectbox("Select KPI", options=list(team_data.keys()))

        if selected_kpi in team_data:
            team_df = pd.DataFrame(team_data[selected_kpi])
            create_styled_bar_chart(
                team_df["team"], team_df["score"], "Team", selected_kpi
            )
            st.table(team_df)

    with tabs[2]:
        st.header("Risk Assessment")

        # High Risk Areas
        st.subheader("High Risk Areas")
        high_risk_areas = [
            "Cybersecurity: Potential vulnerabilities in remote work infrastructure",
            "Talent Retention: Increased turnover in key departments",
            "Compliance: Upcoming regulatory changes in data privacy",
        ]
        for area in high_risk_areas:
            st.warning(area)

        # Risk Mitigation Strategies
        st.subheader("Risk Mitigation Strategies")
        mitigation_strategies = {
            "Cybersecurity": [
                "Implement multi-factor authentication for all remote access",
                "Conduct regular security audits and penetration testing",
                "Provide ongoing cybersecurity training for all employees",
            ],
            "Talent Retention": [
                "Review and improve compensation packages for key roles",
                "Implement a structured career development program",
                "Conduct regular employee satisfaction surveys and act on feedback",
            ],
            "Compliance": [
                "Form a task force to study upcoming regulatory changes",
                "Update data handling processes and policies",
                "Provide training on new compliance requirements to relevant staff",
            ],
        }

        for risk, strategies in mitigation_strategies.items():
            with st.expander(f"Mitigation Strategies for {risk}"):
                for strategy in strategies:
                    st.write(f"- {strategy}")

    # Insights and Recommendations
    st.header("Insights and Recommendations")
    insights = [
        "Turnover Rate: The current rate is slightly above target. Consider investigating reasons for employee departures and implementing retention strategies.",
        "Engagement Score: While close to the target, there's room for improvement. Consider conducting employee surveys to identify areas for enhancing workplace satisfaction.",
        "Team Performance: Sales team shows the highest overall productivity score. Consider sharing best practices across teams to improve overall company performance.",
    ]
    create_styled_bullet_list(insights, "Key Insights")

    next_steps = [
        "Conduct a detailed analysis of factors contributing to turnover in underperforming teams.",
        "Implement targeted engagement initiatives based on team-specific engagement scores.",
        "Review and optimize resource allocation based on productivity scores and staffing levels.",
    ]
    create_styled_bullet_list(next_steps, "Next Steps")


if __name__ == "__main__":
    director_executive_summary_dashboard()
