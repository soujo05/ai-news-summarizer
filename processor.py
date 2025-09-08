from transformers import pipeline
import re
from text_cleaning import fix_mojibake   # This fixes the garbage text in the words

# Load models once
summarizer_model = pipeline(
    "summarization", 
    model="facebook/bart-large-cnn", 
    device=-1
)
sentiment_model = pipeline(
    task="text-classification",  
    model="fhamborg/roberta-targeted-sentiment-classification-newsarticles",
    tokenizer="fhamborg/roberta-targeted-sentiment-classification-newsarticles"
)
def chunk_text(text, max_words=800):
    """Split long text into smaller chunks."""
    words = text.split()
    for i in range(0, len(words), max_words):
        yield " ".join(words[i:i+max_words])

def process_article(text):
    # ---- Using Chunks to handle long texts ----
    chunks = list(chunk_text(text))
    summaries = []

    for chunk in chunks:
        summary = summarizer_model(
            chunk, max_length=200, min_length=80, do_sample=False
        )[0]["summary_text"]
        summaries.append(summary)

   
    full_summary = " ".join(summaries)

    # ---- Key Points ----
    short_summary = summarizer_model(
        full_summary, max_length=150, min_length=60, do_sample=False
    )[0]["summary_text"]

    
    key_points = re.split(r"(?<=[.!?]) +", short_summary)
    key_points = [s.strip() for s in key_points if s.strip()]

    if len(key_points) < 5:
        raw_sentences = re.split(r"(?<=[.!?]) +", text)
        for s in raw_sentences:
            if len(s.split()) > 8 and s not in key_points:
                key_points.append(s.strip())
            if len(key_points) >= 5:
                break

    key_points = key_points[:5]  # take top 5

    # ---- Sentiment(Positive/Negative)----
    sentiment = sentiment_model(full_summary[:512])[0]["label"]
    sentiment = "Positive" if sentiment == "POSITIVE" else "Negative"

    # ---- Clean outputs  ----
    full_summary = fix_mojibake(full_summary)
    key_points = [fix_mojibake(kp) for kp in key_points]

    return {
        "summary": full_summary,
        "key_points": key_points,
        "sentiment": sentiment
    }
