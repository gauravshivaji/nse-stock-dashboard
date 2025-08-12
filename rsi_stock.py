import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

st.set_page_config(page_title="🏠 House Price Prediction", layout="centered")
st.title("🏠 House Price Prediction using Linear Regression")

# Load dataset
st.subheader("Upload CSV Dataset")
uploaded_file = st.file_uploader("Upload your dataset (must include area, bedrooms, location, price)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### Dataset Preview", df.head())

    # Encode location (if categorical)
    if df['location'].dtype == 'object':
        df = pd.get_dummies(df, columns=['location'], drop_first=True)

    X = df.drop("price", axis=1)
    y = df["price"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)

    # Evaluation
    st.write(f"**R² Score:** {r2_score(y_test, y_pred):.2f}")
    st.write(f"**RMSE:** {np.sqrt(mean_squared_error(y_test, y_pred)):.2f}")

    # Plot
    fig, ax = plt.subplots()
    ax.scatter(y_test, y_pred, alpha=0.7)
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
    ax.set_xlabel("Actual Price")
    ax.set_ylabel("Predicted Price")
    st.pyplot(fig)

    # User prediction
    st.subheader("Predict a New Price")
    input_data = {}
    for col in X.columns:
        input_data[col] = st.number_input(f"Enter {col}", value=float(X[col].mean()))
    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)[0]
    st.success(f"Predicted Price: ₹{prediction:,.2f}")
else:
    st.info("Please upload a dataset to start.")
