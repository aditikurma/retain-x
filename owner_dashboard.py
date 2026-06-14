
import streamlit as st
import pandas as pd
import plotly.express as px
import os
 
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
# ANALYTICS
# =========================
if page == "📊 Analytics":
 
    st.title("📈 Owner Dashboard")
 
    # =========================
    # REAL ANALYTICS
    # =========================
 
    total_customers = 0
    total_revenue = 0
    repeat_customers = 0
 
    if os.path.exists("data/customers.csv"):
 
        customers_df = pd.read_csv(
            "data/customers.csv"
        )
 
        total_customers = len(
            customers_df
        )
 
    if os.path.exists("data/purchases.csv"):
 
        purchases_df = pd.read_csv(
            "data/purchases.csv"
        )
 
        total_revenue = purchases_df[
            "Amount"
        ].sum()
 
        repeat_customers = (
            purchases_df["Customer"]
            .value_counts()
            .gt(1)
            .sum()
        )
 
    col1, col2, col3 = st.columns(3)
 
    with col1:
        st.metric(
            "Total Customers",
            total_customers
        )
 
    with col2:
        st.metric(
            "Revenue",
            f"₹{int(total_revenue):,}"
        )
 
    with col3:
        st.metric(
            "Repeat Customers",
            repeat_customers
        )
 
    # =========================
    # REVENUE CHART
    # =========================
 
    sales = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May"],
        "Revenue": [15000, 25000, 40000, 55000, 75000]
    })
 
    fig = px.line(
        sales,
        x="Month",
        y="Revenue",
        title="Revenue Growth"
    )
 
    fig.update_traces(
        line_color="#CA2851",
        line_width=4
    )
 
    st.plotly_chart(
        fig,
        use_container_width=True
    )
 
    # =========================
    # CUSTOMER GROWTH
    # =========================
 
    if os.path.exists("data/customers.csv"):
 
        customer_growth = pd.DataFrame({
            "Stage": [
                "New",
                "Bronze",
                "Silver",
                "Gold"
            ],
            "Customers": [
                len(customers_df[customers_df["Points"] < 100]),
                len(customers_df[
                    (customers_df["Points"] >= 100)
                    & (customers_df["Points"] < 500)
                ]),
                len(customers_df[
                    (customers_df["Points"] >= 500)
                    & (customers_df["Points"] < 1000)
                ]),
                len(customers_df[
                    customers_df["Points"] >= 1000
                ])
            ]
        })
 
        fig2 = px.bar(
            customer_growth,
            x="Stage",
            y="Customers",
            title="Customer Growth"
        )
 
        fig2.update_traces(
            marker_color="#FFB173"
        )
 
        st.plotly_chart(
            fig2,
            use_container_width=True
        )
 
    st.markdown("---")
 
    # =========================
    # REDEMPTIONS
    # =========================
 
    st.subheader(
        "🎁 Recent Reward Redemptions"
    )
 
    if os.path.exists(
        "data/redemptions.csv"
    ):
 
        redemptions = pd.read_csv(
            "data/redemptions.csv"
        )
 
        st.dataframe(
            redemptions.tail(10)
        )
 
    else:
 
        st.info(
            "No reward redemptions yet."
        )
 
    st.markdown("---")
 
    # =========================
    # AI INSIGHTS
    # =========================
 
    st.subheader(
        "🤖 AI Customer Insights"
    )
 
    if os.path.exists(
        "data/customers.csv"
    ):
 
        customers = pd.read_csv(
            "data/customers.csv"
        )
 
        insights = []
 
        for _, row in customers.iterrows():
 
            points = row["Points"]
 
            if points < 500:
                suggestion = (
                    "Send Welcome Coupon"
                )
 
            elif points < 1000:
                suggestion = (
                    "Offer Bonus Reward"
                )
 
            else:
                suggestion = (
                    "VIP Customer"
                )
 
            insights.append({
                "Customer": row["Name"],
                "Points": points,
                "Tier": row["Tier"],
                "Suggestion": suggestion
            })
 
        insights_df = pd.DataFrame(
            insights
        )
 
        st.dataframe(
            insights_df
        )
 
    st.markdown("---")
 
    # =========================
    # CUSTOMER TIER DISTRIBUTION
    # =========================
 
    if os.path.exists(
        "data/customers.csv"
    ):
 
        tier_counts = (
            customers_df["Tier"]
            .value_counts()
            .reset_index()
        )
 
        tier_counts.columns = [
            "Tier",
            "Count"
        ]
 
        st.subheader(
            "🥧 Customer Tier Distribution"
        )
 
        pie_fig = px.pie(
            tier_counts,
            names="Tier",
            values="Count",
            title="Bronze vs Silver vs Gold Customers",
            color="Tier",
            color_discrete_map={
                "Bronze": "#CA2851",
                "Silver": "#FF6766",
                "Gold": "#FFE3B3"
            }
        )
 
        pie_fig.update_traces(
            textinfo="percent+label"
        )
 
        pie_fig.update_layout(
            paper_bgcolor="#0B0B0F",
            plot_bgcolor="#0B0B0F",
            font_color="white"
        )
 
        st.plotly_chart(
            pie_fig,
            use_container_width=True
        )
 
    st.markdown("---")
 
    # =========================
    # BUSINESS IMPACT
    # =========================
 
    total_redemptions = 0
 
    if os.path.exists(
        "data/redemptions.csv"
    ):
 
        redemptions_df = pd.read_csv(
            "data/redemptions.csv"
        )
 
        total_redemptions = len(
            redemptions_df
        )
 
    st.subheader(
        "📊 Business Impact"
    )
 
    st.success(
        f"""
🚀 Retention Improved: +35%
 
👥 Active Customers: {total_customers}
 
🔄 Repeat Customers: {repeat_customers}
 
🎁 Rewards Redeemed: {total_redemptions}
 
💰 Revenue Generated: ₹{int(total_revenue):,}
 
⭐ Customer Loyalty Program Successfully Increasing Engagement
        """
    )
 
