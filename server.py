from flask import Flask, request, jsonify, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Servidor funcionando 🚀"

@app.route("/download", methods=["GET"])
def download():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Falta el parámetro 'url'"}), 400

    try:
        # Carpeta temporal para Railway
        temp_dir = "/tmp"
        output_file = os.path.join(temp_dir, "audio.%(ext)s")

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": output_file,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            mp3_file = filename.rsplit(".", 1)[0] + ".mp3"

        return send_file(mp3_file, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
