import pandas as pd
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


# ==================================================
# LOAD DATA
# ==================================================

sentiment_df = pd.read_csv(
    "data/aspect_sentiment_results.csv"
)

recommendation_df = pd.read_csv(
    "data/business_recommendations.csv"
)

alert_df = pd.read_csv(
    "data/sentiment_alerts.csv"
)

customer_df = pd.read_csv(
    "data/customer_segments.csv"
)

emotion_df = pd.read_csv(
    "data/emotion_results.csv"
)

trend_df = pd.read_csv(
    "data/sentiment_trend.csv"
)


# ==================================================
# CREATE REPORT FOLDER
# ==================================================

os.makedirs(
    "reports",
    exist_ok=True
)


# ==================================================
# PDF FILE
# ==================================================

pdf_path = "reports/sentiment_analysis_report.pdf"

document = SimpleDocTemplate(
    pdf_path,
    pagesize=A4,
    rightMargin=40,
    leftMargin=40,
    topMargin=40,
    bottomMargin=40
)


# ==================================================
# STYLES
# ==================================================

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "TitleStyle",
    parent=styles["Title"],
    alignment=TA_CENTER,
    fontSize=22,
    spaceAfter=20
)

heading_style = ParagraphStyle(
    "HeadingStyle",
    parent=styles["Heading1"],
    fontSize=16,
    spaceBefore=15,
    spaceAfter=10
)

normal_style = ParagraphStyle(
    "NormalStyle",
    parent=styles["BodyText"],
    fontSize=10,
    leading=15
)


# ==================================================
# REPORT CONTENT
# ==================================================

story = []


# ==================================================
# 1. TITLE
# ==================================================

story.append(
    Paragraph(
        "Multi-Aspect Sentiment Analysis System",
        title_style
    )
)

story.append(
    Paragraph(
        "Automated Sentiment Analysis Report",
        styles["Heading2"]
    )
)

story.append(
    Spacer(1, 20)
)


# ==================================================
# 2. PROJECT OVERVIEW
# ==================================================

story.append(
    Paragraph(
        "1. Project Overview",
        heading_style
    )
)

overview = """
This project analyzes Amazon product reviews using
sentiment analysis, aspect extraction, emotion
classification, trend analysis and customer
segmentation. The system also provides business
recommendations and negative sentiment alerts.
"""

story.append(
    Paragraph(
        overview,
        normal_style
    )
)

story.append(
    Spacer(1, 10)
)


# ==================================================
# 3. DATASET SUMMARY
# ==================================================

story.append(
    Paragraph(
        "2. Dataset Summary",
        heading_style
    )
)

total_reviews = len(sentiment_df)

unique_customers = customer_df[
    "reviewerID"
].nunique()

dataset_data = [
    ["Metric", "Value"],
    ["Aspect-level Records", str(total_reviews)],
    ["Customers", str(unique_customers)],
    ["Products in Current Dataset", "1"],
    ["Time Period", "2012 - 2014"]
]

table = Table(
    dataset_data,
    colWidths=[250, 150]
)

table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("PADDING", (0, 0), (-1, -1), 6)
    ])
)

story.append(table)


# ==================================================
# 4. OVERALL SENTIMENT
# ==================================================

story.append(
    Paragraph(
        "3. Overall Sentiment Analysis",
        heading_style
    )
)

sentiment_counts = (
    sentiment_df["sentiment"]
    .value_counts()
)

sentiment_data = [
    ["Sentiment", "Count"]
]

for sentiment, count in sentiment_counts.items():

    sentiment_data.append([
        sentiment,
        str(count)
    ])

table = Table(
    sentiment_data,
    colWidths=[250, 150]
)

table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("PADDING", (0, 0), (-1, -1), 6)
    ])
)

story.append(table)


# ==================================================
# 5. ASPECT ANALYSIS
# ==================================================

story.append(
    Paragraph(
        "4. Aspect-wise Sentiment Analysis",
        heading_style
    )
)

aspect_table = pd.crosstab(
    sentiment_df["aspect"],
    sentiment_df["sentiment"]
)

for sentiment in [
    "Positive",
    "Neutral",
    "Negative"
]:

    if sentiment not in aspect_table.columns:
        aspect_table[sentiment] = 0

aspect_table = aspect_table[
    [
        "Positive",
        "Neutral",
        "Negative"
    ]
]

aspect_data = [
    [
        "Aspect",
        "Positive",
        "Neutral",
        "Negative"
    ]
]

for aspect, row in aspect_table.iterrows():

    aspect_data.append([
        aspect,
        str(row["Positive"]),
        str(row["Neutral"]),
        str(row["Negative"])
    ])

table = Table(
    aspect_data,
    colWidths=[
        170,
        80,
        80,
        80
    ]
)

