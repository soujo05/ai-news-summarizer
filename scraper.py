import requests
from newspaper import Article

# For fallback
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from text_cleaning import fix_mojibake

def _safe_decode(resp: requests.Response) -> str:
    # Prefer UTF-8; fall back to requests’ guess
    try:
        return resp.content.decode("utf-8")
    except UnicodeDecodeError:
        enc = resp.apparent_encoding or "latin-1"
        return resp.content.decode(enc, errors="replace")


def scrape_news(url):
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/115.0.0.0 Safari/537.36"
            )
        }

        # --- Try newspaper3k first ---
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return {"error": f"Failed to fetch URL, status code: {response.status_code}"}

        article = Article(url)
        article.set_html(response.text)
        article.parse()

        if article.text and len(article.text.split()) > 50:  # ✅ Enough text found
            return {
                "title": article.title,
                "authors": article.authors,
                "publish_date": article.publish_date,
                "text": article.text,
            }

        # --- Fallback: Playwright ---
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=30000)  # wait up to 30s
            html = page.content()
            browser.close()

        soup = BeautifulSoup(html, "html.parser")
        paragraphs = [p.get_text() for p in soup.find_all("p")]
        text = " ".join(paragraphs)

        return {
            "title": article.title or soup.title.string if soup.title else "",
            "authors": article.authors or [],
            "publish_date": article.publish_date,
            "text": text.strip(),
        }

    except Exception as e:
        return {"error": str(e)}
