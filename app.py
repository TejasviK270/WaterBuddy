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
    st.session_state.screen = min(st.session_state.screen + 1, 5)

def go_prev():
    st.session_state.screen = max(st.session_state.screen - 1, 0)

# ------------------ Screen 0: Home ------------------
if st.session_state.screen == 0:
    st.title("💧 WaterBuddy: Your Daily Hydration Companion")
    st.write("Welcome! Let's start your hydration journey.")
    st.info("💡 Tip of the Day: " + random.choice(st.session_state.tips))

    # Use a simple form so navigation only happens on submit
    with st.form("home_form", clear_on_submit=False):
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

    # Show a form; values only commit when submitted
    with st.form("goals_form", clear_on_submit=False):
        # Prepopulate temporary inputs from session if available, else defaults
        default_age = st.session_state.age_group if st.session_state.age_group in age_groups else "Adults (14–64 yrs)"
        age_group_choice = st.selectbox(
            "Choose your age group:", list(age_groups.keys()),
            index=list(age_groups.keys()).index(default_age),
            key="tmp_age_group_choice"
        )

        standard_goal = age_groups[age_group_choice]
        default_goal = st.session_state.goal if st.session_state.goal > 0 else standard_goal
        adjusted_goal_choice = st.number_input(
            "Suggested goal (ml):", value=int(default_goal), step=100, key="tmp_goal_choice"
        )

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Standard Goal", f"{standard_goal} ml")
        with col2:
            st.metric("Your Goal", f"{adjusted_goal_choice} ml")

        colA, colB = st.columns(2)
        with colA:
            back_pressed = st.form_submit_button("⬅️ Back")
        with colB:
            save_next_pressed = st.form_submit_button("💾 Save & ➡️ Next")

    # Handle navigation only after submit
    if back_pressed:
        # Do not change saved session data; just go back
        go_prev()
    if save_next_pressed:
        # Commit choices to session state, then go next
        st.session_state.age_group = age_group_choice
        st.session_state.goal = int(adjusted_goal_choice)
        go_next()

# ------------------ Screen 2: Log Intake ------------------
elif st.session_state.screen == 2:
    st.subheader("🚰 Log Your Water Intake")

    with st.form("log_form", clear_on_submit=False):
        log_amount = st.number_input("Enter amount (ml):", value=250, step=50, key="tmp_log_amount")
        add_pressed = st.form_submit_button("➕ Add Water")
        reset_pressed = st.form_submit_button("🔄 Reset")

        colA, colB = st.columns(2)
        with colA:
            back_pressed = st.form_submit_button("⬅️ Back")
        with colB:
            next_pressed = st.form_submit_button("➡️ Next")

    if add_pressed:
        st.session_state.total_intake += int(log_amount)
    if reset_pressed:
        st.session_state.total_intake = 0
    st.write(f"💧 Total Intake so far: {st.session_state.total_intake} ml")

    if back_pressed:
        go_prev()
    if next_pressed:
        go_next()

# ------------------ Screen 3: Progress ------------------
elif st.session_state.screen == 3:
    goal = st.session_state.goal
    total = st.session_state.total_intake
    remaining = max(goal - total, 0)
    progress = min((total / goal) * 100, 100) if goal > 0 else 0

    st.subheader("📊 Your Progress")
    st.progress(progress / 100 if goal > 0 else 0)
    st.write(f"💧 Total Intake: {total} ml")
    st.write(f"📉 Remaining: {remaining} ml")
    st.write(f"📈 Progress: {progress:.1f}%")

    with st.form("progress_form", clear_on_submit=False):
        colA, colB = st.columns(2)
        with colA:
            back_pressed = st.form_submit_button("⬅️ Back")
        with colB:
            next_pressed = st.form_submit_button("➡️ Next")

    if back_pressed:
        go_prev()
    if next_pressed:
        go_next()

# ------------------ Screen 4: Mascot ------------------
elif st.session_state.screen == 4:
    goal = st.session_state.goal
    total = st.session_state.total_intake
    progress = min((total / goal) * 100, 100) if goal > 0 else 0

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

    with st.form("mascot_form", clear_on_submit=False):
        colA, colB = st.columns(2)
        with colA:
            back_pressed = st.form_submit_button("⬅️ Back")
        with colB:
            next_pressed = st.form_submit_button("➡️ Next")

    if back_pressed:
        go_prev()
    if next_pressed:
        go_next()

# ------------------ Screen 5: Summary ------------------
elif st.session_state.screen == 5:
    total = st.session_state.total_intake
    st.subheader("📅 End-of-Day Summary")
    st.balloons()
    st.success(f"Today you drank {total} ml of water. Great job staying hydrated!")

    with st.form("summary_form", clear_on_submit=False):
        colA, colB = st.columns(2)
        with colA:
            back_pressed = st.form_submit_button("⬅️ Back")
        with colB:
            restart_pressed = st.form_submit_button("🔄 Restart")

    if back_pressed:
        go_prev()
    if restart_pressed:
        # Reset to beginning and clear intake
        st.session_state.screen = 0
        st.session_state.total_intake = 0
