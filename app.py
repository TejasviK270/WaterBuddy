import streamlit as st
import random

# ------------------ Setup ------------------
st.set_page_config(page_title="WaterBuddy", layout="centered")

# ------------------ Session State Init ------------------
if "screen" not in st.session_state:
    st.session_state.screen = 0
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

# ------------------ Helper Functions ------------------
def next_screen():
    st.session_state.screen += 1

def prev_screen():
    if st.session_state.screen > 0:
        st.session_state.screen -= 1

# ------------------ Screen 0: Home ------------------
if st.session_state.screen == 0:
    st.title("💧 WaterBuddy: Your Daily Hydration Companion")
    st.write("Welcome! Let's start your hydration journey.")
    st.info("💡 Tip of the Day: " + random.choice(st.session_state.tips))

    if st.button("➡️ Next"):
        next_screen()

# ------------------ Screen 1: Goals ------------------
elif st.session_state.screen == 1:
    st.subheader("🎯 Set Your Hydration Goal")
    age_groups = {
        "Children (4–8 yrs)": 1200,
        "Teens (9–13 yrs)": 1700,
        "Adults (14–64 yrs)": 2500,
        "Seniors (65+ yrs)": 2000
    }

    # Inputs only update temporary variables
    age_group_choice = st.selectbox("Choose your age group:", list(age_groups.keys()), key="age_group_choice")
    standard_goal = age_groups[age_group_choice]
    adjusted_goal_choice = st.number_input("Suggested goal (ml):", value=standard_goal, step=100, key="goal_choice")

    col1, col2 = st.columns(2)
    col1.metric("Standard Goal", f"{standard_goal} ml")
    col2.metric("Your Goal", f"{adjusted_goal_choice} ml")

    colA, colB = st.columns([1,1])
    with colA:
        if st.button("⬅️ Back"):
            prev_screen()
    with colB:
        if st.button("➡️ Next"):
            # Save values only when Next is clicked
            st.session_state.age_group = age_group_choice
            st.session_state.goal = adjusted_goal_choice
            next_screen()

# ------------------ Screen 2: Log Intake ------------------
elif st.session_state.screen == 2:
    st.subheader("🚰 Log Your Water Intake")
    log_amount = st.number_input("Enter amount (ml):", value=250, step=50, key="log_amount")
    if st.button("➕ Add Water"):
        st.session_state.total_intake += log_amount
    if st.button("🔄 Reset"):
        st.session_state.total_intake = 0
    st.write(f"💧 Total Intake so far: {st.session_state.total_intake} ml")

    colA, colB = st.columns([1,1])
    with colA:
        if st.button("⬅️ Back"):
            prev_screen()
    with colB:
        if st.button("➡️ Next"):
            next_screen()

# ------------------ Screen 3: Progress ------------------
elif st.session_state.screen == 3:
    goal = st.session_state.goal
    total = st.session_state.total_intake
    remaining = max(goal - total, 0)
    progress = min((total / goal) * 100, 100) if goal > 0 else 0

    st.subheader("📊 Your Progress")
    st.progress(progress / 100)
    st.write(f"💧 Total Intake: {total} ml")
    st.write(f"📉 Remaining: {remaining} ml")
    st.write(f"📈 Progress: {progress:.1f}%")

    colA, colB = st.columns([1,1])
    with colA:
        if st.button("⬅️ Back"):
            prev_screen()
    with colB:
        if st.button("➡️ Next"):
            next_screen()

# ------------------ Screen 4: Mascot ------------------
elif st.session_state.screen == 4:
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

    colA, colB = st.columns([1,1])
    with colA:
        if st.button("⬅️ Back"):
            prev_screen()
    with colB:
        if st.button("➡️ Next"):
            next_screen()

# ------------------ Screen 5: Summary ------------------
elif st.session_state.screen == 5:
    total = st.session_state.total_intake
    st.subheader("📅 End-of-Day Summary")
    st.balloons()
    st.success(f"Today you drank {total} ml of water. Great job staying hydrated!")

    colA, colB = st.columns([1,1])
    with colA:
        if st.button("⬅️ Back"):
            prev_screen()
    with colB:
        if st.button("🔄 Restart"):
            st.session_state.screen = 0
            st.session_state.total_intake = 0
