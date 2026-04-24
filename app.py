import streamlit as st
import pandas as pd
import pickle

# Load saved model and feature columns
model = pickle.load(open("model.pkl", "rb"))
feature_columns = pickle.load(open("feature_columns.pkl", "rb"))

teams = [
    'Chennai Super Kings',
    'Mumbai Indians',
    'Royal Challengers Bangalore',
    'Royal Challengers Bengaluru',
    'Kolkata Knight Riders',
    'Delhi Capitals',
    'Delhi Daredevils',
    'Punjab Kings',
    'Kings XI Punjab',
    'Rajasthan Royals',
    'Sunrisers Hyderabad',
    'Deccan Chargers',
    'Gujarat Titans',
    'Gujarat Lions',
    'Lucknow Super Giants',
    'Rising Pune Supergiant',
    'Rising Pune Supergiants',
    'Pune Warriors',
    'Kochi Tuskers Kerala'
]

st.set_page_config(page_title="IPL Win Predictor", page_icon="🏏")
st.title("🏏 IPL Win Predictor")
st.write("Predict the batting team's win probability during a chase.")

batting_team = st.selectbox("Batting Team", teams)
bowling_team = st.selectbox("Bowling Team", teams)

current_score = st.number_input("Current Score", min_value=0, step=1)
target = st.number_input("Target", min_value=1, step=1)
balls_left = st.number_input("Balls Left", min_value=1, max_value=120, step=1)
wickets_left = st.number_input("Wickets Left", min_value=0, max_value=10, step=1)

if st.button("Predict Win Probability"):

    if batting_team == bowling_team:
        st.error("Batting team and bowling team cannot be the same.")
    elif current_score >= target:
        st.success("Batting side has already won. Win probability: 100%")
    else:
        runs_left = target - current_score
        balls_bowled = 120 - balls_left

        current_rr = (current_score / balls_bowled) * 6 if balls_bowled > 0 else 0
        required_rr = (runs_left / balls_left) * 6 if balls_left > 0 else 0

        input_df = pd.DataFrame(0, index=[0], columns=feature_columns)

        if 'current_score' in input_df.columns:
            input_df['current_score'] = current_score
        if 'cum_runs' in input_df.columns:
            input_df['cum_runs'] = current_score

        input_df['runs_left'] = runs_left
        input_df['balls_left'] = balls_left
        input_df['wickets_left'] = wickets_left
        input_df['current_rr'] = current_rr
        input_df['required_rr'] = required_rr

        batting_col = f'batting_team_{batting_team}'
        bowling_col = f'bowling_team_{bowling_team}'

        if batting_col in input_df.columns:
            input_df[batting_col] = 1
        else:
            st.error(f"Missing column in model: {batting_col}")

        if bowling_col in input_df.columns:
            input_df[bowling_col] = 1
        else:
            st.error(f"Missing column in model: {bowling_col}")

        prob = model.predict_proba(input_df)[0][1]

        st.success(f"{batting_team} win probability: {round(prob * 100, 2)}%")
        st.info(f"{bowling_team} win probability: {round((1 - prob) * 100, 2)}%")

        st.write("### Match Situation")
        st.write(f"Current Score: {current_score}")
        st.write(f"Target: {target}")
        st.write(f"Runs Left: {runs_left}")
        st.write(f"Balls Left: {balls_left}")
        st.write(f"Wickets Left: {wickets_left}")
        st.write(f"Current Run Rate: {round(current_rr, 2)}")
        st.write(f"Required Run Rate: {round(required_rr, 2)}")
        