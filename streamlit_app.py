import streamlit as st
import requests
import urllib.parse

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="AI Virtual Tour Guide", page_icon="🌍")

st.title("🌍 AI Virtual Tour Guide")
st.write("Route, traffic, stays & rentals – 100% FREE")

# ---------------- SAFE FUNCTIONS ----------------
def get_extratags(item):
    if isinstance(item.get("extratags"), dict):
        return item["extratags"]
    return {}

def search_places(query):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "extratags": 1,
        "limit": 5
    }
    headers = {"User-Agent": "AI-Tour-Guide-App"}
    return requests.get(url, params=params, headers=headers).json()

# ---------------- USER INPUT ----------------
start_place = st.text_input("🚩 Start Location (eg: Salem)")
destination_place = st.text_input("🎯 Destination (eg: Ooty)")

if st.button("Search & Show Results"):
    if not start_place or not destination_place:
        st.warning("Please enter both locations")
    else:
        # -------- GOOGLE MAPS FREE ROUTE --------
        s = urllib.parse.quote(start_place)
        d = urllib.parse.quote(destination_place)

        maps_url = (
            f"https://www.google.com/maps/dir/?api=1"
            f"&origin={s}&destination={d}&travelmode=driving"
        )

        st.subheader("🗺️ Route with Live Traffic")
        st.markdown(f"[👉 Open Google Maps Route]({maps_url})")
        st.info("Shows live traffic, travel time & alternate routes")

        # -------- HOTELS --------
        st.subheader("🏨 Room Stays / Hotels")
        hotels = search_places(f"hotels in {destination_place}")

        if not hotels:
            st.write("No hotels found")
        for h in hotels:
            tags = get_extratags(h)
            phone = tags.get("phone", "Not available")
            website = tags.get("website", "Not available")
            map_link = f"https://www.openstreetmap.org/{h['osm_type']}/{h['osm_id']}"

            st.markdown(f"### 🏨 {h['display_name'].split(',')[0]}")
            st.write("Comfortable stay for travellers.")
            st.write(f"📞 Contact: {phone}")
            if website != "Not available":
                st.markdown(f"🌐 Website: {website}")
            st.markdown(f"📍 [View Location]({map_link})")
            st.divider()

        # -------- CAR RENTALS --------
        st.subheader("🚗 Car Rentals")
        cars = search_places(f"car rental in {destination_place}")

        if not cars:
            st.write("No car rentals found")
        for c in cars:
            tags = get_extratags(c)
            phone = tags.get("phone", "Not available")
            website = tags.get("website", "Not available")
            map_link = f"https://www.openstreetmap.org/{c['osm_type']}/{c['osm_id']}"

            st.markdown(f"### 🚗 {c['display_name'].split(',')[0]}")
            st.write("Reliable car rental service.")
            st.write(f"📞 Contact: {phone}")
            if website != "Not available":
                st.markdown(f"🌐 Website: {website}")
            st.markdown(f"📍 [View Location]({map_link})")
            st.divider()

        # -------- BIKE RENTALS --------
        st.subheader("🏍️ Bike Rentals")
        bikes = search_places(f"bike rental in {destination_place}")

        if not bikes:
            st.write("No bike rentals found")
        for b in bikes:
            tags = get_extratags(b)
            phone = tags.get("phone", "Not available")
            website = tags.get("website", "Not available")
            map_link = f"https://www.openstreetmap.org/{b['osm_type']}/{b['osm_id']}"

            st.markdown(f"### 🏍️ {b['display_name'].split(',')[0]}")
            st.write("Affordable bikes for local travel.")
            st.write(f"📞 Contact: {phone}")
            if website != "Not available":
                st.markdown(f"🌐 Website: {website}")
            st.markdown(f"📍 [View Location]({map_link})")
            st.divider()

        st.success("🤖 Search completed successfully!")
