
import streamlit as st
import joblib
from pathlib import Path
import pandas as pd

# --------------------------------
# 1. Page configuration
# --------------------------------
st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide"
)
if st.button("🔄 New Prediction"):
    st.rerun()

# --------------------------------
# 2. Load the trained model
# --------------------------------
BASE_DIR = Path(__file__).resolve().parent

model = joblib.load(
    BASE_DIR / "models" / "churn_model.pkl"
)

feature_names = joblib.load(
    BASE_DIR / "models" / "feature_names.pkl"
)

# --------------------------------
# 3. Application title
# --------------------------------
st.title("📊 Customer Churn Prediction")

st.write(
    "Predict whether a customer is likely to "
    "stay or leave using a Machine Learning model."
)

# --------------------------------
# 4. Sidebar
# --------------------------------
st.sidebar.title("About the Project")

st.sidebar.write(
    "This application uses Logistic Regression "
    "to predict customer churn."
)

st.sidebar.write("Dataset: IBM Telco Customer Churn")
st.sidebar.write("Model: Logistic Regression")
st.sidebar.write("Features: 30")
st.sidebar.subheader("Model Performance")
st.sidebar.write("Test Accuracy: 80.48%")
st.sidebar.write("ROC-AUC: 84.27%")

# --------------------------------
# 5. Customer input form
# --------------------------------
st.header("Enter Customer Details")

with st.form("customer_form"):

    st.subheader("Personal Information")

    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox(
            "Gender",
            ["Female", "Male"]
        )

        senior_citizen = st.selectbox(
            "Senior Citizen",
            [0, 1],
            format_func=lambda x: "Yes" if x == 1 else "No"
        )

        partner = st.selectbox(
            "Partner",
            ["Yes", "No"]
        )

        dependents = st.selectbox(
            "Dependents",
            ["Yes", "No"]
        )

    with col2:
        tenure = st.number_input(
            "Tenure (months)",
            min_value=0,
            max_value=72,
            value=12,
            step=1
        )

        phone_service = st.selectbox(
            "Phone Service",
            ["Yes", "No"]
        )

        multiple_lines = st.selectbox(
            "Multiple Lines",
            ["No", "Yes", "No phone service"]
        )

    st.subheader("Internet Services")

    col3, col4 = st.columns(2)

    with col3:
        internet_service = st.selectbox(
            "Internet Service",
            ["DSL", "Fiber optic", "No"]
        )

        online_security = st.selectbox(
            "Online Security",
            ["Yes", "No", "No internet service"]
        )

        online_backup = st.selectbox(
            "Online Backup",
            ["Yes", "No", "No internet service"]
        )

        device_protection = st.selectbox(
            "Device Protection",
            ["Yes", "No", "No internet service"]
        )

    with col4:
        tech_support = st.selectbox(
            "Tech Support",
            ["Yes", "No", "No internet service"]
        )

        streaming_tv = st.selectbox(
            "Streaming TV",
            ["Yes", "No", "No internet service"]
        )

        streaming_movies = st.selectbox(
            "Streaming Movies",
            ["Yes", "No", "No internet service"]
        )

    st.subheader("Account Information")

    col5, col6 = st.columns(2)

    with col5:
        contract = st.selectbox(
            "Contract",
            ["Month-to-month", "One year", "Two year"]
        )

        paperless_billing = st.selectbox(
            "Paperless Billing",
            ["Yes", "No"]
        )

        payment_method = st.selectbox(
            "Payment Method",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)"
            ]
        )

    with col6:
        monthly_charges = st.number_input(
            "Monthly Charges",
            min_value=0.0,
            value=70.0,
            step=1.0
        )

        total_charges = st.number_input(
            "Total Charges",
            min_value=0.0,
            value=840.0,
            step=1.0
        )

    submitted = st.form_submit_button(
        "Predict Churn",
        use_container_width=True
    )

