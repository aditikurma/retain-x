import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="RetainX",
    page_icon="🎯",
    layout="wide"
)

if "multiplier_active" not in st.session_state:
    st.session_state.multiplier_active = False
if "multiplier_val" not in st.session_state:
    st.session_state.multiplier_val = 1.0
if "campaign_name" not in st.session_state:
    st.session_state.campaign_name = "Standard Rates"

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">

<style>

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #4A3530;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    font-weight: 700;
    color: #4A3530;
}

.block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 0 !important;
}

.stApp {
    background-color: #FFFFFF;
}

/* ── Hide Streamlit top header bar ── */
header[data-testid="stHeader"] {
    display: none !important;
}

/* ── FIX: Hide ONLY the sidebar collapse toggle button text ──
   Target only the specific toggle button, not ALL sidebar content */
button[data-testid="collapsedControl"],
button[kind="header"] {
    font-size: 0px !important;
    color: transparent !important;
    overflow: hidden !important;
}

/* Hide the keyboard_double_arrow icon text that leaks above sidebar */
section[data-testid="stSidebar"] > div:first-child > div:first-child {
    font-size: 0px !important;
    color: transparent !important;
    height: 0px !important;
    overflow: hidden !important;
    padding: 0 !important;
}

/* ── Sidebar base ── */
section[data-testid="stSidebar"] {
    background-color: #ECE4DB !important;
}

/* ── Sidebar text — explicit, NOT via wildcard ── */
section[data-testid="stSidebar"] p {
    color: #4A3530 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
}

section[data-testid="stSidebar"] span {
    color: #4A3530 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
}

section[data-testid="stSidebar"] label {
    color: #4A3530 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    font-family: 'Playfair Display', serif !important;
    color: #C4A69B !important;
}

/* ── Nav radio active item ── */
div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) {
    background-color: #C4A69B !important;
    border-radius: 8px !important;
}

div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) p {
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

div[role="radiogroup"] label[data-baseweb="radio"] p {
    font-size: 14px !important;
    color: #4A3530 !important;
}

/* ── Metric containers ── */
[data-testid="metric-container"] {
    background-color: #ECE4DB !important;
    border: 1px solid #CFC8BE !important;
    padding: 16px !important;
    border-radius: 12px !important;
}

[data-testid="metric-container"] label,
[data-testid="metric-container"] div {
    color: #4A3530 !important;
}

/* ── Buttons ── */
.stButton button {
    font-family: 'Inter', sans-serif !important;
    background-color: #C4A69B !important;
    color: #FFFFFF !important;
    font-size: 14px !important;
    border-radius: 8px !important;
    border: none !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
}

.stButton button:hover {
    background-color: #4A3530 !important;
    color: #FFFFFF !important;
    transform: translateY(-1px);
}

/* ── Inputs ── */
div[data-testid="stTextInput"] input,
div[data-testid="stSelectbox"] > div > div {
    background-color: #FFFFFF !important;
    border: 1px solid #B8AB9C !important;
    border-radius: 8px !important;
    color: #4A3530 !important;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #C4A69B !important;
    box-shadow: 0 0 0 2px rgba(196, 166, 155, 0.2) !important;
}

/* ── HOME PAGE ── */

.hero-section {
    text-align: center;
    padding: 20px 20px 30px;
}

.hero-logo {
    font-family: 'Playfair Display', serif !important;
    font-size: 68px;
    font-weight: 700;
    color: #C4A69B;
    margin-bottom: 12px;
}

.hero-tagline {
    font-family: 'Inter', sans-serif;
    font-size: 20px;
    color: #4A3530;
    font-weight: 400;
}

.portal-row {
    display: flex;
    gap: 24px;
    justify-content: center;
    flex-wrap: wrap;
    margin: 20px auto 30px;
}

.portal-card {
    background: #FFFFFF;
    border: 1px solid #CFC8BE;
    border-radius: 16px;
    padding: 32px;
    width: 280px;
    text-align: center;
    box-shadow: 0 4px 12px rgba(74, 53, 48, 0.04);
    transition: all 0.2s ease;
}

.portal-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(196, 166, 155, 0.15);
    border-color: #C4A69B;
}

.portal-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 20px;
    font-weight: 700;
    color: #4A3530;
    margin: 12px 0 8px;
}

.portal-desc {
    font-size: 13px;
    color: #B8AB9C;
    line-height: 1.5;
}

.features-strip {
    background: #ECE4DB;
    border-radius: 16px;
    border: 1px solid #CFC8BE;
    padding: 20px;
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
    margin: 40px auto 0;
    max-width: 900px;
}

.feature-item {
    text-align: center;
    padding: 10px;
    flex: 1;
    min-width: 150px;
}

.feat-label {
    font-family: 'Playfair Display', serif !important;
    font-size: 16px;
    font-weight: 700;
    color: #4A3530;
}

