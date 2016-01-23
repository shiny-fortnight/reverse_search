from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html', display=True)

app.debug = True
if __name__ == "__main__":
    app.run()
