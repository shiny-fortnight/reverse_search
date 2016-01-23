from flask import Flask, render_template, request
from FacebookResetPasswordAPI import FacebookResetPasswordAPI
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == "GET":
        return render_template('reverseSearch.html', new=True)
    if request.method == "POST":
        emailQuery = request.form['email']
        res = FacebookResetPasswordAPI({'verbose': True}).get(emailQuery)
        profilePicture = res['profile_picture'][:-2]+'250'
        profileName = res['full_name']
        return render_template('reverseSearch.html', new=False, res=res, profilePicture=profilePicture, profileName=profileName)

app.debug = True
if __name__ == "__main__":
    app.run()
