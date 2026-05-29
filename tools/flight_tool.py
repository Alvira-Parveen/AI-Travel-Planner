import json


def search_flights(source, destination):
    """
    Search flights between source and destination.
    """

    try:

        # Load flight data
        with open("data/flights.json", "r") as file:
            flights = json.load(file)

        matching_flights = []

        # Filter matching flights
        for flight in flights:

            if (
                flight["from"].strip().lower() == source.strip().lower()
                and
                flight["to"].strip().lower() == destination.strip().lower()
            ):

                matching_flights.append(flight)

        # No flights found
        if not matching_flights:
            return "No flights found."

        # Sort by cheapest price
        matching_flights.sort(key=lambda x: x["price"])

        # Format output
        formatted_flights = []

        for flight in matching_flights:

            formatted_flights.append(
                f"""
Flight ID: {flight['flight_id']}
Airline: {flight['airline']}
From: {flight['from']}
To: {flight['to']}
Departure: {flight['departure_time']}
Arrival: {flight['arrival_time']}
Price: ₹{flight['price']}
-----------------------------------
"""
            )

        return "\n".join(formatted_flights)

    except Exception as e:
        return f"Error: {str(e)}"