import streamlit as st

from PIL import Image
import glob
import folium

from streamlit_folium import st_folium

from agent.travel_agent import run_travel_agent
from pdf_generator import create_pdf


# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide"
)

# ---------------- SESSION STATE ---------------- #

if "generated" not in st.session_state:
    st.session_state.generated = False

if "result" not in st.session_state:
    st.session_state.result = ""

if "destination" not in st.session_state:
    st.session_state.destination = ""

if "source" not in st.session_state:
    st.session_state.source = ""

if "budget" not in st.session_state:
    st.session_state.budget = ""

if "days" not in st.session_state:
    st.session_state.days = 3

if "travel_type" not in st.session_state:
    st.session_state.travel_type = ""


# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

.main {
    background-color: #0E1117;
    color: white;
}

.stApp {
    background-color: #0E1117;
}

h1, h2, h3, h4, h5, h6 {
    color: white;
}

p, div {
    color: white;
}

.stButton>button {
    width: 100%;
    height: 3em;
    border-radius: 12px;
    background-color: #ff4b4b;
    color: white;
    font-size: 18px;
    font-weight: bold;
    border: none;
}

.stButton>button:hover {
    background-color: #ff2e2e;
}

.stTextInput>div>div>input {
    border-radius: 10px;
    background-color: #1E1E1E;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #1A1A2E;
}

