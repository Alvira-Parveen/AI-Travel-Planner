import json


def search_hotels(city, max_price=None, min_stars=None):
    """
    Search hotels based on city, price, and star rating.
    """

    try:

        # Load hotel data
        with open("data/hotels.json", "r") as file:
            hotels = json.load(file)

        matching_hotels = []

        # Filter hotels
        for hotel in hotels:

            if hotel["city"].lower() == city.lower():

                # Filter by max price
                if max_price is not None:
                    if hotel["price_per_night"] > max_price:
                        continue

                # Filter by minimum stars
                if min_stars is not None:
                    if hotel["stars"] < min_stars:
                        continue

                matching_hotels.append(hotel)

        # No hotels found
        if not matching_hotels:
            return "No hotels found."

        # Sort by cheapest price
        matching_hotels.sort(key=lambda x: x["price_per_night"])

        # Format output
        formatted_hotels = []

        for hotel in matching_hotels:

            formatted_hotels.append(
                f"""
Hotel ID: {hotel['hotel_id']}
Hotel Name: {hotel['name']}
City: {hotel['city']}
Stars: {hotel['stars']}
Price Per Night: ₹{hotel['price_per_night']}
Amenities: {', '.join(hotel['amenities'])}
-----------------------------------
"""
            )

        return "\n".join(formatted_hotels)

    except Exception as e:
        return f"Error: {str(e)}"