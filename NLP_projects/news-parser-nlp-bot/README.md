# News NLP Bot

This project focuses on collecting news articles from a public news portal, analyzing the collected data, and applying Natural Language Processing (NLP) techniques to extract meaningful insights. The final step involves building a Telegram bot that allows users to query and receive news based on their preferences.

## Project Breakdown:

### 1. **Web Scraping**
   - **Objective**: Scraping articles from a public news portal using a Python scraper.
   - **Tools**: Selenium.
   - **Result**: Collect news articles along with metadata such as title, publication date, and content.

### 2. **Exploratory Data Analysis (EDA)**
   - **Objective**: Analyzing the collected articles to identify trends, frequently used words, patterns in the publication dates, etc.
   - **Tools**: Pandas, Matplotlib, Seaborn, etc.
   - **Result**: Visualizations of article frequency over time, distribution of topics, and frequent words across the dataset.

### 3. **NLP Modeling**
   - **Objective**: Using NLP techniques for text analysis, such as topic modeling, sentiment analysis, or text summarization.
   - **Tools**: NLTK, SpaCy, HuggingFace Transformers, etc.
   - **Result**: An NLP model trained on news data for tasks like classification or summarization.

### 4. **Telegram Bot**
   - **Objective**: Build a Telegram bot to deliver news to users based on their queries (e.g., topic-based, date-based).
   - **Tools**: Python-telegram-bot, Flask (optional for API endpoints).
   - **Result**: A fully functional Telegram bot that interacts with users and fetches relevant news.

## Requirements:

- requirements.txt


