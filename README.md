# Multi-Aspect Sentiment Analysis System

## 📌 Overview

The **Multi-Aspect Sentiment Analysis System** is an NLP-based application that analyzes customer reviews and identifies sentiment for specific product aspects.

Unlike traditional sentiment analysis, which provides only an overall sentiment, this system identifies individual aspects such as **Battery, Camera, Price, Quality, Performance, and Delivery** and analyzes customer opinions related to them.

The system also provides emotion detection, sarcasm detection, customer segmentation, sentiment trends, alerts, business recommendations, a real-time API, and an interactive Streamlit dashboard.

---

## 🎯 Objectives

- Analyze customer reviews using Natural Language Processing.
- Identify important product aspects.
- Classify reviews as Positive, Negative, or Neutral.
- Detect customer emotions.
- Detect possible sarcastic reviews.
- Analyze sentiment trends over time.
- Segment customers based on sentiment patterns.
- Generate business recommendations.
- Provide an interactive dashboard.
- Provide a real-time REST API.
- Generate automated PDF and PPT reports.

---

## 🚀 Features

- 🔍 Aspect-Based Sentiment Analysis
- 😊 Sentiment Classification
- 🎭 8-Emotion Classification
- 😏 Sarcasm Detection
- 📊 Sentiment Trend Analysis
- 👥 Customer Segmentation
- 🚨 Negative Sentiment Alerts
- 💡 Business Recommendations
- 🌐 Multilingual Support (English + Tamil)
- ⚡ Real-Time Review Analysis
- 📈 Interactive Streamlit Dashboard
- 🔌 Flask REST API
- 📄 Automated PDF Report
- 📊 Automated PowerPoint Report

---

## 🔎 Product Aspects

The system identifies 10 major product aspects:

1. Battery
2. Price
3. Quality
4. Performance
5. Design
6. Size
7. Display
8. Camera
9. Delivery
10. Customer Service

---

## 📂 Dataset

The current project uses an Amazon customer review dataset.

### Dataset Information

- **Number of Reviews:** 4,915
- **Product:** Single product
- **ASIN:** B007WTAJTO
- **Review Data:** Review text, rating, reviewer ID, review date
- **Customer Data:** Review count, average rating, helpful votes
- **Product Aspects:** 10

> Note: The current dataset contains reviews for a single product. Competitor comparison requires additional multi-product datasets.

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- NLTK
- TextBlob
- Scikit-learn
- Streamlit
- Flask
- Matplotlib
- ReportLab
- Python-PPTX

---

## 🏗️ System Architecture

customer Reviews
       ↓
Data Preprocessing
       ↓
Aspect Extraction
       ↓
Sentiment Analysis
       ↓
Emotion Detection
       ↓
Sarcasm Detection
       ↓
Trend Analysis
       ↓
Customer Segmentation
       ↓
Business Recommendations
       ↓
Streamlit Dashboard / REST API


## Running Process

# 1. Clone the repository
git clone YOUR_GITHUB_REPOSITORY_LINK
cd sentiment_analysis

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start Flask API
python api.py

# 5. Open another terminal and activate the environment
venv\Scripts\activate

# 6. Start Streamlit dashboard
python -m streamlit run app.py

# 7. Open the displayed localhost URL in your browser
