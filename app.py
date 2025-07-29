import pickle
import re
import nltk
import requests
import os
from flask import Flask, render_template, request
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Download only once (if needed)
nltk.download('stopwords')

# Initialize
app = Flask(__name__)
nltk.download('stopwords')

# Load model & vectorizer
model = pickle.load(open('model_12.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer_12.pkl', 'rb'))

# Preprocessing function
stop_words = set(stopwords.words('english')) - {'no', 'not', 'never'}
ps = PorterStemmer()

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return ' '.join([ps.stem(word) for word in text.split() if word not in stop_words])

# NewsAPI setup
NEWSAPI_KEY = os.environ.get('NEWSAPI_KEY')
NEWSAPI_URL = 'https://newsapi.org/v2/everything'

def fetch_news_sources(query):
    try:
        response = requests.get(NEWSAPI_URL, params={
            'q': query,
            'apiKey': NEWSAPI_KEY,
            'pageSize': 5
        })
        response.raise_for_status()
        return response.json().get('articles', [])
    except Exception as e:
        print("NewsAPI Error:", e)
        return []

@app.route('/', methods=['GET', 'POST'])
def home():
    verdict = None
    confidence = None
    summary = None
    sources = []

    if request.method == 'POST':
        text = request.form.get('news')
        cleaned_text = clean_text(text)
        X_t = vectorizer.transform([cleaned_text])
        pred = model.predict(X_t)[0]
        prob = model.predict_proba(X_t)[0][pred]

        verdict = "REAL" if pred == 1 else "FAKE"
        confidence = prob * 100  # float
        # confidence = f"{prob * 100:.2f}%" 
        summary = "This appears to be a real news article." if verdict == "REAL" else "This might be a fake or misleading news article."
        sources = fetch_news_sources(text)

    return render_template("index.html", verdict=verdict, confidence=confidence, summary=summary, sources=sources)

if __name__ == '__main__':
    app.run(debug=True)
