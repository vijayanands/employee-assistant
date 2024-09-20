import streamlit as st
import pandas as pd
import plotly.express as px
from ui.style import (
    create_styled_metric, create_styled_bullet_list, create_styled_tabs,
    create_pie_chart, display_pie_chart, create_multi_bar_chart,
    apply_styled_dropdown_css
)

def director_engagement_compliance_dashboard():
    st.title("Engagement and Compliance Dashboard")

    # Apply styled dropdown CSS
    apply_styled_dropdown_css()

    # Dummy data (unchanged)
    engagement_data = pd.DataFrame({
        'team': ['Product Development', 'Customer Support', 'Sales', 'Marketing', 'Human Resources'],
        'score': [80, 75, 85, 78, 82],
        'previousScore': [75, 78, 82, 76, 80]
    })

    engagement_trends = pd.DataFrame({
        'quarter': ['Q1', 'Q2', 'Q3', 'Q4'],
        'overall': [76, 78, 79, 80],
        'productDev': [74, 76, 78, 80],
        'customerSupport': [75, 77, 76, 75],
        'sales': [80, 82, 83, 85],
        'marketing': [75, 76, 77, 78],
        'hr': [76, 79, 81, 82]
    })

    compliance_data = pd.DataFrame({
        'category': ['Mandatory Training', 'Policy Acknowledgment', 'Data Protection', 'Code of Conduct', 'Ethics Training'],
        'compliance': [100, 95, 98, 97, 93],
        'previousCompliance': [98, 92, 95, 95, 90]
    })

    # Tabs using styled tabs
    tabs = create_styled_tabs(["Employee Engagement", "Compliance Overview"])

    with tabs[0]:
        st.subheader("Team Engagement Scores")
        for _, row in engagement_data.iterrows():
            delta = row['score'] - row['previousScore']
            col1, col2 = st.columns([3, 2])
            with col1:
                st.write(row['team'])
            with col2:
                create_styled_metric(f"{row['score']}%", "Current Score", "📊")

        st.subheader("Team Engagement Scores Chart")
        fig = create_multi_bar_chart(engagement_data, 'team', ['score', 'previousScore'], 
                                     {'score': 'Current Score', 'previousScore': 'Previous Score'},
                                     "Team Engagement Scores Comparison")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Engagement Trends Over Time")
        fig = px.line(engagement_trends, x='quarter', y=['overall', 'productDev', 'customerSupport', 'sales', 'marketing', 'hr'])
        fig.update_layout(yaxis_range=[70, 90])
        st.plotly_chart(fig, use_container_width=True)

    with tabs[1]:
        st.subheader("Compliance Overview")

        # Pie chart for compliance rates
        fig = create_pie_chart(compliance_data, 'category', 'compliance', 
                               title="Compliance Rates by Category", 
                               color_sequence=px.colors.sequential.RdBu)
        display_pie_chart(fig)

        st.write("This chart shows the current compliance rates for different categories:")
        compliance_list = [f"{row['category']}: {row['compliance']}% compliant (Change: {row['compliance'] - row['previousCompliance']:+.1f}%)" for _, row in compliance_data.iterrows()]
        create_styled_bullet_list(compliance_list, "Compliance Rates")

        st.write("\nInterpretation:")
        interpretation_list = [
            "Larger slices indicate better compliance.",
            "The color gradient (red to blue) also indicates the level of compliance.",
            "Categories with smaller slices may require more attention."
        ]
        create_styled_bullet_list(interpretation_list, "Chart Interpretation")

        if min(compliance_data['compliance']) < 95:
            st.warning("Note: Categories with compliance rates below 95% may need immediate attention.")

        st.subheader("Actionable Insights")
        insights = [
            "Ethics Training compliance is below 95%. Consider sending reminders or scheduling additional sessions.",
            "Mandatory Training compliance is at 100%. Excellent work maintaining full compliance in this critical area.",
            "Policy Acknowledgment shows the largest improvement. Consider applying similar strategies to other areas."
        ]
        create_styled_bullet_list(insights, "Key Insights")

# This function can be called from another Python script
if __name__ == "__main__":
    director_engagement_compliance_dashboard()
