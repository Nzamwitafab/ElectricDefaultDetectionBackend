import pandas as pd # type: ignore
from sklearn.model_selection import train_test_split # type: ignore
from sklearn.preprocessing import StandardScaler, OneHotEncoder # type: ignore
from sklearn.compose import ColumnTransformer # type: ignore
from sklearn.pipeline import Pipeline # type: ignore
from sklearn.ensemble import RandomForestClassifier # type: ignore
from sklearn.metrics import classification_report # type: ignore
import joblib # type: ignore

# Load the dataset
df = pd.read_csv('dataset.csv')

# Preprocessing
# Separate features and target
X = df.drop(['Fault ID', 'Fault Type'], axis=1)
y = df['Fault Type']

# Identify categorical and numerical columns
categorical_cols = ['Fault Location', 'Weather Condition', 
                    'Maintenance Status', 'Component Health']
numerical_cols = ['Voltage (V)', 'Current (A)', 'Power Load (MW)', 'Temperature (°C)', 
                 'Wind Speed (km/h)', 'Duration of Fault (hrs)', 'Down time (hrs)']

# Create transformers
numerical_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

# Create preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

# Create pipeline with Random Forest Classifier
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save the model
joblib.dump(model, 'fault_type_predictor.joblib')

print("Model trained and saved successfully!")