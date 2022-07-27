from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
@app.route("/index")
def index():
    sentence = request.args.get("sentence")
    if sentence == None:
        return render_template("index.html")
    else:
        return render_template("index.html", result='a')

if __name__ == '__main__':
    app.run()