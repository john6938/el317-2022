from flask import Flask, render_template
import nltk

app = Flask(__name__)

@app.route('/')
def index():
    text = 'Is he human?'
    try:
      morph = nltk.word_tokenize(text)
      pos = nltk.pos_tag(morph)
    except:
      nltk.download('punkt')
      nltk.download('averaged_perceptron_tagger')
    return render_template("index.html")

if __name__ == '__main__':
    app.run()