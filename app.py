"""TravelPulse application entry point."""

import streamlit as st


st.set_page_config(page_title="TravelPulse", page_icon="🌍", layout="wide")

st.title("TravelPulse")
st.subheader("A clearer view of anywhere")
st.write(
	"Explore live weather, country context, currency, and local time for your next destination."
)

with st.form("destination_form"):
	destination = st.text_input(
		"Destination",
		placeholder="Try Paris, Tokyo, or Cape Town",
		help="Enter a city or destination to begin.",
	)
	submitted = st.form_submit_button("Search destination", type="primary")

if submitted:
	if destination.strip():
		st.info(f"TravelPulse is ready to explore **{destination.strip()}**.")
	else:
		st.warning("Enter a destination before searching.")

st.divider()
st.markdown("### About TravelPulse")
st.write(
	"TravelPulse combines public APIs into one friendly dashboard so you can understand "
	"the essentials of a place before you go."
)
