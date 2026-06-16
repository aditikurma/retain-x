import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

st.sidebar.title("🎯 RetainX")

page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Analytics",
        "👥 Customers",
        "🎟 Coupons",
        "🛒 Purchases",
        "🏆 Leaderboard",
        "🤖 AI Insights"
    ]
)

# =========================
# LOAD DATA
# =========================
total_customers = 0
total_revenue = 0
repeat_customers = 0
total_redemptions = 0
customers_df = pd.DataFrame()
purchases_df = pd.DataFrame()

if os.path.exists("data/customers.csv"):
    customers_df = pd.read_csv("data/customers.csv")
    total_customers = len(customers_df)

if os.path.exists("data/purchases.csv"):
    purchases_df = pd.read_csv("data/purchases.csv")
    total_revenue = purchases_df["Amount"].sum()
    repeat_customers = purchases_df["Customer"].value_counts().gt(1).sum()

if os.path.exists("data/redemptions.csv"):
    redemptions_df = pd.read_csv("data/redemptions.csv")
    total_redemptions = len(redemptions_df)

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

st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #ECE4DB 0%, #FFFFFF 100%);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 24px;
    border: 1px solid #CFC8BE;
">
    <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
        <div>
            <p style="margin:0; color:#C4A69B; font-size:13px; font-weight:600;">{greeting},</p>
            <h2 style="margin:0; color:#4A3530; font-size:24px; font-weight:700;">🏪 Business Owner</h2>
            <p style="margin:4px 0 0; color:#C4A69B; font-size:12px; opacity:0.8;">{datetime.now().strftime("%A, %d %B %Y")}</p>
        </div>
        <div style="display:flex; gap:12px; flex-wrap:wrap;">
            <div style="background:#FFFFFF; border:1px solid #CFC8BE; border-radius:12px; padding:12px 20px; text-align:center;">
                <p style="margin:0; color:#C4A69B; font-size:11px; text-transform:uppercase; letter-spacing:1px; font-weight:600;">Customers</p>
                <p style="margin:2px 0 0; color:#4A3530; font-size:22px; font-weight:700;">{total_customers}</p>
            </div>
            <div style="background:#FFFFFF; border:1px solid #C4A69B; border-radius:12px; padding:12px 20px; text-align:center;">
                <p style="margin:0; color:#C4A69B; font-size:11px; text-transform:uppercase; letter-spacing:1px; font-weight:600;">Revenue</p>
                <p style="margin:2px 0 0; color:#C4A69B; font-size:22px; font-weight:700;">₹{int(total_revenue):,}</p>
            </div>
            <div style="background:#FFFFFF; border:1px solid #CFC8BE; border-radius:12px; padding:12px 20px; text-align:center;">
                <p style="margin:0; color:#C4A69B; font-size:11px; text-transform:uppercase; letter-spacing:1px; font-weight:600;">Redemptions</p>
                <p style="margin:2px 0 0; color:#4A3530; font-size:22px; font-weight:700;">{total_redemptions}</p>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# ANALYTICS
