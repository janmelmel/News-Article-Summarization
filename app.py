from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from newspaper import Article
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

app = Flask(__name__)
CORS(app)  # Apply CORS to your Flask app

def summarize_article(text, num_sentences=3):
    parser = PlaintextParser.from_string(text, Tokenizer('english'))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    summarized_text = ' '.join([str(sentence) for sentence in summary])
    return summarized_text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST', 'OPTIONS'])  # Allow both POST and OPTIONS
def summarize():
    if request.method == 'OPTIONS':
        return '', 200  # Just return a 200 status for OPTIONS requests

    data = request.json
    url_or_text = data['url_or_text']
    if url_or_text.startswith('http'):
        article = Article(url_or_text)
        article.download()
        article.parse()
        text = article.text
    else:
        text = url_or_text
    summary = summarize_article(text)
    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=True)
