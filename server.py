from flask import Flask, request, jsonify, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Servidor activo 🚀. Usa /download?url=LINK_DE_YOUTUBE"

@app.route("/download")
def download_audio():
    try:
        url = request.args.get("url")  # obtenemos la URL del video
        if not url:
            return jsonify({"error": "Falta el parámetro url"}), 400

        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).first()

        # nombre temporal
        out_file = audio.download(filename="temp_audio")

        # renombrar a mp3
        base, ext = os.path.splitext(out_file)
        new_file = base + ".mp3"
        os.rename(out_file, new_file)

        return send_file(new_file, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
