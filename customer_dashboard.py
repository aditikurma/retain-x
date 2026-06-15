import streamlit as st
import pandas as pd
import os
from datetime import datetime

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

customers_df = pd.read_csv("data/customers.csv")

customer_name = st.session_state.current_customer

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

tier_config = {
    "Bronze": {
        "color": "#CA2851",
        "bg": "#2B0A14",
        "emoji": "🥉",
        "next": "Silver",
        "next_points": 500,
        "bar_color": "#CA2851"
    },
    "Silver": {
        "color": "#FF6766",
        "bg": "#2B1010",
        "emoji": "🥈",
        "next": "Gold",
        "next_points": 1000,
        "bar_color": "#FF6766"
    },
    "Gold": {
        "color": "#FFB173",
        "bg": "#1C1008",
        "emoji": "🥇",
        "next": None,
        "next_points": 1000,
        "bar_color": "#FFB173"
    }
}

tc = tier_config[tier]

# =========================
# WELCOME HEADER
# =========================

hour = datetime.now().hour
if hour < 12:
    greeting = "Good morning"
elif hour < 17:
    greeting = "Good afternoon"
else:
    greeting = "Good evening"

if tier == "Gold":
    progress_pct = 100
    progress_label = "Max Tier Reached"
else:
    progress_pct = int((points / tc["next_points"]) * 100)
    points_left = tc["next_points"] - points
    progress_label = f"{points_left} points to {tc['next']} Tier"

initials = "".join([n[0].upper() for n in customer_name.split()][:2])

st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #1C1008 0%, #2B1420 100%);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 24px;
    border: 1px solid #FFB17340;
">
    <div style="display:flex; align-items:center; gap:16px; margin-bottom:16px;">
        <div style="
            width:56px; height:56px;
            border-radius:50%;
            background: {tc['color']};
            display:flex; align-items:center; justify-content:center;
            font-size:20px; font-weight:700; color:#FFF6E8;
            flex-shrink:0;
        ">{initials}</div>
        <div>
            <p style="margin:0; color:#FFB173; font-size:13px;">{greeting},</p>
            <h2 style="margin:0; color:#FFE3B3; font-size:22px; font-weight:700;">{customer_name}</h2>
        </div>
        <div style="
            margin-left:auto;
            background:{tc['color']}22;
            border:1px solid {tc['color']};
            border-radius:20px;
            padding:6px 16px;
            color:{tc['color']};
            font-weight:700;
            font-size:14px;
        ">{tc['emoji']} {tier}</div>
    </div>
    <div style="display:flex; gap:24px; margin-bottom:14px;">
        <div>
            <p style="margin:0; color:#FFB17399; font-size:11px; text-transform:uppercase; letter-spacing:1px;">Total Points</p>
            <p style="margin:0; color:#FFE3B3; font-size:24px; font-weight:700;">{points:,}</p>
        </div>
        <div style="width:1px; background:#FFB17330;"></div>
        <div>
            <p style="margin:0; color:#FFB17399; font-size:11px; text-transform:uppercase; letter-spacing:1px;">Progress</p>
            <p style="margin:0; color:#FFE3B3; font-size:14px; font-weight:600; margin-top:4px;">{progress_label}</p>
        </div>
    </div>
    <div style="background:#FFB17322; border-radius:999px; height:8px; overflow:hidden;">
        <div style="
            background:{tc['color']};
            width:{min(progress_pct, 100)}%;
            height:100%;
            border-radius:999px;
            transition: width 0.4s ease;
        "></div>
    </div>
    <div style="display:flex; justify-content:space-between; margin-top:6px;">
        <span style="font-size:11px; color:#FFB17380;">0</span>
        <span style="font-size:11px; color:#FFB17380;">{tc['next_points']} pts</span>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# DASHBOARD
# =========================

if page == "🏠 Dashboard":

    leaderboard = customers_df.sort_values(
        by="Points", ascending=False
    ).reset_index(drop=True)

    rank = leaderboard[leaderboard["Name"] == customer_name].index[0] + 1

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div style="background:#1C1008; border:1px solid #FFB17340; border-radius:12px; padding:16px; text-align:center;">
            <p style="margin:0; color:#FFB173; font-size:12px; text-transform:uppercase; letter-spacing:1px;">Points</p>
            <p style="margin:4px 0 0; color:#FFE3B3; font-size:28px; font-weight:700;">{points:,}</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="background:#1C1008; border:1px solid #FFB17340; border-radius:12px; padding:16px; text-align:center;">
            <p style="margin:0; color:#FFB173; font-size:12px; text-transform:uppercase; letter-spacing:1px;">Tier</p>
            <p style="margin:4px 0 0; color:{tc['color']}; font-size:28px; font-weight:700;">{tc['emoji']} {tier}</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="background:#1C1008; border:1px solid #FFB17340; border-radius:12px; padding:16px; text-align:center;">
            <p style="margin:0; color:#FFB173; font-size:12px; text-transform:uppercase; letter-spacing:1px;">Rank</p>
            <p style="margin:4px 0 0; color:#FFE3B3; font-size:28px; font-weight:700;">#{rank}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)

    if tier == "Bronze":
        points_needed = 500 - points
        st.info(f"🎯 Earn {points_needed} more points to reach Silver Tier.")
    elif tier == "Silver":
        points_needed = 1000 - points
        st.info(f"🎯 Earn {points_needed} more points to reach Gold Tier.")
    else:
        st.success("🥇 You have reached the highest tier!")

    st.markdown("---")

    st.subheader("🤖 AI Recommendations")

    if tier == "Bronze":
        st.warning("🥉 Bronze Member")
        st.info("Complete one more purchase to unlock Silver benefits.")
    elif tier == "Silver":
        st.info("🥈 Silver Member")
        st.info("You are close to Gold Tier. Keep earning points!")
    else:
        st.success("🥇 Gold Member")
        st.success("You are one of our most loyal customers.")