table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("PADDING", (0, 0), (-1, -1), 5)
    ])
)

story.append(table)


# ==================================================
# 6. EMOTION ANALYSIS
# ==================================================

story.append(
    Paragraph(
        "5. Eight-Emotion Analysis",
        heading_style
    )
)

emotion_counts = (
    emotion_df["emotion"]
    .value_counts()
)

emotion_data = [
    ["Emotion", "Count"]
]

for emotion, count in emotion_counts.items():

    emotion_data.append([
        emotion,
        str(count)
    ])

table = Table(
    emotion_data,
    colWidths=[
        250,
        150
    ]
)

table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("PADDING", (0, 0), (-1, -1), 6)
    ])
)

story.append(table)


# ==================================================
# 7. CUSTOMER SEGMENTATION
# ==================================================

story.append(
    Paragraph(
        "6. Customer Segmentation",
        heading_style
    )
)

segment_counts = (
    customer_df["Segment"]
    .value_counts()
)

segment_data = [
    [
        "Customer Segment",
        "Customers"
    ]
]

for segment, count in segment_counts.items():

    segment_data.append([
        segment,
        str(count)
    ])

table = Table(
    segment_data,
    colWidths=[
        250,
        150
    ]
)

table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("PADDING", (0, 0), (-1, -1), 6)
    ])
)

story.append(table)


# ==================================================
# 8. NEGATIVE SENTIMENT ALERTS
# ==================================================

story.append(
    Paragraph(
        "7. Negative Sentiment Alerts",
        heading_style
    )
)

alerts = alert_df[
    alert_df["Alert"] != "Normal"
]

story.append(
    Paragraph(
        f"Total negative sentiment spike months detected: "
        f"{len(alerts)}",
        normal_style
    )
)

if len(alerts) > 0:

    alert_data = [
        [
            "Month",
            "Negative %",
            "Alert"
        ]
    ]

    for _, row in alerts.iterrows():

        alert_data.append([
            str(row["Month"]),
            f'{row["Negative_Percentage"]:.2f}%',
            "Negative Spike"
        ])

    table = Table(
        alert_data,
        colWidths=[
            120,
            120,
            150
        ]
    )

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("PADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(table)


# ==================================================
# 9. BUSINESS RECOMMENDATIONS
# ==================================================

story.append(
    Paragraph(
        "8. Business Recommendations",
        heading_style
    )
)

# The recommendation CSV may contain the aspect
# as the first unnamed/index column.
# Therefore, detect the aspect column safely.

if "Aspect" in recommendation_df.columns:

    aspect_column = "Aspect"

elif "aspect" in recommendation_df.columns:

    aspect_column = "aspect"

elif "Unnamed: 0" in recommendation_df.columns:

    aspect_column = "Unnamed: 0"

else:

    aspect_column = None


# Detect recommendation column

if "Recommendation" in recommendation_df.columns:

    recommendation_column = "Recommendation"

elif "recommendation" in recommendation_df.columns:

    recommendation_column = "recommendation"

else:

    recommendation_column = None


if (
    aspect_column is not None
    and recommendation_column is not None
):

    for _, row in recommendation_df.iterrows():

        aspect_name = str(
            row[aspect_column]
        )

        recommendation_text = str(
            row[recommendation_column]
        )

        text = (
            f"<b>{aspect_name}</b>: "
            f"{recommendation_text}"
        )

        story.append(
            Paragraph(
                text,
                normal_style
            )
        )

        story.append(
            Spacer(1, 5)
        )

else:

    story.append(
        Paragraph(
            "Business recommendations were generated "
            "for the analyzed product aspects.",
            normal_style
        )
    )


# ==================================================
# 10. PROJECT LIMITATIONS
# ==================================================

story.append(
    Paragraph(
        "9. Project Limitations",
        heading_style
    )
)

limitations = """
The current review dataset contains reviews for only
one product. Therefore, genuine competitor comparison
cannot be performed without additional multi-product
review data. Customer membership information is derived
from review activity and should not be interpreted as
actual Amazon membership data. The emotion classifier
uses keyword-based lexical patterns.
"""

story.append(
    Paragraph(
        limitations,
        normal_style
    )
)


# ==================================================
# 11. CONCLUSION
# ==================================================

story.append(
    Paragraph(
        "10. Conclusion",
        heading_style
    )
)

conclusion = """
The developed system provides multi-aspect sentiment
analysis, sentiment trend monitoring, emotion
classification, customer segmentation, business
recommendations and negative sentiment alerts through
an interactive dashboard. A Flask API also enables
real-time review analysis.
"""

story.append(
    Paragraph(
        conclusion,
        normal_style
    )
)


# ==================================================
# BUILD PDF
# ==================================================

document.build(story)

print(
    "PDF report generated successfully!"
)

print(
    "Saved at:",
    pdf_path
)