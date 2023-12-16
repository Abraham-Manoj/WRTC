import numpy as np
import pandas as pd
import pickle
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from datetime import datetime

# Function to calculate Haversine distance
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat / 2) ** 2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c
    return distance

# Function to get time of day
def get_time_of_day():
    now = datetime.now()
    current_hour = now.hour
    if 5 <= current_hour < 12:
        time_of_day = "morning"
    elif 12 <= current_hour < 18:
        time_of_day = "afternoon"
    else:
        time_of_day = "evening"
    return time_of_day

# Function to get day of the week
def get_day_of_week():
    now = datetime.now()
    return now.strftime("%A")

# Function to calculate ETA
def eta(latitude_user, longitude_user, latitude_bus, longitude_bus):
    # Calculate Haversine distance
    distance = haversine_distance(latitude_user, longitude_user, latitude_bus, longitude_bus)

    # Get time of day and day of the week
    time_of_day = get_time_of_day()
    day_of_week = get_day_of_week()

    # Load the pre-trained model using pickle
    with open('linear_regression_model.pkl', 'rb') as model_file:
        loaded_model = pickle.load(model_file)

    # Prepare data for prediction
    new_data = {
        'bus_latitude': [latitude_bus],
        'bus_longitude': [longitude_bus],
        'distance': [distance],
        'time_of_day': [time_of_day],
        'day_of_week': [day_of_week]
    }

    # Convert the dictionary to a DataFrame
    new_data_df = pd.DataFrame(new_data)

    # Load the preprocessor from the pipeline
    preprocessor = loaded_model.named_steps['preprocessor']

    # Preprocess the new data
    new_data_transformed = preprocessor.transform(new_data_df)

    # Make prediction using the loaded model
    predicted_eta = loaded_model.named_steps['regressor'].predict(new_data_transformed)

    return predicted_eta[0]# Assuming the model returns a single prediction

# Example usage:
latitude_user = 40.123
longitude_user = -74.567
latitude_bus = 40.456
longitude_bus = -74.789

estimated_eta = eta(latitude_user, longitude_user, latitude_bus, longitude_bus)
print(f'Estimated ETA: {estimated_eta} minutes')
print(haversine_distance(latitude_user, longitude_user, latitude_bus, longitude_bus))
