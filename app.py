from flask import Flask, request, jsonify
from flask_cors import CORS
import youtube_dl

app = Flask(__name__)
CORS(app)
# Set up Chrome options for headless mode

@app.route('/',methods=['GET'])
def home():
    return jsonify({"Message":"Welcome To This Api"})
@app.route('/get_video_src', methods=['GET'])
def get_video_src():
    # Get the website link from the request query parameters
    website_link = request.args.get('website_link')
   ydl_opts = {
    'quiet': True,
    'extract_flat': True,
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(website_link, download=False)
            if 'entries' in result:  # If multiple videos are found
                return [video['url'] for video in result['entries']]
            else:  # If only one video is found
                return jsonify({"Video":result['url']})
        except youtube_dl.utils.DownloadError as e:
            return jsonify({"Error ":str(e)})

if __name__ == '__main__':
    app.run(debug=True)
