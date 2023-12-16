import firebase_admin
from firebase_admin import credentials, db
import folium

# Replace 'path/to/your/credentials.json' with the actual path to your Firebase private key file
cred = credentials.Certificate('secret.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://mappy-1382f-default-rtdb.firebaseio.com/'})

# Function to store data in the Realtime Database
def store_location(driver_id, latitude, longitude):
    ref = db.reference('locations/' + str(driver_id))
    ref.set({
        'latitude': latitude,
        'longitude': longitude
    })


def get_current_coordinates(driver_id):
    ref = db.reference('locations/' + str(driver_id))
    snapshot = ref.get()

    if snapshot:
        latitude = snapshot.get('latitude')
        longitude = snapshot.get('longitude')
        if latitude is not None and longitude is not None:
            print(f"Driver {driver_id} is currently at coordinates: Latitude {latitude}, Longitude {longitude}")
            mark_pin_on_map(latitude,longitude,driver_id)
        else:
            print(f"Driver {driver_id} coordinates not found.")
    else:
        print(f"Driver {driver_id} not found.")

def mark_pin_on_map(latitude, longitude, driver_id):
    if latitude is not None and longitude is not None:
        # Create a folium map centered at the given coordinates
        my_map = folium.Map(location=[latitude, longitude], zoom_start=15)

        # Mark a pin at the driver's location
        folium.Marker(
            location=[latitude, longitude],
            popup=f"Driver {driver_id}",
            icon=folium.Icon(color='blue')
        ).add_to(my_map)
        # Save the map as an HTML file
        my_map.save("./templates/map.html")
get_current_coordinates("ravi")