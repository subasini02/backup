import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split, KFold, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.compose import ColumnTransformer
import numpy as np

# Function to convert time to seconds since midnight
def time_to_seconds(t):
    return t.hour * 3600 + t.minute * 60 + t.second

# Streamlit app title
st.title("Model Comparison and Prediction App")

# Upload CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    # Load the dataset
    data = pd.read_csv(uploaded_file)

    # Data preprocessing
    data['order_date'] = pd.to_datetime(data['order_date'], format='%d-%m-%Y')
    data['status_6_time'] = pd.to_datetime(data['status_6_timestamp'], format='%d-%m-%Y %H:%M').dt.time
    data['status_13_time'] = pd.to_datetime(data['status_13_timestamp'], format='%d-%m-%Y %H:%M').dt.time
    data['status_6_time'] = data['status_6_time'].apply(time_to_seconds)
    data['status_13_time'] = data['status_13_time'].apply(time_to_seconds)
    
    if 'day_name' not in data.columns:
        data['day_name'] = data['order_date'].dt.day_name()

    # Separate features and target variable
    X = data.drop(columns=["entity_id", "order_date", "food_prep_time", "status_6_timestamp", "status_13_timestamp"])
    y = data["food_prep_time"]

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define preprocessing steps
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(), ['hour_category', 'day_name']),
            ('num', StandardScaler(), ['status_6_time', 'status_13_time'])
        ],
        remainder='passthrough'
    )

    # Define models
    models = [
        ("Linear Regression", LinearRegression()),
        ("Random Forest", RandomForestRegressor()),
        ("Gradient Boosting", GradientBoostingRegressor()),
        ("Support Vector Machine", SVR())
    ]

    # Define pipeline for preprocessing and model
    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", None)
    ])

    # Perform k-fold cross-validation and grid search for each model
    results = {}
    for name, model in models:
        pipeline.set_params(model=model)
        kfold = KFold(n_splits=5, shuffle=True, random_state=42)
        grid_search = GridSearchCV(estimator=pipeline, param_grid={}, scoring='neg_mean_absolute_error', cv=kfold)
        grid_search.fit(X_train, y_train)
        results[name] = {
            "best_params": grid_search.best_params_,
            "best_score": -grid_search.best_score_,
            "model": grid_search.best_estimator_
        }

    # Select the best model based on cross-validation performance
    best_model_name = min(results, key=lambda x: results[x]["best_score"])
    best_model = results[best_model_name]["model"]

    # Train the best model on the entire dataset
    best_model.fit(X, y)
    st.write(f"### Best Model: {best_model_name}")

    # Evaluate the best model on the test set
    y_pred = best_model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    st.write(f"### Performance of the Best Model on Test Set")
    st.write(f"Mean Absolute Error: {mae:.2f}")
    st.write(f"Mean Squared Error: {mse:.2f}")
    st.write(f"Root Mean Squared Error: {rmse:.2f}")
    st.write(f"R² Score: {r2:.2f}")

    # Allow users to input new data for prediction
    st.write("### Input New Data for Prediction")
    hour_category = st.selectbox("Hour Category", data['hour_category'].unique())
    day_name = st.selectbox("Day Name", data['day_name'].unique())
    status_6_time = st.text_input("Status 6 Time (HH:MM:SS)", "12:00:00")
    status_13_time = st.text_input("Status 13 Time (HH:MM:SS)", "12:00:00")

    if st.button("Predict"):
        new_data = pd.DataFrame({
            'hour_category': [hour_category],
            'day_name': [day_name],
            'status_6_time': [time_to_seconds(pd.to_datetime(status_6_time, format='%H:%M:%S').time())],
            'status_13_time': [time_to_seconds(pd.to_datetime(status_13_time, format='%H:%M:%S').time())]
        })

        new_data_preprocessed = preprocessor.transform(new_data)
        prediction = best_model.predict(new_data_preprocessed)

        st.write(f"### Predicted Food Preparation Time: {prediction[0]:.2f} minutes")

# To run this Streamlit app, use the command:
# streamlit run app.py
