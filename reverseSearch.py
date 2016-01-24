<<<<<<< HEAD
from flask import Flask, render_template, request, url_for, redirect
from FacebookResetPasswordAPI import FacebookResetPasswordAPI
from whitepages_api import makeAPIRequest
=======
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

>>>>>>> e69585e9b05ab91c54b5b042d0830d930d444ae3
app = Flask(__name__)



@app.route("/", methods=["GET", "POST"])
def hello():
    print "outside"
    if request.method == "GET":
        print "hahahhaa"
        return render_template('index.html')

    if request.method == "POST":
        print "========"
        print url_for('search')
        return redirect(url_for('search'))

@app.route("/search", methods=["GET", "POST"])
def search():


    if request.method == "GET":
        return render_template('reverseSearch.html', resultFound=False)

    if request.method == "POST":
        query = request.form['email']
<<<<<<< HEAD
        facebookRes = FacebookResetPasswordAPI({'verbose': True}).get(query)
=======
        keywords = request.form['keywords']
        radius = request.form['radius']

        try:
            facebookRes = FacebookResetPasswordAPI({'verbose': True}).get(query)
        except Exception:
            facebookRes = None
        
>>>>>>> e69585e9b05ab91c54b5b042d0830d930d444ae3
        if facebookRes:
            profilePicture = facebookRes['profile_picture'][:-2]+'250'
            profileName = facebookRes['full_name']
        else:
            profilePicture = None
            profileName = None

        try:
            whitepateRes = makeAPIRequest(str(query))
        except Exception, e:
            whitepateRes = e

<<<<<<< HEAD
        # twitterRes = 

        return render_template('/reverseSearch.html', resultFound=True, profilePicture=profilePicture, profileName=profileName, whitepateRes=whitepateRes)
        # return render_template('reverseSearch.html', resultFound=True, profilePicture=profilePicture, profileName=profileName, whitepateRes=whitepateRes, twitterRes=twitterRes)
=======
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
            forum = [forum[0]]

        return render_template('reverseSearch.html', resultFound=True, profilePicture=profilePicture, profileName=profileName, whitepateRes=whitepateRes, openCNAMAPIRes=openCNAMAPIRes, calleridserviceRes=calleridserviceRes, googleReverseImageSearchRes=googleReverseImageSearchRes, twitterRes=twitterRes, forumMatches=forum, adMatches=ads)
>>>>>>> e69585e9b05ab91c54b5b042d0830d930d444ae3

app.debug = True
if __name__ == "__main__":
    app.run()
