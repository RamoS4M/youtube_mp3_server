from flask import Flask, request, send_file
import yt_dlp

app = Flask(__name__)

@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    if not url:
        return "No URL provided", 400

    filename = "/tmp/audio.mp3"  # carpeta temporal de Heroku
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': filename,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run()
