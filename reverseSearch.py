import os
import itertools
from flask import Flask, render_template, request
from FacebookResetPasswordAPI import FacebookResetPasswordAPI
from whitepages_api import makeAPIRequest
from OpenCNAMAPI import OpenCNAMAPI
from calleridservice import call_calleridservice
from GoogleReverseImageSearch import searchImage
from geo_twitter_lookup import search_twitter
from related_lookup import GetRelatedInfo

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == "GET":
        return render_template('reverseSearch.html', resultFound=False)

    if request.method == "POST":
        query = request.form['email']
        keywords = request.form['keywords']
        try:
            facebookRes = FacebookResetPasswordAPI({'verbose': True}).get(query)
        except Exception:
            facebookRes = None
        
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

        try:
            openCNAMAPIRes = OpenCNAMAPI({'verbose': True}).get(query)
        except ValueError:
            openCNAMAPIRes = dict()
            openCNAMAPIRes['full_name'] = "None Found"
            openCNAMAPIRes['phone_number'] = "None Found"

        calleridserviceRes = call_calleridservice(query)
    
        try:
            griclass = GetRelatedInfo()
            gri = griclass.checkPhoneNumber(query)
            ads = gri['ads'] if len(gri['ads']) > 0 else [['None Found']*4]
            forum = gri['forums'] if len(gri['forums']) > 0 else [['None Found']*3]
        except Exception, e:
            ads = [['None Found']*4]
            forum = [['None Found']*3]
       

        return render_template('reverseSearch.html', resultFound=True, profilePicture=profilePicture, profileName=profileName, whitepateRes=whitepateRes, openCNAMAPIRes=openCNAMAPIRes, calleridserviceRes=calleridserviceRes, googleReverseImageSearchRes=googleReverseImageSearchRes, twitterRes=twitterRes, forumMatches=forum, adMatches=ads)

app.debug = True
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
