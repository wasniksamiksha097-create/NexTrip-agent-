import streamlit as st
from google import genai

# Page Configuration
st.set_page_config(page_title="NexTrip Agent", page_icon="✈️", layout="wide")

st.title("✈️ NexTrip Agent")
st.write("Autonomous Travel Disruption & Replanning Agent")

# Sidebar for Gemini API Key
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

SYSTEM_PROMPT = """
You are NexTrip Agent, an expert travel disruption and autonomous replanning agent.
Your role is to analyze multi-step travel itineraries, calculate the domino-effect impacts of delays or cancellations, 
recalculate the entire schedule, and generate ready-to-send communications.

When a user provides an itinerary and a disruption, process the input using this exact 4-part structure:

1. 🚨 DISRUPTION ASSESSMENT
   - State the original event, the revised event time, and the total shift in minutes or hours.

2. ⚡ DEPENDENCY CHAIN IMPACT ANALYSIS
   - Evaluate every subsequent step in the itinerary (pickups, check-ins, meetings, dinners).
   - Explain explicitly why each step is impacted.

3. 📅 REVISED ITINERARY
   - Present a revised, realistic step-by-step timeline with operational buffers.
   - Mark any unresolvable time conflicts that require manual intervention.

4. ✉️ AUTOMATED DRAFT COMMUNICATIONS
   - Draft concise, professional, ready-to-send messages for affected contacts/vendors.

Tone: Professional, calm, executive, and decisive.
"""

default_itinerary = """Original Itinerary:
- 09:00 AM: Flight lands at Heathrow
- 09:45 AM: Airport Express Train to City Center
- 10:30 AM: Hotel Check-In & Luggage Drop
- 11:30 AM: Keynote Presentation at Tech Summit
- 01:30 PM: Client Lunch

Disruption: Flight delayed on tarmac by 2 hours. Revised landing time is 11:00 AM."""

user_input = st.text_area("Itinerary & Disruption Details:", value=default_itinerary, height=200)

if st.button("⚡ Run NexTrip Replanner"):
    if not api_key:
        st.error("Please enter a valid Gemini API Key in the sidebar.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            with st.spinner("Calculating dependency impact..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[SYSTEM_PROMPT, f"Replan this scenario:\n{user_input}"]
                )
                st.success("Replanning Complete!")
                st.markdown(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
