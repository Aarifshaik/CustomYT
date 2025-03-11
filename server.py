from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "YT-DLP Render API is running!"

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    video_url = data.get("url")

    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    output_path = "downloads/%(title)s.%(ext)s"

    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path,
    }

    try:
        os.makedirs("downloads", exist_ok=True)  # Ensure downloads folder exists
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return jsonify({"message": "Download complete!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
