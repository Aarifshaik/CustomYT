# from flask import Flask, request, send_file, jsonify
# import yt_dlp
# import os
# import glob
# import re

# app = Flask(__name__)

# def sanitize_filename(filename):
#     """Sanitize filename by removing invalid characters and replacing spaces with underscores."""
#     filename = re.sub(r'[<>:"/\\|?*]', '_', filename)  # Remove invalid characters
#     return filename.replace(" ", "_")  # Replace spaces with underscores

# @app.route('/')
# def home():
#     return "YT-DLP Server is Running!"

# @app.route('/download', methods=['POST'])
# def download_video():
#     data = request.get_json()
#     video_url = data.get("url")

#     if not video_url:
#         return jsonify({"error": "No URL provided"}), 400

#     output_path = "downloads/%(title)s.%(ext)s"
#     print(f"Video path: {output_path}")

#     ydl_opts = {
#         'format': 'best',
#         'outtmpl': output_path,
#         'cookiefile': 'cookies.txt', 
#     }

#     try:
#         os.makedirs("downloads", exist_ok=True)  # Ensure downloads folder exists

#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info_dict = ydl.extract_info(video_url, download=True)
#             video_title = info_dict.get('title', 'video')
#             print(f"Video Title: {video_title}")
#             video_ext = info_dict.get('ext', 'mp4')
#             # video_filename = f"downloads/{video_title}.{video_ext}"
            
#             sanitized_name = sanitize_filename(video_title)  # Sanitize title
#             sanitized_path = f"downloads/{sanitized_name}.{video_ext}"  # New path
#             original_path = f"downloads/{video_title}.{video_ext}"
#             if os.path.exists(original_path):
#                 os.rename(original_path, sanitized_path)  # Rename file

#         if not os.path.exists(sanitized_path):
#             return jsonify({"error": "Download failed"}), 500        

#         return send_file(sanitized_path, as_attachment=True)

#     except Exception as e:
#         print(f"Error: {str(e)}")  # Debug log
#         return jsonify({"error": str(e)}), 500

# @app.route('/removeall', methods=['DELETE'])
# def remove_all_downloads():
#     try:
#         files = glob.glob("downloads/*")  # Get all files in downloads folder

#         if not files:
#             return jsonify({"message": "No files to delete"}), 200

#         for file in files:
#             os.remove(file)

#         return jsonify({"message": "All files deleted successfully"}), 200

#     except Exception as e:
#         print(f"Error: {str(e)}")  # Debug log
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=10000)



import os
import re
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS  # Import CORS
# import time
import yt_dlp
import glob

app = Flask(__name__)
CORS(app)  # Add CORS support

def sanitize_filename(filename):
    """Sanitize filename by removing invalid characters and replacing spaces with underscores."""
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)  # Remove invalid characters
    return filename.replace(" ", "_")  # Replace spaces with underscores

@app.route('/')
def home():
    return "YT-DLP Server is Running!"


@app.route('/download', methods=['POST'])
def download_video():
    # startTime= time.time()
    data = request.get_json()
    video_url = data.get("url")

    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        os.makedirs("downloads", exist_ok=True)  # Ensure downloads folder exists

        with yt_dlp.YoutubeDL({'format': 'best'}) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)  # Get video info first
            video_title = info_dict.get('title', 'video')
            video_ext = info_dict.get('ext', 'mp4')

            sanitized_name = sanitize_filename(video_title)
            sanitized_path = f"downloads/{sanitized_name}.{video_ext}"

            ydl_opts = {
                'format': 'best',
                'outtmpl': sanitized_path,  # Save directly with sanitized name
                'cookiefile': 'cookies.txt',
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        if not os.path.exists(sanitized_path):
            return jsonify({"error": "Download failed Because File not Found"}), 500       
        # endTime= time.time()
        # print(f"Time taken to download the video: {endTime-startTime} seconds") 

        return send_file(sanitized_path, as_attachment=True)

    except Exception as e:
        print(f"Error: {str(e)}")  # Debug log
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
        print(f"Error: {str(e)}")  # Debug log
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
