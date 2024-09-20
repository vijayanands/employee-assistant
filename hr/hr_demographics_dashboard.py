import pandas as pd
import streamlit as st

from ui.style import (apply_styled_dropdown_css, create_multi_bar_chart,
                      create_pie_chart, create_styled_tabs, display_pie_chart)

# Dummy data (unchanged)
dummyData = {
    "genderDistribution": [
        {"name": "Male", "value": 55},
        {"name": "Female", "value": 42},
        {"name": "Non-binary", "value": 3},
    ],
    "ageDistribution": [
        {"name": "18-25", "value": 15},
        {"name": "26-35", "value": 30},
        {"name": "36-45", "value": 25},
        {"name": "46-55", "value": 20},
        {"name": "56+", "value": 10},
    ],
    "ethnicityDistribution": [
        {"name": "White", "value": 60},
        {"name": "Asian", "value": 15},
        {"name": "Black", "value": 12},
        {"name": "Hispanic", "value": 10},
        {"name": "Other", "value": 3},
    ],
    "tenureDistribution": [
        {"name": "0-1 years", "value": 20},
        {"name": "1-3 years", "value": 30},
        {"name": "3-5 years", "value": 25},
        {"name": "5-10 years", "value": 15},
        {"name": "10+ years", "value": 10},
    ],
    "diversityHiring": [
        {"year": "2020", "diverse": 25, "nonDiverse": 75},
        {"year": "2021", "diverse": 30, "nonDiverse": 70},
        {"year": "2022", "diverse": 35, "nonDiverse": 65},
        {"year": "2023", "diverse": 40, "nonDiverse": 60},
        {"year": "2024", "diverse": 45, "nonDiverse": 55},
    ],
}

# Convert dummy data to DataFrames (unchanged)
gender_df = pd.DataFrame(dummyData["genderDistribution"])
age_df = pd.DataFrame(dummyData["ageDistribution"])
ethnicity_df = pd.DataFrame(dummyData["ethnicityDistribution"])
tenure_df = pd.DataFrame(dummyData["tenureDistribution"])
diversity_hiring_df = pd.DataFrame(dummyData["diversityHiring"])


def diversity_index_component(score):
    return f"""
    <div style="
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    ">
        <h2 style="color: #31333F; margin-bottom: 10px;">Diversity Index</h2>
        <div style="font-size: 48px; font-weight: bold; color: #0088FE;">{score}</div>
        <div style="font-size: 18px; color: #666;">out of 100</div>
    </div>
    """


def hr_demographics_dashboard():
    st.title("Employee Demographics & Diversity Dashboard")

    # Display the Diversity Index at the top
    st.markdown(diversity_index_component(78), unsafe_allow_html=True)

    # Add some space
    st.markdown("<br>", unsafe_allow_html=True)

    # Apply styled dropdown CSS
    apply_styled_dropdown_css()

    # Filter dropdowns
    col1, col2 = st.columns(2)
    with col1:
        filter_option = st.selectbox(
            "Filter by:", ("All Employees", "By Department", "By Role", "By Location")
        )
    with col2:
        duration_option = st.selectbox(
            "Time period:",
            ("Last 30 days", "Last 90 days", "Last 6 months", "Last year", "All time"),
        )

    # Create tabs for different sections
    tabs = create_styled_tabs(["Demographics", "Diversity Metrics"])

    with tabs[0]:
        col1, col2 = st.columns(2)

        with col1:
            fig_gender = create_pie_chart(
                gender_df, "name", "value", "Gender Distribution"
            )
            display_pie_chart(fig_gender)

            fig_ethnicity = create_pie_chart(
                ethnicity_df, "name", "value", "Ethnicity/Race Representation"
            )
            display_pie_chart(fig_ethnicity)

        with col2:
            fig_age = create_pie_chart(age_df, "name", "value", "Age Demographics")
            display_pie_chart(fig_age)

            fig_tenure = create_pie_chart(
                tenure_df, "name", "value", "Tenure Distribution"
            )
            display_pie_chart(fig_tenure)

    with tabs[1]:
        # Diversity Hiring Metrics
        fig_diversity = create_multi_bar_chart(
            diversity_hiring_df,
            "year",
            ["diverse", "nonDiverse"],
            {"diverse": "Diverse Hires", "nonDiverse": "Non-Diverse Hires"},
            "Diversity Hiring Metrics",
        )
        st.plotly_chart(fig_diversity, use_container_width=True)


if __name__ == "__main__":
    hr_demographics_dashboard()
