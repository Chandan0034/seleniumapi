from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Set up Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

@app.route('/get_video_src', methods=['GET'])
def get_video_src():
    # Get the website link from the request query parameters
    website_link = request.args.get('website_link')
    
    if not website_link:
        return jsonify({'error': 'Website link not provided'}), 400
    
    try:
        # Initialize Chrome WebDriver with headless mode
        driver = webdriver.Chrome(options=chrome_options)
        
        # Open the website link in ChromeDriver
        driver.get(website_link)
        
        # Get the page source after JavaScript has executed
        html = driver.page_source
        
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find the video tag and get the source attribute
        video_tag = soup.find('video')
        if video_tag:
            video_src = video_tag.get('src')
            return jsonify({'video_src': video_src}), 200
        else:
            return jsonify({'error': 'No video tag found on the page'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Close the WebDriver session
        if 'driver' in locals():
            driver.quit()

if __name__ == '__main__':
    app.run(debug=True)
