from transformers import pipeline

# Load sentiment analysis pipeline
sentiment = pipeline("sentiment-analysis")

# Load summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Sample review
review = "The food was delicious but the service was slow and the tables were not clean."

# Run sentiment analysis
sentiment_result = sentiment(review)
print("Sentiment:", sentiment_result)

# Run summarization
summary_result = summarizer(review, max_length=50, min_length=10, do_sample=False)
print("Summary:", summary_result[0]["summary_text"])
