from flask import Flask, send_from_directory, jsonify
import os
import requests
import threading
import time

app = Flask(__name__)

# Browserless configuration
BROWSERLESS_TOKEN = os.environ.get("BROWSERLESS_TOKEN", "2UE5AkChTxVhuOfa918d58ed477655d03be8abd47f7fe748f")
BROWSERLESS_API_URL = os.environ.get("BROWSERLESS_API_URL", "https://production-lon.browserless.io")

# Global cache
cache = {
    "data": None,
    "last_updated": 0,
    "is_updating": False,
    "last_error": None
}

def scrape_odds():
    """Background task to scrape odds and update the cache."""
    while True:
        try:
            cache["is_updating"] = True
            print("Starting background scrape...")
            
            # Script that captures both text
            puppeteer_script = """
            export default async ({ page }) => {
              await page.setViewport({ width: 1280, height: 1600 });
              // Use a common user agent to avoid some blocks
              await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
              
              await page.goto("https://fitzdares.com", { waitUntil: "networkidle2", timeout: 45000 });
              
              // Handle potential cookie banner
              try {
                const cookieButton = await page.$('#onetrust-accept-btn-handler');
                if (cookieButton) {
                   await cookieButton.click();
                   await new Promise(r => setTimeout(r, 1000));
                }
              } catch (e) {}

              // Scroll a bit to trigger lazy loading if any
              await page.evaluate(() => window.scrollBy(0, 500));
              await new Promise(r => setTimeout(r, 8000));
              
              const data = await page.evaluate(() => document.body.innerText);
              return { data, type: "text/plain" };
            };
            """
            response = requests.post(
                f"{BROWSERLESS_API_URL}/function?token={BROWSERLESS_TOKEN}",
                headers={"Content-Type": "application/javascript"},
                data=puppeteer_script,
                timeout=90
            )
            
            if response.status_code == 200:
                try:
                    res_json = response.json()
                    text_content = res_json.get("data", "")
                    if text_content and len(text_content) > 500:
                        cache["data"] = text_content
                        cache["last_updated"] = time.time()
                        cache["last_error"] = None
                        print(f"Cache updated successfully. Length: {len(text_content)}")
                    else:
                        cache["last_error"] = "Scraped data too short or empty."
                        print(f"Validation failed: {cache['last_error']}")
                except Exception as je:
                    cache["last_error"] = f"JSON parse error: {str(je)}"
                    print(cache["last_error"])
            else:
                cache["last_error"] = f"Browserless HTTP {response.status_code}"
                print(f"Scrape failed: {cache['last_error']}")
        except Exception as e:
            cache["last_error"] = str(e)
            print(f"Scrape error: {str(e)}")
        finally:
            cache["is_updating"] = False
        
        time.sleep(60)

threading.Thread(target=scrape_odds, daemon=True).start()

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/api/odds')
def get_odds():
    if cache["data"]:
        return jsonify({
            "ok": True, 
            "data": cache["data"], 
            "last_updated": cache["last_updated"]
        })
    else:
        return jsonify({
            "ok": False, 
            "error": cache["last_error"] or "Warming up...",
            "is_updating": cache["is_updating"]
        }), 503

if __name__ == '__main__':
    app.run(debug=True, port=5001, use_reloader=False)