# =========================
# REWARDS
# =========================

elif page == "🎯 Rewards":

    st.title("🎁 Rewards")

    rewards = [
        {"name": "Free Coffee", "emoji": "☕", "points": 100, "min_tier": "Bronze"},
        {"name": "₹100 Coupon", "emoji": "🎁", "points": 200, "min_tier": "Silver"},
        {"name": "Free Burger", "emoji": "🍔", "points": 300, "min_tier": "Gold"},
    ]

    tier_rank = {"Bronze": 0, "Silver": 1, "Gold": 2}

    for r in rewards:
        unlocked = tier_rank[tier] >= tier_rank[r["min_tier"]]
        border = "#FFB173" if unlocked else "#44281040"
        opacity = "1" if unlocked else "0.5"
        lock = "" if unlocked else "🔒 "
        badge_bg = "#FFB17322" if unlocked else "#44281022"
        badge_color = "#FFB173" if unlocked else "#FFB17360"

        st.markdown(f"""
        <div style="
            background:#1C1008;
            border:1px solid {border};
            border-radius:12px;
            padding:16px 20px;
            margin-bottom:10px;
            opacity:{opacity};
            display:flex;
            align-items:center;
            justify-content:space-between;
        ">
            <div style="display:flex; align-items:center; gap:14px;">
                <span style="font-size:28px;">{r['emoji']}</span>
                <div>
                    <p style="margin:0; color:#FFE3B3; font-weight:600; font-size:15px;">{lock}{r['name']}</p>
                    <p style="margin:2px 0 0; color:#FFB17399; font-size:12px;">{r['min_tier']} Tier required</p>
                </div>
            </div>
            <div style="
                background:{badge_bg};
                border:1px solid {badge_color};
                border-radius:20px;
                padding:4px 14px;
                color:{badge_color};
                font-weight:700;
                font-size:13px;
            ">{r['points']} pts</div>
        </div>
        """, unsafe_allow_html=True)

# =========================
# REDEEM  ← WORKING NOW
# =========================

elif page == "🎁 Redeem":

    st.title("🎁 Rewards Catalog")

    redeem_items = [
        {"emoji": "☕", "name": "Free Coffee",  "points": 100, "min_tier": "Bronze"},
        {"emoji": "🎁", "name": "₹100 Coupon",  "points": 200, "min_tier": "Silver"},
        {"emoji": "🍔", "name": "Free Burger",   "points": 300, "min_tier": "Gold"},
    ]

    tier_rank = {"Bronze": 0, "Silver": 1, "Gold": 2}

    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]

    for idx, item in enumerate(redeem_items):
        unlocked = tier_rank[tier] >= tier_rank[item["min_tier"]]
        can_afford = points >= item["points"]

        with cols[idx]:
            if unlocked:
                st.markdown(f"""
                <div style="
                    background:#1C1008;
                    border:1px solid #FFB173;
                    border-radius:14px;
                    padding:20px;
                    text-align:center;
                    margin-bottom:8px;
                ">
                    <div style="font-size:36px; margin-bottom:8px;">{item['emoji']}</div>
                    <p style="color:#FFB173; font-weight:700; font-size:14px; margin:0;">{item['name']}</p>
                    <p style="color:#FFE3B3; font-size:20px; font-weight:700; margin:6px 0;">{item['points']} pts</p>
                    <p style="color:{'#4CAF50' if can_afford else '#FF6766'}; font-size:12px; margin:0;">
                        {'✅ You can redeem this' if can_afford else f"❌ Need {item['points'] - points} more pts"}
                    </p>
                </div>
                """, unsafe_allow_html=True)

                btn_label = f"Redeem {item['emoji']}"
                if st.button(btn_label, key=f"redeem_{idx}", use_container_width=True, disabled=not can_afford):
                    # 1. Deduct points from customers.csv
                    customers_df.loc[
                        customers_df["Name"] == customer_name, "Points"
                    ] = points - item["points"]
                    customers_df.to_csv("data/customers.csv", index=False)

                    # 2. Log to redemptions.csv
                    redemption_row = pd.DataFrame([{
                        "Customer": customer_name,
                        "Reward": item["name"],
                        "Points": item["points"],
                        "Date": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }])

                    if os.path.exists("data/redemptions.csv"):
                        existing = pd.read_csv("data/redemptions.csv")
                        updated = pd.concat([existing, redemption_row], ignore_index=True)
                    else:
                        updated = redemption_row

                    updated.to_csv("data/redemptions.csv", index=False)

                    # 3. Show success & refresh
                    st.success(f"🎉 {item['name']} redeemed! {item['points']} points deducted.")
                    st.balloons()
                    st.rerun()

            else:
                st.markdown(f"""
                <div style="
                    background:#1C1008;
                    border:1px solid #44281060;
                    border-radius:14px;
                    padding:20px;
                    text-align:center;
                    opacity:0.5;
                    margin-bottom:8px;
                ">
                    <div style="font-size:36px; margin-bottom:8px;">🔒</div>
                    <p style="color:#FFB17360; font-weight:700; font-size:14px; margin:0;">{item['name']}</p>
                    <p style="color:#FFE3B380; font-size:20px; font-weight:700; margin:6px 0;">{item['points']} pts</p>
                    <p style="color:#FFB17350; font-size:12px; margin:0;">{item['min_tier']} Tier Required</p>
                </div>
                """, unsafe_allow_html=True)

                st.button("🔒 Locked", key=f"locked_{idx}", use_container_width=True, disabled=True)

    st.markdown("---")
    st.subheader("🎯 Your Membership Status")

    remaining = points  # shown after potential rerun
    if tier == "Bronze":
        st.warning(f"🥉 Bronze access — {remaining} pts remaining")
    elif tier == "Silver":
        st.info(f"🥈 Silver access — {remaining} pts remaining")
    else:
        st.success(f"🥇 Gold access — {remaining} pts remaining")

