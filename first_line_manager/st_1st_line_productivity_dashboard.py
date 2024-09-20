import streamlit as st
import random
from datetime import datetime, timedelta
from ui.style import (
    create_styled_metric, create_styled_bullet_list, create_pie_chart, display_pie_chart, create_styled_tabs, create_progress_bar,
    create_styled_line_chart, create_styled_bar_chart, apply_styled_dropdown_css
)

# Helper functions to generate dummy data
def generate_employee_list():
    return ["John Doe", "Jane Smith", "Bob Johnson", "Alice Brown", "Charlie Davis"]

def generate_employee_position(employee):
    positions = {
        "John Doe": "Senior Developer",
        "Jane Smith": "Project Manager",
        "Bob Johnson": "UX Designer",
        "Alice Brown": "Data Analyst",
        "Charlie Davis": "Quality Assurance Specialist"
    }
    return positions.get(employee, "Employee")

def generate_productivity_score():
    return round(random.uniform(1, 10), 1)

def generate_task_data():
    total_tasks = random.randint(50, 100)
    completed = random.randint(20, total_tasks - 10)
    in_progress = total_tasks - completed
    on_track = random.randint(0, in_progress)
    overdue = in_progress - on_track
    return total_tasks, completed, in_progress, on_track, overdue

def generate_weekly_task_completion():
    return [random.randint(5, 20) for _ in range(12)]

def generate_communication_data():
    return {
        "avg_email_response_time": round(random.uniform(0.5, 4), 1),
        "meetings_attended": random.randint(10, 30),
        "feedback_implemented": random.randint(5, 15),
        "time_in_meetings": random.randint(10, 40)
    }

def generate_email_response_trend():
    return [round(random.uniform(0.5, 4), 1) for _ in range(12)]

def generate_knowledge_data():
    return {
        "articles_written": random.randint(1, 10),
        "articles_contributed": random.randint(5, 20),
        "training_sessions": random.randint(1, 5),
        "mentoring_hours": random.randint(5, 30),
        "documentation_contributions": random.randint(10, 50)
    }

def generate_recent_contributions():
    contributions = [
        "Updated user manual",
        "Created new onboarding guide",
        "Commented on API documentation",
        "Edited team best practices",
        "Contributed to project wiki"
    ]
    dates = [datetime.now() - timedelta(days=random.randint(1, 30)) for _ in range(5)]
    return list(zip(contributions, dates))

def generate_meeting_data():
    return {
        "organized": random.randint(5, 15),
        "attended": random.randint(20, 40),
        "avg_duration": round(random.uniform(0.5, 2), 1),
        "effectiveness": random.randint(1, 10),
        "weekly_time_percentage": random.randint(10, 40)
    }

def generate_raci_data():
    roles = ["Responsible", "Accountable", "Consulted", "Informed", "None"]
    return {role: random.randint(5, 25) for role in roles}

def generate_learning_data():
    courses = ["Python Advanced", "Machine Learning Basics", "Agile Methodologies", "Cloud Computing", "Data Visualization"]
    certifications = ["AWS Certified Developer", "Scrum Master", "Google Analytics", "Cybersecurity Fundamentals"]
    return {
        "courses_completed": random.sample(courses, random.randint(1, len(courses))),
        "certifications": random.sample(certifications, random.randint(1, len(certifications))),
        "learning_hours": random.randint(20, 100),
        "conferences_attended": random.randint(1, 3),
        "skill_improvement": random.randint(1, 10)
    }

def generate_code_data():
    return {
        "quality_score": round(random.uniform(1, 10), 1),
        "peer_reviews": random.randint(5, 20),
        "refactoring_tasks": random.randint(2, 10),
        "features_developed": random.randint(1, 5),
        "bugs_fixed": {
            "low": random.randint(5, 15),
            "medium": random.randint(3, 10),
            "high": random.randint(1, 5),
            "critical": random.randint(0, 3)
        },
        "git_commits": random.randint(20, 100),
        "bug_fix_rate": round(random.uniform(0.5, 5), 1)
    }

