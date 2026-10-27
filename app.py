import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Customer Lifetime Value Prediction",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("customer_results.csv")

st.title("📊 Customer Lifetime Value Prediction")
st.subheader("Using Behavioural Analytics")

try:
    df = load_data()

    # Key performance indicators
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Customers", f"{len(df):,}")

    if "PredictedCLV90Days" in df.columns:
        col2.metric(
            "Average Predicted CLV",
            f"{df['PredictedCLV90Days'].mean():,.2f}"
        )
        col3.metric(
            "Total Predicted CLV",
            f"{df['PredictedCLV90Days'].sum():,.2f}"
        )

    st.divider()

    if "Segment" in df.columns:
        st.subheader("Customer Segments")
        segment_counts = df["Segment"].value_counts()
        st.bar_chart(segment_counts)

    st.subheader("Customer Data")

    if "CustomerID" in df.columns:
        customer_ids = df["CustomerID"].dropna().unique()
        selected_customer = st.selectbox(
            "Select a Customer ID",
            sorted(customer_ids, key=str)
        )

        customer_data = df[
            df["CustomerID"] == selected_customer
        ]

        st.write("Selected Customer Details")
        st.dataframe(customer_data, use_container_width=True)

    st.subheader("All Customer Records")
    st.dataframe(df, use_container_width=True)

    st.download_button(
        label="Download Customer Results CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="customer_results.csv",
        mime="text/csv"
    )

except FileNotFoundError:
    st.error(
        "customer_results.csv was not found. "
        "Place it in the same folder as app.py."
    )
