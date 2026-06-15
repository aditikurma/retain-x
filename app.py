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

div[role="radiogroup"] > label > div > p {
    color: #FFE3B3 !important;
}

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

/* HOME PAGE GLOW-UP */

.hero-section {
    text-align: center;
    padding: 60px 20px 20px;
}

.hero-logo {
    font-size: 80px;
    font-weight: 800;
    color: #CA2851;
    margin: 0 0 10px 0;
    line-height: 1.1;
    letter-spacing: -2px;
    animation: fadeSlideDown 0.7s ease both;
}

.hero-tagline {
    font-size: 22px;
    color: #6B3A2A;
    font-weight: 400;
    margin-top: 10px;
    margin-bottom: 6px;
    animation: fadeSlideDown 0.9s ease both;
}

.hero-sub {
    font-size: 16px;
    color: #A0695A;
    margin-bottom: 10px;
    animation: fadeSlideDown 1.1s ease both;
}

@keyframes fadeSlideDown {
    from { opacity: 0; transform: translateY(-18px); }
    to   { opacity: 1; transform: translateY(0); }
}

.portal-row {
    display: flex;
    gap: 24px;
    justify-content: center;
    flex-wrap: wrap;
    margin: 24px auto 16px;
}

.portal-card {
    background: #1C1008;
    border: 1.5px solid #FFB173;
    border-radius: 20px;
    padding: 36px 40px;
    width: 260px;
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    text-align: center;
}

.portal-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 16px 40px rgba(202, 40, 81, 0.25);
    border-color: #CA2851;
}

.portal-icon {
    font-size: 48px;
    margin-bottom: 14px;
    display: block;
}

.portal-title {
    font-size: 20px;
    font-weight: 700;
    color: #FFE3B3;
    margin-bottom: 8px;
}

.portal-desc {
    font-size: 13px;
    color: #A0856A;
    line-height: 1.5;
}

.features-strip {
    background: #1C1008;
    border-radius: 20px;
    padding: 28px 40px;
    display: flex;
    gap: 0;
    justify-content: space-around;
    flex-wrap: wrap;
    margin: 8px auto 0;
    max-width: 860px;
}

.feature-item {
    text-align: center;
    padding: 12px 20px;
    flex: 1;
    min-width: 140px;
}

.feat-icon {
    font-size: 28px;
    margin-bottom: 8px;
    display: block;
}

.feat-label {
    font-size: 13px;
    font-weight: 600;
    color: #FFE3B3;
    margin-bottom: 4px;
}

.feat-sub {
    font-size: 11px;
    color: #A0856A;
}

.divider-line {
    width: 1px;
    background: #3A2510;
    align-self: stretch;
    margin: 8px 0;
}

/* LOGIN PAGES */

.login-card {
    background: #1C1008;
    border: 1.5px solid #FFB173;
    border-radius: 24px;
    padding: 48px 52px 40px;
    width: 100%;
    max-width: 460px;
    margin: 40px auto 0;
    text-align: center;
}

.login-brand-icon {
    font-size: 48px;
    display: block;
    margin-bottom: 8px;
}

.login-brand-name {
    font-size: 28px;
    font-weight: 800;
    color: #CA2851;
    letter-spacing: -0.5px;
    margin: 0 0 4px 0;
}

.login-brand-sub {
    font-size: 14px;
    color: #A0856A;
    margin: 0 0 28px 0;
}

