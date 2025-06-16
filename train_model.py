import json
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error
import joblib

# Load data
with open("training_data.json") as f:
    data = json.load(f)

# Convert to DataFrame
records = []
for entry in data:
    features = entry["features"]
    features["label"] = entry["label"]
    records.append(features)

df = pd.DataFrame(records)

# Separate features and label
X = df.drop("label", axis=1)
y = df["label"]

# One-hot encode 'content_type'
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
encoded_content = encoder.fit_transform(X[["content_type"]])
encoded_df = pd.DataFrame(encoded_content, columns=encoder.get_feature_names_out(["content_type"]))

# Drop original column and join encoded
X = X.drop("content_type", axis=1)
X = X.reset_index(drop=True)
X_encoded = pd.concat([X, encoded_df], axis=1)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Model trained. MSE: {mse:.4f}")

# Save model and encoder
joblib.dump(model, "model.pkl")
joblib.dump(encoder, "encoder.pkl")

print("model.pkl and encoder.pkl saved successfully.")