# =========================
if page == "📊 Analytics":
    col1, col2, col3, col4 = st.columns(4)

    stats = [
        ("👥", "Total Customers", str(total_customers), "#4A3530"),
        ("💰", "Revenue", f"₹{int(total_revenue):,}", "#C4A69B"),
        ("🔄", "Repeat Customers", str(repeat_customers), "#4A3530"),
        ("🎁", "Redemptions", str(total_redemptions), "#C4A69B"),
    ]

    for col, (icon, label, value, color) in zip([col1, col2, col3, col4], stats):
        with col:
            st.markdown(f"""
            <div style="
                background:#ECE4DB;
                border:1px solid #CFC8BE;
                border-radius:12px;
                padding:16px;
                text-align:center;
                margin-bottom:16px;
            ">
                <p style="font-size:24px; margin:0;">{icon}</p>
                <p style="margin:4px 0 2px; color:{color}; font-size:11px; text-transform:uppercase; letter-spacing:1px; font-weight:600;">{label}</p>
                <p style="margin:0; color:#4A3530; font-size:20px; font-weight:700;">{value}</p>
            </div>
            """, unsafe_allow_html=True)

    sales = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May"],
        "Revenue": [15000, 25000, 40000, 55000, 75000]
    })

    fig = px.line(sales, x="Month", y="Revenue", title="Revenue Growth")
    fig.update_traces(line_color="#C4A69B", line_width=3)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(236,228,219,0.4)",
        font_color="#4A3530",
        title_font_color="#4A3530",
        xaxis=dict(gridcolor="#CFC8BE", color="#4A3530"),
        yaxis=dict(gridcolor="#CFC8BE", color="#4A3530"),
    )
    st.plotly_chart(fig, use_container_width=True)

    if not customers_df.empty:
        customers_df["Tier_Clean"] = customers_df["Tier"].str.capitalize()
        customer_growth = pd.DataFrame({
            "Stage": ["New", "Bronze", "Silver", "Gold"],
            "Customers": [
                len(customers_df[customers_df["Points"] < 100]),
                len(customers_df[(customers_df["Points"] >= 100) & (customers_df["Tier_Clean"] == "Bronze")]),
                len(customers_df[(customers_df["Tier_Clean"] == "Silver")]),
                len(customers_df[(customers_df["Tier_Clean"] == "Gold")])
            ]
        })

        fig2 = px.bar(
            customer_growth, x="Stage", y="Customers",
            title="Customer Stage Distribution",
            color="Stage",
            color_discrete_map={"New": "#CFC8BE", "Bronze": "#C4A69B", "Silver": "#B8AB9C", "Gold": "#ECE4DB"}
        )
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(236,228,219,0.4)",
            font_color="#4A3530",
            title_font_color="#4A3530",
            xaxis=dict(gridcolor="#CFC8BE", color="#4A3530"),
            yaxis=dict(gridcolor="#CFC8BE", color="#4A3530"),
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    if not customers_df.empty:
        tier_counts = customers_df["Tier_Clean"].value_counts().reset_index()
        tier_counts.columns = ["Tier", "Count"]

        st.subheader("Customer Tier Distribution")
        pie_fig = px.pie(
            tier_counts, names="Tier", values="Count", color="Tier",
            color_discrete_map={"Bronze": "#C4A69B", "Silver": "#B8AB9C", "Gold": "#ECE4DB"}
        )
        pie_fig.update_traces(textinfo="percent+label")
        pie_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#4A3530")
        st.plotly_chart(pie_fig, use_container_width=True)

    st.markdown("---")
    st.subheader("🎁 Recent Reward Redemptions")
    if os.path.exists("data/redemptions.csv"):
        redemptions = pd.read_csv("data/redemptions.csv")
        st.dataframe(redemptions.tail(10), use_container_width=True)
    else:
        st.info("No reward redemptions yet.")

    st.markdown("---")
    st.subheader("📊 Business Impact")
    imp_col1, imp_col2, imp_col3 = st.columns(3)

    with imp_col1:
        st.markdown(f"""
        <div style="background:#ECE4DB; border:1px solid #CFC8BE; border-radius:12px; padding:16px; text-align:center;">
            <p style="font-size:28px; margin:0;">🚀</p>
            <p style="color:#4A3530; font-size:11px; text-transform:uppercase; letter-spacing:1px; margin:6px 0 2px; font-weight:600;">Retention</p>
            <p style="color:#C4A69B; font-size:22px; font-weight:700; margin:0;">+35%</p>
        </div>
        """, unsafe_allow_html=True)

    with imp_col2:
        st.markdown(f"""
        <div style="background:#ECE4DB; border:1px solid #CFC8BE; border-radius:12px; padding:16px; text-align:center;">
            <p style="font-size:28px; margin:0;">🔄</p>
            <p style="color:#4A3530; font-size:11px; text-transform:uppercase; letter-spacing:1px; margin:6px 0 2px; font-weight:600;">Repeat Customers</p>
            <p style="color:#C4A69B; font-size:22px; font-weight:700; margin:0;">{repeat_customers}</p>
        </div>
        """, unsafe_allow_html=True)

    with imp_col3:
        st.markdown(f"""
        <div style="background:#ECE4DB; border:1px solid #C4A69B; border-radius:12px; padding:16px; text-align:center;">
            <p style="font-size:28px; margin:0;">💰</p>
            <p style="color:#4A3530; font-size:11px; text-transform:uppercase; letter-spacing:1px; margin:6px 0 2px; font-weight:600;">Revenue</p>
            <p style="color:#C4A69B; font-size:22px; font-weight:700; margin:0;">₹{int(total_revenue):,}</p>
        </div>
        """, unsafe_allow_html=True)

