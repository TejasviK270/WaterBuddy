# ------------------ Screen 1: Goals (FIXED) ------------------
elif st.session_state.screen == 1:
    st.subheader("🎯 Set Your Hydration Goal")

    age_groups = {
        "Children (4–8 yrs)": 1200,
        "Teens (9–13 yrs)": 1700,
        "Adults (14–64 yrs)": 2500,
        "Seniors (65+ yrs)": 2000
    }

    # Pre-fill from session if already chosen
    default_age_index = 0
    if st.session_state.age_group in age_groups:
        default_age_index = list(age_groups.keys()).index(st.session_state.age_group)

    age_group = st.selectbox(
        "Choose your age group:",
        options=list(age_groups.keys()),
        index=default_age_index
    )

    standard_goal = age_groups[age_group]

    # Pre-fill custom goal if already set
    current_goal = st.session_state.goal if st.session_state.goal > 0 else standard_goal

    adjusted_goal = st.number_input(
        "Your daily goal (ml):",
        min_value=500,
        max_value=5000,
        value=current_goal,
        step=100
    )

    col1, col2 = st.columns(2)
    col1.metric("Recommended", f"{standard_goal} ml")
    col2.metric("Your Goal", f"{adjusted_goal} ml")

    st.write("")  # spacing
    col_prev, col_next = st.columns([1, 1)
    
    if col_prev.button("⬅️ Back"):
        prev_screen()

    if col_next.button("➡️ Next", type="primary"):
        # Only NOW do we save the selected values!
        st.session_state.goal = adjusted_goal
        st.session_state.age_group = age_group
        next_screen()
