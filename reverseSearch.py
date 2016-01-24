from flask import Flask, render_template, request, url_for, redirect
import os
import itertools
from flask import Flask, render_template, request
from modules.FacebookResetPasswordAPI import FacebookResetPasswordAPI
from modules.whitepages_api import makeAPIRequest
from modules.OpenCNAMAPI import OpenCNAMAPI
from modules.calleridservice import call_calleridservice
from modules.GoogleReverseImageSearch import searchImage
from modules.geo_twitter_lookup import search_twitter
from modules.related_lookup import GetRelatedInfo
from modules.truecaller import get_truecaller_result
from backpage_api import doBackpageRequest
app = Flask(__name__)



@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == "GET":
        return render_template('index.html')

    if request.method == "POST":
        return redirect(url_for('search'))

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template('reverseSearch.html', resultFound=False)

    if request.method == "POST":
        query = request.form['email']
        keywords = request.form['keywords']
        radius = request.form['radius']

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
            whitepageRes = makeAPIRequest(str(query))
        except Exception, e:
            whitepageRes = e

        try:
            twitterRes = search_twitter(str(query), str(keywords), str(radius))
        except Exception, e:
            twitterRes = e

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
        if len(ads) > 1:
            ads = [ads[0]]
        if len(forum) > 1:
            print forum
            forum = [forum[0]]

        try:
            truecallerRes = get_truecaller_result(query)
        except IOError:
            truecallerRes = "None Found on TrueCaller"

        try:
            backpageResults = doBackpageRequest(query)
            if len(backpageResults) > 5:
                backpageResults = backpageResults[:4]
        except Exception:
            backpageResults = ["No Results Found"]
        if len(backpageResults) == 0:
            backpageResults = ["No Results Found"]

        return render_template('reverseSearch.html', resultFound=True, profilePicture=profilePicture, profileName=profileName, whitepageRes=whitepageRes, openCNAMAPIRes=openCNAMAPIRes, calleridserviceRes=calleridserviceRes, googleReverseImageSearchRes=googleReverseImageSearchRes, twitterRes=twitterRes, forumMatches=forum, adMatches=ads, truecallerRes=truecallerRes, backpageRes = backpageResults)

app.debug = True
if __name__ == "__main__":
    app.run()
