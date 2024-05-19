from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from newspaper import Article
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import requests
import re

app = Flask(__name__)
CORS(app)

def summarize_article(text, min_sentences=5):
    parser = PlaintextParser.from_string(text, Tokenizer('english'))
    summarizer = LsaSummarizer()
    num_sentences = min(len(parser.document.sentences), min_sentences)
    if num_sentences < min_sentences:
        num_sentences = min_sentences
    summary = summarizer(parser.document, num_sentences)
    summarized_text = ' '.join([str(sentence) for sentence in summary])
    return summarized_text

def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https:// or ftp://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,63}|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST', 'OPTIONS'])
def summarize():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.json
    url_or_text = data['url_or_text']

    if is_valid_url(url_or_text):
        try:
            if url_or_text.startswith('http'):
                article = Article(url_or_text)
                article.download()
                article.parse()
                text = article.text
            else:
                response = requests.get(url_or_text)
                response.raise_for_status()  # Raise an exception for invalid responses
                text = response.text
        except Exception as e:
            return jsonify({'summary': f'Error: {str(e)}'})
    else:
        text = url_or_text

    summary = summarize_article(text)
    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=True)