.login-divider {
    border: none;
    border-top: 1px solid #3A2510;
    margin: 0 0 24px 0;
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

    st.markdown("""
    <style>
        .block-container { padding-top: 2rem !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-logo">🎯 RetainX</h1>
        <p class="hero-tagline">Customer Retention &amp; Loyalty, Reimagined</p>
        <p class="hero-sub">Points. Rewards. Insights — all in one place.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="portal-row">
        <div class="portal-card">
            <span class="portal-icon">👤</span>
            <div class="portal-title">I'm a Customer</div>
            <div class="portal-desc">Check your points, redeem rewards, and view your purchase history.</div>
        </div>
        <div class="portal-card">
            <span class="portal-icon">🏪</span>
            <div class="portal-title">I'm a Business Owner</div>
            <div class="portal-desc">Manage customers, track redemptions, and get AI-powered insights.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col_gap, col2 = st.columns([1, 0.15, 1])
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
            <span class="feat-icon">⭐</span>
            <div class="feat-label">Loyalty Points</div>
            <div class="feat-sub">Earn on every purchase</div>
        </div>
        <div class="divider-line"></div>
        <div class="feature-item">
            <span class="feat-icon">🎁</span>
            <div class="feat-label">Rewards</div>
            <div class="feat-sub">Redeem for perks &amp; coupons</div>
        </div>
        <div class="divider-line"></div>
        <div class="feature-item">
            <span class="feat-icon">🤖</span>
            <div class="feat-label">AI Insights</div>
            <div class="feat-sub">Smart suggestions per customer</div>
        </div>
        <div class="divider-line"></div>
        <div class="feature-item">
            <span class="feat-icon">📊</span>
            <div class="feat-label">Analytics</div>
            <div class="feat-sub">Track retention in real time</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# CUSTOMER LOGIN
# =========================
elif st.session_state.page == "customer_login":

    st.markdown("""
    <style>
        .block-container { padding-top: 1rem !important; }
        /* dark inputs */
        div[data-testid="stTextInput"] input {
            background-color: #2A1A0A !important;
            border: 1.5px solid #4A2E14 !important;
            border-radius: 10px !important;
            color: #FFE3B3 !important;
        }
        div[data-testid="stTextInput"] input:focus {
            border-color: #FFB173 !important;
            box-shadow: 0 0 0 2px rgba(255,177,115,0.15) !important;
        }
        div[data-testid="stTextInput"] label {
            color: #FFE3B3 !important;
            font-weight: 600 !important;
            font-size: 13px !important;
        }
        div[data-testid="stSelectbox"] > div > div {
            background-color: #2A1A0A !important;
            border: 1.5px solid #4A2E14 !important;
            border-radius: 10px !important;
            color: #FFE3B3 !important;
        }
        div[data-testid="stSelectbox"] label {
            color: #FFE3B3 !important;
            font-weight: 600 !important;
            font-size: 13px !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Centered card header
    st.markdown("""
    <div class="login-card">
        <span class="login-brand-icon">👤</span>
        <h2 class="login-brand-name">Customer Login</h2>
        <p class="login-brand-sub">Welcome back! Enter your details to continue.</p>
        <hr class="login-divider">
    </div>
    """, unsafe_allow_html=True)

    # Center the inputs using columns
    _, col, _ = st.columns([1, 2, 1])
    with col:
        mobile = st.text_input("📱 Mobile Number", placeholder="e.g. 9876543210")

        if st.button("Send OTP", use_container_width=True):
            st.success("Demo OTP sent: **1234**")

        otp = st.text_input("🔐 Enter OTP", placeholder="Enter 4-digit OTP")

        if otp == "1234":
            customers_df = pd.read_csv("data/customers.csv")
            customer_name = st.selectbox("👤 Select Your Name", customers_df["Name"])

            if st.button("Login →", use_container_width=True):
                st.session_state.current_customer = customer_name
                st.session_state.page = "customer_dashboard"
                st.rerun()

        st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)

        if st.button("⬅ Back to Home", use_container_width=True, key="back_cust"):
            st.session_state.page = "home"
            st.rerun()

# =========================
# OWNER LOGIN
# =========================
elif st.session_state.page == "owner_login":

    st.markdown("""
    <style>
        .block-container { padding-top: 1rem !important; }
        div[data-testid="stTextInput"] input {
            background-color: #2A1A0A !important;
            border: 1.5px solid #4A2E14 !important;
            border-radius: 10px !important;
            color: #FFE3B3 !important;
        }
        div[data-testid="stTextInput"] input:focus {
            border-color: #FFB173 !important;
            box-shadow: 0 0 0 2px rgba(255,177,115,0.15) !important;
        }
        div[data-testid="stTextInput"] label {
            color: #FFE3B3 !important;
            font-weight: 600 !important;
            font-size: 13px !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-card">
        <span class="login-brand-icon">🏪</span>
        <h2 class="login-brand-name">Owner Login</h2>
        <p class="login-brand-sub">Access your business dashboard and insights.</p>
        <hr class="login-divider">
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 2, 1])
    with col:
        email = st.text_input("📧 Email Address", placeholder="owner@yourbrand.com")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")

        st.markdown("<div style='margin-top:4px;'></div>", unsafe_allow_html=True)

        if st.button("Login →", use_container_width=True):
            st.session_state.page = "owner_dashboard"
            st.rerun()

        st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)

        if st.button("⬅ Back to Home", use_container_width=True, key="back_owner"):
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