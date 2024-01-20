import nltk
from nltk.tokenize import word_tokenize
from flask import Flask, render_template, request
from flask import Flask

app = Flask(__name__, static_url_path='/static')

nltk.download('punkt')

def tokenize_text(text):
    tokens = word_tokenize(text)
    return tokens

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_plagiarism', methods=['POST'])
def check_plagiarism():
    text1 = request.form['text1']
    text2 = request.form['text2']

    tokens1 = tokenize_text(text1)
    tokens2 = tokenize_text(text2)

    common_tokens = set(tokens1) & set(tokens2)
    similarity = (len(common_tokens) / len(set(tokens1 + tokens2))) * 100

    return render_template('result.html', similarity=similarity)

if __name__ == '__main__':
    app.run(debug=True)
