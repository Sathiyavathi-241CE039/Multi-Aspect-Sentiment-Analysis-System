import streamlit as st
import pandas as pd
import requests
import os
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Sentiment Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #263244;
}

.dashboard-title {
    font-size: 34px;
    font-weight: 750;
    color: #f8fafc;
    margin-bottom: 3px;
}

.dashboard-subtitle {
    font-size: 15px;
    color: #9ca3af;
    margin-bottom: 25px;
}

.sidebar-title {
    font-size: 22px;
    font-weight: 700;
    color: white;
}

.sidebar-subtitle {
    font-size: 13px;
    color: #9ca3af;
    margin-bottom: 20px;
}

.section-title {
    font-size: 21px;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 14px;
    color: #f8fafc;
}


/* KPI */

.kpi-card {
    border-radius: 16px;
    padding: 20px;
    min-height: 140px;
    border: 1px solid;
    transition: 0.2s;
}

.kpi-card:hover {
    transform: translateY(-3px);
}

.kpi-label {
    font-size: 14px;
    margin-bottom: 10px;
}

.kpi-value {
    font-size: 30px;
    font-weight: 750;
}

.kpi-small {
    font-size: 12px;
    margin-top: 5px;
    opacity: 0.75;
}


/* KPI COLORS */

.kpi-total {
    background: #e8eef7;
    border-color: #c7d5e8;
    color: #1e3a5f;
}

.kpi-positive {
    background: #e8f7ee;
    border-color: #b9e4c8;
    color: #16803c;
}

.kpi-neutral {
    background: #fff6dd;
    border-color: #f0d58a;
    color: #a66a00;
}

.kpi-negative {
    background: #fdecec;
    border-color: #f2b8b8;
    color: #c62828;
}


/* Insight */

.insight-card {
    background: #151c28;
    border: 1px solid #263244;
    border-radius: 14px;
    padding: 18px;
}

.insight-title {
    font-size: 13px;
    color: #9ca3af;
}

.insight-value {
    font-size: 20px;
    font-weight: 700;
    color: white;
    margin-top: 5px;
}


/* Result */

.result-card {
    background: #151c28;
    border: 1px solid #263244;
    border-radius: 14px;
    padding: 18px;
    text-align: center;
}

.result-label {
    color: #9ca3af;
    font-size: 13px;
}

.result-value {
    color: white;
    font-size: 20px;
    font-weight: 700;
    margin-top: 5px;
}


/* Report */

.report-card {
    background: #151c28;
    border: 1px solid #263244;
    border-radius: 15px;
    padding: 25px;
    text-align: center;
    min-height: 170px;
}

.footer {
    text-align: center;
    color: #6b7280;
    font-size: 12px;
    padding: 30px 0 10px 0;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# CONSTANTS
# ============================================================

API_URL = "http://127.0.0.1:5000/predict"


# ============================================================
# FUNCTIONS
# ============================================================

def load_data(filename):

    path = os.path.join("data", filename)

    if os.path.exists(path):

        try:
            return pd.read_csv(path)

        except Exception:

            return pd.DataFrame()

    return pd.DataFrame()


def find_column(df, names):

    if df.empty:
        return None

    columns = {
        str(col).strip().lower(): col
        for col in df.columns
    }

    for name in names:

        key = str(name).strip().lower()

        if key in columns:
            return columns[key]

    return None


def percentage(value, total):

    if total == 0:
        return 0

    return value / total * 100


def sentiment_colour(value):

    if value == "Positive":
        return "#16803C"

    if value == "Negative":
        return "#C62828"

    if value == "Neutral":
        return "#A66A00"

    return "#64748b"


# ============================================================
# LOAD DATA
# ============================================================

reviews = load_data("amazon_reviews.csv")
aspect_data = load_data("aspect_sentiment_results.csv")
trend = load_data("sentiment_trend.csv")
emotions = load_data("emotion_results.csv")
segments = load_data("customer_segments.csv")
alerts = load_data("sentiment_alerts.csv")
recommendations = load_data("business_recommendations.csv")


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    '<div class="sidebar-title">📊 Sentiment Intelligence</div>',
    unsafe_allow_html=True
)

