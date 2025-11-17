# app.py

import streamlit as st
import random

# ------------------ Setup ------------------
st.set_page_config(page_title="WaterBuddy", layout="centered")
st.title("💧 WaterBuddy: Your Daily Hydration Companion")

# ------------------ Age Groups & Goals ------------------
age_groups = {
    "Children (4–8 yrs)": 1200,
    "Teens (9–13 yrs)": 1700,
    "Adults (14–64 yrs)": 2500,
    "Seniors (65+ yrs)": 2000
}

# ------------------ Session State Init ------------------
if "total_intake" not in st.session_state:
    st.session_state.total_intake = 0
if "goal" not in st.session_state:
    st.session_state.goal = 0
if "age_group" not in st.session_state:
    st.session_state.age_group = None

# ------------------ Age Selection ------------------
st.subheader("👤 Select Your Age Group")
age_group = st.selectbox("Choose your age group:", list(age_groups.keys()))
default_goal = age_groups[age_group]
adjusted_goal = st.number_input("Suggested goal (ml):", value=default_goal, step=100)
st.session_state.goal = adjusted_goal
st.session_state.age_group = age_group

# ------------------ Log Water Intake ------------------
st.subheader("🚰 Log Your Water Intake")
log_amount = st.number_input("Enter amount (ml):", value=250, step=50)
if st.button("➕ Add Water"):
    st.session_state.total_intake += log_amount

# ------------------ Reset Button ------------------
if st.button("🔄 New Day / Reset"):
    st.session_state.total_intake = 0

# ------------------ Calculations ------------------
goal = st.session_state.goal
total = st.session_state.total_intake
remaining = max(goal - total, 0)
progress = min((total / goal) * 100, 100)

# ------------------ Visual Feedback ------------------
st.subheader("📊 Your Progress")
st.progress(progress / 100)
st.write(f"💧 Total Intake: {total} ml")
st.write(f"🎯 Goal: {goal} ml")
st.write(f"📉 Remaining: {remaining} ml")
st.write(f"📈 Progress: {progress:.1f}%")

# ------------------ Motivational Messages ------------------
st.subheader("🌟 Motivation")
if progress >= 100:
    st.success("🏆 Amazing! You've reached your goal!")
elif progress >= 75:
    st.info("👏 Great job! You're almost there!")
elif progress >= 50:
    st.info("😊 Keep going! You're halfway there!")
else:
    st.warning("💡 Stay hydrated! You can do it!")

# ------------------ Daily Tips ------------------
tips = [
    "Drink a glass of water before each meal.",
    "Keep a water bottle on your desk.",
    "Use a hydration reminder app.",
    "Start your day with a glass of water.",
    "Add fruit slices to make water tastier."
]
st.subheader("📝 Daily Hydration Tip")
st.write(random.choice(tips))
