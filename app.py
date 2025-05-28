# location_app.py
from davia import Davia
from geopy.geocoders import Nominatim
import folium

# Initialize the Davia app
app = Davia()

# Initialize geocoder
geolocator = Nominatim(user_agent="LocationApp")

# Task 1: Search for a place and return coordinates
@app.task
def search_place(place: str) -> dict:
    """
    Search for a place and return its coordinates.
    Args:
        place (str): Name of the place to search for (e.g., "New York").
    Returns:
        dict: Contains latitude, longitude, and place name.
    """
    try:
        location = geolocator.geocode(place)
        if location:
            return {
                "place": place,
                "latitude": location.latitude,
                "longitude": location.longitude,
            }
        else:
            return {"error": f"Could not find location: {place}"}
    except Exception as e:
        return {"error": str(e)}

# Task 2: Get location details from coordinates
@app.task
def get_location_info(latitude: float, longitude: float) -> dict:
    """
    Get location details from coordinates.
    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
    Returns:
        dict: Contains address details.
    """
    try:
        location = geolocator.reverse((latitude, longitude))
        if location:
            return {
                "address": location.address,
                "latitude": latitude,
                "longitude": longitude,
            }
        else:
            return {"error": "Could not retrieve location details"}
    except Exception as e:
        return {"error": str(e)}

# Task 3: Generate a map with a marker at the specified location
@app.task
def generate_map(latitude: float, longitude: float) -> str:
    """
    Generate an interactive map with a marker at the specified location.
    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
    Returns:
        str: HTML content of the map (Davia will render it in the UI).
    """
    try:
        # Create a map centered at the given coordinates
        m = folium.Map(location=[latitude, longitude], zoom_start=15)
        # Add a marker
        folium.Marker([latitude, longitude], popup="Location").add_to(m)
        # Save the map as HTML string
        return m._repr_html_()
    except Exception as e:
        return f"Error generating map: {str(e)}"

# Run the app (optional, for local testing)
if __name__ == "__main__":
    app.run()