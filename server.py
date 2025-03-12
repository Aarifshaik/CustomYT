from flask import Flask, request, send_file, jsonify
import yt_dlp
import os
import glob
# import re

app = Flask(__name__)


# def clean_youtube_url(url):
#     match = re.search(r"(https://youtube\.com/shorts/[\w-]+)", url)
#     return match.group(1) if match else None


# def sanitize_filename(filename):
    # return re.sub(r'[\\/*?:"<>|]', "", filename).replace(" ", "_")

@app.route('/')
def home():
    return "YT-DLP Server is Running!"


@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    video_url = data.get("url")
    # video_url = clean_youtube_url(video_url)
    # print(video_url)
    # return 0

    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    output_path = "downloads/%(title)s.%(ext)s"

    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path,
        'cookiefile': 'cookies.txt', 
    }

    try:
        os.makedirs("downloads", exist_ok=True)  # Ensure downloads folder exists

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_title = info_dict.get('title', 'video')
            video_ext = info_dict.get('ext', 'mp4')
            video_filename = f"downloads/{video_title}.{video_ext}"

        if not os.path.exists(video_filename):
            return jsonify({"error": "Download failed"}), 500

        response = send_file(video_filename, as_attachment=True)


        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/removeall', methods=['DELETE'])
def remove_all_downloads():
    try:
        files = glob.glob("downloads/*")  # Get all files in downloads folder

        if not files:
            return jsonify({"message": "No files to delete"}), 200

        for file in files:
            os.remove(file)

        return jsonify({"message": "All files deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
