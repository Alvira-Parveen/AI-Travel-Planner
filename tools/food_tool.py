food_data = {

    "goa": {
        "foods": [
            "Goan Fish Curry",
            "Prawn Balchao",
            "Bebinca",
            "Chicken Cafreal"
        ],
        "restaurants": [
            "Fisherman's Wharf",
            "Thalassa",
            "Gunpowder",
            "Vinayak Family Restaurant"
        ]
    },

    "mumbai": {
        "foods": [
            "Vada Pav",
            "Pav Bhaji",
            "Bombay Sandwich",
            "Bhel Puri"
        ],
        "restaurants": [
            "Leopold Cafe",
            "Bademiya",
            "Britannia & Co",
            "Cafe Mondegar"
        ]
    },

    "delhi": {
        "foods": [
            "Chole Bhature",
            "Butter Chicken",
            "Parathas",
            "Kebabs"
        ],
        "restaurants": [
            "Karim's",
            "Indian Accent",
            "Paranthe Wali Gali",
            "Moti Mahal"
        ]
    },

    "kashmir": {
        "foods": [
            "Rogan Josh",
            "Gushtaba",
            "Kahwa",
            "Yakhni"
        ],
        "restaurants": [
            "Lazeez Restaurant",
            "Ok F Café",
            "Fainaam Restaurant",
            "Mughal Darbar",
            "Shinam Restaurant"
        ]
    },

    "kerala": {
        "foods": [
            "Appam",
            "Puttu and Kadala Curry",
            "Kerala Fish Curry",
            "Payasam"
        ],
        "restaurants": [
            "Paragon Restaurant",
            "Kethal's Chicken",
            "Grand Pavilion",
            "Dhe Puttu"
        ]
    }
}


def get_food_recommendations(city):

    city = city.lower()

    if city not in food_data:
        return "Food recommendations unavailable."

    data = food_data[city]

    foods = "\n".join(
        [f"• {food}" for food in data["foods"]]
    )

    restaurants = "\n".join(
        [f"• {restaurant}" for restaurant in data["restaurants"]]
    )

    return f"""
FAMOUS LOCAL FOODS:
{foods}

BEST RESTAURANTS:
{restaurants}
"""