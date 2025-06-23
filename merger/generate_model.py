import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
import pickle

# Dummy data (same as in notebook)
X = pd.DataFrame({
    "Gender": ["male", "female"],
    "Age": [25, 30],
    "Height": [175, 160],
    "Weight": [70, 55],
    "Duration": [30, 45],
    "Heart_Rate": [120, 130],
    "Body_Temp": [37.0, 38.0]
})
y = [200, 220]  # Calories burnt

# Preprocessing and pipeline
preprocessor = ColumnTransformer([
    ("gender", OneHotEncoder(handle_unknown='ignore'), [0]),
    ("num", StandardScaler(), [1, 2, 3, 4, 5, 6])
])

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", LinearRegression())
])

# Fit and save model
pipeline.fit(X.values, y)

# Save the model
with open("pipeline.pkl", "wb") as f:
    pickle.dump(pipeline, f)

print("✅ Model saved successfully as 'pipeline.pkl'")
print("You can now run app.py")