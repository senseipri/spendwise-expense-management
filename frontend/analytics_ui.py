import streamlit as st
import requests
import pandas as pd
from datetime import date, timedelta

API_BASE_URL = "http://localhost:8000"  # match your backend


def fetch_category_analytics(start_date: date, end_date: date):
    """Call POST /analytics/ and return the raw JSON dict."""
    try:
        url = f"{API_BASE_URL}/analytics/"
        payload = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        }
        resp = requests.post(url, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, dict):
            return data
        return {}
    except requests.RequestException as exc:
        st.error(f"Failed to fetch analytics: {exc}")
        return {}


def show_analytics_section():
    """Analytics page – breakdown by category with chart + table."""
    st.markdown(
        """
        <div style='text-align:center;'>
            <h3 style='font-weight:800;'>📊 Analytics</h3>
            <p class='section-subtitle'>
                Choose a date range to see where your money is going.
                We’ll break down total amounts and category percentages for you.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    today = date.today()
    default_start = today - timedelta(days=30)

    col1, col2 = st.columns(2)
    start_date = col1.date_input(
        "Start date", value=default_start, key="analytics_start"
    )
    end_date = col2.date_input("End date", value=today, key="analytics_end")

    if st.button("Get analytics"):
        if start_date > end_date:
            st.error("Start date must be before or equal to end date.")
            return

        with st.spinner("Crunching the numbers..."):
            raw_data = fetch_category_analytics(start_date, end_date)

        if not raw_data:
            st.info("No analytics data available for the selected range yet.")
            return

        records = []
        for cat, values in raw_data.items():
            if not isinstance(values, dict):
                continue
            total = float(values.get("total", 0) or 0)
            pct = float(values.get("percentage", 0) or 0)
            records.append({"Category": cat, "Total": total, "Percentage": pct})

        if not records:
            st.info("No valid analytics records returned from the backend.")
            return

        df = pd.DataFrame(records)
        df = df.sort_values("Percentage", ascending=False)

        total_spent = df["Total"].sum()
        num_categories = len(df)

        # Summary cards
        card1, card2, card3 = st.columns(3)
        card1.metric("Total spent", f"₹{total_spent:,.2f}")
        card2.metric("Categories", str(num_categories))
        card3.metric(
            "Date range",
            f"{start_date.strftime('%b %d')} – {end_date.strftime('%b %d')}",
        )

        st.markdown("")
        chart_col, table_col = st.columns([1.1, 1])
        with chart_col:
            st.markdown("#### Category share")
            chart_df = df.set_index("Category")["Percentage"]
            st.bar_chart(chart_df)

        with table_col:
            st.markdown("#### Breakdown table")
            styled = df.style.format(
                {"Total": "₹{:,.2f}", "Percentage": "{:.2f}%"}
            )
            st.dataframe(styled, use_container_width=True)