# Main Streamlit UI function
def team_productivity_dashboard():
    st.title("Employee Productivity Dashboard")

    # Apply custom CSS for dropdowns
    apply_styled_dropdown_css()

    # Dropdowns for employee and duration
    col1, col2 = st.columns(2)
    with col1:
        employees = generate_employee_list()
        selected_employee = st.selectbox("Select Employee", employees, key="employee_select")
    with col2:
        duration = st.selectbox("Select Duration", ["Quarterly", "Yearly"], key="duration_select")

    # Display employee info and productivity score in a single row
    employee_position = generate_employee_position(selected_employee)
    productivity_score = generate_productivity_score()

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        create_styled_metric("Employee", selected_employee, "👤")
    with col2:
        create_styled_metric("Position", employee_position, "💼")
    with col3:
        create_styled_metric("Productivity Score", f"{productivity_score}/10", "🌟")
    with col4:
        total_tasks, completed, _, _, _ = generate_task_data()
        create_styled_metric("Total Tasks", total_tasks, "📋")
    with col5:
        create_styled_metric("Completed Tasks", completed, "✅")

    # Tabs
    tabs = create_styled_tabs(["Tasks", "Communication", "Knowledge", "Meetings", "Learning", "Code"])

    # Tab 1: Tasks
    with tabs[0]:
        st.header("Tasks")
        total_tasks, completed, in_progress, on_track, overdue = generate_task_data()

        # Task metrics in a single row
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            create_styled_metric("Total Tasks", total_tasks, "📋")
        with col2:
            create_styled_metric("Completed", completed, "✅")
        with col3:
            create_styled_metric("In Progress", in_progress, "🔄")
        with col4:
            create_styled_metric("On Track", on_track, "🎯")
        with col5:
            create_styled_metric("Overdue", overdue, "⏰")

        # Weekly Task Completion and Task Distribution in one row
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Weekly Task Completion Rate")
            weekly_completion = generate_weekly_task_completion()
            create_styled_line_chart(weekly_completion, "Week", "Tasks Completed")

        with col2:
            st.subheader("Task Distribution")
            task_distribution = {
                'Status': ['Completed', 'On Track', 'Overdue'],
                'Count': [completed, on_track, overdue]
            }
            fig = create_pie_chart(task_distribution, 'Status', 'Count', title="Task Distribution")
            display_pie_chart(fig)

    # Tab 2: Communication Efficiency
    with tabs[1]:
        st.header("Communication Efficiency")
        comm_data = generate_communication_data()

        # Communication metrics in a single row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            create_styled_metric("Avg Email Response Time", f"{comm_data['avg_email_response_time']} hours", "📧")
        with col2:
            create_styled_metric("Meetings Attended", comm_data['meetings_attended'], "🗓️")
        with col3:
            create_styled_metric("Feedback Implemented", comm_data['feedback_implemented'], "💡")
        with col4:
            create_styled_metric("Time in Meetings", f"{comm_data['time_in_meetings']}%", "⏱️")

        st.subheader("Email Response Time Trend")
        email_trend = generate_email_response_trend()
        create_styled_line_chart(email_trend, "Week", "Response Time (hours)")

    # Tab 3: Knowledge
    with tabs[2]:
        st.header("Knowledge")
        knowledge_data = generate_knowledge_data()

        # Knowledge metrics in a single row
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            create_styled_metric("Articles Written", knowledge_data['articles_written'], "📝")
        with col2:
            create_styled_metric("Articles Contributed", knowledge_data['articles_contributed'], "💬")
        with col3:
            create_styled_metric("Training Sessions", knowledge_data['training_sessions'], "🎓")
        with col4:
            create_styled_metric("Mentoring Hours", knowledge_data['mentoring_hours'], "🤝")
        with col5:
            create_styled_metric("Doc Contributions", f"{knowledge_data['documentation_contributions']} pages", "📚")

        # Recent Contributions
        st.subheader("Recent Contributions")
        contributions = generate_recent_contributions()
        contrib_list = [f"{contrib} - {date.strftime('%Y-%m-%d')}" for contrib, date in contributions]
        create_styled_bullet_list(contrib_list, "Recent Knowledge Contributions")

    # Tab 4: Meetings
    with tabs[3]:
        st.header("Meetings")
        meeting_data = generate_meeting_data()

        # Meeting metrics in a single row
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            create_styled_metric("Meetings Organized", meeting_data['organized'], "📅")
        with col2:
            create_styled_metric("Meetings Attended", meeting_data['attended'], "👥")
        with col3:
            create_styled_metric("Avg Duration", f"{meeting_data['avg_duration']} hours", "⏳")
        with col4:
            create_styled_metric("Effectiveness", f"{meeting_data['effectiveness']}/10", "📊")
        with col5:
            create_styled_metric("Weekly Time", f"{meeting_data['weekly_time_percentage']}%", "🕰️")

        st.subheader("Role in Meetings (RACI)")
        raci_data = generate_raci_data()
        create_styled_bar_chart(list(raci_data.keys()), list(raci_data.values()), "Role", "Count")

    # Tab 5: Learning
    with tabs[4]:
        st.header("Learning")
        learning_data = generate_learning_data()

        # Learning metrics in a single row
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            create_styled_metric("Learning Hours", learning_data['learning_hours'], "📚")
        with col2:
            create_styled_metric("Conferences", learning_data['conferences_attended'], "🎤")
        with col3:
            create_styled_metric("Skill Improvement", f"{learning_data['skill_improvement']}/10", "📈")
        with col4:
            create_styled_metric("Courses Completed", len(learning_data['courses_completed']), "🎓")
        with col5:
            create_styled_metric("Certifications", len(learning_data['certifications']), "🏅")

        # Courses and Certifications
        col1, col2 = st.columns(2)
        with col1:
            create_styled_bullet_list(learning_data['courses_completed'], "Courses Completed")
        with col2:
            create_styled_bullet_list(learning_data['certifications'], "Certifications Achieved")

    # Tab 6: Code
    with tabs[5]:
        st.header("Code")
        code_data = generate_code_data()

        # All code metrics in two rows
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            create_styled_metric("Code Quality", f"{code_data['quality_score']}/10", "🏆")
        with col2:
            create_styled_metric("Code Reviews", code_data['peer_reviews'], "👁️")
        with col3:
            create_styled_metric("Refactoring Tasks", code_data['refactoring_tasks'], "🔧")
        with col4:
            create_styled_metric("Features Developed", code_data['features_developed'], "🚀")
        with col5:
            create_styled_metric("Git Commits", code_data['git_commits'], "💻")

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            create_styled_metric("Bug Fix Rate", f"{code_data['bug_fix_rate']} bugs/week", "🐛")
        with col2:
            create_styled_metric("Critical Bugs Fixed", code_data['bugs_fixed']['critical'], "🚨")
        with col3:
            create_styled_metric("High Bugs Fixed", code_data['bugs_fixed']['high'], "🔴")
        with col4:
            create_styled_metric("Medium Bugs Fixed", code_data['bugs_fixed']['medium'], "🟠")
        with col5:
            create_styled_metric("Low Bugs Fixed", code_data['bugs_fixed']['low'], "🟡")

        # Bugs Fixed by Criticality pie chart
        st.subheader("Bugs Fixed by Criticality")
        bug_data = {
            'Criticality': list(code_data['bugs_fixed'].keys()),
            'Count': list(code_data['bugs_fixed'].values())
        }
        fig = create_pie_chart(bug_data, 'Criticality', 'Count', title="Bugs Fixed by Criticality")
        display_pie_chart(fig)

if __name__ == "__main__":
    team_productivity_dashboard()