# =========================
# HISTORY
# =========================

elif page == "📜 History":

    st.title("📜 Activity History")

    st.subheader("🛒 Purchase History")

    if os.path.exists("data/purchases.csv"):
        purchases = pd.read_csv("data/purchases.csv")
        customer_purchases = purchases[purchases["Customer"] == customer["Name"]]

        if len(customer_purchases) > 0:
            st.dataframe(customer_purchases)
        else:
            st.info("No purchases yet.")

    st.markdown("---")

    st.subheader("🎁 Redeemed Rewards")

    if os.path.exists("data/redemptions.csv"):
        history = pd.read_csv("data/redemptions.csv")
        customer_history = history[history["Customer"] == customer["Name"]]

        if len(customer_history) > 0:
            st.dataframe(customer_history)
        else:
            st.info("No rewards redeemed yet.")
    else:
        st.info("No rewards redeemed yet.")

# =========================
# PROFILE
# =========================

elif page == "👤 Profile":

    st.title("👤 Profile")

    st.markdown(f"""
    <div style="
        background:#1C1008;
        border:1px solid #FFB17340;
        border-radius:16px;
        padding:24px;
        margin-bottom:16px;
    ">
        <div style="display:flex; align-items:center; gap:16px; margin-bottom:20px;">
            <div style="
                width:64px; height:64px;
                border-radius:50%;
                background:{tc['color']};
                display:flex; align-items:center; justify-content:center;
                font-size:24px; font-weight:700; color:#FFF6E8;
            ">{initials}</div>
            <div>
                <h3 style="margin:0; color:#FFE3B3;">{customer_name}</h3>
                <span style="
                    background:{tc['color']}22;
                    border:1px solid {tc['color']};
                    border-radius:20px;
                    padding:3px 12px;
                    color:{tc['color']};
                    font-size:12px;
                    font-weight:600;
                ">{tc['emoji']} {tier} Member</span>
            </div>
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
            <div style="background:#FFB17310; border-radius:10px; padding:12px;">
                <p style="margin:0; color:#FFB17399; font-size:11px; text-transform:uppercase; letter-spacing:1px;">Points</p>
                <p style="margin:4px 0 0; color:#FFE3B3; font-size:20px; font-weight:700;">{points:,}</p>
            </div>
            <div style="background:#FFB17310; border-radius:10px; padding:12px;">
                <p style="margin:0; color:#FFB17399; font-size:11px; text-transform:uppercase; letter-spacing:1px;">Tier</p>
                <p style="margin:4px 0 0; color:{tc['color']}; font-size:20px; font-weight:700;">{tier}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Customer Details")

    st.text_input("Name", str(customer["Name"]), disabled=True)

    if "Phone" in customers_df.columns:
        st.text_input("Phone", str(customer["Phone"]), disabled=True)

    st.text_input("Tier", tier, disabled=True)
    st.text_input("Points", str(points), disabled=True)

# =========================
# LOGOUT
# =========================

if st.sidebar.button("Logout"):
    st.session_state.page = "home"
    if "current_customer" in st.session_state:
        del st.session_state["current_customer"]
    st.rerun()