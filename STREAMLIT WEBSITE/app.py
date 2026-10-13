import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Workie Competitor Intelligence",
    page_icon="🟠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# WORKIE-INSPIRED THEME
# =========================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #ffffff;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #fff7f0;
        border-right: 1px solid #eeeeee;
    }

    /* Main title */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #222222;
        margin-bottom: 5px;
    }

    .orange-text {
        color: #f97316;
    }

    .subtitle {
        font-size: 17px;
        color: #666666;
        margin-bottom: 30px;
    }

    /* KPI cards */
    .kpi-card {
        background: #ffffff;
        border: 1px solid #eeeeee;
        border-left: 5px solid #f97316;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0px 3px 12px rgba(0,0,0,0.06);
        min-height: 120px;
    }

    .kpi-title {
        font-size: 14px;
        color: #777777;
        margin-bottom: 8px;
    }

    .kpi-value {
        font-size: 28px;
        font-weight: 800;
        color: #222222;
    }

    /* Section headers */
    .section-title {
        font-size: 25px;
        font-weight: 750;
        color: #222222;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    /* Info box */
    .info-box {
        background: #fff7f0;
        border: 1px solid #fed7aa;
        border-radius: 12px;
        padding: 18px;
        margin: 15px 0;
    }

    /* Insight cards */
    .insight-card {
        background: #ffffff;
        border: 1px solid #eeeeee;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 12px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
    }

    /* Buttons */
    .stButton > button {
        background-color: #f97316;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }

    .stButton > button:hover {
        background-color: #ea580c;
        color: white;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
    r"C:\Users\sujal\workie competitor analysis\workie_competitor_raw.csv"
)


    # =====================================================
    # DATE
    # =====================================================

    if "data_date" in df.columns:
        df["data_date"] = pd.to_datetime(
            df["data_date"],
            errors="coerce"
        )

    # =====================================================
    # NUMERIC COLUMNS
    # =====================================================

    numeric_columns = [
        "seat_capacity",
        "price_per_seat_month",
        "day_pass_price",
        "meeting_room_price_hour"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # =====================================================
    # CREATE AMENITY SCORE IF IT DOES NOT EXIST
    # =====================================================

    amenity_columns = [
        "private_office_available",
        "dedicated_desk",
        "hot_desk",
        "virtual_office",
        "meeting_room",
        "conference_room",
        "wifi",
        "parking",
        "power_backup",
        "cafeteria",
        "housekeeping",
        "security",
        "24x7_access",
        "air_conditioning",
        "printing",
        "event_space",
        "community_events",
        "managed_office",
        "build_to_suit",
        "enterprise_solution"
    ]

    available_amenity_columns = [
        col for col in amenity_columns
        if col in df.columns
    ]

    if available_amenity_columns:

        df["amenity_score"] = (
            df[available_amenity_columns]
            .eq("Yes")
            .sum(axis=1)
        )

    else:

        df["amenity_score"] = 0

    # =====================================================
    # CREATE COMPLETENESS SCORE IF NEEDED
    # =====================================================

    if "completeness_score" not in df.columns:

        df["completeness_score"] = (
            df.notna().sum(axis=1)
            / len(df.columns)
            * 100
        ).round(2)

    else:

        df["completeness_score"] = pd.to_numeric(
            df["completeness_score"],
            errors="coerce"
        )

    return df

df = load_data()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    "<h1 style='color:#f97316;'>WORKIE</h1>",
    unsafe_allow_html=True
)

st.sidebar.markdown(
    "**Competitor Intelligence**"
)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Executive Overview",
        "💰 Pricing Analysis",
        "📍 Location Analysis",
        "🏢 Workspace Analysis",
        "✨ Amenities",
        "⚔️ Workie vs Competitors",
        "💡 Business Insights"
    ]
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Competitor analysis based on the provided dataset."
)

st.sidebar.caption(
    "Practice / analytical project — not an official Workie website."
)


# =========================================================
# GLOBAL FILTERS
# =========================================================

st.sidebar.subheader("Filters")

companies = sorted(
    df["company"].dropna().unique()
)

selected_companies = st.sidebar.multiselect(
    "Company",
    companies,
    default=companies
)

locations = sorted(
    df["location"].dropna().unique()
)

selected_locations = st.sidebar.multiselect(
    "Location",
    locations,
    default=locations
)

filtered_df = df[
    df["company"].isin(selected_companies) &
    df["location"].isin(selected_locations)
].copy()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">Workie <span class="orange-text">Competitor Intelligence</span></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Competitive pricing, workspace and amenity analysis for the flexible-office market.</div>',
    unsafe_allow_html=True
)


# =========================================================
# EXECUTIVE OVERVIEW
# =========================================================