# =========================
# CUSTOMERS
# =========================
elif page == "👥 Customers":
    st.title("👥 Customer Management")

    with st.expander("➕ Add New Customer", expanded=False):
        customer_name = st.text_input("Customer Name")
        if st.button("Add Customer"):
            if customer_name:
                new_customer = pd.DataFrame({"Name": [customer_name], "Phone": [""], "Points": [0], "Tier": ["Bronze"]})
                if os.path.exists("data/customers.csv"):
                    existing = pd.read_csv("data/customers.csv")
                    updated = pd.concat([existing, new_customer], ignore_index=True)
                else:
                    updated = new_customer
                updated.to_csv("data/customers.csv", index=False)
                st.success(f"✅ {customer_name} added successfully!")
                st.rerun()
            else:
                st.warning("Please enter a customer name.")

    st.subheader("Customer List")
    if os.path.exists("data/customers.csv"):
        df = pd.read_csv("data/customers.csv")
        search = st.text_input("🔍 Search Customer")

        if search:
            df = df[df["Name"].str.contains(search, case=False, na=False)]

        tier_colors = {"Bronze": "#C4A69B", "Silver": "#B8AB9C", "Gold": "#4A3530"}
        tier_emojis = {"Bronze": "🥉", "Silver": "🥈", "Gold": "🥇"}

        for _, row in df.iterrows():
            raw_tier = str(row.get("Tier", "Bronze")).capitalize()
            color = tier_colors.get(raw_tier, "#C4A69B")
            emoji = tier_emojis.get(raw_tier, "🥉")
            st.markdown(f"""
            <div style="
                background:#ECE4DB; border:1px solid #CFC8BE; border-radius:10px;
                padding:12px 16px; margin-bottom:8px; display:flex; align-items:center; justify-content:space-between;
            ">
                <div style="display:flex; align-items:center; gap:12px;">
                    <div style="
                        width:36px; height:36px; border-radius:50%; background:{color}; 
                        display:flex; align-items:center; justify-content:center; color:#FFFFFF; font-weight:700; font-size:14px;
                    ">{"".join([n[0].upper() for n in str(row["Name"]).split()][:2])}</div>
                    <div>
                        <p style="margin:0; color:#4A3530; font-weight:600; font-size:14px;">{row["Name"]}</p>
                        <p style="margin:0; color:#4A3530; font-size:12px; opacity:0.8;">{int(row["Points"]):,} points</p>
                    </div>
                </div>
                <span style="
                    background:#FFFFFF; border:1px solid {color}; border-radius:20px; 
                    padding:3px 12px; color:{color}; font-size:12px; font-weight:600;
                ">{emoji} {raw_tier}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        csv = df.to_csv(index=False)
        st.download_button(label="📥 Download Customer Report", data=csv, file_name="customers_report.csv", mime="text/csv")

# =========================
# COUPONS
# =========================
elif page == "🎟 Coupons":
    st.title("🎟 Coupon Management")

    with st.expander("➕ Create New Coupon", expanded=False):
        coupon = st.text_input("Coupon Name")
        discount = st.number_input("Discount Amount (₹)", min_value=0, step=10)
        if st.button("Create Coupon"):
            if coupon:
                new_coupon = pd.DataFrame({"Coupon": [coupon], "Discount": [discount]})
                if os.path.exists("data/coupons.csv"):
                    existing = pd.read_csv("data/coupons.csv")
                    updated = pd.concat([existing, new_coupon], ignore_index=True)
                else:
                    updated = new_coupon
                updated.to_csv("data/coupons.csv", index=False)
                st.success(f"✅ {coupon} created successfully!")
            else:
                st.warning("Please enter a coupon name.")

    if os.path.exists("data/coupons.csv"):
        coupons_df = pd.read_csv("data/coupons.csv")
        st.subheader("Active Coupons")

        cols = st.columns(3)
        for i, (_, row) in enumerate(coupons_df.iterrows()):
            with cols[i % 3]:
                st.markdown(f"""
                <div style="
                    background:#ECE4DB; border:2px dashed #C4A69B; border-radius:14px;
                    padding:20px; text-align:center; margin-bottom:12px;
                ">
                    <p style="font-size:28px; margin:0;">🎟️</p>
                    <p style="color:#4A3530; font-weight:700; font-size:15px; margin:8px 0 4px;">{row["Coupon"]}</p>
                    <p style="color:#C4A69B; font-size:22px; font-weight:700; margin:0;">₹{int(row["Discount"])}</p>
                    <p style="color:#C4A69B; opacity:0.6; font-size:11px; margin:6px 0 0;">OFF</p>
                </div>
                """, unsafe_allow_html=True)

# =========================
# PURCHASES
# =========================
elif page == "🛒 Purchases":
    st.title("🛒 Record Purchase")

    if os.path.exists("data/customers.csv"):
        customers_df = pd.read_csv("data/customers.csv")

        col1, col2 = st.columns(2)
        with col1:
            customer = st.selectbox("Select Customer", customers_df["Name"].unique())
        with col2:
            amount = st.number_input("Purchase Amount (₹)", min_value=0, step=100)

        points_preview = amount // 10
        st.markdown(f"""
        <div style="
            background:#ECE4DB; border:1px solid #CFC8BE;
            border-radius:10px; padding:12px 16px; margin:8px 0 16px;
        ">
            <p style="margin:0; color:#4A3530; font-size:12px; opacity:0.8;">Points that will be earned</p>
            <p style="margin:2px 0 0; color:#C4A69B; font-size:20px; font-weight:700;">+{points_preview} pts</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Add Purchase"):
            points_earned = amount // 10
            customers_df.loc[customers_df["Name"] == customer, "Points"] += points_earned
            new_points = customers_df.loc[customers_df["Name"] == customer, "Points"].values[0]

            if new_points < 500:
                new_tier = "Bronze"
            elif new_points < 1000:
                new_tier = "Silver"
            else:
                new_tier = "Gold"

            customers_df.loc[customers_df["Name"] == customer, "Tier"] = new_tier
            customers_df.to_csv("data/customers.csv", index=False)

            new_purchase = pd.DataFrame({"Customer": [customer], "Amount": [amount], "Points": [points_earned]})
            if os.path.exists("data/purchases.csv"):
                existing = pd.read_csv("data/purchases.csv")
                updated = pd.concat([existing, new_purchase], ignore_index=True)
            else:
                updated = new_purchase
            updated.to_csv("data/purchases.csv", index=False)
            st.success(f"✅ Purchase completed successfully!")
            st.rerun()

        st.subheader("Customer Points Overview")
        tier_colors = {"Bronze": "#C4A69B", "Silver": "#B8AB9C", "Gold": "#4A3530"}
        tier_emojis = {"Bronze": "🥉", "Silver": "🥈", "Gold": "🥇"}

        for _, row in customers_df.iterrows():
            raw_tier = str(row.get("Tier", "Bronze")).capitalize()
            color = tier_colors.get(raw_tier, "#C4A69B")
            emoji = tier_emojis.get(raw_tier, "🥉")
            bar_pct = min(int(row["Points"]) / 1000 * 100, 100)
            st.markdown(f"""
            <div style="
                background:#ECE4DB; border:1px solid #CFC8BE;
                border-radius:10px; padding:12px 16px; margin-bottom:8px;
            ">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <p style="margin:0; color:#4A3530; font-weight:600;">{row["Name"]}</p>
                    <span style="
                        background:#FFFFFF; border:1px solid {color}; border-radius:20px; 
                        padding:2px 10px; color:{color}; font-size:11px; font-weight:600;
                    ">{emoji} {raw_tier}</span>
                </div>
                <div style="display:flex; align-items:center; gap:10px;">
                    <div style="flex:1; background:#FFFFFF; border-radius:999px; height:6px; border:1px solid #CFC8BE;">
                        <div style="background:{color}; width:{bar_pct}%; height:100%; border-radius:999px;"></div>
                    </div>
                    <span style="color:#4A3530; font-size:12px; font-weight:600; min-width:60px; text-align:right;">{int(row["Points"]):,} pts</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# =========================
# LEADERBOARD
# =========================
elif page == "🏆 Leaderboard":
    st.title("🏆 Customer Leaderboard")

    if os.path.exists("data/customers.csv"):
        leaderboard = pd.read_csv("data/customers.csv").sort_values(by="Points", ascending=False).reset_index(drop=True)
        medals = ["🥇", "🥈", "🥉"]
        tier_colors = {"Bronze": "#C4A69B", "Silver": "#B8AB9C", "Gold": "#4A3530"}
        tier_emojis = {"Bronze": "🥉", "Silver": "🥈", "Gold": "🥇"}

        for i, (_, row) in enumerate(leaderboard.iterrows()):
            rank = i + 1
            raw_tier = str(row.get("Tier", "Bronze")).capitalize()
            color = tier_colors.get(raw_tier, "#C4A69B")
            tier_emoji = tier_emojis.get(raw_tier, "🥉")
            medal = medals[i] if i < 3 else f"#{rank}"
            
            bg = "#ECE4DB" if i == 0 else "#FFFFFF"
            border = "#C4A69B" if i == 0 else "#B8AB9C" if i == 1 else "#CFC8BE"
            initials = "".join([n[0].upper() for n in str(row["Name"]).split()][:2])
            bar_pct = min(int(row["Points"]) / 1000 * 100, 100)

            st.markdown(f"""
            <div style="
                background:{bg}; border:1px solid {border}; border-radius:12px;
                padding:14px 18px; margin-bottom:8px; display:flex; align-items:center; gap:14px;
            ">
                <div style="font-size:24px; min-width:36px; text-align:center;">{medal}</div>
                <div style="
                    width:38px; height:38px; border-radius:50%; background:{color}; 
                    display:flex; align-items:center; justify-content:center; color:#FFFFFF; font-weight:700; font-size:13px; flex-shrink:0;
                ">{initials}</div>
                <div style="flex:1;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">
                        <p style="margin:0; color:#4A3530; font-weight:600; font-size:14px;">{row["Name"]}</p>
                        <div style="display:flex; align-items:center; gap:8px;">
                            <span style="color:#4A3530; font-weight:700; font-size:14px;">{int(row["Points"]):,} pts</span>
                            <span style="
                                background:#FFFFFF; border:1px solid {color}; border-radius:20px; 
                                padding:2px 10px; color:{color}; font-size:11px; font-weight:600;
                            ">{tier_emoji} {raw_tier}</span>
                        </div>
                    </div>
                    <div style="background:#CFC8BE80; border-radius:999px; height:5px;">
                        <div style="background:{color}; width:{bar_pct}%; height:100%; border-radius:999px;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# =========================
# AI INSIGHTS
# =========================
elif page == "🤖 AI Insights":
    st.title("🤖 AI Insights")

    if not customers_df.empty:
        tier_colors = {"Bronze": "#C4A69B", "Silver": "#B8AB9C", "Gold": "#4A3530"}
        tier_emojis = {"Bronze": "🥉", "Silver": "🥈", "Gold": "🥇"}
        suggestions = {
            "Bronze": ("Send Welcome Coupon", "🎟️", "Offer a first-purchase discount to motivate engagement."),
            "Silver": ("Offer Bonus Reward", "⭐", "Customer is close to Gold — a bonus push could convert them."),
            "Gold": ("VIP Customer", "👑", "Highly loyal. Consider exclusive perks or early access offers."),
        }

        for _, row in customers_df.iterrows():
            raw_tier = str(row.get("Tier", "Bronze")).capitalize()
            color = tier_colors.get(raw_tier, "#C4A69B")
            emoji = tier_emojis.get(raw_tier, "🥉")
            sugg_label, sugg_icon, sugg_desc = suggestions.get(raw_tier, ("Send Promotion", "✨", "Engage customer with target rewards."))
            initials = "".join([n[0].upper() for n in str(row["Name"]).split()][:2])

            st.markdown(f"""
            <div style="
                background:#ECE4DB; border:1px solid #CFC8BE; border-radius:12px;
                padding:14px 18px; margin-bottom:10px; display:flex; align-items:center; gap:14px;
            ">
                <div style="
                    width:38px; height:38px; border-radius:50%; background:{color}; 
                    display:flex; align-items:center; justify-content:center; color:#FFFFFF; font-weight:700; font-size:13px; flex-shrink:0;
                ">{initials}</div>
                <div style="flex:1;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <p style="margin:0; color:#4A3530; font-weight:600; font-size:14px;">{row["Name"]}</p>
                        <span style="
                            background:#FFFFFF; border:1px solid {color}; border-radius:20px; 
                            padding:2px 10px; color:{color}; font-size:11px; font-weight:600;
                        ">{emoji} {raw_tier}</span>
                    </div>
                    <p style="margin:4px 0 2px; color:#C4A69B; font-size:13px; font-weight:600;">{sugg_icon} {sugg_label}</p>
                    <p style="margin:0; color:#4A3530; font-size:12px; opacity:0.8;">{sugg_desc}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No customer data available yet.")

# =========================
# LOGOUT
# =========================
if st.sidebar.button("Logout"):
    st.session_state.page = "home"
    st.rerun()