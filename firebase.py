import firebase_admin
from firebase_admin import credentials, db

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
        else:
            print(f"Driver {driver_id} coordinates not found.")
    else:
        print(f"Driver {driver_id} not found.")

