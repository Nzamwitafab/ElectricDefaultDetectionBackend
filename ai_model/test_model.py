import joblib
import pandas as pd

# Load the trained model
model = joblib.load('fault_type_predictor.joblib')

# Define your test data (replace with actual values)
test_data = pd.DataFrame({
    'Voltage (V)': [230], 
    'Current (A)': [15], 
    'Power Load (MW)': [3.45], 
    'Temperature (°C)': [25], 
    'Wind Speed (km/h)': [10], 
    'Duration of Fault (hrs)': [0.5], 
    'Down time (hrs)': [2],
    'Fault Location': ['Kigali, Kicukiro'], 
    'Weather Condition': ['Sunny'], 
    'Maintenance Status': ['Good'], 
    'Component Health': ['Optimal']
})

# Make predictions
predictions = model.predict(test_data)

# Output predictions
print("Predicted Fault Type:", predictions)