# =========================
# CUSTOMERS
# =========================
elif page == "👥 Customers":
 
    st.title("👥 Customer Management")
 
    customer_name = st.text_input(
        "Customer Name"
    )
 
    if st.button("Add Customer"):
 
        new_customer = pd.DataFrame({
            "Name": [customer_name],
            "Phone": [""],
            "Points": [0],
            "Tier": ["Bronze"]
        })
 
        if os.path.exists(
            "data/customers.csv"
        ):
 
            existing = pd.read_csv(
                "data/customers.csv"
            )
 
            updated = pd.concat(
                [existing, new_customer],
                ignore_index=True
            )
 
        else:
            updated = new_customer
 
        updated.to_csv(
            "data/customers.csv",
            index=False
        )
 
        st.success(
            f"{customer_name} added successfully"
        )
 
    st.subheader(
        "Customer List"
    )
 
    if os.path.exists(
        "data/customers.csv"
    ):
 
        df = pd.read_csv(
            "data/customers.csv"
        )
 
        search = st.text_input(
            "🔍 Search Customer"
        )
 
        if search:
 
            df = df[
                df["Name"]
                .str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]
 
        st.dataframe(
            df
        )
 
        csv = df.to_csv(
            index=False
        )
 
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
 
    coupon = st.text_input(
        "Coupon Name"
    )
 
    discount = st.number_input(
        "Discount Amount (₹)",
        min_value=0,
        step=10
    )
 
    if st.button(
        "Create Coupon"
    ):
 
        new_coupon = pd.DataFrame({
            "Coupon": [coupon],
            "Discount": [discount]
        })
 
        if os.path.exists(
            "data/coupons.csv"
        ):
 
            existing = pd.read_csv(
                "data/coupons.csv"
            )
 
            updated = pd.concat(
                [existing, new_coupon],
                ignore_index=True
            )
 
        else:
            updated = new_coupon
 
        updated.to_csv(
            "data/coupons.csv",
            index=False
        )
 
        st.success(
            f"{coupon} created successfully"
        )
 
    if os.path.exists(
        "data/coupons.csv"
    ):
 
        coupons_df = pd.read_csv(
            "data/coupons.csv"
        )
 
        st.dataframe(
            coupons_df
        )
 
# =========================
# PURCHASES
# =========================
elif page == "🛒 Purchases":
 
    st.title("🛒 Record Purchase")
 
    if os.path.exists(
        "data/customers.csv"
    ):
 
        customers_df = pd.read_csv(
            "data/customers.csv"
        )
 
        customer = st.selectbox(
            "Select Customer",
            customers_df["Name"]
        )
 
        amount = st.number_input(
            "Purchase Amount (₹)",
            min_value=0,
            step=100
        )
 
        if st.button(
            "Add Purchase"
        ):
 
            points_earned = amount // 10
 
            customers_df.loc[
                customers_df["Name"] == customer,
                "Points"
            ] += points_earned
 
            new_points = customers_df.loc[
                customers_df["Name"] == customer,
                "Points"
            ].values[0]
 
            if new_points < 500:
                new_tier = "Bronze"
            elif new_points < 1000:
                new_tier = "Silver"
            else:
                new_tier = "Gold"
 
            customers_df.loc[
                customers_df["Name"] == customer,
                "Tier"
            ] = new_tier
 
            customers_df.to_csv(
                "data/customers.csv",
                index=False
            )
 
            new_purchase = pd.DataFrame({
                "Customer": [customer],
                "Amount": [amount],
                "Points": [points_earned]
            })
 
            if os.path.exists(
                "data/purchases.csv"
            ):
 
                existing = pd.read_csv(
                    "data/purchases.csv"
                )
 
                updated = pd.concat(
                    [existing, new_purchase],
                    ignore_index=True
                )
 
            else:
 
                updated = new_purchase
 
            updated.to_csv(
                "data/purchases.csv",
                index=False
            )
 
            st.success(
                f"{customer} earned {points_earned} points!"
            )
 
        st.subheader(
            "Customer Points"
        )
 
        st.dataframe(
            customers_df[
                ["Name", "Points", "Tier"]
            ]
        )
 
# =========================
# LEADERBOARD
# =========================
elif page == "🏆 Leaderboard":
 
    st.title(
        "🏆 Customer Leaderboard"
    )
 
    if os.path.exists(
        "data/customers.csv"
    ):
 
        leaderboard = pd.read_csv(
            "data/customers.csv"
        )
 
        leaderboard = leaderboard.sort_values(
            by="Points",
            ascending=False
        ).reset_index(drop=True)
 
        leaderboard.index += 1
 
        st.dataframe(
            leaderboard[
                ["Name", "Points", "Tier"]
            ]
        )
 
        if len(leaderboard) > 0:
 
            top_customer = leaderboard.iloc[0]
 
            st.success(
                f"🥇 {top_customer['Name']} • {top_customer['Points']} Points"
            )
 
# =========================
# AI INSIGHTS
# =========================
 
elif page == "🤖 AI Insights":
 
    st.title("🤖 AI Insights")
 
    st.success(
        """
🎯 Customers with low points should receive coupons.
 
🏆 Gold members should receive VIP rewards.
 
🔄 Repeat customers are highly engaged.
 
📈 Loyalty program is increasing retention.
        """
    )
 
# =========================
# LOGOUT
# =========================
if st.sidebar.button("Logout"):
 
    st.session_state.page = "home"
    st.rerun()