from flask import Flask, render_template, request
from FacebookResetPasswordAPI import FacebookResetPasswordAPI
from whitepages_api import makeAPIRequest
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == "GET":
        return render_template('reverseSearch.html', resultFound=False)
    if request.method == "POST":
        query = request.form['email']
        # facebookRes = FacebookResetPasswordAPI({'verbose': True}).get(query)
        # profilePicture = facebookRes['profile_picture'][:-2]+'250'
        # profileName = facebookRes['full_name']

        try:
            whitepateRes = makeAPIRequest(str(query))
        except Exception, e:
            whitepateRes = e
        print whitepateRes
        return render_template('reverseSearch.html', resultFound=True, whitepateRes=whitepateRes)
        # return render_template('reverseSearch.html', resultFound=True, profilePicture=profilePicture, profileName=profileName, whitepateRes=whitepateRes)

app.debug = True
if __name__ == "__main__":
    app.run()