# --------------------------------
# 6. Process customer data
# --------------------------------
if submitted:

    # Validate phone service
    if (
        phone_service == "No"
        and multiple_lines != "No phone service"
    ):
        st.error(
            "If Phone Service is No, "
            "Multiple Lines must be No phone service."
        )
        st.stop()

    if (
        phone_service == "Yes"
        and multiple_lines == "No phone service"
    ):
        st.error(
            "If Phone Service is Yes, "
            "select No or Yes for Multiple Lines."
        )
        st.stop()

    # Validate internet services
    internet_features = {
        "Online Security": online_security,
        "Online Backup": online_backup,
        "Device Protection": device_protection,
        "Tech Support": tech_support,
        "Streaming TV": streaming_tv,
        "Streaming Movies": streaming_movies
    }

    if internet_service == "No":
        invalid = [
            name
            for name, value in internet_features.items()
            if value != "No internet service"
        ]

        if invalid:
            st.error(
                "When Internet Service is No, select "
                "No internet service for: "
                + ", ".join(invalid)
            )
            st.stop()

    else:
        invalid = [
            name
            for name, value in internet_features.items()
            if value == "No internet service"
        ]

        if invalid:
            st.error(
                "Select Yes or No for: "
                + ", ".join(invalid)
                + " because Internet Service is available."
            )
            st.stop()

    # Validate total charges
    if tenure == 0 and total_charges != 0:
        st.error(
            "For zero months of tenure, "
            "Total Charges should be zero."
        )
        st.stop()

    # --------------------------------
    # 7. Create customer DataFrame
    # --------------------------------
    customer_data = pd.DataFrame([{
        "gender": gender,
        "SeniorCitizen": senior_citizen,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone_service,
        "MultipleLines": multiple_lines,
        "InternetService": internet_service,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "Contract": contract,
        "PaperlessBilling": paperless_billing,
        "PaymentMethod": payment_method,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges
    }])

    # --------------------------------
    # 8. Categorical encoding
    # --------------------------------
    categories = {
        "gender": ["Female", "Male"],
        "Partner": ["No", "Yes"],
        "Dependents": ["No", "Yes"],
        "PhoneService": ["No", "Yes"],
        "MultipleLines": [
            "No", "No phone service", "Yes"
        ],
        "InternetService": [
            "DSL", "Fiber optic", "No"
        ],
        "OnlineSecurity": [
            "No", "No internet service", "Yes"
        ],
        "OnlineBackup": [
            "No", "No internet service", "Yes"
        ],
        "DeviceProtection": [
            "No", "No internet service", "Yes"
        ],
        "TechSupport": [
            "No", "No internet service", "Yes"
        ],
        "StreamingTV": [
            "No", "No internet service", "Yes"
        ],
        "StreamingMovies": [
            "No", "No internet service", "Yes"
        ],
        "Contract": [
            "Month-to-month", "One year", "Two year"
        ],
        "PaperlessBilling": ["No", "Yes"],
        "PaymentMethod": [
            "Bank transfer (automatic)",
            "Credit card (automatic)",
            "Electronic check",
            "Mailed check"
        ]
    }

    # Preserve all training categories
    for col, values in categories.items():
        customer_data[col] = pd.Categorical(
            customer_data[col],
            categories=values
        )

    # Convert categorical values to numerical columns
    encoded_data = pd.get_dummies(
        customer_data,
        drop_first=True,
        dtype=int
    )

    # Match the training feature columns
    encoded_data = encoded_data.reindex(
        columns=feature_names,
        fill_value=0
    )

    # --------------------------------
    # 9. Display encoded data
    # --------------------------------
    with st.expander("View Encoded Customer Data"):
        st.dataframe(encoded_data)

        st.write(
            f"Number of features: {encoded_data.shape[1]}"
        )

    # --------------------------------
    # 10. Make prediction
    # --------------------------------
    prediction = model.predict(encoded_data)[0]

    probability = model.predict_proba(
        encoded_data
    )[0][1]

    if prediction == 1:
        st.error("⚠️ This customer is likely to churn.")
    else:
        st.success("✅ This customer is likely to stay.")

    # --------------------------------
    # 11. Display prediction
    # --------------------------------
    st.header("Prediction Results")

    if prediction == 1:
        prediction_label = "Likely to churn"
    else:
        prediction_label = "Likely to stay"

    col7, col8 = st.columns(2)

    with col7:
        st.metric(
            "Prediction",
            prediction_label
        )

    with col8:
        st.metric(
            "Churn Probability",
            f"{probability:.2%}"
        )

    # --------------------------------
    # 12. Churn risk explanation
    # --------------------------------
    st.subheader("Churn Risk")

    if probability < 0.3:
        risk = "Low"
        st.success("Low churn risk")

    elif probability < 0.6:
        risk = "Medium"
        st.warning("Medium churn risk")

    else:
        risk = "High"
        st.error("High churn risk")

    st.subheader("Download Prediction Report")

    report_data = customer_data.copy()
    report_data["Prediction"] = (
        "Likely to churn" if prediction == 1
        else "Likely to stay"
    )
    report_data["Churn Probability"] = f"{probability:.2%}"
    report_data["Risk Level"] = risk
    csv = report_data.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Report (CSV)",
        data=csv,
        file_name="customer_churn_report.csv",
        mime="text/csv"
    )
    
    st.subheader("About This Prediction")
    st.write(
        f"The model estimates a {probability:.2%} probability "
        f"that this customer will churn.")

    st.write(
        "This prediction is based on the customer information "
        "provided in the form.")

    st.write(f"Churn risk: {risk}")

    st.info(
        "Note: This prediction is an estimate from a machine learning model "
        "and should not be considered a guaranteed outcome.")

    st.progress(float(probability))

    st.caption(
        "Risk levels use illustrative probability "
        "ranges and are not validated business thresholds."
    )

    # --------------------------------
    # 13. Probability comparison chart
    # --------------------------------
    st.subheader("Stay vs Churn Probability")

    probability_data = pd.DataFrame({
        "Outcome": ["Stay", "Churn"],
        "Probability": [
            1 - probability,
            probability
        ]
    })

    st.bar_chart(
        probability_data.set_index("Outcome")
    )

    # --------------------------------
    # 14. Prediction explanation
    # --------------------------------
    if prediction == 1:
        st.info(
            "The model predicts that this customer "
            "is likely to churn."
        )
    else:
        st.info(
            "The model predicts that this customer "
            "is likely to stay."
        )
st.markdown("---")
st.caption("Customer Churn Prediction | Machine Learning Project")