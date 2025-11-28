import streamlit as st
import random

# ------------------ Setup ------------------
st.set_page_config(page_title="WaterBuddy", layout="centered")

# ------------------ Session State Init ------------------
def init_state():
    defaults = {
        "screen": 0,
        "total_intake": 0,
        "goal": 0,
        "age_group": None,
        "tips": [
            "Drink a glass of water before each meal.",
            "Keep a water bottle on your desk.",
            "Start your day with a glass of water.",
            "Add fruit slices to make water tastier.",
            "Use a hydration reminder app."
        ]
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ------------------ Navigation Helpers ------------------
def go_next():
    st.session_state.screen = min(st.session_state.screen + 1, 2)

def go_prev():
    st.session_state.screen = max(st.session_state.screen - 1, 0)

def reset_day():
    st.session_state.screen = 0
    st.session_state.total_intake = 0
    st.session_state.goal = 0
    st.session_state.age_group = None

# ------------------ Screen 0: Home ------------------
if st.session_state.screen == 0:
    st.title("💧 WaterBuddy: Your Daily Hydration Companion")
    st.write("Welcome! Let's start your hydration journey.")
    st.info("💡 Tip of the Day: " + random.choice(st.session_state.tips))

    with st.form("home_form"):
        next_pressed = st.form_submit_button("➡️ Next")
    if next_pressed:
        go_next()

# ------------------ Screen 1: Goals ------------------
elif st.session_state.screen == 1:
    st.subheader("🎯 Set Your Hydration Goal")

    age_groups = {
        "Children (4–8 yrs)": 1200,
        "Teens (9–13 yrs)": 1700,
        "Adults (14–64 yrs)": 2500,
        "Seniors (65+ yrs)": 2000
    }

    with st.form("goals_form"):
        age_group_choice = st.selectbox("Choose your age group:", list(age_groups.keys()))
        standard_goal = age_groups[age_group_choice]
        adjusted_goal_choice = st.number_input("Suggested goal (ml):", value=standard_goal, step=100)

        col1, col2 = st.columns(2)
        col1.metric("Standard Goal", f"{standard_goal} ml")
        col2.metric("Your Goal", f"{adjusted_goal_choice} ml")

        back_pressed = st.form_submit_button("⬅️ Back")
        save_next_pressed = st.form_submit_button("💾 Save & ➡️ Next")

    if back_pressed:
        go_prev()
    if save_next_pressed:
        st.session_state.age_group = age_group_choice
        st.session_state.goal = int(adjusted_goal_choice)
        go_next()

# ------------------ Screen 2: Log Intake + Progress + Mascot ------------------
elif st.session_state.screen == 2:
    st.subheader("🚰 Log Your Water Intake")

    with st.form("log_form"):
        log_amount = st.number_input("Enter amount (ml):", value=250, step=50)
        add_pressed = st.form_submit_button("➕ Add Water")
        reset_pressed = st.form_submit_button("🔄 Reset Intake")
        back_pressed = st.form_submit_button("⬅️ Back")
        reset_day_pressed = st.form_submit_button("🌅 Reset Day")

    if add_pressed:
        st.session_state.total_intake += int(log_amount)
    if reset_pressed:
        st.session_state.total_intake = 0
    if back_pressed:
        go_prev()
    if reset_day_pressed:
        reset_day()

    # --- Progress Bar ---
    goal = st.session_state.goal
    total = st.session_state.total_intake
    remaining = max(goal - total, 0)
    progress = min((total / goal) * 100, 100) if goal > 0 else 0

    st.subheader("📊 Your Progress")
    st.progress(progress / 100 if goal > 0 else 0)
    st.write(f"💧 Total Intake: {total} ml")
    st.write(f"📉 Remaining: {remaining} ml")
    st.write(f"📈 Progress: {progress:.1f}%")

    # --- Mascot Reaction ---
    st.subheader("🐢 Turtle Mascot Reaction")
    if goal == 0:
        st.warning("Set a goal first on the Goals screen.")
    else:
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
