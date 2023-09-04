import requests
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from tkinter import *
from tkinter import ttk
from bs4 import BeautifulSoup
from selenium import webdriver
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import numpy as np


def analyze_tweets(query):
    # Replace these with your own API keys and access tokens
    api_key = ''
    api_secret_key = ''
    bearer_token = ''

    # Set the base URL for the API endpoint
    base_url = 'https://api.twitter.com/2/tweets/search/recent'

    # Set the search parameters
    params = {
        'query': query,
        'max_results': 100,
        'expansions': 'author_id',
        'user.fields': 'username',
        'tweet.fields': 'created_at,public_metrics',
    }

    # Set the headers
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'User-Agent': 'MyApp1.0'
    }

    # Make the request
    response = requests.get(base_url, params=params, headers=headers)

    # Parse the JSON data
    data = response.json()

    # Perform sentiment analysis on each tweet and store the scores
    sentiments = []
    for tweet in data['data']:
        text = tweet['text']
        score = SentimentIntensityAnalyzer().polarity_scores(text)['compound']
        sentiments.append(score)

    # Create a pie graph of the sentiment scores
    labels = ['Positive', 'Negative', 'Neutral']
    positive_count = len([s for s in sentiments if s > 0])
    negative_count = len([s for s in sentiments if s < 0])
    neutral_count = len([s for s in sentiments if s == 0])
    sizes = [positive_count, negative_count, neutral_count]
    colors = ['yellowgreen', 'lightcoral', 'gold']
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.title('Sentiment Analysis of Tweets')
    plt.axis('equal')
    plt.show()


def handle_click():
    query = entry.get()
    analyze_tweets(query)

def analyse_sentiment():
    # Get the URL and keyword from the GUI entry widgets
    url = url_entry.get()
    keyword = keyword_entry.get()

    # Initialize the sentiment analyzer
    sia = SentimentIntensityAnalyzer()

    # Initialize the Chrome web driver
    driver = webdriver.Chrome()

    # Load the webpage
    driver.get(url)

    # Get the HTML source code of the page after it has fully loaded
    html = driver.execute_script("return document.documentElement.outerHTML")

    # Create a soup object from the HTML source code
    soup = BeautifulSoup(html, "html.parser")

    # Close the web driver
    driver.close()

    # Split the HTML response into substrings based on the word "review"
    reviews = str(soup).split("review")

    # Initialize lists to store the compound sentiment scores and review texts
    compound_scores = []
    review_texts = []

    # Iterate over each substring, search for the keyword, perform sentiment analysis, and store the results
    for r in reviews:
        # Check if the keyword is a substring of the review substring
        if keyword in r:
            # If the keyword is found, perform sentiment analysis on the review
            review = "review" + r
            sentiment_scores = sia.polarity_scores(review)
            compound_scores.append(sentiment_scores["compound"])
            review_texts.append(review)

    # Calculate the percentage of positive, negative, and neutral reviews
    positive_percent = sum(np.array(compound_scores) > 0) / len(compound_scores)
    negative_percent = sum(np.array(compound_scores) < 0) / len(compound_scores)
    neutral_percent = sum(np.array(compound_scores) == 0) / len(compound_scores)

    # Define the labels and sizes for the pie chart
    if neutral_percent <= 0.6:
        labels = ["Positive", "Negative", "Neutral"]
        sizes = [positive_percent, negative_percent, neutral_percent]
    else:
        labels = ["Positive", "Negative"]
        sizes = [positive_percent, negative_percent]

    # Create the pie chart
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)

    # Add a title to the chart
    ax.set_title("Sentiment Analysis of Reviews Containing '{}'".format(keyword))

    # Show the chart
    plt.show()

def handle_analyze_sentiment():
    analyse_sentiment()

# Create the GUI
root = Tk()
root.title('Twitter Sentiment Analysis & Review Sentiment Analysis')

# Create a label and entry for the Twitter query
label = Label(root, text='Enter a query for Twitter:')
label.pack()
entry = Entry(root)
entry.pack()

# Create a button to perform the Twitter analysis
button = Button(root, text='Analyze Twitter', command=handle_click)
button.pack()

# Create the URL label and entry widget for Reviews
url_label = ttk.Label(root, text="Enter the URL of the webpage to scrape:")
url_label.pack(pady=5)
url_entry = ttk.Entry(root, width=50)
url_entry.pack(pady=5)

# Create the keyword label and entry for Reviews
keyword_label = ttk.Label(root, text="Enter a keyword to search for:")
keyword_label.pack(pady=5)
keyword_entry = ttk.Entry(root, width=50)
keyword_entry.pack(pady=5)

# Create the analyze button for Reviews
analyze_button = ttk.Button(root, text="Analyze Reviews", command=handle_analyze_sentiment)
analyze_button.pack(pady=10)

# Start the main event loop
root.mainloop()