import streamlit as st
import pandas as pd
import os

st.sidebar.title("🎯 RetainX")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🎯 Rewards",
        "🎁 Redeem",
        "📜 History",
        "👤 Profile"
    ]
)

# =========================
# LOAD CUSTOMER DATA
# =========================

customers_df = pd.read_csv(
    "data/customers.csv"
)

customer_name = (
    st.session_state.current_customer
)

customer = customers_df[
    customers_df["Name"] == customer_name
].iloc[0]

points = int(customer["Points"])

if points < 500:
    tier = "Bronze"
elif points < 1000:
    tier = "Silver"
else:
    tier = "Gold"

# =========================
# DASHBOARD
# =========================

if page == "🏠 Dashboard":

    st.title("👤 Customer Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Current Points",
            points
        )

    with col2:
        st.metric(
            "Tier",
            tier
        )

    st.progress(
        min(points / 1000, 1.0)
    )

    # =========================
    # NEXT TIER PROGRESS
    # =========================

    if tier == "Bronze":

        points_needed = 500 - points

        st.info(
            f"🎯 Earn {points_needed} more points to reach Silver Tier."
        )

    elif tier == "Silver":

        points_needed = 1000 - points

        st.info(
            f"🎯 Earn {points_needed} more points to reach Gold Tier."
        )

    else:

        st.success(
            "🥇 You have reached the highest tier!"
        )

    st.markdown("---")

    # =========================
    # RANK
    # =========================

    leaderboard = customers_df.sort_values(
        by="Points",
        ascending=False
    ).reset_index(drop=True)

    rank = (
        leaderboard[
            leaderboard["Name"]
            == customer_name
        ].index[0]
        + 1
    )

    st.subheader("🏆 My Rank")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Rank",
            f"#{rank}"
        )

    with col2:
        st.metric(
            "Points",
            points
        )

    with col3:
        st.metric(
            "Tier",
            tier
        )

    st.markdown("---")

    # =========================
    # AI RECOMMENDATIONS
    # =========================

    st.subheader(
        "🤖 AI Recommendations"
    )

    if tier == "Bronze":

        st.warning(
            "🥉 Bronze Member"
        )

        st.info(
            "Complete one more purchase to unlock Silver benefits."
        )

    elif tier == "Silver":

        st.info(
            "🥈 Silver Member"
        )

        st.info(
            "You are close to Gold Tier. Keep earning points!"
        )

    else:

        st.success(
            "🥇 Gold Member"
        )

        st.success(
            "You are one of our most loyal customers."
        )

# =========================
# REWARDS
# =========================

elif page == "🎯 Rewards":

    st.title("🎁 Rewards")

    if tier == "Bronze":

        st.success(
            "☕ Free Coffee (100 Points)"
        )

        st.warning(
            "🔒 ₹100 Coupon (200 Points)"
        )

        st.warning(
            "🔒 Free Burger (300 Points)"
        )

    elif tier == "Silver":

        st.success(
            "☕ Free Coffee (100 Points)"
        )

        st.success(
            "🎁 ₹100 Coupon (200 Points)"
        )

        st.warning(
            "🔒 Free Burger (300 Points)"
        )

    else:

        st.success(
            "☕ Free Coffee (100 Points)"
        )

        st.success(
            "🎁 ₹100 Coupon (200 Points)"
        )

        st.success(
            "🍔 Free Burger (300 Points)"
        )

# =========================
# REDEEM
# =========================

elif page == "🎁 Redeem":

    st.title("🎁 Rewards Catalog")

    col1, col2, col3 = st.columns(3)

    # Coffee Card
    with col1:

        st.success(
            """
☕ FREE COFFEE

100 Points

Available Now
            """
        )

    # Coupon Card
    with col2:

        if tier in ["Silver", "Gold"]:

            st.success(
                """
🎁 ₹100 COUPON

200 Points

Available Now
                """
            )

        else:

            st.warning(
                """
🔒 ₹100 COUPON

200 Points

Silver Tier Required
                """
            )

    # Burger Card
    with col3:

        if tier == "Gold":

            st.success(
                """
🍔 FREE BURGER

300 Points

Available Now
                """
            )

        else:

            st.warning(
                """
🔒 FREE BURGER

300 Points

Gold Tier Required
                """
            )

    st.markdown("---")

    st.subheader("🎯 Your Membership Status")

    if tier == "Bronze":

        st.warning(
            "You currently have Bronze access."
        )

    elif tier == "Silver":

        st.info(
            "You currently have Silver access."
        )

    else:

        st.success(
            "You currently have Gold access."
        )

# =========================
# HISTORY
# =========================

elif page == "📜 History":

    st.title(
        "📜 Activity History"
    )

    st.subheader(
        "🛒 Purchase History"
    )

    if os.path.exists(
        "data/purchases.csv"
    ):

        purchases = pd.read_csv(
            "data/purchases.csv"
        )

        customer_purchases = purchases[
            purchases["Customer"]
            == customer["Name"]
        ]

        if len(
            customer_purchases
        ) > 0:

            st.dataframe(
                customer_purchases
            )

        else:

            st.info(
                "No purchases yet."
            )

    st.markdown("---")

    st.subheader(
        "🎁 Redeemed Rewards"
    )

    if os.path.exists(
        "data/redemptions.csv"
    ):

        history = pd.read_csv(
            "data/redemptions.csv"
        )

        customer_history = history[
            history["Customer"]
            == customer["Name"]
        ]

        if len(
            customer_history
        ) > 0:

            st.dataframe(
                customer_history
            )

        else:

            st.info(
                "No rewards redeemed yet."
            )

# =========================
# PROFILE
# =========================

elif page == "👤 Profile":

    st.title("👤 Profile")

    st.subheader(
        "Customer Details"
    )

    st.text_input(
        "Name",
        str(customer["Name"]),
        disabled=True
    )

    if "Phone" in customers_df.columns:

        st.text_input(
            "Phone",
            str(customer["Phone"]),
            disabled=True
        )

    st.text_input(
        "Tier",
        tier,
        disabled=True
    )

    st.text_input(
        "Points",
        str(points),
        disabled=True
    )

# =========================
# LOGOUT
# =========================

if st.sidebar.button("Logout"):

    st.session_state.page = "home"

    if (
        "current_customer"
        in st.session_state
    ):
        del st.session_state[
            "current_customer"
        ]

    st.rerun()