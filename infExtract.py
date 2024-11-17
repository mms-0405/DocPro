# pip install nltk spacy flask
# python -m spacy download en_core_web_sm

import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    # Tokenization
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token.lower() not in stop_words]
    
    # Join tokens back into a string
    processed_text = ' '.join(filtered_tokens)
    
    return processed_text

import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm

nlp = en_core_web_sm.load()

def extract_keywords(text, num_keywords=5):
    doc = nlp(text)
    keywords = [token.text for token in doc if token.is_stop != True and token.is_punct != True]
    keyword_freq = Counter(keywords)
    most_common_keywords = keyword_freq.most_common(num_keywords)
    
    return [keyword[0] for keyword in most_common_keywords]


from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/extract_keywords', methods=['POST'])
def api_extract_keywords():
    data = request.json
    text = data.get('text', '')
    num_keywords = data.get('num_keywords', 5)
    
    processed_text = preprocess_text(text)
    keywords = extract_keywords(processed_text, num_keywords)
    
    return jsonify({'keywords': keywords})

if __name__ == '__main__':
    app.run(debug=True)