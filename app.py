from flask import Flask, render_template, request,jsonify
from firebase import   get_current_coordinates ,store_location

app = Flask(__name__)


drivers = {
    'driver123': {'password': '123', 'name': 'suresh', 'busID': '01'},
    # Add more users as needed
}
busID = ""

@app.route('/')
def driver_login():
    return render_template('driver_login.html')

@app.route('/driver_auth', methods=['POST'])
def driver_auth():
    data = request.get_json()
    driver_id = data.get('driverId')
    password = data.get('password')

    # Check if user exists and the password is correct (replace with database queries)
    if driver_id in drivers and drivers[driver_id]['password'] == password:
        busID = drivers[driver_id]['busID']
        return jsonify({'success': True, 'message': 'Login successful', 'name': drivers[driver_id]['name']})
    else:
        return jsonify({'success': False, 'message': 'Login failed'})

@app.route('/driver_track')
def driver_track():
    return render_template('driver_track.html')

#Live Location from Driver Below:>
@app.route('/process_data', methods=['POST'])
def process_data():
    try:
        driver_id = "driver123"
        data_from_js = request.get_json()
        lattitude = data_from_js.get('latitude')
        longitude = data_from_js.get('longitude')
        #passing data to Firbase real time database: 
        #pass_to_firebase(busID, lattitude, longitude)
        print(busID, lattitude, longitude)
        store_location(driver_id,lattitude,longitude)
        return jsonify({'status': 'success'})
        
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)})
    
#####
#####   THIS IS WEHRE USER STARTS
####

@app.route('/user')
def user():
    return render_template('user.html')


@app.route('/submit', methods=['POST'])
def submit():
    try:
        data_from_js = request.get_json()
        selected_value = data_from_js.get('user_value')
        print(selected_value)
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
    


    
