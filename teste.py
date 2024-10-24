from flask import Flask, request, jsonify, send_file
from yt_dlp import YoutubeDL
import requests
import os
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    format = data.get('format')
    ext = data.get('ext')

    if not url or not format or not ext:
        return jsonify({"error": "URL, format, and extension are required!"}), 400

    ydl_opts = {
        "format": f"{format}",
        "outtmpl": "download/%(title)s.%(ext)s",
        "cookiefile": "www.youtube.com_cookies.txt",  # Caminho para seu arquivo de cookies
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get("title", None)
            video_ext = info_dict.get("ext", None)
            video_path = f"./download/{video_title}.{video_ext}"
            final_path = f"./download/{video_title}.{ext}"
            os.rename(video_path, final_path)

            return send_file(final_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/thumbnail', methods=['POST'])
def get_thumbnail():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({"error": "URL is required!"}), 400

    ydl_opts = {
        "skip_download": True,  # Não baixar o vídeo
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            thumbnail_url = info_dict.get('thumbnail')  # Obtém a URL da thumbnail

            # Faz a requisição para baixar a thumbnail
            response = requests.get(thumbnail_url)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                img_path = f"./download/{info_dict['title']}_thumbnail.jpg"
                img.save(img_path)

                return send_file(img_path, mimetype='image/jpeg')
            else:
                return jsonify({"error": "Failed to download thumbnail"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)