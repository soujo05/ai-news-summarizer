# app.py
import streamlit as st
import tempfile
from scraper import scrape_news
from processor import process_article
from utils import save_pdf   # styled PDF
from gtts import gTTS

st.set_page_config(page_title="AI News Summarizer", layout="wide")

st.title("📰 AI News Summarizer")
st.write("Paste news article URLs **or** raw text and get **summary, key points, sentiment, and audio playback**.")

# ---- Session State ----
if "articles" not in st.session_state:
    st.session_state["articles"] = []

tab1, tab2 = st.tabs(["🌐 From URLs", "✍️ From Text"])

# ---------- TAB 1: URLs ----------
with tab1:
    urls = st.text_area("Enter URLs (comma separated):")

    if st.button("Summarize from URLs"):
        if urls.strip():
            url_list = [u.strip() for u in urls.split(",") if u.strip()]
            articles = []

            progress_bar = st.progress(0)
            status_text = st.empty()
            total = len(url_list)

            for idx, url in enumerate(url_list, 1):
                status_text.text(f"Processing article {idx} of {total} ...")

                with st.spinner(f"Fetching & summarizing: {url}"):
                    news = scrape_news(url)
                    if "error" in news:
                        st.error(news["error"])
                        continue

                    result = process_article(news["text"]) if news.get("text") else {
                        "summary": "", "key_points": [], "sentiment": "N/A"
                    }

                    articles.append({
                        "url": url,
                        "title": news.get("title", ""),
                        "authors": news.get("authors", []),
                        "publish_date": news.get("publish_date"),
                        "sentiment": result["sentiment"],
                        "summary": result["summary"],
                        "key_points": result["key_points"]
                    })

                progress_bar.progress(idx / total)

            status_text.text("✅ All articles processed!")
            st.session_state["articles"] = articles
        else:
            st.warning("⚠️ Please enter at least one URL.")

# ---------- TAB 2: Raw Text ----------
with tab2:
    raw_text = st.text_area("Paste article text or transcript here:", height=300)

    if st.button("Summarize Text"):
        if raw_text.strip():
            with st.spinner("Summarizing text..."):
                result = process_article(raw_text)

                st.session_state["articles"] = [{
                    "url": "N/A (pasted text)",
                    "title": "User Input Text",
                    "authors": [],
                    "publish_date": None,
                    "sentiment": result["sentiment"],
                    "summary": result["summary"],
                    "key_points": result["key_points"]
                }]
        else:
            st.warning("⚠️ Please paste some text.")

# ---------- Redisplay Results ----------
if st.session_state["articles"]:
    for idx, article in enumerate(st.session_state["articles"], 1):
        st.markdown(f"## Article {idx}")
        st.markdown(f"**URL:** {article['url']}")
        st.markdown(f"**Title:** {article['title']}")
        if article["authors"]:
            st.markdown(f"**Authors:** {', '.join(article['authors'])}")
        if article["publish_date"]:
            st.markdown(f"**Published on:** {article['publish_date']}")
        st.markdown(f"### Sentiment: {article['sentiment']}")
        st.markdown("### Summary")
        st.write(article["summary"])

        # ---- Audio Summary ----
        if article["summary"]:
            tts = gTTS(text=article["summary"], lang="en", slow=False)
            audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(audio_file.name)

            st.audio(audio_file.name)  # play inside Streamlit

            with open(audio_file.name, "rb") as f:
                st.download_button(
                    label="🔊 Download Audio Summary",
                    data=f,
                    file_name=f"article_{idx}_summary.mp3",
                    mime="audio/mp3"
                )

        st.markdown("### Key Points")
        for kp in article["key_points"]:
            st.write(f"- {kp}")
        st.divider()

    # ---- PDF Download ----
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    save_pdf(st.session_state["articles"], tmp_file.name)

    with open(tmp_file.name, "rb") as f:
        st.download_button(
            label="📥 Download Summaries as PDF",
            data=f,
            file_name="news_digest.pdf",
            mime="application/pdf"
        )
