from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from flask_cors import CORS

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
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(website_link)
    return jsonify({"title":driver.title})
if __name__ == '__main__':
    app.run(debug=True)
