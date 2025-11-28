# app.py

import streamlit as st
import random

# ------------------ Setup ------------------
st.set_page_config(page_title="WaterBuddy", layout="centered")

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

# ------------------ Sidebar Navigation ------------------
st.sidebar.title("📑 Navigation")
screen = st.sidebar.radio("Go to:", ["🏠 Home", "🎯 Goals", "🚰 Log Intake", "📊 Progress", "🐢 Mascot", "📅 Summary"])

# ------------------ Home Screen ------------------
if screen == "🏠 Home":
    st.title("💧 WaterBuddy: Your Daily Hydration Companion")
    st.sidebar.write("💡 Tip of the Day:")
    st.sidebar.info(random.choice(st.session_state.tips))
    st.write("Welcome! Use the sidebar to navigate through the app.")

# ------------------ Goals Screen ------------------
elif screen == "🎯 Goals":
    st.subheader("👤 Select Your Age Group")
    age_groups = {
        "Children (4–8 yrs)": 1200,
        "Teens (9–13 yrs)": 1700,
        "Adults (14–64 yrs)": 2500,
        "Seniors (65+ yrs)": 2000
    }
    age_group = st.selectbox("Choose your age group:", list(age_groups.keys()))
    standard_goal = age_groups[age_group]
    adjusted_goal = st.number_input("Suggested goal (ml):", value=standard_goal, step=100)
    st.session_state.goal = adjusted_goal
    st.session_state.age_group = age_group

    col1, col2 = st.columns(2)
    col1.metric("Standard Goal", f"{standard_goal} ml")
    col2.metric("Your Goal", f"{adjusted_goal} ml")

# ------------------ Log Intake Screen ------------------
elif screen == "🚰 Log Intake":
    st.subheader("🚰 Log Your Water Intake")
    log_amount = st.number_input("Enter amount (ml):", value=250, step=50)
    if st.button("➕ Add Water"):
        st.session_state.total_intake += log_amount
    if st.button("🔄 Reset"):
        st.session_state.total_intake = 0
    st.write(f"💧 Total Intake so far: {st.session_state.total_intake} ml")

# ------------------ Progress Screen ------------------
elif screen == "📊 Progress":
    goal = st.session_state.goal
    total = st.session_state.total_intake
    remaining = max(goal - total, 0)
    progress = min((total / goal) * 100, 100) if goal > 0 else 0

    st.subheader("📊 Your Progress")
    st.progress(progress / 100)
    st.write(f"💧 Total Intake: {total} ml")
    st.write(f"📉 Remaining: {remaining} ml")
    st.write(f"📈 Progress: {progress:.1f}%")

# ------------------ Mascot Screen ------------------
elif screen == "🐢 Mascot":
    goal = st.session_state.goal
    total = st.session_state.total_intake
    progress = min((total / goal) * 100, 100) if goal > 0 else 0

    st.subheader("🐢 Turtle Mascot Reaction")
    if progress == 0:
        st.warning("💡 Stay hydrated! You can do it!")
        st.markdown("🐢 Turtle Mascot: 😢 Looking thirsty!")
    elif progress < 50:
        st.info("🙂 You're on your way! Keep sipping!")
        st.markdown("🐢 Turtle Mascot: 😐 Staying hopeful!")
    elif progress < 100:
        st.success("😄 Great job! You're almost there!")
        st.markdown("🐢 Turtle Mascot: 😊 Smiling and cheering you on!")
    else:
        st.success("🎉 Fantastic! You've reached your hydration goal!")
        st.markdown("🐢 Turtle Mascot: 😄 Clapping with joy!")

# ------------------ Summary Screen ------------------
elif screen == "📅 Summary":
    total = st.session_state.total_intake
    st.subheader("📅 End-of-Day Summary")
    st.balloons()
    st.success(f"Today you drank {total} ml of water. Great job staying hydrated!")
