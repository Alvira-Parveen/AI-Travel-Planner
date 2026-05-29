from groq import Groq

from tools.flight_tool import search_flights
from tools.hotel_tool import search_hotels
from tools.places_tool import search_places
from tools.weather_tool import get_weather
from tools.food_tool import get_food_recommendations


# ---------------- GROQ CLIENT ---------------- #
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

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


# ---------------- MAIN FUNCTION ---------------- #

def run_travel_agent(
    source,
    destination,
    budget,
    days,
    travel_type
):

    # ---------------- FLIGHTS ---------------- #

    flights = search_flights(
        source,
        destination
    )

    # ---------------- HOTELS ---------------- #

    if budget == "Low":

        hotels = search_hotels(
            destination,
            max_price=3000
        )

    elif budget == "Medium":

        hotels = search_hotels(
            destination,
            max_price=6000
        )

    else:

        hotels = search_hotels(destination)

    # ---------------- PLACES ---------------- #

    places = search_places(destination)

    # ---------------- FOOD ---------------- #

    foods = get_food_recommendations(destination)

    # ---------------- WEATHER ---------------- #

    weather = "Weather data unavailable."

    destination_lower = destination.lower()

    if destination_lower in city_coordinates:

        latitude, longitude = city_coordinates[destination_lower]

        weather = get_weather(
            latitude,
            longitude
        )

    # ---------------- PROMPT ---------------- #

    prompt = f"""

You are an advanced AI Travel Planner.

Create a beautiful, intelligent, and highly personalized travel plan.

---------------- TRAVEL DETAILS ----------------

Source: {source}

Destination: {destination}

Budget: {budget}

Trip Duration: {days} Days

Travel Type: {travel_type}

---------------- FLIGHTS ----------------

{flights}

---------------- HOTELS ----------------

{hotels}

---------------- TOURIST PLACES ----------------

{places}

---------------- FOOD & RESTAURANTS ----------------

{foods}

---------------- WEATHER ----------------

{weather}

---------------- IMPORTANT INSTRUCTIONS ----------------

1. You MUST use the flight data provided above.
   If flight data exists, do NOT say "No flights found".
   Recommend the cheapest and best available flight option.

2. You MUST use the hotel data provided above.
   If hotel data exists, do NOT generate generic hotel recommendations.
   Recommend the best available hotel from the supplied data based on budget.

3. Make itinerary visually beautiful and engaging.

4. If destination is Kashmir:
    - Include one peaceful day in Baramulla.
    - Describe Baramulla emotionally and beautifully.
    - Mention nature, peace, mountains, local warmth, and serenity.
    - Include kashmiris cuisine recommendations:
            "Rogan Josh",
            "Gushtaba",
            "Kahwa",
            "Yakhni"
        ],
        "restaurants": 
            "Lazeez Restaurant",
            "Ok F Café",
            "Fainaam Restaurant",
            "Mughal Darbar",
            "Shinam Restaurant"

5. Use 1 or 2 emojis only to enhance visual appeal.

6. Create a highly detailed, premium quality travel itinerary.

7. Every section must contain detailed explanations and descriptive paragraphs.

8. Do NOT give only short bullet points.

9. Write in a professional travel-guide style.

10. Explain WHY a flight, hotel, place, restaurant or activity is recommended.

11. Each section should contain multiple sentences and meaningful details, complete paragraphs and not just one-line points.

12. Use rich descriptions, local insights, travel tips and recommendations.

13. Generate a complete day-by-day itinerary with Morning, Afternoon and Evening activities.

14. Describe tourist attractions in detail instead of only naming them.

15. Describe hotels with their facilities, atmosphere, location benefits and suitability for the selected travel type.

16. Describe local food, famous dishes and dining experiences in detail.

17. Include transportation recommendations between attractions.

18. Include weather-related travel advice.

19. Include local culture, traditions and etiquette.

20. Include hidden gems and lesser-known experiences.

21. Include photography spots and best locations for memorable pictures.

22. Include shopping recommendations and local markets.

23. Format the output using clear headings and detailed content.

24. End the itinerary with a detailed section titled:

    "Why This Destination Will Leave You With Unforgettable Memories"
    written as a heartfelt travel conclusion.

25. Give Food Recommendations based on the destination's local cuisine and must-try dishes.

26. Travel Type Guidance:
- Family → family-friendly places
- Couple → romantic places
- Adventure → thrilling activities
- Solo → exploration-focused itinerary
- Friends → nightlife and fun activities

27. Budget Guidance:
- Low → affordable suggestions
- Medium → balanced suggestions
- Luxury → premium recommendations

28. If flight data, hotel data, places data or food data are provided, you MUST use them directly.

    Do not ignore provided data.

    Do not generate generic fallback recommendations when actual data exists.

"""
    print("\n====================")
    print("SOURCE:", source)
    print("DESTINATION:", destination)

    print("\nFLIGHTS DATA:")
    print(flights)

    print("\nHOTELS DATA:")
    print(hotels)

    print("====================\n")

    print("\n========== FLIGHTS ==========")
    print(flights)

    print("\n========== HOTELS ==========")
    print(hotels)

    print("\n========== PLACES ==========")
    print(places)

    print("\n========== FOOD ==========")
    print(foods)

    # ---------------- AI RESPONSE ---------------- #
    
    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.7

    )

    return response.choices[0].message.content
