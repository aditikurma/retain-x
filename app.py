
import streamlit as st
import pandas as pd
 
st.set_page_config(
    page_title="RetainX",
    page_icon="🎯",
    layout="wide"
)
 
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
 
<style>
 
html, body, [class*="css"] {
    font-family: 'Open Sans', sans-serif;
}
 
h1, h2, h3 {
    font-family: 'Open Sans', sans-serif;
    font-weight: 700;
    color: #CA2851;
}
 
.stApp {
    background-color: #FFF6E8;
}
 
section[data-testid="stSidebar"] {
    background-color: #1C1008;
}
 
section[data-testid="stSidebar"] .st-emotion-cache-1rtdyuf,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label {
    color: #FFE3B3 !important;
}
 
section[data-testid="stSidebar"] .st-emotion-cache-16txtl3 h1 {
    color: #FFE3B3 !important;
}
 
/* Navigation label */
div[role="radiogroup"] > label > div > p {
    color: #FFE3B3 !important;
}
 
/* Active menu item */
div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) {
    background-color: #FFB173;
    color: #1C1008 !important;
    font-weight: 700;
    border-radius: 10px;
    padding: 10px;
}
 
div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) p {
    color: #1C1008 !important;
    font-weight: 700;
}
 
/* Inactive menu items */
div[role="radiogroup"] label[data-baseweb="radio"] {
    padding: 8px;
    border-radius: 10px;
}
 
[data-testid="metric-container"] {
    background-color: #1C1008;
    border: 1px solid #FFB173;
    padding: 18px;
    border-radius: 15px;
}
 
[data-testid="metric-container"] label,
[data-testid="metric-container"] div {
    color: #FFE3B3 !important;
}
 
.stButton button {
    background-color: #CA2851;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: 600;
}
 
.stButton button:hover {
    background-color: #FFB173;
    color: #1C1008;
}
 
.stSuccess {
    border-left: 5px solid #FFB173;
}
 
.stInfo {
    border-left: 5px solid #FF6766;
}
 
</style>
""", unsafe_allow_html=True)
 
# Session State
if "page" not in st.session_state:
    st.session_state.page = "home"
if "current_customer" not in st.session_state:
    st.session_state.current_customer = None
 
# =========================
# HOME PAGE
# =========================
if st.session_state.page == "home":
 
    st.markdown(
        """
        <h1 style="
        font-size:60px;
        font-weight:700;
        color:#CA2851;
        margin-bottom:0;
        ">
        🎯 RetainX
        </h1>
        """,
        unsafe_allow_html=True
    )
 
    st.subheader("Customer Retention & Loyalty Platform")
 
    st.markdown("---")
 
    st.write("## Who are you?")
 
    col1, col2 = st.columns(2)
 
    with col1:
        if st.button("👤 Customer", use_container_width=True):
            st.session_state.page = "customer_login"
            st.rerun()
 
    with col2:
        if st.button("🏪 Business Owner", use_container_width=True):
            st.session_state.page = "owner_login"
            st.rerun()
 
# =========================
# CUSTOMER LOGIN
# =========================
elif st.session_state.page == "customer_login":
 
    st.title("👤 Customer Login")
 
    mobile = st.text_input(
        "Mobile Number"
    )
 
    if st.button("Send OTP"):
        st.success(
            "Demo OTP Sent: 1234"
        )
 
    otp = st.text_input(
        "Enter OTP"
    )
 
    if otp == "1234":
 
        customers_df = pd.read_csv(
            "data/customers.csv"
        )
 
        customer_name = st.selectbox(
            "Select Customer",
            customers_df["Name"]
        )
 
        if st.button(
            "Login as Customer"
        ):
 
            st.session_state.current_customer = (
                customer_name
            )
 
            st.session_state.page = (
                "customer_dashboard"
            )
 
            st.rerun()
 
    if st.button("⬅ Back"):
 
        st.session_state.page = "home"
 
        st.rerun()
 
# =========================
# OWNER LOGIN
# =========================
elif st.session_state.page == "owner_login":
 
    st.title("🏪 Business Owner Login")
 
    email = st.text_input("Email")
 
    password = st.text_input(
        "Password",
        type="password"
    )
 
    if st.button("Login"):
        st.session_state.page = "owner_dashboard"
        st.rerun()
 
    if st.button("⬅ Back"):
        st.session_state.page = "home"
        st.rerun()
 
# =========================
# CUSTOMER DASHBOARD
# =========================
elif st.session_state.page == "customer_dashboard":
 
    exec(open("customer_dashboard.py").read())
 
# =========================
# OWNER DASHBOARD
# =========================
elif st.session_state.page == "owner_dashboard":
 
    exec(open("owner_dashboard.py").read())