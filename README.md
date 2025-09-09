# AI News Summarizer

## Overview

The **AI News Summarizer** is an AI-powered application built with **Streamlit**, **Hugging Face Transformers**, and **Newspaper3k**.  
It allows users to paste **news article URLs** or raw **article text** and generates:

- Concise summaries  
- Extracted key points  
- Sentiment analysis  
- Audio summaries (TTS)  
- Exportable PDF reports  

## Features

- **Automatic Article Extraction:** Fetches full articles from URLs.  
- **Summarization:** Generates clean and concise summaries using **BART-Large-CNN**.  
- **Key Point Extraction:** Extracts top highlights for quick scanning.  
- **Sentiment Analysis:** Determines if the article sentiment is positive or negative.  
- **PDF Export:** Saves results in professional PDF format with Unicode-safe fonts.  
- **Audio Summaries:** Provides audio playback and downloadable MP3s using **gTTS**.  
- **Batch Processing:** Supports multiple articles with progress tracking.  

## Project Structure

├── app.py # Streamlit main app
├── processor.py # Summarization, sentiment, key points
├── scraper.py # News scraping
├── utils.py # PDF generation utilities
├── text_cleaning.py # Fixes mojibake & text artifacts
├── requirements.txt # Dependencies
└── fonts/ # DejaVuSans fonts for Unicode PDF export

## Tech Stack

- **Python** (core programming language)
- **Streamlit** (for UI and app deployment)
- **Newspaper3k** (for web scraping and article extraction)
- **Hugging Face Transformers** (for text summarization and sentiment analysis)
- **gTTS** (for text-to-speech conversion)
- **ReportLab** (for PDF generation)

## Challenges Faced

- **Article Extraction Issues:** Some websites block scrapers or provide incomplete text, requiring cleaning and fallback handling.
- **Long Article Summarization:** Very lengthy news articles required chunking before summarization to avoid model limitations.
- **Mojibake and Encoding Errors:** Non-English characters and formatting artifacts needed preprocessing fixes.
- **Performance:** Processing multiple long articles at once caused slower response times; optimized with progress tracking.
- **PDF Formatting:** Ensuring proper Unicode font support was necessary for multilingual text in exports.

## How to Run

### Prerequisites

- Python 3.10  
- Required dependencies (install using `requirements.txt`)  
- Playwright installed (`playwright install`)  

### Installation

```sh
# Clone the repository
git clone https://github.com/soujo05/ai-news-summarizer.git
cd ai-news-summarizer

# Create a virtual environment
'''sh
python -m venv .venv
source .venv/bin/activate   # On Linux/Mac
.venv\Scripts\activate      # On Windows
'''
# Install dependencies
pip install -r requirements.txt

# Install Playwright dependencies
playwright install
```
### Running the Application

```sh
streamlit run app.py
```

### Modes

- ***From URLs:*** Paste one or more article URLs (comma separated).
- ***From Text:*** Paste raw article text or transcripts.

### Outputs

- Summary + Key Points + Sentiment
- Audio playback + Downloadable .mp3
- PDF digest of all articles

### Example Output

- ***Summary (text):*** Concise overview of the article
- ***Key Points:*** 5 bullet highlights
- ***Sentiment:*** Positive / Negative
- ***Audio Summary:*** Play or download as .mp3
- ***PDF Export:*** Professional digest of multiple articles

## Future Improvements

- **Multilingual Support:** Extend summarization and sentiment analysis to multiple languages.  
- **Advanced Summarization Models:** Integrate newer LLMs (e.g., Llama 3, Mistral) for more accurate summaries.  
- **Better Sentiment Analysis:** Provide more nuanced sentiment (e.g., neutral, mixed) instead of just positive/negative.  
- **Faster Processing:** Optimize long-text summarization with GPU support or model distillation.  
- **UI Enhancements:** Add interactive dashboards with filters, keyword search, and article comparison.  
- **Database Integration:** Store summarized articles in a database for future retrieval and analytics.  
- **Deployment Options:** Provide Docker support and deployment guides for cloud platforms.  

## Contributing

Feel free to open issues and submit pull requests to improve this project.

## License

[MIT License](LICENSE)