st.sidebar.markdown(
    '<div class="sidebar-subtitle">'
    'Customer Review Analytics'
    '</div>',
    unsafe_allow_html=True
)

page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Dashboard",
        "🔍 Live Review Analyzer",
        "📄 Reports"
    ]
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Multi-Aspect Sentiment Analysis System"
)

st.sidebar.caption(
    "Python • NLP • Analytics • Streamlit"
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "📊 Dashboard":

    st.markdown(
        '<div class="dashboard-title">'
        '📊 Sentiment Intelligence'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        'Customer Review Analytics & Business Insights'
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # KPI CALCULATION
    # ========================================================

    total_reviews = len(reviews)

    positive = 0
    neutral = 0
    negative = 0

    if (
        not aspect_data.empty
        and "sentiment" in aspect_data.columns
    ):

        counts = aspect_data["sentiment"].value_counts()

        positive = int(counts.get("Positive", 0))
        neutral = int(counts.get("Neutral", 0))
        negative = int(counts.get("Negative", 0))

    total_sentiment = positive + neutral + negative

    positive_percent = percentage(
        positive,
        total_sentiment
    )

    neutral_percent = percentage(
        neutral,
        total_sentiment
    )

    negative_percent = percentage(
        negative,
        total_sentiment
    )


    # ========================================================
    # KPI CARDS
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '📌 Overall Performance'
        '</div>',
        unsafe_allow_html=True
    )

    k1, k2, k3, k4 = st.columns(4)


    with k1:

        st.markdown(
            f"""
            <div class="kpi-card kpi-total">
                <div class="kpi-label">📦 Total Reviews</div>
                <div class="kpi-value">{total_reviews:,}</div>
                <div class="kpi-small">Customer reviews analyzed</div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with k2:

        st.markdown(
            f"""
            <div class="kpi-card kpi-positive">
                <div class="kpi-label">😊 Positive</div>
                <div class="kpi-value">{positive_percent:.2f}%</div>
                <div class="kpi-small">{positive:,} records</div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with k3:

        st.markdown(
            f"""
            <div class="kpi-card kpi-neutral">
                <div class="kpi-label">😐 Neutral</div>
                <div class="kpi-value">{neutral_percent:.2f}%</div>
                <div class="kpi-small">{neutral:,} records</div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with k4:

        st.markdown(
            f"""
            <div class="kpi-card kpi-negative">
                <div class="kpi-label">😡 Negative</div>
                <div class="kpi-value">{negative_percent:.2f}%</div>
                <div class="kpi-small">{negative:,} records</div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # FILTERS
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '🔎 Explore Customer Feedback'
        '</div>',
        unsafe_allow_html=True
    )

    f1, f2, f3 = st.columns(3)

    aspect_col = find_column(
        aspect_data,
        ["aspect"]
    )

    sentiment_col = find_column(
        aspect_data,
        ["sentiment"]
    )


    with f1:

        if aspect_col:

            aspect_list = sorted(
                aspect_data[aspect_col]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            selected_aspect = st.selectbox(
                "🎯 Product Aspect",
                ["All"] + aspect_list
            )

        else:

            selected_aspect = "All"


    with f2:

        selected_sentiment = st.selectbox(
            "💬 Sentiment",
            [
                "All",
                "Positive",
                "Neutral",
                "Negative"
            ]
        )


    with f3:

        search_aspect = st.text_input(
            "🔍 Search Aspect",
            placeholder="Example: Camera"
        )


    # ========================================================
    # FILTER DATA
    # ========================================================

    filtered = aspect_data.copy()


    if (
        selected_aspect != "All"
        and aspect_col
    ):

        filtered = filtered[
            filtered[aspect_col].astype(str)
            == selected_aspect
        ]


    if (
        selected_sentiment != "All"
        and sentiment_col
    ):

        filtered = filtered[
            filtered[sentiment_col].astype(str)
            == selected_sentiment
        ]


    if (
        search_aspect
        and aspect_col
    ):

        filtered = filtered[
            filtered[aspect_col]
            .astype(str)
            .str.contains(
                search_aspect,
                case=False,
                na=False
            )
        ]


    st.caption(
        f"Showing {len(filtered):,} matching records"
    )


    # ========================================================
    # TABS
    # ========================================================

    overview_tab, aspect_tab, trend_tab, customer_tab, alert_tab, review_tab = st.tabs(
        [
            "📊 Overview",
            "🎯 Aspects",
            "📈 Trends",
            "👥 Customer Insights",
            "🚨 Alerts & Actions",
            "📋 Reviews"
        ]
    )


    # ========================================================
    # OVERVIEW
    # ========================================================

    with overview_tab:

        c1, c2 = st.columns(2)


        # ----------------------------------------------------
        # SENTIMENT PIE
        # ----------------------------------------------------

        with c1:

            st.markdown(
                '<div class="section-title">'
                '💬 Sentiment Distribution'
                '</div>',
                unsafe_allow_html=True
            )

            if (
                not filtered.empty
                and sentiment_col
            ):

                data = (
                    filtered[sentiment_col]
                    .value_counts()
                    .reset_index()
                )

                data.columns = [
                    "Sentiment",
                    "Count"
                ]

                fig = px.pie(
                    data,
                    names="Sentiment",
                    values="Count",
                    hole=0.55
                )

                fig.update_traces(
                    textinfo="percent+label"
                )

                fig.update_layout(
                    height=400,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#e5e7eb"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:

                st.info(
                    "No sentiment data available."
                )


        # ----------------------------------------------------
        # ASPECT BAR
        # ----------------------------------------------------

        with c2:

            st.markdown(
                '<div class="section-title">'
                '🎯 Most Discussed Aspects'
                '</div>',
                unsafe_allow_html=True
            )

            if (
                not filtered.empty
                and aspect_col
            ):

                data = (
                    filtered[aspect_col]
                    .value_counts()
                    .reset_index()
                )

                data.columns = [
                    "Aspect",
                    "Count"
                ]

                data = (
                    data
                    .head(10)
                    .sort_values("Count")
                )

                fig = px.bar(
                    data,
                    x="Count",
                    y="Aspect",
                    orientation="h"
                )

                fig.update_layout(
                    height=400,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#e5e7eb",
                    xaxis_title="Reviews",
                    yaxis_title=""
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )


        # ----------------------------------------------------
        # BUSINESS INSIGHTS
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '💡 Quick Business Insights'
            '</div>',
            unsafe_allow_html=True
        )

        q1, q2, q3 = st.columns(3)


        with q1:

            if (
                not filtered.empty
                and aspect_col
            ):

                top_aspect = (
                    filtered[aspect_col]
                    .value_counts()
                    .idxmax()
                )

                top_count = (
                    filtered[aspect_col]
                    .value_counts()
                    .max()
                )

                st.markdown(
                    f"""
                    <div class="insight-card">
                        <div class="insight-title">
                            🔥 Most Discussed Aspect
                        </div>
                        <div class="insight-value">
                            {top_aspect}
                        </div>
                        <div class="kpi-small">
                            {top_count:,} records
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


        with q2:

            st.markdown(
                f"""
                <div class="insight-card">
                    <div class="insight-title">
                        😊 Positive Rate
                    </div>
                    <div class="insight-value">
                        {positive_percent:.2f}%
                    </div>
                    <div class="kpi-small">
                        Overall customer sentiment
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        with q3:

            st.markdown(
                f"""
                <div class="insight-card">
                    <div class="insight-title">
                        ⚠️ Negative Rate
                    </div>
                    <div class="insight-value">
                        {negative_percent:.2f}%
                    </div>
                    <div class="kpi-small">
                        Customer dissatisfaction
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


    # ========================================================
    # ASPECTS
    # ========================================================

    with aspect_tab:

        st.markdown(
            '<div class="section-title">'
            '🎯 Aspect-Level Sentiment Analysis'
            '</div>',
            unsafe_allow_html=True
        )

        if (
            not filtered.empty
            and aspect_col
            and sentiment_col
        ):

            cross = pd.crosstab(
                filtered[aspect_col],
                filtered[sentiment_col]
            ).reset_index()


            for sentiment in [
                "Positive",
                "Neutral",
                "Negative"
            ]:

                if sentiment not in cross.columns:

                    cross[sentiment] = 0


            fig = go.Figure()


            fig.add_trace(
                go.Bar(
                    name="Positive",
                    x=cross[aspect_col],
                    y=cross["Positive"],
                    marker_color="#3BA55D"
                )
            )


            fig.add_trace(
                go.Bar(
                    name="Neutral",
                    x=cross[aspect_col],
                    y=cross["Neutral"],
                    marker_color="#D89B24"
                )
            )


            fig.add_trace(
                go.Bar(
                    name="Negative",
                    x=cross[aspect_col],
                    y=cross["Negative"],
                    marker_color="#D9534F"
                )
            )


            fig.update_layout(
                barmode="group",
                height=500,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e5e7eb",
                xaxis_title="Product Aspect",
                yaxis_title="Number of Reviews"
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )


            st.markdown(
                "### 📋 Aspect Summary"
            )

            st.dataframe(
                cross,
                use_container_width=True,
                hide_index=True
            )


        else:

            st.info(
                "Aspect data not available."
            )


    # ========================================================
    # TRENDS
    # ========================================================

    with trend_tab:

        st.markdown(
            '<div class="section-title">'
            '📈 Sentiment Trend Analysis'
            '</div>',
            unsafe_allow_html=True
        )

        if not trend.empty:

            trend_data = trend.copy()

            date_col = find_column(
                trend_data,
                [
                    "month",
                    "Month",
                    "date",
                    "Date"
                ]
            )


            if date_col:

                trend_data[date_col] = pd.to_datetime(
                    trend_data[date_col],
                    errors="coerce"
                )

                trend_data = trend_data.dropna(
                    subset=[date_col]
                )

                trend_data = trend_data.sort_values(
                    date_col
                )


            numeric_cols = (
                trend_data
                .select_dtypes(
                    include="number"
                )
                .columns
                .tolist()
            )


            if date_col and numeric_cols:

                fig = px.line(
                    trend_data,
                    x=date_col,
                    y=numeric_cols,
                    markers=True
                )

                fig.update_layout(
                    height=500,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#e5e7eb",
                    hovermode="x unified",
                    xaxis_title="Month",
                    yaxis_title="Sentiment Value"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )


            st.markdown(
                "### 📋 Trend Data"
            )

            st.dataframe(
                trend_data,
                use_container_width=True,
                hide_index=True
            )


        else:

            st.info(
                "Trend data not available."
            )


    # ========================================================
    # CUSTOMER INSIGHTS
    # ========================================================

    with customer_tab:

        c1, c2 = st.columns(2)


        # ----------------------------------------------------
        # EMOTION
        # ----------------------------------------------------

        with c1:

            st.markdown(
                '<div class="section-title">'
                '😊 Customer Emotion Analysis'
                '</div>',
                unsafe_allow_html=True
            )

            emotion_col = find_column(
                emotions,
                [
                    "emotion",
                    "Emotion"
                ]
            )


            if (
                not emotions.empty
                and emotion_col
            ):

                data = (
                    emotions[emotion_col]
                    .value_counts()
                    .reset_index()
                )

                data.columns = [
                    "Emotion",
                    "Count"
                ]


                fig = px.bar(
                    data,
                    x="Emotion",
                    y="Count"
                )

                fig.update_layout(
                    height=400,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#e5e7eb"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )


            else:

                st.info(
                    "Emotion data not available."
                )


        # ----------------------------------------------------
        # CUSTOMER SEGMENTS
        # ----------------------------------------------------

        with c2:

            st.markdown(
                '<div class="section-title">'
                '👥 Customer Segmentation'
                '</div>',
                unsafe_allow_html=True
            )

            segment_col = find_column(
                segments,
                [
                    "Segment",
                    "segment",
                    "Customer_Segment",
                    "customer_segment"
                ]
            )


            if (
                not segments.empty
                and segment_col
            ):

                data = (
                    segments[segment_col]
                    .value_counts()
                    .reset_index()
                )

                data.columns = [
                    "Segment",
                    "Customers"
                ]


                fig = px.pie(
                    data,
                    names="Segment",
                    values="Customers",
                    hole=0.5
                )

                fig.update_layout(
                    height=400,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#e5e7eb"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )


            else:

                st.info(
                    "Customer segmentation data not available."
                )


        if not segments.empty:

            st.markdown(
                "### 📋 Customer Segment Data"
            )

            st.dataframe(
                segments,
                use_container_width=True,
                hide_index=True
            )


    # ========================================================
    # ALERTS & ACTIONS
    # ========================================================

    with alert_tab:

        c1, c2 = st.columns(2)


        # ----------------------------------------------------
        # ALERTS
        # ----------------------------------------------------

        with c1:

            st.markdown(
                '<div class="section-title">'
                '🚨 Negative Sentiment Alerts'
                '</div>',
                unsafe_allow_html=True
            )


            if not alerts.empty:

                st.error(
                    f"{len(alerts)} alert period(s) detected."
                )

                st.dataframe(
                    alerts,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.success(
                    "No negative sentiment alerts."
                )


        # ----------------------------------------------------
        # RECOMMENDATIONS
        # ----------------------------------------------------

        with c2:

            st.markdown(
                '<div class="section-title">'
                '💡 Business Recommendations'
                '</div>',
                unsafe_allow_html=True
            )


            if not recommendations.empty:

                recommendation_col = find_column(
                    recommendations,
                    [
                        "aspect",
                        "Aspect"
                    ]
                )


                if recommendation_col:

                    options = sorted(
                        recommendations[
                            recommendation_col
                        ]
                        .dropna()
                        .astype(str)
                        .unique()
                        .tolist()
                    )


                    selected = st.selectbox(
                        "Select Aspect",
                        options,
                        key="recommendation"
                    )


                    selected_data = recommendations[
                        recommendations[
                            recommendation_col
                        ].astype(str) == selected
                    ]


                    st.dataframe(
                        selected_data,
                        use_container_width=True,
                        hide_index=True
                    )


                else:

                    st.dataframe(
                        recommendations,
                        use_container_width=True,
                        hide_index=True
                    )


            else:

                st.info(
                    "Recommendations not available."
                )


    # ========================================================
    # REVIEWS
    # ========================================================

    with review_tab:

        st.markdown(
            '<div class="section-title">'
            '📋 Customer Review Explorer'
            '</div>',
            unsafe_allow_html=True
        )


        review_col = find_column(
            reviews,
            [
                "reviewText",
                "review_text",
                "Review",
                "review"
            ]
        )


        if (
            not reviews.empty
            and review_col
        ):

            search_review = st.text_input(
                "🔍 Search Reviews",
                placeholder="Example: battery, camera, price..."
            )


            review_data = reviews.copy()


            if search_review:

                review_data = review_data[
                    review_data[
                        review_col
                    ]
                    .astype(str)
                    .str.contains(
                        search_review,
                        case=False,
                        na=False
                    )
                ]


            st.caption(
                f"{len(review_data):,} matching reviews"
            )


            st.dataframe(
                review_data.head(200),
                use_container_width=True,
                hide_index=True
            )


            st.download_button(
                "⬇️ Download Filtered Reviews",
                review_data.to_csv(
                    index=False
                ),
                file_name="filtered_reviews.csv",
                mime="text/csv"
            )


        else:

            st.info(
                "Review data not available."
            )


    st.markdown(
        '<div class="footer">'
        'Multi-Aspect Sentiment Analysis System • Customer Review Intelligence'
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# LIVE REVIEW ANALYZER
# ============================================================

elif page == "🔍 Live Review Analyzer":

    st.markdown(
        '<div class="dashboard-title">'
        '🔍 Live Review Analyzer'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        'Real-time customer review analysis'
        '</div>',
        unsafe_allow_html=True
    )


    review = st.text_area(
        "Enter Customer Review",
        height=150,
        placeholder=(
            "Example: I love this product! "
            "The battery is amazing."
        )
    )


    if st.button(
        "🔎 Analyze Review",
        type="primary",
        use_container_width=True
    ):

        if not review.strip():

            st.warning(
                "Please enter a review."
            )

        else:

            try:

                response = requests.post(
                    API_URL,
                    json={
                        "review": review
                    },
                    timeout=30
                )


                if response.status_code == 200:

                    result = response.json()


                    # ------------------------------------------------
                    # ORIGINAL REVIEW
                    # ------------------------------------------------

                    st.markdown(
                        '<div class="section-title">'
                        '📝 Original Review'
                        '</div>',
                        unsafe_allow_html=True
                    )

                    st.info(
                        result.get(
                            "review",
                            review
                        )
                    )


                    # ------------------------------------------------
                    # PROCESSING
                    # ------------------------------------------------

                    with st.expander(
                        "🔄 View Text Processing"
                    ):

                        c1, c2 = st.columns(2)


                        with c1:

                            st.markdown(
                                "**Cleaned Text**"
                            )

                            st.code(
                                result.get(
                                    "cleaned_review",
                                    ""
                                )
                            )


                            st.markdown(
                                "**Tokens**"
                            )

                            st.write(
                                result.get(
                                    "tokens",
                                    []
                                )
                            )


                        with c2:

                            st.markdown(
                                "**NLTK Lemmatized**"
                            )

                            st.write(
                                result.get(
                                    "lemmatized",
                                    []
                                )
                            )


                            st.markdown(
                                "**spaCy Tokens**"
                            )

                            spacy_tokens = result.get(
                                "spacy_tokens",
                                []
                            )


                            if spacy_tokens:

                                st.write(
                                    spacy_tokens
                                )

                            else:

                                st.warning(
                                    result.get(
                                        "spacy_status",
                                        "spaCy unavailable"
                                    )
                                )


                    # ------------------------------------------------
                    # ANALYSIS
                    # ------------------------------------------------

                    st.markdown(
                        '<div class="section-title">'
                        '📊 Analysis Result'
                        '</div>',
                        unsafe_allow_html=True
                    )


                    sentiment = result.get(
                        "sentiment",
                        "Unknown"
                    )

                    polarity = result.get(
                        "polarity",
                        0
                    )

                    aspects = result.get(
                        "aspects",
                        []
                    )

                    emotion = result.get(
                        "emotion",
                        "Unknown"
                    )


                    if isinstance(
                        aspects,
                        list
                    ):

                        aspect_text = (
                            ", ".join(aspects)
                            if aspects
                            else "No Aspect"
                        )

                    else:

                        aspect_text = str(
                            aspects
                        )


                    r1, r2, r3, r4 = st.columns(4)


                    with r1:

                        st.markdown(
                            f"""
                            <div class="result-card">
                                <div class="result-label">
                                    Sentiment
                                </div>
                                <div class="result-value"
                                style="color:{sentiment_colour(sentiment)};">
                                    {sentiment}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                    with r2:

                        st.markdown(
                            f"""
                            <div class="result-card">
                                <div class="result-label">
                                    Polarity
                                </div>
                                <div class="result-value">
                                    {float(polarity):.3f}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                    with r3:

                        st.markdown(
                            f"""
                            <div class="result-card">
                                <div class="result-label">
                                    Aspect
                                </div>
                                <div class="result-value">
                                    {aspect_text}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                    with r4:

                        st.markdown(
                            f"""
                            <div class="result-card">
                                <div class="result-label">
                                    Emotion
                                </div>
                                <div class="result-value">
                                    {emotion}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                    # ------------------------------------------------
                    # SARCASM
                    # ------------------------------------------------

                    st.markdown(
                        '<div class="section-title">'
                        '🎭 Sarcasm Analysis'
                        '</div>',
                        unsafe_allow_html=True
                    )


                    sarcasm = result.get(
                        "sarcasm",
                        False
                    )

                    confidence = result.get(
                        "sarcasm_confidence",
                        0
                    )

                    score = result.get(
                        "sarcasm_score",
                        0
                    )


                    s1, s2, s3 = st.columns(3)


                    with s1:

                        st.metric(
                            "Detected",
                            "Yes" if sarcasm else "No"
                        )


                    with s2:

                        st.metric(
                            "Confidence",
                            confidence
                        )


                    with s3:

                        st.metric(
                            "Score",
                            score
                        )


                else:

                    st.error(
                        f"API Error: {response.status_code}"
                    )


            except requests.exceptions.ConnectionError:

                st.error(
                    "Flask API is not running."
                )

                st.info(
                    "Run this in another terminal: python api.py"
                )


            except Exception as e:

                st.error(
                    f"Error: {e}"
                )


# ============================================================
# REPORTS
# ============================================================

elif page == "📄 Reports":

    st.markdown(
        '<div class="dashboard-title">'
        '📄 Automated Reports'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        'Download your project reports'
        '</div>',
        unsafe_allow_html=True
    )


    pdf_path = os.path.join(
        "reports",
        "sentiment_analysis_report.pdf"
    )

    ppt_path = os.path.join(
        "reports",
        "sentiment_analysis_report.pptx"
    )


    c1, c2 = st.columns(2)


    # --------------------------------------------------------
    # PDF
    # --------------------------------------------------------

    with c1:

        st.markdown(
            """
            <div class="report-card">
                <h3>📄 PDF Report</h3>
                <p>
                    Complete sentiment analysis report
                    with results and recommendations.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")


        if os.path.exists(pdf_path):

            with open(
                pdf_path,
                "rb"
            ) as file:

                st.download_button(
                    "⬇️ Download PDF",
                    file,
                    file_name="sentiment_analysis_report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

        else:

            st.warning(
                "PDF report not found."
            )


    # --------------------------------------------------------
    # PPT
    # --------------------------------------------------------

    with c2:

        st.markdown(
            """
            <div class="report-card">
                <h3>📊 PowerPoint Report</h3>
                <p>
                    Project presentation with analysis,
                    results and conclusions.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")


        if os.path.exists(ppt_path):

            with open(
                ppt_path,
                "rb"
            ) as file:

                st.download_button(
                    "⬇️ Download PowerPoint",
                    file,
                    file_name="sentiment_analysis_report.pptx",
                    mime=(
                        "application/vnd.openxmlformats-"
                        "officedocument.presentationml.presentation"
                    ),
                    use_container_width=True
                )

        else:

            st.warning(
                "PowerPoint report not found."
            )


    # --------------------------------------------------------
    # PROJECT OUTPUTS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '📌 Project Outputs'
        '</div>',
        unsafe_allow_html=True
    )


    o1, o2, o3 = st.columns(3)


    with o1:

        st.markdown(
            """
            <div class="insight-card">
                <div class="insight-title">
                    📊 Analytics
                </div>
                <div class="insight-value">
                    Sentiment Trends
                </div>
                <div class="kpi-small">
                    Monthly customer sentiment
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with o2:

        st.markdown(
            """
            <div class="insight-card">
                <div class="insight-title">
                    🎯 Aspect Analysis
                </div>
                <div class="insight-value">
                    10 Product Aspects
                </div>
                <div class="kpi-small">
                    Feature-level insights
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with o3:

        st.markdown(
            """
            <div class="insight-card">
                <div class="insight-title">
                    💡 Business Intelligence
                </div>
                <div class="insight-value">
                    Recommendations
                </div>
                <div class="kpi-small">
                    Actionable business insights
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown(
        '<div class="footer">'
        'Multi-Aspect Sentiment Analysis System'
        '</div>',
        unsafe_allow_html=True
    )