if page == "🏠 Executive Overview":

    st.markdown(
        '<div class="section-title">Executive Overview</div>',
        unsafe_allow_html=True
    )

    # KPIs
    total_records = len(filtered_df)

    total_companies = filtered_df["company"].nunique()

    total_locations = filtered_df["location"].nunique()

    avg_price = filtered_df[
        "price_per_seat_month"
    ].mean()

    avg_day_pass = filtered_df[
        "day_pass_price"
    ].mean()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Records</div>
                <div class="kpi-value">{total_records:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Competitors</div>
                <div class="kpi-value">{total_companies}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Locations</div>
                <div class="kpi-value">{total_locations}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Avg Monthly Price</div>
                <div class="kpi-value">₹{avg_price:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col5:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Avg Day Pass</div>
                <div class="kpi-value">₹{avg_day_pass:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # Company distribution
    col1, col2 = st.columns(2)

    with col1:

        company_count = (
            filtered_df["company"]
            .value_counts()
            .reset_index()
        )

        company_count.columns = [
            "company",
            "records"
        ]

        fig = px.bar(
            company_count,
            x="company",
            y="records",
            title="Records by Competitor",
            text="records"
        )

        fig.update_traces(
            marker_color="#f97316"
        )

        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        workspace_count = (
            filtered_df["workspace_type"]
            .value_counts()
            .reset_index()
        )

        workspace_count.columns = [
            "workspace_type",
            "records"
        ]

        fig = px.pie(
            workspace_count,
            names="workspace_type",
            values="records",
            title="Workspace Type Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# PRICING ANALYSIS
# =========================================================

elif page == "💰 Pricing Analysis":

    st.markdown(
        '<div class="section-title">Pricing Analysis</div>',
        unsafe_allow_html=True
    )

    price_by_company = (
        filtered_df
        .groupby("company")["price_per_seat_month"]
        .mean()
        .reset_index()
        .sort_values(
            "price_per_seat_month"
        )
    )

    fig = px.bar(
        price_by_company,
        x="company",
        y="price_per_seat_month",
        title="Average Monthly Seat Price by Company",
        text_auto=".0f"
    )

    fig.update_traces(
        marker_color="#f97316"
    )

    fig.update_layout(
        yaxis_title="Average Price (₹)",
        xaxis_title="Company",
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Workspace price
    workspace_price = (
        filtered_df
        .groupby("workspace_type")[
            "price_per_seat_month"
        ]
        .mean()
        .reset_index()
        .sort_values(
            "price_per_seat_month"
        )
    )

    fig = px.bar(
        workspace_price,
        x="workspace_type",
        y="price_per_seat_month",
        title="Average Price by Workspace Type",
        text_auto=".0f"
    )

    fig.update_traces(
        marker_color="#fb923c"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("### Price Records")

    st.dataframe(
        filtered_df[
            [
                "company",
                "location",
                "workspace_type",
                "price_per_seat_month"
            ]
        ].sort_values(
            "price_per_seat_month"
        ),
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# LOCATION ANALYSIS
# =========================================================

elif page == "📍 Location Analysis":

    st.markdown(
        '<div class="section-title">Location Analysis</div>',
        unsafe_allow_html=True
    )

    location_count = (
        filtered_df["location"]
        .value_counts()
        .reset_index()
    )

    location_count.columns = [
        "location",
        "records"
    ]

    fig = px.bar(
        location_count.head(20),
        x="records",
        y="location",
        orientation="h",
        title="Competitor Presence by Location",
        text="records"
    )

    fig.update_traces(
        marker_color="#f97316"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("### Janjeerwala Square")

    janjeerwala = filtered_df[
        filtered_df["location"]
        .str.contains(
            "Janjeerwala",
            case=False,
            na=False
        )
    ]

    if len(janjeerwala) > 0:

        st.dataframe(
            janjeerwala[
                [
                    "company",
                    "location",
                    "workspace_type",
                    "price_per_seat_month",
                    "amenity_score"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No Janjeerwala records match the current filters."
        )


# =========================================================
# WORKSPACE ANALYSIS
# =========================================================

elif page == "🏢 Workspace Analysis":

    st.markdown(
        '<div class="section-title">Workspace Analysis</div>',
        unsafe_allow_html=True
    )

    workspace_summary = (
        filtered_df
        .groupby("workspace_type")
        .agg(
            records=("record_id", "count"),
            avg_price=("price_per_seat_month", "mean"),
            avg_capacity=("seat_capacity", "mean")
        )
        .reset_index()
    )

    st.dataframe(
        workspace_summary.round(2),
        use_container_width=True,
        hide_index=True
    )

    fig = px.bar(
        workspace_summary,
        x="workspace_type",
        y="records",
        title="Workspace Type Availability"
    )

    fig.update_traces(
        marker_color="#f97316"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# AMENITIES
# =========================================================

elif page == "✨ Amenities":

    st.markdown(
        '<div class="section-title">Amenity Analysis</div>',
        unsafe_allow_html=True
    )

    amenity_columns = [
        "private_office_available",
        "dedicated_desk",
        "hot_desk",
        "virtual_office",
        "meeting_room",
        "conference_room",
        "wifi",
        "parking",
        "power_backup",
        "cafeteria",
        "housekeeping",
        "security",
        "24x7_access",
        "air_conditioning",
        "printing",
        "event_space",
        "community_events",
        "managed_office",
        "build_to_suit",
        "enterprise_solution"
    ]

    available_amenities = []

    for col in amenity_columns:

        if col in filtered_df.columns:

            yes_count = (
                filtered_df[col]
                .eq("Yes")
                .sum()
            )

            available_amenities.append(
                {
                    "Amenity": col.replace("_", " ").title(),
                    "Yes Count": yes_count
                }
            )

    amenity_df = pd.DataFrame(
        available_amenities
    ).sort_values(
        "Yes Count",
        ascending=False
    )

    fig = px.bar(
        amenity_df,
        x="Yes Count",
        y="Amenity",
        orientation="h",
        title="Recorded Amenity Availability",
        text="Yes Count"
    )

    fig.update_traces(
        marker_color="#f97316"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    if "amenity_score" in filtered_df.columns:

        company_amenity = (
            filtered_df
            .groupby("company")[
                "amenity_score"
            ]
            .mean()
            .reset_index()
            .sort_values(
                "amenity_score"
            )
        )

        fig = px.bar(
            company_amenity,
            x="company",
            y="amenity_score",
            title="Average Amenity Score by Company",
            text_auto=".1f"
        )

        fig.update_traces(
            marker_color="#fb923c"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# WORKIE VS COMPETITORS
# =========================================================

elif page == "⚔️ Workie vs Competitors":

    st.markdown(
        '<div class="section-title">Workie vs Competitors</div>',
        unsafe_allow_html=True
    )

    workie_df = filtered_df[
        filtered_df["company"].str.lower() == "workie"
    ]

    if len(workie_df) == 0:

        st.warning(
            "No Workie records match the selected filters."
        )

    else:

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Workie Records",
                len(workie_df)
            )

        with col2:

            workie_price = workie_df[
                "price_per_seat_month"
            ].mean()

            st.metric(
                "Workie Avg Price",
                f"₹{workie_price:,.0f}"
            )

        with col3:

            workie_amenity = workie_df[
                "amenity_score"
            ].mean()

            st.metric(
                "Workie Avg Amenity Score",
                f"{workie_amenity:.1f}"
            )

        st.markdown("### Workie Recorded Data")

        st.dataframe(
            workie_df[
                [
                    "location",
                    "workspace_type",
                    "target_segment",
                    "seat_capacity",
                    "price_per_seat_month",
                    "day_pass_price",
                    "amenity_score"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        # Company price comparison
        comparison = (
            filtered_df
            .groupby("company")[
                "price_per_seat_month"
            ]
            .mean()
            .reset_index()
            .sort_values(
                "price_per_seat_month"
            )
        )

        fig = px.bar(
            comparison,
            x="company",
            y="price_per_seat_month",
            title="Recorded Average Monthly Price Comparison",
            text_auto=".0f"
        )

        fig.update_traces(
            marker_color="#f97316"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# BUSINESS INSIGHTS
# =========================================================

elif page == "💡 Business Insights":

    st.markdown(
        '<div class="section-title">Business Insights</div>',
        unsafe_allow_html=True
    )

    st.info(
        "These observations are generated from the provided dataset. "
        "They should not be interpreted as verified market-wide claims."
    )

    # Company with most records
    company_records = (
        filtered_df["company"]
        .value_counts()
    )

    if len(company_records) > 0:

        top_company = company_records.index[0]
        top_company_records = company_records.iloc[0]

        st.markdown(
            f"""
            <div class="insight-card">
            <b>📊 Dataset Coverage</b><br><br>
            {top_company} has the highest number of records in the
            currently filtered dataset with {top_company_records} records.
            </div>
            """,
            unsafe_allow_html=True
        )

    # Average price
    if filtered_df["price_per_seat_month"].notna().any():

        highest_price_company = (
            filtered_df
            .groupby("company")[
                "price_per_seat_month"
            ]
            .mean()
            .idxmax()
        )

        highest_price = (
            filtered_df
            .groupby("company")[
                "price_per_seat_month"
            ]
            .mean()
            .max()
        )

        st.markdown(
            f"""
            <div class="insight-card">
            <b>💰 Recorded Pricing</b><br><br>
            {highest_price_company} has the highest average recorded
            monthly seat price in the current filtered dataset:
            ₹{highest_price:,.0f}.
            </div>
            """,
            unsafe_allow_html=True
        )

    # Janjeerwala
    janjeerwala = filtered_df[
        filtered_df["location"]
        .str.contains(
            "Janjeerwala",
            case=False,
            na=False
        )
    ]

    if len(janjeerwala) > 0:

        competitors = janjeerwala[
            "company"
        ].nunique()

        st.markdown(
            f"""
            <div class="insight-card">
            <b>📍 Janjeerwala Square</b><br><br>
            The dataset contains {competitors} companies represented
            in the Janjeerwala Square location records.
            </div>
            """,
            unsafe_allow_html=True
        )

    # Data quality
    if "completeness_score" in filtered_df.columns:

        completeness = (
            filtered_df["completeness_score"]
            .mean()
        )

        st.markdown(
            f"""
            <div class="insight-card">
            <b>🧹 Data Quality</b><br><br>
            Average record completeness in the current filtered
            dataset is {completeness:.1f}%.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    st.caption(
        "Source: Workie Competitor Analysis practice dataset."
    )