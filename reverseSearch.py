from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('reverseSearch.html')

app.debug = True
if __name__ == "__main__":
    app.run()
