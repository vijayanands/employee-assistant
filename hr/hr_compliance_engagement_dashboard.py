import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from ui.style import (apply_styled_dropdown_css, create_pie_chart,
                      create_styled_metric, create_styled_tabs,
                      display_pie_chart)

# Mock data (same as before)
dummy_compliance_data = {
    "trainingCompletion": {
        "overall": 85,
        "departments": [
            {"name": "HR", "completion": 95},
            {"name": "IT", "completion": 88},
            {"name": "Finance", "completion": 82},
            {"name": "Marketing", "completion": 78},
            {"name": "Operations", "completion": 80},
        ],
    },
    "policyAcknowledgments": {
        "overall": 92,
        "departments": [
            {"name": "HR", "acknowledgment": 98},
            {"name": "IT", "acknowledgment": 95},
            {"name": "Finance", "acknowledgment": 90},
            {"name": "Marketing", "acknowledgment": 89},
            {"name": "Operations", "acknowledgment": 88},
        ],
    },
    "complianceIncidents": [
        {
            "id": 1,
            "issue": "Data breach",
            "severity": "High",
            "status": "Investigating",
        },
        {"id": 2, "issue": "Late filing", "severity": "Medium", "status": "Resolved"},
        {
            "id": 3,
            "issue": "Policy violation",
            "severity": "Low",
            "status": "Pending review",
        },
    ],
}

dummy_engagement_data = [
    {
        "subject": "Job Satisfaction",
        "score": 4.2,
        "description": "Overall contentment with job roles and responsibilities",
    },
    {
        "subject": "Work-Life Balance",
        "score": 3.9,
        "description": "Ability to maintain a healthy balance between work and personal life",
    },
    {
        "subject": "Career Growth",
        "score": 3.6,
        "description": "Opportunities for professional development and advancement",
    },
    {
        "subject": "Company Culture",
        "score": 4.1,
        "description": "Alignment with organizational values and work environment",
    },
    {
        "subject": "Leadership",
        "score": 3.8,
        "description": "Confidence in company leadership and management",
    },
    {
        "subject": "Compensation",
        "score": 3.5,
        "description": "Satisfaction with salary and benefits package",
    },
]

score_interpretation = [
    {
        "range": "1.0 - 2.0",
        "interpretation": "Poor - Immediate attention required",
        "color": "#FF4136",
    },
    {
        "range": "2.1 - 3.0",
        "interpretation": "Below Average - Needs improvement",
        "color": "#FF851B",
    },
    {
        "range": "3.1 - 4.0",
        "interpretation": "Good - Meeting expectations",
        "color": "#FFDC00",
    },
    {
        "range": "4.1 - 5.0",
        "interpretation": "Excellent - Exceeding expectations",
        "color": "#2ECC40",
    },
]


def hr_engagement_and_compliance_dashboard():
    st.title("Compliance & Engagement Dashboard")

    # Apply styled dropdown CSS
    apply_styled_dropdown_css()

    # Duration dropdown
    time_period = st.selectbox(
        "Select time period",
        options=["Last Month", "Last 3 Months", "Last 6 Months", "Last Year"],
        index=2,
    )

    # Create styled tabs
    tab1, tab2, tab3 = create_styled_tabs(["Compliance", "Engagement", "Incidents"])

    with tab1:
        st.subheader("Compliance Training Completion")
        col1, col2 = st.columns(2)
        with col1:
            create_styled_metric(
                "Overall Completion",
                f"{dummy_compliance_data['trainingCompletion']['overall']}%",
                "📊",
            )
        with col2:
            pie_data = dummy_compliance_data["trainingCompletion"]["departments"]
            fig = create_pie_chart(
                data=pie_data,
                names="name",
                values="completion",
                title="Department-wise Completion",
            )
            display_pie_chart(fig)

        st.subheader("Policy Acknowledgments")
        col1, col2 = st.columns(2)
        with col1:
            create_styled_metric(
                "Overall Acknowledgment",
                f"{dummy_compliance_data['policyAcknowledgments']['overall']}%",
                "✅",
            )
        with col2:
            acknowledgment_data = dummy_compliance_data["policyAcknowledgments"][
                "departments"
            ]
            df = pd.DataFrame(acknowledgment_data)
            fig = px.bar(
                df,
                x="name",
                y="acknowledgment",
                title="Department-wise Acknowledgments",
            )
            fig.update_layout(
                xaxis_title="Department", yaxis_title="Acknowledgment Rate (%)"
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Engagement Survey Results")
        fig = go.Figure(
            data=go.Scatterpolar(
                r=[item["score"] for item in dummy_engagement_data],
                theta=[item["subject"] for item in dummy_engagement_data],
                fill="toself",
                line_color="#0074D9",
            )
        )
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
            showlegend=False,
            height=400,
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Score Interpretation")
        interpretation_list = [
            f"{item['range']}: {item['interpretation']}"
            for item in score_interpretation
        ]
        for item in interpretation_list:
            st.write(f"• {item}")

        st.subheader("Detailed Engagement Scores")
        for item in dummy_engagement_data:
            percentage = (item["score"] / 5) * 100  # Convert score to percentage
            st.write(
                f"**{item['subject']}:** {item['score']} out of 5 ({percentage:.1f}%)"
            )
            st.write(f"_{item['description']}_")
            st.write("---")

    with tab3:
        st.subheader("Compliance Incidents")
        for incident in dummy_compliance_data["complianceIncidents"]:
            st.write(f"**Incident {incident['id']}**")
            st.write(f"• Issue: {incident['issue']}")
            st.write(f"• Severity: {incident['severity']}")
            st.write(f"• Status: {incident['status']}")
            st.write("---")

        st.warning(
            f"There are {len(dummy_compliance_data['complianceIncidents'])} active compliance incidents. Please review and take necessary actions."
        )


if __name__ == "__main__":
    hr_engagement_and_compliance_dashboard()
