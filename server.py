from flask import Flask, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download():
    video_url = request.args.get('url')
    if not video_url:
        return "No se proporcionó URL", 400

    print("URL recibida:", video_url)

    try:
        yt = YouTube(video_url)
        stream = yt.streams.filter(only_audio=True).first()
        filename = "/tmp/audio.mp3"
        stream.download(output_path="/tmp", filename="audio.mp3")
        print("Archivo descargado:", filename)
        return send_file(filename, as_attachment=True)
    except Exception as e:
        print("Error:", e)
        return f"Error al descargar: {e}", 500

if __name__ == "__main__":
    app.run()
