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
    repeat_customers = (
        purchases_df["Customer"]
        .value_counts()
        .gt(1)
        .sum()
    )

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
    background: linear-gradient(135deg, #1C1008 0%, #2B1420 100%);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 24px;
    border: 1px solid #FFB17340;
">
    <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
        <div>
            <p style="margin:0; color:#FFB173; font-size:13px;">{greeting},</p>
            <h2 style="margin:0; color:#FFE3B3; font-size:24px; font-weight:700;">🏪 Business Owner</h2>
            <p style="margin:4px 0 0; color:#FFB17380; font-size:12px;">{datetime.now().strftime("%A, %d %B %Y")}</p>
        </div>
        <div style="display:flex; gap:12px; flex-wrap:wrap;">
            <div style="background:#FFB17315; border:1px solid #FFB17340; border-radius:12px; padding:12px 20px; text-align:center;">
                <p style="margin:0; color:#FFB17399; font-size:11px; text-transform:uppercase; letter-spacing:1px;">Customers</p>
                <p style="margin:2px 0 0; color:#FFE3B3; font-size:22px; font-weight:700;">{total_customers}</p>
            </div>
            <div style="background:#CA285115; border:1px solid #CA285140; border-radius:12px; padding:12px 20px; text-align:center;">
                <p style="margin:0; color:#CA285199; font-size:11px; text-transform:uppercase; letter-spacing:1px;">Revenue</p>
                <p style="margin:2px 0 0; color:#FFE3B3; font-size:22px; font-weight:700;">₹{int(total_revenue):,}</p>
            </div>
            <div style="background:#FF676615; border:1px solid #FF676640; border-radius:12px; padding:12px 20px; text-align:center;">
                <p style="margin:0; color:#FF676699; font-size:11px; text-transform:uppercase; letter-spacing:1px;">Redemptions</p>
                <p style="margin:2px 0 0; color:#FFE3B3; font-size:22px; font-weight:700;">{total_redemptions}</p>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# ANALYTICS
# =========================

if page == "📊 Analytics":

    # Stat cards
    col1, col2, col3, col4 = st.columns(4)

    stats = [
        ("👥", "Total Customers", str(total_customers), "#FFB173"),
        ("💰", "Revenue", f"₹{int(total_revenue):,}", "#CA2851"),
        ("🔄", "Repeat Customers", str(repeat_customers), "#FF6766"),
        ("🎁", "Redemptions", str(total_redemptions), "#FFB173"),
    ]

    for col, (icon, label, value, color) in zip([col1, col2, col3, col4], stats):
        with col:
            st.markdown(f"""
            <div style="
                background:#1C1008;
                border:1px solid {color}40;
                border-radius:12px;
                padding:16px;
                text-align:center;
                margin-bottom:16px;
            ">
                <p style="font-size:24px; margin:0;">{icon}</p>
                <p style="margin:4px 0 2px; color:{color}99; font-size:11px; text-transform:uppercase; letter-spacing:1px;">{label}</p>
                <p style="margin:0; color:#FFE3B3; font-size:20px; font-weight:700;">{value}</p>
            </div>
            """, unsafe_allow_html=True)

    # Revenue chart
    sales = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May"],
        "Revenue": [15000, 25000, 40000, 55000, 75000]
    })

    fig = px.line(
        sales, x="Month", y="Revenue",
        title="Revenue Growth"
    )
    fig.update_traces(line_color="#CA2851", line_width=3)
    fig.update_layout(
        paper_bgcolor="#1C1008",
        plot_bgcolor="#1C1008",
        font_color="#FFE3B3",
        title_font_color="#FFB173",
        xaxis=dict(gridcolor="rgba(255,177,115,0.08)", color="rgba(255,177,115,0.6)"),
        yaxis=dict(gridcolor="rgba(255,177,115,0.08)", color="rgba(255,177,115,0.6)"),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Customer growth bar chart
    if not customers_df.empty:

        customer_growth = pd.DataFrame({
            "Stage": ["New", "Bronze", "Silver", "Gold"],
            "Customers": [
                len(customers_df[customers_df["Points"] < 100]),
                len(customers_df[(customers_df["Points"] >= 100) & (customers_df["Points"] < 500)]),
                len(customers_df[(customers_df["Points"] >= 500) & (customers_df["Points"] < 1000)]),
                len(customers_df[customers_df["Points"] >= 1000])
            ]
        })

        fig2 = px.bar(
            customer_growth, x="Stage", y="Customers",
            title="Customer Stage Distribution",
            color="Stage",
            color_discrete_map={
                "New": "#FFE3B3",
                "Bronze": "#CA2851",
                "Silver": "#FF6766",
                "Gold": "#FFB173"
            }
        )
        fig2.update_layout(
            paper_bgcolor="#1C1008",
            plot_bgcolor="#1C1008",
            font_color="#FFE3B3",
            title_font_color="#FFB173",
            xaxis=dict(gridcolor="rgba(255,177,115,0.08)", color="rgba(255,177,115,0.6)"),
            yaxis=dict(gridcolor="rgba(255,177,115,0.08)", color="rgba(255,177,115,0.6)"),
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # Tier pie chart
    if not customers_df.empty:

        tier_counts = (
            customers_df["Tier"]
            .value_counts()
            .reset_index()
        )
        tier_counts.columns = ["Tier", "Count"]

        st.subheader("🥧 Customer Tier Distribution")

        pie_fig = px.pie(
            tier_counts,
            names="Tier",
            values="Count",
            color="Tier",
            color_discrete_map={
                "Bronze": "#CA2851",
                "Silver": "#FF6766",
                "Gold": "#FFB173"
            }
        )
        pie_fig.update_traces(textinfo="percent+label")
        pie_fig.update_layout(
            paper_bgcolor="#1C1008",
            plot_bgcolor="#1C1008",
            font_color="#FFE3B3",
        )
        st.plotly_chart(pie_fig, use_container_width=True)

    st.markdown("---")

    # Recent redemptions
    st.subheader("🎁 Recent Reward Redemptions")

    if os.path.exists("data/redemptions.csv"):
        redemptions = pd.read_csv("data/redemptions.csv")
        st.dataframe(redemptions.tail(10), use_container_width=True)
    else:
        st.info("No reward redemptions yet.")

    st.markdown("---")

    # Business impact
    st.subheader("📊 Business Impact")

    imp_col1, imp_col2, imp_col3 = st.columns(3)

    with imp_col1:
        st.markdown(f"""
        <div style="background:#1C1008; border:1px solid #CA285140; border-radius:12px; padding:16px; text-align:center;">
            <p style="font-size:28px; margin:0;">🚀</p>
            <p style="color:#CA285199; font-size:11px; text-transform:uppercase; letter-spacing:1px; margin:6px 0 2px;">Retention</p>
            <p style="color:#FFE3B3; font-size:22px; font-weight:700; margin:0;">+35%</p>
        </div>
        """, unsafe_allow_html=True)

    with imp_col2:
        st.markdown(f"""
        <div style="background:#1C1008; border:1px solid #FF676640; border-radius:12px; padding:16px; text-align:center;">
            <p style="font-size:28px; margin:0;">🔄</p>
            <p style="color:#FF676699; font-size:11px; text-transform:uppercase; letter-spacing:1px; margin:6px 0 2px;">Repeat Customers</p>
            <p style="color:#FFE3B3; font-size:22px; font-weight:700; margin:0;">{repeat_customers}</p>
        </div>
        """, unsafe_allow_html=True)

    with imp_col3:
        st.markdown(f"""
        <div style="background:#1C1008; border:1px solid #FFB17340; border-radius:12px; padding:16px; text-align:center;">
            <p style="font-size:28px; margin:0;">💰</p>
            <p style="color:#FFB17399; font-size:11px; text-transform:uppercase; letter-spacing:1px; margin:6px 0 2px;">Revenue</p>
            <p style="color:#FFE3B3; font-size:22px; font-weight:700; margin:0;">₹{int(total_revenue):,}</p>
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
                new_customer = pd.DataFrame({
                    "Name": [customer_name],
                    "Phone": [""],
                    "Points": [0],
                    "Tier": ["Bronze"]
                })
                if os.path.exists("data/customers.csv"):
                    existing = pd.read_csv("data/customers.csv")
                    updated = pd.concat([existing, new_customer], ignore_index=True)
                else:
                    updated = new_customer
                updated.to_csv("data/customers.csv", index=False)
                st.success(f"✅ {customer_name} added successfully!")
            else:
                st.warning("Please enter a customer name.")

    st.subheader("Customer List")

    if os.path.exists("data/customers.csv"):

        df = pd.read_csv("data/customers.csv")
        search = st.text_input("🔍 Search Customer")

        if search:
            df = df[df["Name"].str.contains(search, case=False, na=False)]

        # Styled customer rows
        tier_colors = {"Bronze": "#CA2851", "Silver": "#FF6766", "Gold": "#FFB173"}
        tier_emojis = {"Bronze": "🥉", "Silver": "🥈", "Gold": "🥇"}

        for _, row in df.iterrows():
            t = row.get("Tier", "Bronze")
            color = tier_colors.get(t, "#FFB173")
            emoji = tier_emojis.get(t, "🥉")
            st.markdown(f"""
            <div style="
                background:#1C1008;
                border:1px solid {color}40;
                border-radius:10px;
                padding:12px 16px;
                margin-bottom:8px;
                display:flex;
                align-items:center;
                justify-content:space-between;
            ">
                <div style="display:flex; align-items:center; gap:12px;">
                    <div style="
                        width:36px; height:36px; border-radius:50%;
                        background:{color}; display:flex; align-items:center;
                        justify-content:center; color:#FFF6E8; font-weight:700; font-size:14px;
                    ">{"".join([n[0].upper() for n in str(row["Name"]).split()][:2])}</div>
                    <div>
                        <p style="margin:0; color:#FFE3B3; font-weight:600; font-size:14px;">{row["Name"]}</p>
                        <p style="margin:0; color:#FFB17380; font-size:12px;">{int(row["Points"]):,} points</p>
                    </div>
                </div>
                <span style="
                    background:{color}22; border:1px solid {color};
                    border-radius:20px; padding:3px 12px;
                    color:{color}; font-size:12px; font-weight:600;
                ">{emoji} {t}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Customer Report",
            data=csv,
            file_name="customers_report.csv",
            mime="text/csv"
        )

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
                    background:#1C1008;
                    border:2px dashed #FFB173;
                    border-radius:14px;
                    padding:20px;
                    text-align:center;
                    margin-bottom:12px;
                ">
                    <p style="font-size:28px; margin:0;">🎟️</p>
                    <p style="color:#FFE3B3; font-weight:700; font-size:15px; margin:8px 0 4px;">{row["Coupon"]}</p>
                    <p style="color:#FFB173; font-size:22px; font-weight:700; margin:0;">₹{int(row["Discount"])}</p>
                    <p style="color:#FFB17360; font-size:11px; margin:6px 0 0;">OFF</p>
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
            customer = st.selectbox("Select Customer", customers_df["Name"])
        with col2:
            amount = st.number_input("Purchase Amount (₹)", min_value=0, step=100)

        points_preview = amount // 10
        st.markdown(f"""
        <div style="
            background:#1C1008; border:1px solid #FFB17340;
            border-radius:10px; padding:12px 16px; margin:8px 0 16px;
        ">
            <p style="margin:0; color:#FFB17399; font-size:12px;">Points that will be earned</p>
            <p style="margin:2px 0 0; color:#FFB173; font-size:20px; font-weight:700;">+{points_preview} pts</p>
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

            new_purchase = pd.DataFrame({
                "Customer": [customer],
                "Amount": [amount],
                "Points": [points_earned]
            })

            if os.path.exists("data/purchases.csv"):
                existing = pd.read_csv("data/purchases.csv")
                updated = pd.concat([existing, new_purchase], ignore_index=True)
            else:
                updated = new_purchase

            updated.to_csv("data/purchases.csv", index=False)
            st.success(f"✅ {customer} earned {points_earned} points! Now at {int(new_points)} total.")

        st.subheader("Customer Points Overview")

        tier_colors = {"Bronze": "#CA2851", "Silver": "#FF6766", "Gold": "#FFB173"}
        tier_emojis = {"Bronze": "🥉", "Silver": "🥈", "Gold": "🥇"}

        for _, row in customers_df.iterrows():
            t = row.get("Tier", "Bronze")
            color = tier_colors.get(t, "#FFB173")
            emoji = tier_emojis.get(t, "🥉")
            bar_pct = min(int(row["Points"]) / 1000 * 100, 100)
            st.markdown(f"""
            <div style="
                background:#1C1008; border:1px solid {color}30;
                border-radius:10px; padding:12px 16px; margin-bottom:8px;
            ">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <p style="margin:0; color:#FFE3B3; font-weight:600;">{row["Name"]}</p>
                    <span style="
                        background:{color}22; border:1px solid {color};
                        border-radius:20px; padding:2px 10px;
                        color:{color}; font-size:11px; font-weight:600;
                    ">{emoji} {t}</span>
                </div>
                <div style="display:flex; align-items:center; gap:10px;">
                    <div style="flex:1; background:#FFB17315; border-radius:999px; height:6px;">
                        <div style="background:{color}; width:{bar_pct}%; height:100%; border-radius:999px;"></div>
                    </div>
                    <span style="color:#FFB173; font-size:12px; font-weight:600; min-width:60px; text-align:right;">{int(row["Points"]):,} pts</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# =========================
# LEADERBOARD
# =========================

elif page == "🏆 Leaderboard":

    st.title("🏆 Customer Leaderboard")

    if os.path.exists("data/customers.csv"):

        leaderboard = pd.read_csv("data/customers.csv")
        leaderboard = leaderboard.sort_values(
            by="Points", ascending=False
        ).reset_index(drop=True)

        medals = ["🥇", "🥈", "🥉"]
        tier_colors = {"Bronze": "#CA2851", "Silver": "#FF6766", "Gold": "#FFB173"}
        tier_emojis = {"Bronze": "🥉", "Silver": "🥈", "Gold": "🥇"}

        for i, (_, row) in enumerate(leaderboard.iterrows()):
            rank = i + 1
            t = row.get("Tier", "Bronze")
            color = tier_colors.get(t, "#FFB173")
            tier_emoji = tier_emojis.get(t, "🥉")
            medal = medals[i] if i < 3 else f"#{rank}"
            bg = "#FFB17310" if i == 0 else "#FF676608" if i == 1 else "#CA285108" if i == 2 else "#1C1008"
            border = "#FFB173" if i == 0 else "#FF6766" if i == 1 else "#CA2851" if i == 2 else f"{color}30"
            initials = "".join([n[0].upper() for n in str(row["Name"]).split()][:2])
            bar_pct = min(int(row["Points"]) / 1000 * 100, 100)

            st.markdown(f"""
            <div style="
                background:{bg};
                border:1px solid {border};
                border-radius:12px;
                padding:14px 18px;
                margin-bottom:8px;
                display:flex;
                align-items:center;
                gap:14px;
            ">
                <div style="font-size:24px; min-width:36px; text-align:center;">{medal}</div>
                <div style="
                    width:38px; height:38px; border-radius:50%;
                    background:{color}; display:flex; align-items:center;
                    justify-content:center; color:#FFF6E8;
                    font-weight:700; font-size:13px; flex-shrink:0;
                ">{initials}</div>
                <div style="flex:1;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">
                        <p style="margin:0; color:#FFE3B3; font-weight:600; font-size:14px;">{row["Name"]}</p>
                        <div style="display:flex; align-items:center; gap:8px;">
                            <span style="color:#FFB173; font-weight:700; font-size:14px;">{int(row["Points"]):,} pts</span>
                            <span style="
                                background:{color}22; border:1px solid {color};
                                border-radius:20px; padding:2px 10px;
                                color:{color}; font-size:11px; font-weight:600;
                            ">{tier_emoji} {t}</span>
                        </div>
                    </div>
                    <div style="background:#FFB17315; border-radius:999px; height:5px;">
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

        tier_colors = {"Bronze": "#CA2851", "Silver": "#FF6766", "Gold": "#FFB173"}
        tier_emojis = {"Bronze": "🥉", "Silver": "🥈", "Gold": "🥇"}
        suggestions = {
            "Bronze": ("Send Welcome Coupon", "🎟️", "Offer a first-purchase discount to motivate engagement."),
            "Silver": ("Offer Bonus Reward", "⭐", "Customer is close to Gold — a bonus push could convert them."),
            "Gold": ("VIP Customer", "👑", "Highly loyal. Consider exclusive perks or early access offers."),
        }

        for _, row in customers_df.iterrows():
            t = row.get("Tier", "Bronze")
            color = tier_colors.get(t, "#FFB173")
            emoji = tier_emojis.get(t, "🥉")
            sugg_label, sugg_icon, sugg_desc = suggestions.get(t, ("", "", ""))
            initials = "".join([n[0].upper() for n in str(row["Name"]).split()][:2])

            st.markdown(f"""
            <div style="
                background:#1C1008;
                border:1px solid {color}40;
                border-radius:12px;
                padding:14px 18px;
                margin-bottom:10px;
                display:flex;
                align-items:center;
                gap:14px;
            ">
                <div style="
                    width:38px; height:38px; border-radius:50%;
                    background:{color}; display:flex; align-items:center;
                    justify-content:center; color:#FFF6E8;
                    font-weight:700; font-size:13px; flex-shrink:0;
                ">{initials}</div>
                <div style="flex:1;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <p style="margin:0; color:#FFE3B3; font-weight:600; font-size:14px;">{row["Name"]}</p>
                        <span style="
                            background:{color}22; border:1px solid {color};
                            border-radius:20px; padding:2px 10px;
                            color:{color}; font-size:11px; font-weight:600;
                        ">{emoji} {t}</span>
                    </div>
                    <p style="margin:4px 0 2px; color:#FFB173; font-size:13px; font-weight:600;">{sugg_icon} {sugg_label}</p>
                    <p style="margin:0; color:#FFB17380; font-size:12px;">{sugg_desc}</p>
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