from flask import Flask, render_template, request, redirect, url_for
import requests

class Achievement:
    def __init__(self, iName, iApiname, iDesc, iAchieved):
        self.name = iName
        self.apiname = iApiname
        self.description = iDesc
        self.achieved = iAchieved

# TODO: Check if steamID is correct.
def getAchiReq(userId):
    appId = "236850"                                #  The game ID (EU4)
    steamId = userId
    #steamId = "76561198096650725"                   #  The users ID
    apiKey = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"     # !IMPORTANT! This is NOT to be shared with anyone

    url = "https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid=" + appId + "&key=" + apiKey + "&steamid=" + steamId + "&l=en"

    data = requests.get(url).json()

    achievementList = data["playerstats"]["achievements"]
    return achievementList

# TODO: Handle if achiTarget doesnt match anything.
def getAchData(achiTarget, achiList):
    target = next((item for item in achiList if item["name"].lower() == achiTarget.lower()),"Achievement not found")
    return target


app = Flask(__name__, static_url_path='/static')

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":

        """fdata = request.form
        for key in fdata.keys():
            for value in fdata.getlist(key):
                print(value)"""
        inputId = request.form.get("myID")
        #print(request.form.get("myAchi"))
        if "search" in request.form:
            achiInput = request.form.get("myAchi")

            if 0 < len(achiInput) <= 40:
                targetedAchievement = (getAchData(achiInput, getAchiReq(inputId)))
                achiResult = Achievement(targetedAchievement.get("name"), targetedAchievement.get("apiname"), targetedAchievement.get("description"), targetedAchievement.get("achieved"))
                print(achiResult.name)
                print(achiResult.description)
                print(achiResult.achieved)

                return render_template("result.html", achiResult=achiResult)

        elif "show_all" in request.form:
            achiResult_list = []
            print("lol what")
            achi_list = getAchiReq(inputId)
            for i in achi_list:
                #check if achieved:
                if i.get("achieved") == 1:
                    print("1")
                    achiResult_list.append(Achievement(i.get("name"), i.get("apiname"), i.get("description"), i.get("achieved")))

            return render_template("result_list.html", achiResult_list=achiResult_list)


    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5050)
