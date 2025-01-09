### Milestone 1: Data Collection, Cleaning, and Sentiment Analysis
Objective
The goal of Milestone 1 is to collect news articles related to supply chain disruptions, clean and preprocess the data, and analyze the sentiment to understand trends and insights.

Tasks Accomplished
1. Data Collection
API Used: NewsAPI
Keywords:
supply chain management disruption
logistics challenges
global supply chain issues
supply chain delays
Parameters:
Start Date: Adjusted to the last 30 days based on API limitations.
End Date: Set to 2024-12-01.
Language: English.
Sorting: By relevancy.
Pagination: Collected up to 5 pages per keyword to maximize results.
Results:
Articles fetched were saved to a CSV file: news_articles.csv.
2. Data Cleaning
Used regular expressions (re) to clean text data:
Removed newline, tab characters, and extra spaces.
Converted text to lowercase.
Removed special characters and punctuation.
Cleaned columns:
title
description
Saved cleaned data to: cleaned_news_articles.csv.
3. Sentiment Analysis
Models Used:
Hugging Face Transformers:

Model: distilbert-base-uncased-finetuned-sst-2-english.
Task: Sentiment classification (Positive/Negative).
Result: Added sentiment column based on description.
TextBlob:

Extracted:
Polarity: Measures sentiment (-1 to 1).
Subjectivity: Ranges from 0 (objective) to 1 (subjective).
Columns Added:
sentiment
polarity
subjectivity.
