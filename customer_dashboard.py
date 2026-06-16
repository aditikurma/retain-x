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
# LOAD CUSTOMER DATA — always fresh
# =========================
customers_df = pd.read_csv("data/customers.csv")
customer_name = st.session_state.current_customer
customer = customers_df[customers_df["Name"] == customer_name].iloc[0]
points = int(customer["Points"])

if points < 500:
    tier = "Bronze"
elif points < 1000:
    tier = "Silver"
else:
    tier = "Gold"

tier_config = {
    "Bronze": {"color": "#C4A69B", "bg": "#ECE4DB", "emoji": "🥉", "next": "Silver", "next_points": 500, "bar_color": "#C4A69B"},
    "Silver": {"color": "#B8AB9C", "bg": "#ECE4DB", "emoji": "🥈", "next": "Gold",   "next_points": 1000, "bar_color": "#C4A69B"},
    "Gold":   {"color": "#4A3530", "bg": "#ECE4DB", "emoji": "🥇", "next": None,     "next_points": 1000, "bar_color": "#4A3530"}
}
tc = tier_config[tier]

# =========================
# GAMIFICATION LOGIC
# =========================
purchase_count = 0
streak_days = 0

if os.path.exists("data/purchases.csv"):
    purchases_df = pd.read_csv("data/purchases.csv")
    cust_purchases = purchases_df[purchases_df["Customer"] == customer_name]
    purchase_count = len(cust_purchases)
    if purchase_count > 0:
        streak_days = max(2, (purchase_count * 2) - 1)

if points < 250:
    milestone_target, milestone_reward = 250, "Points Starter Badge"
elif points < 500:
    milestone_target, milestone_reward = 500, "Silver Tier Status"
elif points < 750:
    milestone_target, milestone_reward = 750, "Elite Customer Milestone"
elif points < 1000:
    milestone_target, milestone_reward = 1000, "Gold VIP Tier Status"
else:
    milestone_target, milestone_reward = points + 500, "Legendary Elite Reward Group"

points_to_milestone = max(0, milestone_target - points)
milestone_pct = min(100, int((points / milestone_target) * 100)) if milestone_target > 0 else 100
referral_code = f"RTX-{customer_name.replace(' ', '').upper()[:5]}-{points}"