</style>
""", unsafe_allow_html=True)


# ---------------- CITY COORDINATES ---------------- #

city_coordinates = {

    "mumbai": (19.0760, 72.8777),
    "goa": (15.2993, 74.1240),
    "delhi": (28.7041, 77.1025),
    "bangalore": (12.9716, 77.5946),
    "kerala": (10.8505, 76.2711),
    "kashmir": (34.0837, 74.7973),
    "chennai": (13.0827, 80.2707),
    "hyderabad": (17.3850, 78.4867),
    "jaipur": (26.9124, 75.7873),
    "kolkata": (22.5726, 88.3639)

}


# ---------------- TITLE ---------------- #

st.title("✈️ AI Travel Planner")
st.subheader("Plan intelligent and personalized trips using AI")


# ---------------- SIDEBAR ---------------- #

st.sidebar.title("⚙️ Travel Preferences")

budget = st.sidebar.selectbox(
    "💰 Select Budget",
    ["Low", "Medium", "Luxury"]
)

days = st.sidebar.slider(
    "📅 Trip Duration (Days)",
    min_value=1,
    max_value=14,
    value=3
)

travel_type = st.sidebar.selectbox(
    "🧳 Travel Type",
    [
        "Solo",
        "Family",
        "Friends",
        "Couple",
        "Adventure"
    ]
)


# ---------------- INPUTS ---------------- #

col1, col2 = st.columns(2)

with col1:

    source = st.text_input(
        "📍 Source City"
    )

with col2:

    destination = st.text_input(
        "🏙️ Destination City"
    )


# ---------------- BUTTON ---------------- #

if st.button("🚀 Generate AI Travel Plan"):

    if source and destination:

        with st.spinner("Generating your personalized AI itinerary..."):

            result = run_travel_agent(
                source=source,
                destination=destination,
                budget=budget,
                days=days,
                travel_type=travel_type
            )

        st.session_state.generated = True
        st.session_state.result = result
        st.session_state.destination = destination
        st.session_state.source = source
        st.session_state.budget = budget
        st.session_state.days = days
        st.session_state.travel_type = travel_type

    else:

        st.warning("⚠️ Please enter both source and destination cities.")


# ---------------- RESULTS ---------------- #

if st.session_state.generated:

    st.success("✅ Travel Plan Generated Successfully!")

    destination_lower = st.session_state.destination.lower().strip()

    # ---------------- TABS ---------------- #

    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Itinerary",
        "🖼️ Gallery",
        "🌍 Map",
        "📌 Summary"
    ])

    # ---------------- TAB 1 ---------------- #

    with tab1:

        st.header("🧠 AI Generated Travel Plan")

        st.write(st.session_state.result)

        st.markdown("---")

        create_pdf(st.session_state.result)

        with open("AI_Travel_Plan.pdf", "rb") as pdf_file:

            st.download_button(
                label="📄 Download Travel Plan PDF",
                data=pdf_file,
                file_name="AI_Travel_Plan.pdf",
                mime="application/pdf"
            )

    # ---------------- TAB 2 ---------------- #

    with tab2:

        image_files = []

        formats = ["jpg", "jpeg", "png", "webp"]

        for fmt in formats:

            image_files.extend(
                glob.glob(
                    f"images/{destination_lower}*.{fmt}"
                )
            )

        if destination_lower == "kashmir":

            special_places = [
                "baramulla",
                "dallake",
                "sonmarg",
                "gulmarg",
                "kashmir"
            ]

            for place in special_places:

                for fmt in formats:

                    image_files.extend(
                        glob.glob(
                            f"images/{place}*.{fmt}"
                        )
                    )

        unique_images = []

        for img in image_files:

            if img not in unique_images:

                unique_images.append(img)

        if unique_images:

            cols = st.columns(3)

            for index, image_path in enumerate(unique_images):

                try:

                    image = Image.open(image_path)

                    with cols[index % 3]:

                        st.image(
                            image,
                            width='stretch'
                        )

                except:

                    pass

    # ---------------- TAB 3 ---------------- #

    with tab3:

        if destination_lower in city_coordinates:

            latitude, longitude = city_coordinates[destination_lower]

            travel_map = folium.Map(
                location=[latitude, longitude],
                zoom_start=10
            )

            folium.Marker(
                [latitude, longitude],
                popup=st.session_state.destination.title(),
                tooltip=st.session_state.destination.title()
            ).add_to(travel_map)

            st_folium(
                travel_map,
                width=1200,
                height=500
            )

    # ---------------- TAB 4 ---------------- #

    with tab4:

        st.header("📊 Travel Insights")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "📅 Days",
            st.session_state.days
        )

        col2.metric(
            "💰 Budget",
            st.session_state.budget
        )

        col3.metric(
            "🧳 Travel Type",
            st.session_state.travel_type
        )

        col4.metric(
            "🏙️ Destination",
            st.session_state.destination
        )

        st.markdown("---")

        # Hidden Gems

        hidden_gems = {

            "kashmir": "❤️ Hidden Gem: Baramulla — peaceful valleys, mountains, warm & precious people and unforgettable serenity.",

            "goa": "🌴 Hidden Gem: Divar Island",

            "kerala": "🌿 Hidden Gem: Kumbalangi Village",

            "mumbai": "🏛️ Hidden Gem: Banganga Tank",

            "delhi": "🏰 Hidden Gem: Agrasen Ki Baoli"

        }

        destination_lower = st.session_state.destination.lower().strip()

        if destination_lower in hidden_gems:

            st.success(
                hidden_gems[destination_lower]
            )

        # ---------------- DESTINATION HIGHLIGHT ---------------- #

        if destination_lower == "kashmir":

            st.success("""
            🏔 KASHMIR TRAVEL HIGHLIGHT

            ❤️ Must Visit: Baramulla

            Baramulla is one of the most peaceful , beautiful places and people in Kashmir.

            Surrounded by mountains, rivers and greenery, it offers a calm experience away from crowded
            tourist locations.

            Get ready to experience Top-tier dining with ultimate flavor at Ok F Café and Fainaam Restaurant !

            Perfect for people who want to experience the real warmth, culture and serenity of Kashmir.""")

        elif destination_lower == "goa":

            st.success("""
            🌴 GOA TRAVEL HIGHLIGHT

            ❤️ Must Visit: Divar Island

            A peaceful hidden gem away from crowded beaches.

            Enjoy local Goan culture, village life, beautiful churches and scenic landscapes.""")

        elif destination_lower == "kerala":

            st.success("""
            🌿 KERALA TRAVEL HIGHLIGHT

            ❤️ Must Visit: Kumbalangi Village

            Experience authentic backwaters, traditional village life and Kerala's natural beauty.""")

        elif destination_lower == "mumbai":

            st.success("""
            🏙 MUMBAI TRAVEL HIGHLIGHT

            ❤️ Must Visit: Banganga Tank

            One of Mumbai's oldest hidden treasures, offering history, peace and beautiful architecture.""")

        elif destination_lower == "delhi":

            st.success("""
            🏰 DELHI TRAVEL HIGHLIGHT

            ❤️ Must Visit: Agrasen Ki Baoli

            A stunning historical stepwell hidden in the heart of Delhi. """)

        # ---------------- WEATHER DASHBOARD ---------------- #

        st.markdown("---")

        st.subheader("🌦 Destination Weather")

        weather_data = {

            "kashmir": {
            "temp": "18°C",
            "condition": "Cool & Pleasant",
            "best": "Carry warm clothes"
            },

            "goa": {
            "temp": "30°C",
            "condition": "Sunny",
            "best": "Carry sunscreen"
            },

            "mumbai": {
            "temp": "29°C",
            "condition": "Humid",
            "best": "Light clothing recommended"
            },

            "delhi": {
            "temp": "35°C",
            "condition": "Warm",
            "best": "Stay hydrated"
            },

            "kerala": {
            "temp": "28°C",
            "condition": "Tropical",
            "best": "Carry umbrella"
            }

        }

        if destination_lower in weather_data:

            col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
            "🌡 Temperature",
            weather_data[destination_lower]["temp"]
            )

        with col2:
            st.metric(
            "☁ Condition",
            weather_data[destination_lower]["condition"]
            )

        with col3:
            st.metric(
            "🎒 Advice",
            weather_data[destination_lower]["best"]
            )
        
        # ---------------- TOP ATTRACTIONS ---------------- #

        st.markdown("---")

        st.subheader("🏆 Top Attractions")

        if destination_lower == "kashmir":
            col1, col2 = st.columns(2)

            with col1:
                st.image(
                    "images/gulmarg1.jpeg",
                    caption="🏔 Gulmarg"
                )

                st.image(
                    "images/baramulla1.jpeg",
                    caption="❤️ Baramulla"
                )

            with col2:
                st.image(
                    "images/sonmarg1.webp",
                    caption="🌄 Sonmarg"
                )

                st.image(
                    "images/dallake1.webp",
                    caption="🌊 Dal Lake"
                )

        elif destination_lower == "goa":
            col1, col2, col3 = st.columns(3)

            with col1:
                st.image(
                    "images/goa1.webp",
                    caption="🌴 Beaches"
                )

            with col2:
                st.image(
                    "images/goa2.webp",
                    caption="🌅 Sunset"
                )

            with col3:
                st.image(
                    "images/goa3.webp",
                    caption="🍹 Coastal Life"
                )

        elif destination_lower == "kerala":
            col1, col2, col3 = st.columns(3)

            with col1:
                st.image(
                    "images/kerala1.jpeg",
                    caption="🌿 Nature"
                )

            with col2:
                st.image(
                    "images/kerala2.webp",
                    caption="🚣 Backwaters"
                )

            with col3:
                st.image(
                    "images/kerala3.webp",
                    caption="🏞 Village Life"
                )
        # ---------------- TRIP TIMELINE ---------------- #

        st.markdown("---")

        st.subheader("🗓️ Suggested Trip Timeline")

        if destination_lower == "kashmir":

            st.markdown("""
### Day 1 ✈️ Arrival in Srinagar

### Day 2 🌊 Explore Dal Lake

### Day 3 🏔️ Gulmarg Adventure

### Day 4 🌄 Sonmarg Sightseeing

### Day 5 ❤️ Baramulla Experience

### Day 6 🛍️ Shopping & Kashmiri Cuisine

### Day 7 ✈️ Departure
""")

        elif destination_lower == "goa":

            st.markdown("""
### Day 1 🌴 Beach Arrival

### Day 2 🌊 Water Sports

### Day 3 ⛵ Cruise & Sunset

### Day 4 🍹 Cafes & Nightlife

### Day 5 🛍️ Local Markets

### Day 6 🌅 Relaxation Day

### Day 7 ✈️ Departure
""")

        elif destination_lower == "kerala":

            st.markdown("""
### Day 1 🌿 Arrival

### Day 2 🚣 Backwaters Tour

### Day 3 🏞️ Village Exploration

### Day 4 🌴 Tea Gardens

### Day 5 🛍️ Local Culture

### Day 6 🌊 Beach Day

### Day 7 ✈️ Departure
""")

        elif destination_lower == "mumbai":

            st.markdown("""
### Day 1 ✈️ Arrival

### Day 2 🌊 Marine Drive

### Day 3 🏛️ Gateway of India

### Day 4 🎬 Bollywood Tour

### Day 5 🛍️ Colaba Shopping

### Day 6 🌆 City Exploration

### Day 7 ✈️ Departure
""")

        elif destination_lower == "delhi":

            st.markdown("""
### Day 1 ✈️ Arrival

### Day 2 🕌 Red Fort

### Day 3 🏛️ India Gate

### Day 4 🏰 Qutub Minar

### Day 5 🛍️ Chandni Chowk

### Day 6 🍛 Food Tour

### Day 7 ✈️ Departure
""")

        elif destination_lower == "bangalore":

            st.markdown("""
### Day 1 ✈️ Arrival

### Day 2 🌳 Cubbon Park

### Day 3 🏛️ Bangalore Palace

### Day 4 ☕ Cafe Exploration

### Day 5 🛍️ MG Road

### Day 6 🌆 City Tour

### Day 7 ✈️ Departure
""")

        else:

            st.markdown(f"""
### Day 1 ✈️ Arrival in {st.session_state.destination}

### Day 2 🏞️ Explore Attractions

### Day 3 🍴 Local Food Tour

### Day 4 🛍️ Shopping

### Day 5 🌆 City Exploration

### Day 6 📸 Relax & Enjoy

### Day 7 ✈️ Departure
""")
        
        # ---------------- WHY VISIT ---------------- #

        st.markdown("---")

        st.subheader("⭐ Why Visit This Destination?")

        if destination_lower == "kashmir":

            st.info("""
🏔 Snow-covered mountains

🌊 Beautiful lakes

❤️ Peaceful Baramulla with its precious and unforgettable people

🍲 Delicious Kashmiri cuisine

📸 Stunning photography spots
""")

        elif destination_lower == "goa":

            st.info("""
🌴 Beaches

🌅 Sunsets

🍹 Nightlife

🌊 Water Sports

🎶 Relaxed Vibes
""")

        elif destination_lower == "kerala":

            st.info("""
🚣 Backwaters

🌿 Green Landscapes

🍛 Traditional Food

🏞 Nature

🌴 Relaxation
""")

        elif destination_lower == "mumbai":

            st.info("""
🏙 City Life

🌊 Marine Drive

🎬 Bollywood

🍴 Street Food

🛍 Shopping
""")

        elif destination_lower == "delhi":

            st.info("""
🏰 Historical Monuments

🍴 Famous Food

🕌 Rich Culture

🛍 Markets

📸 Heritage Sites
""")

        elif destination_lower == "bangalore":

            st.info("""
🌳 Parks

☕ Cafes

💻 Tech Hub

🍴 Food Scene

🌆 Modern Lifestyle
""")

        # ---------------- BUDGET BREAKDOWN ---------------- #

        st.markdown("---")

        st.subheader("💰 Estimated Budget Breakdown")

        if st.session_state.budget == "Low":

            flight_cost = 5000
            hotel_cost = 6000
            food_cost = 3000
            transport_cost = 2000

        elif st.session_state.budget == "Medium":

            flight_cost = 8000
            hotel_cost = 12000
            food_cost = 5000
            transport_cost = 3000

        else:

            flight_cost = 15000
            hotel_cost = 25000
            food_cost = 8000
            transport_cost = 5000

        total = (
            flight_cost
            + hotel_cost
            + food_cost
            + transport_cost
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric("✈️ Flights", f"Rs. {flight_cost}")

            st.metric("🏨 Hotels", f"Rs. {hotel_cost}")

        with col2:

            st.metric("🍴 Food", f"Rs. {food_cost}")

            st.metric("🚕 Transport", f"Rs. {transport_cost}")

        st.success(
            f"💸 Estimated Total Budget: Rs. {total}"
        )

        # ---------------- DESTINATION SCORE ---------------- #

        st.markdown("---")

        st.subheader("🏆 Destination Score")

        destination_scores = {

        "kashmir": {
            "Scenery": 10,
            "Food": 9,
            "Adventure": 10,
            "Budget": 8
        },

        "goa": {
            "Scenery": 8,
            "Food": 9,
            "Adventure": 9,
            "Budget": 8
        },

        "kerala": {
            "Scenery": 9,
            "Food": 8,
            "Adventure": 7,
            "Budget": 8
        },

        "mumbai": {
            "Scenery": 7,
            "Food": 10,
            "Adventure": 8,
            "Budget": 6
        },

        "delhi": {
            "Scenery": 8,
            "Food": 9,
            "Adventure": 7,
            "Budget": 8
        }

    }

    if destination_lower in destination_scores:

        scores = destination_scores[destination_lower]

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "🌄 Scenery",
                f"{scores['Scenery']}/10"
            )

            st.metric(
                "🍲 Food",
                f"{scores['Food']}/10"
            )

        with col2:

            st.metric(
                "🎯 Adventure",
                f"{scores['Adventure']}/10"
            )

            st.metric(
                "💰 Budget",
                f"{scores['Budget']}/10"
            )

        overall = round(
            sum(scores.values()) / len(scores),
            1
        )

        st.success(
            f"⭐ Overall Destination Score: {overall}/10"
        )

        # ---------------- PACKING CHECKLIST ---------------- #

        st.markdown("---")

        st.subheader("🎒 Packing Checklist")

        st.checkbox("Phone Charger")
        st.checkbox("Power Bank")
        st.checkbox("Identity Card")
        st.checkbox("Medicines")
        st.checkbox("Water Bottle")

        if destination_lower == "kashmir":
            st.checkbox("Winter Jacket")
            st.checkbox("Gloves")
            st.checkbox("Woollen Cap")

        elif destination_lower == "goa":
            st.checkbox("Sunscreen")
            st.checkbox("Beachwear")
            st.checkbox("Sunglasses")

        elif destination_lower == "kerala":
            st.checkbox("Umbrella")
            st.checkbox("Light Cotton Clothes")

        # ---------------- FOOTER ---------------- #

        st.markdown("---")

        st.markdown(
            """
            <center>
            Made using Python, Streamlit and Groq AI
            </center>
            """,
            unsafe_allow_html=True
        )

        if st.session_state.generated:

            if st.session_state.destination.lower() == "kashmir":

                st.caption(
                    "❤️ Special recommendation: Spend a peaceful day in Baramulla."
                    )
    
