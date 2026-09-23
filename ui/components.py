"""Reusable Streamlit dashboard components."""

from typing import Any

import streamlit as st


def card(kicker: str, title: str, body: str, *, image_url: str = "") -> None:
    image = f'<img class="flag" src="{image_url}" alt="Flag">' if image_url else ""
    st.markdown(
        f'<div class="card">{image}<div class="card-kicker">{kicker}</div>'
        f'<div class="card-title">{title}</div><div class="detail">{body}</div></div>',
        unsafe_allow_html=True,
    )


def render_dashboard(data: dict[str, Any]) -> None:
    location = data["location"]
    weather = data["weather"]
    country = data["country"]
    currency = data["currency"]
    timezone = data["timezone"]

    st.markdown("## Destination brief")
    st.caption(f"Live information for {location['city']}, {location['country']}")
    country_details = []
    if country.get("capital") and country["capital"] != "Not available":
        country_details.append(f"Capital: {country['capital']}")
    region = " · ".join(
        value for value in (country.get("region"), country.get("continent"))
        if value and value != "Not available"
    )
    if region:
        country_details.append(region)
    if country.get("population", 0) > 0:
        country_details.append(f"Population: {country['population']:,}")
    currency_code = country.get("currency_code", "")
    currency_name = country.get("currency_name", "")
    columns = st.columns(5)
    with columns[0]:
        card("Location", location["city"], f"{location['country']}<br>{location['latitude']:.2f}° N, {location['longitude']:.2f}° E")
    with columns[1]:
        card("Weather", f"{weather['temperature']:.1f}°C", f"{weather['condition']}<br>Humidity {weather['humidity']}%<br>Wind {weather['wind_speed']:.1f} km/h")
    with columns[2]:
        card("Country", country["country"], "<br>".join(country_details), image_url=country.get("flag", ""))
    with columns[3]:
        rate = currency.get("rate")
        rate_text = f"1 {currency['base']} = {rate:.4f} {currency['quote']}" if rate else ""
        currency_details = [value for value in (currency_name, rate_text) if value]
        card("Currency", f"{currency_code} {country.get('currency_symbol', '')}".strip(), "<br>".join(currency_details))
    with columns[4]:
        card("Local time", timezone["local_time"], f"{timezone['timezone']}<br>{timezone['utc_offset']}")