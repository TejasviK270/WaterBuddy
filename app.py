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
if "tips" not in st.session_state:
    st.session_state.tips = [
        "Drink a glass of water before each meal.",
        "Keep a water bottle on your desk.",
        "Start your day with a glass of water.",
        "Add fruit slices to make water tastier.",
        "Use a hydration reminder app."
    ]

# ------------------ Sidebar Tips ------------------
st.sidebar.title("💡 Daily Hydration Tip")
st.sidebar.write(random.choice(st.session_state.tips))

# ------------------ Age Selection ------------------
st.subheader("👤 Select Your Age Group")
age_group = st.selectbox("Choose your age group:", list(age_groups.keys()))
standard_goal = age_groups[age_group]
adjusted_goal = st.number_input("Suggested goal (ml):", value=standard_goal, step=100)
st.session_state.goal = adjusted_goal
st.session_state.age_group = age_group

# ------------------ Show Standard vs User Goal ------------------
st.markdown("### 🎯 Hydration Goals")
col1, col2 = st.columns(2)
col1.metric("Standard Goal", f"{standard_goal} ml")
col2.metric("Your Goal", f"{adjusted_goal} ml")

# ------------------ Unit Converter ------------------
st.markdown("### 🔄 Unit Converter")
unit = st.radio("Convert:", ["ml ➡️ cups", "cups ➡️ ml"])
value = st.number_input("Enter value:", value=250)
if unit == "ml ➡️ cups":
    converted = round(value / 240, 2)
    st.write(f"{value} ml = {converted} cups")
else:
    converted = round(value * 240)
    st.write(f"{value} cups = {converted} ml")

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
st.write(f"📉 Remaining: {remaining} ml")
st.write(f"📈 Progress: {progress:.1f}%")

# ------------------ Motivational Messages ------------------
st.subheader("🌟 Motivation")
if progress >= 100:
    st.success("🏆 Amazing! You've reached your goal!")
    mascot = "🎉 Clap! You did it!"
elif progress >= 75:
    st.info("👏 Great job! You're almost there!")
    mascot = "😊 Smile! Almost there!"
elif progress >= 50:
    st.info("😊 Keep going! You're halfway there!")
    mascot = "👋 Wave! Keep going!"
else:
    st.warning("💡 Stay hydrated! You can do it!")
    mascot = "💧 Let's hydrate!"

st.write(f"🐢 Mascot Reaction: {mascot}")

# ------------------ End-of-Day Summary ------------------
if st.button("📅 End-of-Day Summary"):
    st.balloons()
    st.success(f"Today you drank {total} ml of water. Great job staying hydrated!")

# ------------------ Reminder Simulation ------------------
if st.button("🔔 Trigger Hydration Reminder"):
    st.toast("💧 Time to drink water!", icon="💧")

# ------------------ Dark/Light Mode Toggle ------------------
theme = st.radio("🌓 Choose Theme:", ["Light", "Dark"])
if theme == "Dark":
    st.markdown(
        """
        <style>
        body { background-color: #1e1e1e; color: white; }
        </style>
        """,
        unsafe_allow_html=True
    )
