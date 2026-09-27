import streamlit as st
import pandas as pd
import os
import subprocess
import sys

from src.live_analyzer import analyze_review


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Multi-Aspect Sentiment Analysis",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# HELPER FUNCTION
# =========================================================

def find_column(df, possible_names):
    """
    Find a column from multiple possible column names.
    Handles uppercase/lowercase and extra spaces.
    """

    normalized_columns = {
        str(col).strip().lower(): col
        for col in df.columns
    }

    for name in possible_names:
        key = name.strip().lower()

        if key in normalized_columns:
            return normalized_columns[key]

    return None


# =========================================================
# LOAD DATA
# =========================================================

try:

    sentiment_df = pd.read_csv(
        "data/aspect_sentiment_results.csv"
    )

    trend_df = pd.read_csv(
        "data/sentiment_trend.csv"
    )

    emotion_df = pd.read_csv(
        "data/emotion_results.csv"
    )

    recommendation_df = pd.read_csv(
        "data/business_recommendations.csv"
    )

    alert_df = pd.read_csv(
        "data/sentiment_alerts.csv"
    )

    segment_df = pd.read_csv(
        "data/customer_segments.csv"
    )

except FileNotFoundError as e:

    st.error(
        f"Required data file not found: {e}"
    )

    st.stop()


# =========================================================
# FIND IMPORTANT COLUMNS
# =========================================================

sentiment_column = find_column(
    sentiment_df,
    [
        "Sentiment",
        "sentiment",
        "Sentiment_Label",
        "sentiment_label"
    ]
)

aspect_column = find_column(
    sentiment_df,
    [
        "Aspect",
        "aspect"
    ]
)

emotion_column = find_column(
    emotion_df,
    [
        "Emotion",
        "emotion"
    ]
)

segment_column = find_column(
    segment_df,
    [
        "Segment",
        "segment",
        "Customer_Segment",
        "customer_segment"
    ]
)


# =========================================================
# CHECK SENTIMENT COLUMN
# =========================================================

if sentiment_column is None:

    st.error(
        "❌ Sentiment column was not found in "
        "aspect_sentiment_results.csv."
    )

    st.write(
        "Available columns:"
    )

    st.code(
        "\n".join(
            str(column)
            for column in sentiment_df.columns
        )
    )

    st.stop()


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select a page",
    [
        "🔍 Live Review Analyzer",
        "📊 Dashboard",
        "📄 Automated Reports"
    ]
)


# =========================================================
# MAIN TITLE
# =========================================================

st.title(
    "Multi-Aspect Sentiment Analysis System"
)

st.write(
    "An AI-powered system for analyzing product reviews "
    "using sentiment analysis, aspect extraction, "
    "emotion classification, sarcasm detection "
    "and customer segmentation."
)


# =========================================================
# LIVE REVIEW ANALYZER
# =========================================================

if page == "🔍 Live Review Analyzer":

    st.header(
        "🔍 Live Review Analyzer"
    )

    st.write(
        "Enter a new product review to analyze "
        "sentiment, aspects, emotion and sarcasm "
        "in real time."
    )


    # -----------------------------------------------------
    # REVIEW INPUT
    # -----------------------------------------------------

    review_input = st.text_area(
        "Enter your product review:",
        placeholder=(
            "Example: The battery is excellent "
            "but the camera is terrible."
        ),
        height=150
    )


    # -----------------------------------------------------
    # ANALYZE BUTTON
    # -----------------------------------------------------

    if st.button(
        "🚀 Analyze Review",
        use_container_width=True
    ):

        if review_input.strip() == "":

            st.warning(
                "Please enter a review."
            )

        else:

            result = analyze_review(
                review_input
            )


            # -------------------------------------------------
            # API ERROR
            # -------------------------------------------------

            if "error" in result:

                st.error(
                    result["error"]
                )


            else:

                st.subheader(
                    "📊 Analysis Results"
                )


                # =============================================
                # RESULT METRICS
                # =============================================

                col1, col2, col3, col4 = (
                    st.columns(4)
                )


                with col1:

                    st.metric(
                        "Sentiment",
                        result.get(
                            "sentiment",
                            "N/A"
                        )
                    )


                with col2:

                    st.metric(
                        "Polarity",
                        result.get(
                            "polarity",
                            0
                        )
                    )


                with col3:

                    st.metric(
                        "Emotion",
                        result.get(
                            "emotion",
                            "N/A"
                        )
                    )


                with col4:

                    sarcasm_status = (
                        "Yes"
                        if result.get(
                            "sarcasm",
                            False
                        )
                        else "No"
                    )

                    st.metric(
                        "Sarcasm",
                        sarcasm_status
                    )


                # =============================================
                # DETECTED ASPECTS
                # =============================================

                st.write(
                    "### 🧩 Detected Aspects"
                )

                aspects = result.get(
                    "aspects",
                    []
                )


                if aspects:

                    st.success(
                        ", ".join(aspects)
                    )

                else:

                    st.info(
                        "No specific product aspect detected."
                    )


                # =============================================
                # PROCESSED REVIEW
                # =============================================

                st.write(
                    "### 📝 Processed Review"
                )

                st.write(
                    result.get(
                        "processed_review",
                        ""
                    )
                )


                # =============================================
                # SARCASM DETAILS
                # =============================================

                if result.get(
                    "sarcasm",
                    False
                ):

                    confidence = result.get(
                        "sarcasm_confidence",
                        0
                    )


                    st.warning(
                        "Sarcasm detected "
                        f"(confidence: {confidence})"
                    )


                    indicators = result.get(
                        "sarcasm_indicators",
                        []
                    )


                    if indicators:

                        st.write(
                            "**Indicators:**"
                        )


                        for indicator in indicators:

                            st.write(
                                f"- {indicator}"
                            )

                else:

                    st.info(
                        "No sarcasm detected."
                    )


                # =============================================
                # COMPLETE API RESPONSE
                # =============================================

                with st.expander(
                    "View Complete API Response"
                ):

                    st.json(
                        result
                    )


