# GiminiTest Live Odds Dashboard

A modern, cinematic web dashboard featuring live horse racing odds from Fitzdares, updated in real-time using Browserless.io cloud browser automation.

## Features
- **Cinematic UI**: Dark-themed, responsive design with dynamic backgrounds.
- **Live Odds Widget**: Real-time horse racing odds from `fitzdares.com`.
- **Background Caching**: Performance-optimized Flask backend with 60-second background scraping cycles to ensure instant frontend delivery.
- **Browserless Integration**: Uses Puppeteer-based cloud scraping for accurate data capture from Single Page Applications (SPAs).

## Getting Started

### Prerequisites
- Python 3.10+
- [Browserless.io](https://www.browserless.io) API Token

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/artpro88/Giminitest.git
   cd Giminitest
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your API credentials in `app.py`:
   ```python
   BROWSERLESS_TOKEN = "your-api-token"
   BROWSERLESS_API_URL = "your-api-url"
   ```
4. Run the server:
   ```bash
   python app.py
   ```
5. Open `http://127.0.0.1:5001` in your browser.

## Tech Stack
- **Frontend**: Bootstrap 5, Vanilla JS, CSS
- **Backend**: Python, Flask
- **Automation**: Browserless.io (Puppeteer), Requests