# =========================
# WELCOME HEADER
# =========================
hour = datetime.now().hour
greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 17 else "Good evening"

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
    background: linear-gradient(135deg, #ECE4DB 0%, #FFFFFF 100%);
    border-radius: 16px; padding: 24px 28px; margin-bottom: 24px; border: 1px solid #CFC8BE;
">
    <div style="display:flex; align-items:center; gap:16px; margin-bottom:16px;">
        <div style="
            width:56px; height:56px; border-radius:50%; background:{tc['color']};
            display:flex; align-items:center; justify-content:center;
            font-size:20px; font-weight:700; color:#FFFFFF; flex-shrink:0;
        ">{initials}</div>
        <div>
            <p style="margin:0; color:#C4A69B; font-size:13px; font-weight:600;">{greeting},</p>
            <h2 style="margin:0; color:#4A3530; font-size:22px; font-weight:700;">{customer_name}</h2>
        </div>
        <div style="margin-left:auto; background:#FFFFFF; border:1px solid {tc['color']}; border-radius:20px; padding:6px 16px; color:{tc['color']}; font-weight:700; font-size:14px;">
            {tc['emoji']} {tier}
        </div>
    </div>
    <div style="display:flex; gap:24px; margin-bottom:14px;">
        <div>
            <p style="margin:0; color:#4A3530; font-size:11px; text-transform:uppercase; letter-spacing:1px; opacity:0.8;">Total Points</p>
            <p style="margin:0; color:#4A3530; font-size:24px; font-weight:700;">{points:,}</p>
        </div>
        <div style="width:1px; background:#CFC8BE;"></div>
        <div>
            <p style="margin:0; color:#4A3530; font-size:11px; text-transform:uppercase; letter-spacing:1px; opacity:0.8;">Progress</p>
            <p style="margin:0; color:#C4A69B; font-size:14px; font-weight:600; margin-top:4px;">{progress_label}</p>
        </div>
    </div>
    <div style="background:#CFC8BE80; border-radius:999px; height:8px; overflow:hidden;">
        <div style="background:{tc['bar_color']}; width:{min(progress_pct,100)}%; height:100%; border-radius:999px;"></div>
    </div>
    <div style="display:flex; justify-content:space-between; margin-top:6px;">
        <span style="font-size:11px; color:#C4A69B;">0</span>
        <span style="font-size:11px; color:#C4A69B;">{tc['next_points']} pts</span>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# DASHBOARD
# =========================
if page == "🏠 Dashboard":
    leaderboard = customers_df.sort_values(by="Points", ascending=False).reset_index(drop=True)
    rank = leaderboard[leaderboard["Name"] == customer_name].index[0] + 1

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""<div style="background:#ECE4DB; border:1px solid #CFC8BE; border-radius:12px; padding:16px; text-align:center;">
            <p style="margin:0; color:#C4A69B; font-size:12px; text-transform:uppercase; letter-spacing:1px; font-weight:600;">Points</p>
            <p style="margin:4px 0 0; color:#4A3530; font-size:28px; font-weight:700;">{points:,}</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div style="background:#ECE4DB; border:1px solid #CFC8BE; border-radius:12px; padding:16px; text-align:center;">
            <p style="margin:0; color:#C4A69B; font-size:12px; text-transform:uppercase; letter-spacing:1px; font-weight:600;">Tier</p>
            <p style="margin:4px 0 0; color:{tc['color']}; font-size:28px; font-weight:700;">{tc['emoji']} {tier}</p></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div style="background:#ECE4DB; border:1px solid #CFC8BE; border-radius:12px; padding:16px; text-align:center;">
            <p style="margin:0; color:#C4A69B; font-size:12px; text-transform:uppercase; letter-spacing:1px; font-weight:600;">Rank</p>
            <p style="margin:4px 0 0; color:#4A3530; font-size:28px; font-weight:700;">#{rank}</p></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🔥 Your Activity & Streaks")
    g_col1, g_col2 = st.columns(2)
    with g_col1:
        st.markdown(f"""<div style="background:#FFFFFF; border:1px solid #CFC8BE; border-radius:14px; padding:20px; display:flex; align-items:center; gap:16px; height:120px; box-shadow:0 4px 12px rgba(0,0,0,0.02);">
            <div style="font-size:40px;">🔥</div>
            <div><p style="margin:0; color:#4A3530; font-weight:700; font-size:18px;">{streak_days}-Purchase Streak</p>
            <p style="margin:4px 0 0; color:#4A3530; font-size:13px; opacity:0.8;">You're an active loyalty shopper! Visit again soon to keep this streak alive.</p></div></div>""", unsafe_allow_html=True)
    with g_col2:
        st.markdown(f"""<div style="background:#FFFFFF; border:1px solid #CFC8BE; border-radius:14px; padding:20px; display:flex; align-items:center; gap:16px; height:120px; box-shadow:0 4px 12px rgba(0,0,0,0.02);">
            <div style="font-size:40px;">🛍️</div>
            <div><p style="margin:0; color:#4A3530; font-weight:700; font-size:18px;">{purchase_count} Orders Logged</p>
            <p style="margin:4px 0 0; color:#4A3530; font-size:13px; opacity:0.8;">Every transaction earns tokens towards premium platform rewards.</p></div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🏆 Next Quest Target")
    st.markdown(f"""
    <div style="background:#4A3530; border:1px solid #C4A69B; border-radius:14px; padding:22px; color:#FFFFFF;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <div>
                <span style="background:#ECE4DB; color:#4A3530; font-size:11px; font-weight:700; padding:3px 10px; border-radius:12px; text-transform:uppercase;">ACTIVE MISSION</span>
                <h4 style="margin:6px 0 0; color:#FFFFFF; font-size:16px; font-weight:700;">Unlock: {milestone_reward}</h4>
            </div>
            <div style="text-align:right;">
                <p style="margin:0; color:#ECE4DB; font-size:18px; font-weight:700;">{points_to_milestone:,} Pts Away</p>
                <p style="margin:0; color:#FFFFFF; opacity:0.7; font-size:11px;">Target: {milestone_target} pts</p>
            </div>
        </div>
        <div style="background:rgba(255,255,255,0.15); border-radius:999px; height:6px; overflow:hidden; margin-bottom:4px;">
            <div style="background:#ECE4DB; width:{milestone_pct}%; height:100%; border-radius:999px;"></div>
        </div>
        <p style="margin:0; color:#FFFFFF; opacity:0.6; font-size:12px; text-align:right;">{milestone_pct}% Mission Complete</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><hr>", unsafe_allow_html=True)

    if tier == "Bronze":
        st.info(f"Earn {500 - points} more points to reach Silver Tier.")
    elif tier == "Silver":
        st.info(f"Earn {1000 - points} more points to reach Gold Tier.")
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
        {"name": "Free Coffee",  "emoji": "☕", "points": 100, "min_tier": "Bronze"},
        {"name": "₹100 Coupon",  "emoji": "🎁", "points": 200, "min_tier": "Silver"},
        {"name": "Free Burger",  "emoji": "🍔", "points": 300, "min_tier": "Gold"},
    ]
    tier_rank = {"Bronze": 0, "Silver": 1, "Gold": 2}

    for r in rewards:
        unlocked = tier_rank[tier] >= tier_rank[r["min_tier"]]
        border = "#C4A69B" if unlocked else "#CFC8BE80"
        opacity = "1" if unlocked else "0.4"
        lock = "" if unlocked else "🔒 "
        badge_bg = "#FFFFFF" if unlocked else "#CFC8BE20"
        badge_color = "#4A3530" if unlocked else "#4A353060"
        st.markdown(f"""
        <div style="background:#ECE4DB; border:1px solid {border}; border-radius:12px; padding:16px 20px; margin-bottom:10px; opacity:{opacity}; display:flex; align-items:center; justify-content:space-between; box-shadow:0 4px 12px rgba(0,0,0,0.03);">
            <div style="display:flex; align-items:center; gap:14px;">
                <span style="font-size:28px;">{r['emoji']}</span>
                <div>
                    <p style="margin:0; color:#4A3530; font-weight:600; font-size:15px;">{lock}{r['name']}</p>
                    <p style="margin:2px 0 0; color:#C4A69B; font-size:12px;">{r['min_tier']} Tier required</p>
                </div>
            </div>
            <div style="background:{badge_bg}; border:1px solid {badge_color}; border-radius:20px; padding:4px 14px; color:{badge_color}; font-weight:700; font-size:13px;">{r['points']} pts</div>
        </div>
        """, unsafe_allow_html=True)

# =========================
# REDEEM  ← FIXED
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
                <div style="background:#ECE4DB; border:1px solid #C4A69B; border-radius:14px; padding:20px; text-align:center; margin-bottom:8px; box-shadow:0 4px 12px rgba(0,0,0,0.02);">
                    <div style="font-size:36px; margin-bottom:8px;">{item['emoji']}</div>
                    <p style="color:#4A3530; font-weight:700; font-size:14px; margin:0;">{item['name']}</p>
                    <p style="color:#C4A69B; font-size:20px; font-weight:700; margin:6px 0;">{item['points']} pts</p>
                    <p style="color:{'#2E7D32' if can_afford else '#D32F2F'}; font-size:12px; font-weight:600; margin:0;">
                        {'✅ Available to redeem' if can_afford else f"❌ Need {item['points'] - points} more pts"}
                    </p>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"Redeem {item['emoji']}", key=f"redeem_{idx}", use_container_width=True, disabled=not can_afford):
                    # 1. Reload CSV fresh to avoid stale data
                    fresh_df = pd.read_csv("data/customers.csv")
                    current_pts = int(fresh_df.loc[fresh_df["Name"] == customer_name, "Points"].values[0])
                    new_pts = current_pts - item["points"]

                    # Recalculate tier
                    new_tier = "Bronze" if new_pts < 500 else "Silver" if new_pts < 1000 else "Gold"

                    # 2. Save updated points + tier
                    fresh_df.loc[fresh_df["Name"] == customer_name, "Points"] = new_pts
                    fresh_df.loc[fresh_df["Name"] == customer_name, "Tier"] = new_tier
                    fresh_df.to_csv("data/customers.csv", index=False)

                    # 3. Log to redemptions.csv
                    redemption_row = pd.DataFrame([{
                        "Customer": customer_name,
                        "Reward":   item["name"],
                        "Points":   item["points"],
                        "Date":     datetime.now().strftime("%Y-%m-%d %H:%M")
                    }])
                    if os.path.exists("data/redemptions.csv"):
                        existing = pd.read_csv("data/redemptions.csv")
                        updated = pd.concat([existing, redemption_row], ignore_index=True)
                    else:
                        updated = redemption_row
                    updated.to_csv("data/redemptions.csv", index=False)

                    st.success(f"🎉 {item['name']} redeemed! {item['points']} pts deducted.")
                    st.balloons()
                    st.rerun()

            else:
                st.markdown(f"""
                <div style="background:#FFFFFF; border:1px solid #CFC8BE; border-radius:14px; padding:20px; text-align:center; opacity:0.4; margin-bottom:8px;">
                    <div style="font-size:36px; margin-bottom:8px;">🔒</div>
                    <p style="color:#4A353090; font-weight:700; font-size:14px; margin:0;">{item['name']}</p>
                    <p style="color:#CFC8BE; font-size:20px; font-weight:700; margin:6px 0;">{item['points']} pts</p>
                    <p style="color:#4A3530; opacity:0.6; font-size:12px; margin:0;">{item['min_tier']} Tier Required</p>
                </div>
                """, unsafe_allow_html=True)
                st.button("🔒 Locked", key=f"locked_{idx}", use_container_width=True, disabled=True)

    st.markdown("---")
    st.subheader("🎯 Your Membership Status")
    if tier == "Bronze":
        st.warning(f"🥉 Bronze access — {points} pts remaining")
    elif tier == "Silver":
        st.info(f"🥈 Silver access — {points} pts remaining")
    else:
        st.success(f"🥇 Gold access — {points} pts remaining")

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
            st.info("No purchases recorded yet.")
    else:
        st.info("No purchases recorded yet.")

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
    <div style="background:#4A3530; border:1px solid #C4A69B; border-radius:16px; padding:24px; margin-bottom:16px;">
        <div style="display:flex; align-items:center; gap:16px; margin-bottom:20px;">
            <div style="width:64px; height:64px; border-radius:50%; background:#FFFFFF; display:flex; align-items:center; justify-content:center; font-size:24px; font-weight:700; color:#4A3530;">{initials}</div>
            <div>
                <h3 style="margin:0; color:#FFFFFF;">{customer_name}</h3>
                <span style="background:#ECE4DB; border:1px solid {tc['color']}; border-radius:20px; padding:3px 12px; color:#4A3530; font-size:12px; font-weight:600;">{tc['emoji']} {tier} Member</span>
            </div>
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
            <div style="background:rgba(255,255,255,0.08); border-radius:10px; padding:12px; border:1px solid #CFC8BE;">
                <p style="margin:0; color:#ECE4DB; font-size:11px; text-transform:uppercase; letter-spacing:1px;">Points</p>
                <p style="margin:4px 0 0; color:#FFFFFF; font-size:20px; font-weight:700;">{points:,}</p>
            </div>
            <div style="background:rgba(255,255,255,0.08); border-radius:10px; padding:12px; border:1px solid #CFC8BE;">
                <p style="margin:0; color:#ECE4DB; font-size:11px; text-transform:uppercase; letter-spacing:1px;">Tier</p>
                <p style="margin:4px 0 0; color:#ECE4DB; font-size:20px; font-weight:700;">{tier}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📢 Spread the Word, Earn Perks")
    st.markdown(f"""
    <div style="background:#ECE4DB; border:1px solid #CFC8BE; border-radius:14px; padding:20px; margin-bottom:20px;">
        <p style="margin:0; color:#4A3530; font-weight:700; font-size:15px;">🎁 Invite Your Friends</p>
        <p style="margin:4px 0 0; color:#4A3530; opacity:0.8; font-size:13px;">Share your code! When a friend signs up, you both get <b>50 bonus points</b>!</p>
    </div>
    """, unsafe_allow_html=True)

    ref_col1, ref_col2 = st.columns([2.5, 1])
    with ref_col1:
        st.text_input("Your Unique Referral Code", value=referral_code, disabled=True, label_visibility="collapsed")
    with ref_col2:
        if st.button("Copy Invite Text", use_container_width=True):
            st.toast(f"Copied: Code {referral_code}! Send to your friends! 🎉")

    st.markdown("<br>", unsafe_allow_html=True)
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