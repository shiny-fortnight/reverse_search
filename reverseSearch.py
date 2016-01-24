import os
from flask import Flask, render_template, request
from modules.FacebookResetPasswordAPI import FacebookResetPasswordAPI
from modules.whitepages_api import makeAPIRequest
from modules.OpenCNAMAPI import OpenCNAMAPI
from modules.calleridservice import call_calleridservice
from modules.GoogleReverseImageSearch import searchImage
from modules.geo_twitter_lookup import search_twitter

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def hello():
#     if request.method == "GET":
#         return render_template('index.html')

#     if request.method == "POST":
#         return redirect(url_for('search'))

# @app.route("/search", methods=["GET", "POST"])
# def search():
    if request.method == "GET":
        return render_template('reverseSearch.html', resultFound=False)

    if request.method == "POST":
        query = request.form['email']
        keywords = request.form['keywords']
        facebookRes = FacebookResetPasswordAPI({'verbose': True}).get(query)
        if facebookRes:
            profilePicture = facebookRes['profile_picture'][:-2]+'250'
            profileName = facebookRes['full_name']

            googleReverseImageSearchRes = searchImage(profilePicture)

        else:
            profilePicture = None
            profileName = None
            googleReverseImageSearchRes = None

        try:
            whitepateRes = makeAPIRequest(str(query))
        except Exception, e:
            whitepateRes = e

        twitterRes = search_twitter(str(query), str(keywords))

        openCNAMAPIRes = OpenCNAMAPI({'verbose': True}).get(query)

        calleridserviceRes = call_calleridservice(query)

        return render_template('reverseSearch.html', resultFound=True, profilePicture=profilePicture, profileName=profileName, whitepateRes=whitepateRes, openCNAMAPIRes=openCNAMAPIRes, calleridserviceRes=calleridserviceRes, googleReverseImageSearchRes=googleReverseImageSearchRes, twitterRes=twitterRes)

app.debug = True
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
