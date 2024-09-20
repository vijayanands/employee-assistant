import pandas as pd
import random

def generate_productivity_data():
    return {
        "Task Completion Rate": round(random.uniform(0.7, 1.0), 2),
        "Communication Efficiency": round(random.uniform(0.6, 0.9), 2),
        "Knowledge Contribution": random.randint(5, 20),
        "Meeting Effectiveness": round(random.uniform(0.5, 0.8), 2),
        "Learning and Development": round(random.uniform(0.6, 0.9), 2),
        "Craftsmanship": round(random.uniform(0.7, 0.95), 2)
    }

def generate_performance_career_data():
    career_levels = ["Junior", "Intermediate", "Senior", "Lead"]
    return {
        "Goals Achieved": random.randint(3, 8),
        "Total Goals": random.randint(8, 12),
        "Feedback Received": random.randint(10, 30),
        "Performance Score": round(random.uniform(3.0, 5.0), 1),
        "Career Level": random.choice(career_levels),
        "Years in Current Role": random.randint(1, 5)
    }

def generate_learning_skills_data():
    courses = ["Python Fundamentals", "Data Analysis", "Machine Learning", "Soft Skills", "Project Management"]
    return {
        "Completed Courses": random.sample(courses, random.randint(1, 3)),
        "In Progress Courses": random.sample(courses, random.randint(1, 2)),
        "Compliance Status": random.choice(["Completed", "In Progress", "Not Started"]),
        "Skills Gap": random.sample(["Leadership", "Communication", "Technical Writing", "Data Visualization"], 2)
    }

def generate_tasks_data():
    return pd.DataFrame({
        "Task": ["Project A", "Report B", "Meeting C", "Training D", "Review E"],
        "Status": random.choices(["Not Started", "In Progress", "Completed"], k=5),
        "Due Date": pd.date_range(start="2024-09-20", periods=5)
    })

# Generate data
productivity_data = generate_productivity_data()
performance_career_data = generate_performance_career_data()
learning_skills_data = generate_learning_skills_data()
tasks_data = generate_tasks_data()
