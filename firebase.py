import firebase_admin
from firebase_admin import credentials, db
import folium

# Replace 'path/to/your/credentials.json' with the actual path to your Firebase private key file
cred = credentials.Certificate('secret.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://bustracking-1618a-default-rtdb.asia-southeast1.firebasedatabase.app/'})

# Function to store data in the Realtime Database
def store_location(busID, latitude, longitude):
    ref = db.reference('locations/' + str(busID))
    ref.set({
        'latitude': latitude,
        'longitude': longitude
    })


def get_current_coordinates(busID):
    ref = db.reference('locations/' + str(busID))
    snapshot = ref.get()

    if snapshot:
        latitude = snapshot.get('latitude')
        longitude = snapshot.get('longitude')
        if latitude is not None and longitude is not None:
            print(f"Driver {busID} is currently at coordinates: Latitude {latitude}, Longitude {longitude}")
            mark_pin_on_map(latitude,longitude,busID)
        else:
            print(f"Driver {busID} coordinates not found.")
    else:
        print(f"Driver {busID} not found.")

def mark_pin_on_map(latitude, longitude, busID):
    if latitude is not None and longitude is not None:
        # Create a folium map centered at the given coordinates
        my_map = folium.Map(location=[latitude, longitude], zoom_start=15)

        # Mark a pin at the driver's location
        folium.Marker(
            location=[latitude, longitude],
            popup=f"Driver {busID}",
            icon=folium.Icon(color='blue')
        ).add_to(my_map)
        # Save the map as an HTML file
        my_map.save("./templates/map.html")
get_current_coordinates("ravi")