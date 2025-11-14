import streamlit as st
from trip_crew import TripCrew
from datetime import datetime, timedelta
import os

# Configuration de la page
st.set_page_config(
    page_title="AI Trip Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
    <style>
    .main-header {
        font-size: 3.5rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .agent-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .agent-card h3 {
        color: white;
        margin-top: 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF6B6B !important;
        color: white !important;
        border-radius: 8px;
        padding: 0.8rem;
        font-size: 1rem;
        font-weight: bold;
    }
    .result-box {
        padding: 1.5rem;
        background-color: #F9FAFB;
        border-radius: 10px;
        border: 1px solid #E5E7EB;
        margin-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<div class='main-header'>✈️ AI Trip Planner</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Plan a complete trip with CrewAI agents powered by your local LLM (Ollama)</div>", unsafe_allow_html=True)

# --- FORM SECTION ---
st.sidebar.header("📝 Trip Information")

origin = st.sidebar.text_input("Departure City", "Rabat")
cities = st.sidebar.text_input("Destination Cities (comma-separated)", "Paris, Rome, Barcelona")

start_date = st.sidebar.date_input("Trip Start Date", datetime.now().date())
duration = st.sidebar.number_input("Trip Duration (days)", min_value=3, max_value=30, value=7)

end_date = start_date + timedelta(days=duration)
date_range = f"{start_date} → {end_date}"

budget = st.sidebar.selectbox("Budget Level", ["Low", "Medium", "High"])
interests = st.sidebar.text_area("Traveler Interests", "Culture, Food, Museums, Nature")

run_button = st.sidebar.button("🚀 Generate Trip Plan")

# --- MAIN LOGIC ---
if run_button:
    with st.spinner("🧠 The AI agents are analyzing destinations..."):
        try:
            # Initialize Crew
            trip_planner = TripCrew(
                origin=origin,
                cities=cities,
                date_range=date_range,
                duration=duration,
                budget=budget,
                interests=interests
            )

            # Run all agents
            result = trip_planner.run()

            # Display result
            st.markdown("## 🧳 Your AI-Generated Trip Plan")
            st.markdown("<div class='result-box'>", unsafe_allow_html=True)
            st.markdown(result)
            st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Error: {e}")

else:
    st.info("👈 Fill out your trip details in the sidebar and click **Generate Trip Plan**.")
