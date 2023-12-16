import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pickle

# Load data from the CSV file
data = pd.read_csv('dataset.csv')

# Assuming 'eta' is the target variable
X = data[['bus_latitude', 'bus_longitude', 'distance', 'time_of_day', 'day_of_week']]
y = data['eta']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define a preprocessing pipeline (including OneHotEncoder for categorical features)
preprocessor = ColumnTransformer(
    transformers=[
        ('time_and_day', OneHotEncoder(), ['time_of_day', 'day_of_week'])
    ],
    remainder='passthrough'
)

# Combine preprocessing with the linear regression model
model = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

# Train the model
model.fit(X_train, y_train)

# Save the trained model using pickle
with open('linear_regression_model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)