.feat-sub {
    font-size: 12px;
    color: #4A3530;
    opacity: 0.8;
}

.divider-line {
    width: 1px;
    background: #CFC8BE;
    align-self: stretch;
}

/* ── LOGIN CARD ── */

.login-card {
    background: #FFFFFF;
    border: 1px solid #CFC8BE;
    border-radius: 20px;
    padding: 40px;
    max-width: 450px;
    margin: 40px auto 20px;
    text-align: center;
    box-shadow: 0 8px 24px rgba(74, 53, 48, 0.05);
}

.login-brand-name {
    font-family: 'Playfair Display', serif !important;
    font-size: 30px;
    color: #C4A69B;
    font-weight: 700;
    margin-bottom: 4px;
}

.login-brand-sub {
    font-size: 14px;
    color: #B8AB9C;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"
if "current_customer" not in st.session_state:
    st.session_state.current_customer = None

# =========================
# HOME PAGE
# =========================
if st.session_state.page == "home":
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-logo">RetainX</h1>
        <p class="hero-tagline">Customer Retention &amp; Loyalty, Reimagined</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="portal-row">
        <div class="portal-card">
            <span style="font-size: 40px;">👤</span>
            <div class="portal-title">I'm a Customer</div>
            <div class="portal-desc">Check your points, redeem rewards, and view your purchase history.</div>
        </div>
        <div class="portal-card">
            <span style="font-size: 40px;">🏪</span>
            <div class="portal-title">I'm a Business Owner</div>
            <div class="portal-desc">Manage customers, track redemptions, and get AI-powered insights.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, _, col2 = st.columns([1, 0.2, 1])
    with col1:
        if st.button("👤 Customer Portal", use_container_width=True, key="btn_customer"):
            st.session_state.page = "customer_login"
            st.rerun()
    with col2:
        if st.button("🏪 Business Owner Portal", use_container_width=True, key="btn_owner"):
            st.session_state.page = "owner_login"
            st.rerun()

    st.markdown("""
    <div class="features-strip">
        <div class="feature-item">
            <span>⭐</span>
            <div class="feat-label">Loyalty Points</div>
            <div class="feat-sub">Earn on every purchase</div>
        </div>
        <div class="divider-line"></div>
        <div class="feature-item">
            <span>🎁</span>
            <div class="feat-label">Rewards</div>
            <div class="feat-sub">Redeem for perks</div>
        </div>
        <div class="divider-line"></div>
        <div class="feature-item">
            <span>🤖</span>
            <div class="feat-label">AI Insights</div>
            <div class="feat-sub">Smart customer tracking</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# CUSTOMER LOGIN
# =========================
elif st.session_state.page == "customer_login":
    st.markdown("""
    <div class="login-card">
        <span style="font-size: 40px;">👤</span>
        <h2 class="login-brand-name">Customer Login</h2>
        <p class="login-brand-sub">Enter your details to continue.</p>
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        mobile = st.text_input("📱 Mobile Number", placeholder="e.g. 9876543210")
        if st.button("Send OTP", use_container_width=True):
            st.success("Demo OTP sent: **1234**")

        otp = st.text_input("🔐 Enter OTP", placeholder="Enter 4-digit OTP")
        if otp == "1234":
            if os.path.exists("data/customers.csv"):
                customers_df = pd.read_csv("data/customers.csv")
                customers_df["Name"] = customers_df["Name"].astype(str).str.strip()
                customer_list = sorted(list(customers_df["Name"].unique()))
                customer_name = st.selectbox("👤 Select Your Name", customer_list)
                if st.button("Login →", use_container_width=True):
                    st.session_state.current_customer = customer_name
                    st.session_state.page = "customer_dashboard"
                    st.rerun()
            else:
                st.error("Missing data file: data/customers.csv not found.")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⬅ Back to Home", use_container_width=True, key="back_cust"):
            st.session_state.page = "home"
            st.rerun()

# =========================
# OWNER LOGIN
# =========================
elif st.session_state.page == "owner_login":
    st.markdown("""
    <div class="login-card">
        <span style="font-size: 40px;">🏪</span>
        <h2 class="login-brand-name">Owner Login</h2>
        <p class="login-brand-sub">Access your corporate business engine.</p>
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        email = st.text_input("📧 Email Address", placeholder="owner@yourbrand.com")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")

        if st.button("Login →", use_container_width=True):
            st.session_state.page = "owner_dashboard"
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⬅ Back to Home", use_container_width=True, key="back_owner"):
            st.session_state.page = "home"
            st.rerun()

elif st.session_state.page == "customer_dashboard":
    exec(open("customer_dashboard.py").read())

elif st.session_state.page == "owner_dashboard":
    exec(open("owner_dashboard.py").read())