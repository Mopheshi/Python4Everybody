import nltk
import requests
from bs4 import BeautifulSoup
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

nltk.download('punkt')

# URL of the website to scrape
url = 'https://www.ngrams.info/'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract text data from the parsed HTML
    text_data = soup.get_text()

    # Tokenize the text data into sentences
    sentences = nltk.sent_tokenize(text_data)
    print(sentences)

    # Initialize sentiment analyzer
    sia = SentimentIntensityAnalyzer()

    # Analyze sentiment for each sentence
    sentiment_scores = []
    for sentence in sentences:
        score = sia.polarity_scores(sentence)
        sentiment_scores.append(score['compound'])  # Use compound score for overall sentiment

    # Plot histogram of sentiment scores
    plt.hist(sentiment_scores, bins=10, color='skyblue', edgecolor='black')
    plt.xlabel('Sentiment Score')
    plt.ylabel('Frequency')
    plt.title('Sentiment Analysis Histogram')
    plt.show()
else:
    print('Failed to retrieve data from the website')
