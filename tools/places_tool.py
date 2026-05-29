import json


def search_places(city, place_type=None, min_rating=None):
    """
    Search tourist places based on city, type, and rating.
    """

    try:

        # Load places data
        with open("data/places.json", "r") as file:
            places = json.load(file)

        matching_places = []

        # Filter places
        for place in places:

            # Match city
            if place["city"].lower() != city.lower():
                continue

            # Match place type
            if place_type is not None:
                if place["type"].lower() != place_type.lower():
                    continue

            # Match minimum rating
            if min_rating is not None:
                if place["rating"] < min_rating:
                    continue

            matching_places.append(place)

        # No places found
        if not matching_places:
            return "No places found."

        # Sort by highest rating
        matching_places.sort(key=lambda x: x["rating"], reverse=True)

        # Format output
        formatted_places = []

        for place in matching_places:

            formatted_places.append(
                f"""
Place ID: {place['place_id']}
Place Name: {place['name']}
City: {place['city']}
Type: {place['type']}
Rating: {place['rating']}
-----------------------------------
"""
            )

        return "\n".join(formatted_places)

    except Exception as e:
        return f"Error: {str(e)}"