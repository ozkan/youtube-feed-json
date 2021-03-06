from flask import Flask, request, jsonify, url_for
from bs4 import BeautifulSoup
import requests, json, xmltodict
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/playlist/', methods=['GET'])
def playlist():
    videoJson = dict()
    playlistId = request.args.get("id", None)
    if not playlistId:
        videoJson["ERROR"] = "no id found, please send a playlist id."
    else:
        r = requests.get('https://www.youtube.com/feeds/videos.xml?playlist_id=' + playlistId)
        source = BeautifulSoup(r.content, "html.parser")
        contentDict = xmltodict.parse(str(source))
        jsonDumps = json.dumps(contentDict)
        jsonLoads = json.loads(jsonDumps)
        feeds = jsonLoads["feed"]["entry"]
        for j, i in enumerate(feeds ):
            videoJson.update({str(j): {'videoTitle' : i['title'], 'videoID' : i['yt:videoid'], 'videolink': i['link']['@href'], 'channelName' : i['author']['name'], 'embedUrl' : 'https://www.youtube.com/embed/'+i['yt:videoid'], 'channelLink': i['author']['uri'], 'videoPublished' : i['published'], 'videoUpdated' : i['updated'], 'videoThumbnailUrl' : i['media:group']['media:thumbnail']['@url'], 'videoDescription': i['media:group']['media:description']}})
    return jsonify(videoJson)


@app.route('/channel/', methods=['GET'])
def channel():
    videoJson = dict()
    channelId = request.args.get("id", None)
    if not channelId:
        videoJson["ERROR"] = "no id found, please send a channel id."
    else:
        r = requests.get('https://www.youtube.com/feeds/videos.xml?channel_id=' + channelId)
        source = BeautifulSoup(r.content, "html.parser")
        contentDict = xmltodict.parse(str(source))
        jsonDumps = json.dumps(contentDict)
        jsonLoads = json.loads(jsonDumps)
        feeds = jsonLoads["feed"]["entry"]
        for j, i in enumerate(feeds):
            videoJson.update({str(j): {'videoTitle' : i['title'], 'videoID' : i['yt:videoid'], 'videolink': i['link']['@href'], 'channelName' : i['author']['name'], 'embedUrl' : 'https://www.youtube.com/embed/'+i['yt:videoid'], 'channelLink': i['author']['uri'], 'videoPublished' : i['published'], 'videoUpdated' : i['updated'], 'videoThumbnailUrl' : i['media:group']['media:thumbnail']['@url'], 'videoDescription': i['media:group']['media:description']}})
    return jsonify(videoJson)

@app.route('/')
def index():
    return  f""" <h1> Youtube-xml to json convert with Flask REST API:</h1><br>
feedtube.herokuapp.com/playlist/?id&lt;playlist_id&gt;<br>
feedtube.herokuapp.com/channel/?id&lt;channel_id&gt; <br> Author: <a href='https://github.com/ozkan/feedtube'>https://https://github.com/ozkan</a>"""

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