# =========================================================
# DASHBOARD
# =========================================================

elif page == "📊 Dashboard":

    st.header(
        "📊 Sentiment Analysis Dashboard"
    )


    # =====================================================
    # OVERALL SENTIMENT
    # =====================================================

    st.subheader(
        "Overall Sentiment"
    )


    # -----------------------------------------------------
    # TOTAL REVIEWS
    # -----------------------------------------------------

    try:

        processed_df = pd.read_csv(
            "data/processed_reviews.csv"
        )

        total_reviews = len(
            processed_df
        )

    except FileNotFoundError:

        total_reviews = len(
            sentiment_df
        )


    # -----------------------------------------------------
    # NORMALIZE SENTIMENT
    # -----------------------------------------------------

    sentiment_values = (
        sentiment_df[sentiment_column]
        .astype(str)
        .str.strip()
        .str.title()
    )


    positive_count = (
        sentiment_values
        .value_counts()
        .get("Positive", 0)
    )


    negative_count = (
        sentiment_values
        .value_counts()
        .get("Negative", 0)
    )


    neutral_count = (
        sentiment_values
        .value_counts()
        .get("Neutral", 0)
    )


    # =====================================================
    # METRICS
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Total Reviews",
            total_reviews
        )


    with col2:

        st.metric(
            "Positive",
            positive_count
        )


    with col3:

        st.metric(
            "Negative",
            negative_count
        )


    with col4:

        st.metric(
            "Neutral",
            neutral_count
        )


    # =====================================================
    # SENTIMENT DISTRIBUTION
    # =====================================================

    st.subheader(
        "📈 Sentiment Distribution"
    )


    sentiment_counts = (
        sentiment_values
        .value_counts()
    )


    st.bar_chart(
        sentiment_counts
    )


    # =====================================================
    # SENTIMENT SUMMARY TABLE
    # =====================================================

    st.write(
        "### Sentiment Summary"
    )


    sentiment_summary = pd.DataFrame(
        {
            "Sentiment": [
                "Positive",
                "Negative",
                "Neutral"
            ],
            "Count": [
                positive_count,
                negative_count,
                neutral_count
            ]
        }
    )


    st.dataframe(
        sentiment_summary,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # SENTIMENT TREND
    # =====================================================

    st.subheader(
        "📅 Sentiment Trend Over Time"
    )


    if not trend_df.empty:

        trend_display = trend_df.copy()


        date_column = find_column(
            trend_display,
            [
                "reviewTime",
                "ReviewTime",
                "date",
                "Date",
                "month",
                "Month"
            ]
        )


        if date_column is not None:

            try:

                trend_display[
                    date_column
                ] = pd.to_datetime(
                    trend_display[
                        date_column
                    ]
                )

                trend_display = (
                    trend_display
                    .set_index(
                        date_column
                    )
                )

            except Exception:

                pass


        numeric_columns = (
            trend_display
            .select_dtypes(
                include="number"
            )
            .columns
        )


        if len(numeric_columns) > 0:

            st.line_chart(
                trend_display[
                    numeric_columns
                ]
            )

        else:

            st.dataframe(
                trend_df,
                use_container_width=True
            )

    else:

        st.info(
            "Sentiment trend data is not available."
        )


    # =====================================================
    # TREND IMAGE
    # =====================================================

    trend_image = (
        "reports/sentiment_trend.png"
    )


    if os.path.exists(
        trend_image
    ):

        st.image(
            trend_image,
            caption="Monthly Sentiment Trend",
            use_container_width=True
        )


    # =====================================================
    # ASPECT-BASED SENTIMENT
    # =====================================================

    st.subheader(
        "🧩 Aspect-Based Sentiment Analysis"
    )


    if aspect_column is not None:

        aspect_summary = pd.crosstab(
            sentiment_df[aspect_column],
            sentiment_values
        )


        st.dataframe(
            aspect_summary,
            use_container_width=True
        )


        st.bar_chart(
            aspect_summary
        )

    else:

        st.warning(
            "Aspect column was not found."
        )


    # =====================================================
    # EMOTION ANALYSIS
    # =====================================================

    st.subheader(
        "😊 8-Emotion Classification"
    )


    if emotion_column is not None:

        emotion_values = (
            emotion_df[
                emotion_column
            ]
            .astype(str)
            .str.strip()
        )


        emotion_counts = (
            emotion_values
            .value_counts()
        )


        st.bar_chart(
            emotion_counts
        )


        emotion_table = (
            emotion_counts
            .reset_index()
        )


        emotion_table.columns = [
            "Emotion",
            "Count"
        ]


        st.dataframe(
            emotion_table,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "Emotion column was not found."
        )


    # =====================================================
    # BUSINESS RECOMMENDATIONS
    # =====================================================

    st.subheader(
        "💡 Business Recommendations"
    )


    if not recommendation_df.empty:

        recommendation_aspect_column = (
            find_column(
                recommendation_df,
                [
                    "Aspect",
                    "aspect",
                    "Unnamed: 0"
                ]
            )
        )


        recommendation_column = (
            find_column(
                recommendation_df,
                [
                    "Recommendation",
                    "recommendation"
                ]
            )
        )


        for _, row in (
            recommendation_df.iterrows()
        ):

            if (
                recommendation_aspect_column
                is not None
            ):

                aspect_name = row[
                    recommendation_aspect_column
                ]

            else:

                aspect_name = "General"


            if (
                recommendation_column
                is not None
            ):

                recommendation = row[
                    recommendation_column
                ]

            else:

                recommendation = (
                    "Review this aspect "
                    "for improvement."
                )


            st.write(
                f"**{aspect_name}:** "
                f"{recommendation}"
            )

    else:

        st.info(
            "No business recommendations available."
        )


    # =====================================================
    # NEGATIVE SENTIMENT ALERTS
    # =====================================================

    st.subheader(
        "🚨 Negative Sentiment Alerts"
    )


    if not alert_df.empty:

        st.dataframe(
            alert_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success(
            "No negative sentiment spikes detected."
        )


    # =====================================================
    # CUSTOMER SEGMENTATION
    # =====================================================

    st.subheader(
        "👥 Customer Segmentation"
    )


    if segment_column is not None:

        segment_values = (
            segment_df[
                segment_column
            ]
            .astype(str)
            .str.strip()
        )


        segment_counts = (
            segment_values
            .value_counts()
        )


        st.bar_chart(
            segment_counts
        )


        segment_table = (
            segment_counts
            .reset_index()
        )


        segment_table.columns = [
            "Customer Segment",
            "Count"
        ]


        st.dataframe(
            segment_table,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "Customer segment column was not found."
        )


# =========================================================
# AUTOMATED REPORTS
# =========================================================

elif page == "📄 Automated Reports":

    st.header(
        "📄 Automated Report Generation"
    )


    st.write(
        "Generate the complete project report "
        "in PDF or PowerPoint format."
    )


    # =====================================================
    # FILE PATHS
    # =====================================================

    pdf_path = (
        "reports/sentiment_analysis_report.pdf"
    )


    ppt_path = (
        "reports/sentiment_analysis_report.pptx"
    )


    # =====================================================
    # REPORT STATUS
    # =====================================================

    st.subheader(
        "📁 Report Status"
    )


    col1, col2 = st.columns(2)


    with col1:

        if os.path.exists(
            pdf_path
        ):

            st.success(
                "✅ PDF report is available."
            )

        else:

            st.warning(
                "⚠️ PDF report is not generated yet."
            )


    with col2:

        if os.path.exists(
            ppt_path
        ):

            st.success(
                "✅ PowerPoint report is available."
            )

        else:

            st.warning(
                "⚠️ PowerPoint report is not generated yet."
            )


    st.divider()


    # =====================================================
    # GENERATE NEW REPORTS
    # =====================================================

    st.subheader(
        "⚙️ Generate New Reports"
    )


    col1, col2 = st.columns(2)


    # =====================================================
    # PDF REPORT
    # =====================================================

    with col1:

        st.write(
            "### 📄 PDF Report"
        )


        st.write(
            "Generate a complete PDF report containing "
            "dataset summary, sentiment analysis, "
            "aspect analysis, emotion analysis, "
            "customer segmentation, alerts, "
            "recommendations and limitations."
        )


        if st.button(
            "📄 Generate PDF Report",
            use_container_width=True
        ):

            with st.spinner(
                "Generating PDF report..."
            ):

                try:

                    result = subprocess.run(
                        [
                            sys.executable,
                            "src/report_generator.py"
                        ],
                        capture_output=True,
                        text=True
                    )


                    if os.path.exists(
                        pdf_path
                    ):

                        st.success(
                            "✅ PDF report generated successfully!"
                        )


                        with open(
                            pdf_path,
                            "rb"
                        ) as file:

                            st.download_button(
                                label=(
                                    "⬇️ Download PDF Report"
                                ),
                                data=file,
                                file_name=(
                                    "sentiment_analysis_report.pdf"
                                ),
                                mime="application/pdf",
                                use_container_width=True
                            )

                    else:

                        st.error(
                            "❌ PDF generation failed."
                        )


                        if result.stderr:

                            st.code(
                                result.stderr
                            )

                except Exception as e:

                    st.error(
                        f"Error: {e}"
                    )


    # =====================================================
    # POWERPOINT REPORT
    # =====================================================

    with col2:

        st.write(
            "### 📊 PowerPoint Report"
        )


        st.write(
            "Generate a complete PowerPoint presentation "
            "containing project objective, dataset, "
            "sentiment analysis, emotions, segmentation, "
            "alerts, recommendations, architecture, "
            "technologies and limitations."
        )


        if st.button(
            "📊 Generate PPT Report",
            use_container_width=True
        ):

            with st.spinner(
                "Generating PowerPoint report..."
            ):

                try:

                    result = subprocess.run(
                        [
                            sys.executable,
                            "src/ppt_report_generator.py"
                        ],
                        capture_output=True,
                        text=True
                    )


                    if os.path.exists(
                        ppt_path
                    ):

                        st.success(
                            "✅ PowerPoint report generated successfully!"
                        )


                        with open(
                            ppt_path,
                            "rb"
                        ) as file:

                            st.download_button(
                                label=(
                                    "⬇️ Download PPT Report"
                                ),
                                data=file,
                                file_name=(
                                    "sentiment_analysis_report.pptx"
                                ),
                                mime=(
                                    "application/vnd.openxmlformats-officedocument."
                                    "presentationml.presentation"
                                ),
                                use_container_width=True
                            )

                    else:

                        st.error(
                            "❌ PowerPoint generation failed."
                        )


                        if result.stderr:

                            st.code(
                                result.stderr
                            )

                except Exception as e:

                    st.error(
                        f"Error: {e}"
                    )


    # =====================================================
    # DOWNLOAD EXISTING REPORTS
    # =====================================================

    st.divider()


    st.subheader(
        "⬇️ Download Existing Reports"
    )


    col1, col2 = st.columns(2)


    # -----------------------------------------------------
    # PDF DOWNLOAD
    # -----------------------------------------------------

    with col1:

        if os.path.exists(
            pdf_path
        ):

            with open(
                pdf_path,
                "rb"
            ) as file:

                st.download_button(
                    label="⬇️ Download Existing PDF",
                    data=file,
                    file_name=(
                        "sentiment_analysis_report.pdf"
                    ),
                    mime="application/pdf",
                    use_container_width=True
                )

        else:

            st.info(
                "Generate the PDF report first."
            )


    # -----------------------------------------------------
    # PPT DOWNLOAD
    # -----------------------------------------------------

    with col2:

        if os.path.exists(
            ppt_path
        ):

            with open(
                ppt_path,
                "rb"
            ) as file:

                st.download_button(
                    label="⬇️ Download Existing PPT",
                    data=file,
                    file_name=(
                        "sentiment_analysis_report.pptx"
                    ),
                    mime=(
                        "application/vnd.openxmlformats-officedocument."
                        "presentationml.presentation"
                    ),
                    use_container_width=True
                )

        else:

            st.info(
                "Generate the PowerPoint report first."
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "📊 Multi-Aspect Sentiment Analysis System | "
    "AI & Machine Learning Project"
)