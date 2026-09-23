"""TravelPulse application entry point."""

import streamlit as st
from dotenv import load_dotenv

from services.travel_service import get_travel_data
from ui.components import render_dashboard
from ui.styles import apply_styles
from utils.api_helpers import APIError


load_dotenv()
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
else:
	st.info("Search for a destination to create your first travel brief.")

st.divider()
st.markdown("### About")
st.write(
	"TravelPulse chains public APIs into one concise destination brief. Results are live and can vary by provider availability."
)

with st.expander("API Basics"):
	st.markdown(
		"""
		An **API** is a contract that lets a client (this app) request data from a server.
		**HTTP** is the communication protocol; **HTTPS** encrypts it. An **endpoint** is a
		URL for a resource. A **GET** reads data, while POST creates, PUT replaces, PATCH
		partially updates, and DELETE removes data.

		```mermaid
		flowchart LR
			A[TravelPulse client] -->|GET + query parameters| B[API endpoint]
			B -->|JSON + status code| A
		```

		**Query parameters** refine a URL request. **Headers** carry metadata such as an
		API key or content type. **JSON** is the structured response format used here.
		Status codes include 2xx success, 4xx client/request problems, and 5xx server
		problems. API keys are credentials and belong in environment variables or hosted
		secrets, never source code.

		**Authentication** identifies a client. **Rate limiting** controls request volume.
		A **REST API** models resources through HTTP methods. **API chaining** is when one
		response supplies inputs to another, as geocoding supplies coordinates to weather.
		Good **error handling** validates input, checks status codes, handles timeouts, and
		gives users a useful recovery message.
		"""
	)
