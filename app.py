"""TravelPulse application entry point."""

import streamlit as st

from services.travel_service import get_travel_data
from ui.components import render_dashboard
from ui.styles import apply_styles
from utils.api_helpers import APIError


st.set_page_config(page_title="TravelPulse", page_icon="🌍", layout="wide")
apply_styles()

st.markdown(
	'<div class="hero"><div class="eyebrow">Travel information dashboard</div>'
	'<h1>Know before you go.</h1><p>One destination search for live weather, country context, currency, and local time.</p></div>',
	unsafe_allow_html=True,
)

with st.form("destination_form"):
	destination = st.text_input(
		"Destination",
		placeholder="Try Paris, Tokyo, or Cape Town",
		help="Enter a city or destination to begin.",
	)
	submitted = st.form_submit_button("Search destination", type="primary")

if submitted:
	try:
		with st.spinner("Gathering destination details..."):
			travel_data = get_travel_data(destination)
		st.session_state["travel_data"] = travel_data
	except APIError as error:
		st.error(str(error))

if st.session_state.get("travel_data"):
	render_dashboard(st.session_state["travel_data"])

st.divider()
st.markdown("### About")
st.write(
	"TravelPulse chains public APIs into one concise destination brief. Results are live and can vary by provider availability."
)
