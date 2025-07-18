from flask import Flask, request, render_template
from youtube import YouTubeAPI

app = Flask(__name__)
yt = YouTubeAPI()

@app.route("/room")
async def room():
    video_id = request.args.get("t")
    if not video_id:
        return "Room not found", 400

    track, _ = await yt.track(video_id)
    return render_template("player.html", track=track)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
