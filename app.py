from flask import Flask, render_template, request
import eng

app = Flask(__name__)

@app.route('/')
@app.route("/index")
def index():
    sentence = request.args.get("sentence")
    if sentence == None:
        return render_template("index.html")
    else:
        result = eng.get_result(sentence)
        return render_template("index.html", result=result, sentence=sentence, noani='True')

if __name__ == '__main__':
    app.run()