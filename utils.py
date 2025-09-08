import os
import unicodedata
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.platypus import PageBreak

#  DejaVu fonts (Regular + Bold)
font_dir = os.path.join(os.path.dirname(__file__), "fonts")
pdfmetrics.registerFont(TTFont("DejaVu", os.path.join(font_dir, "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", os.path.join(font_dir, "DejaVuSans-Bold.ttf")))

registerFontFamily(
    "DejaVu",
    normal="DejaVu",
    bold="DejaVu-Bold"
)

def clean_text(text: str) -> str:
    """Fix encoding issues and normalize Unicode quotes/apostrophes."""
    if not text:
        return ""
    text = unicodedata.normalize("NFC", text)
    replacements = {
        "â€™": "'", "â€œ": "“", "â€�": "”",
        "â€˜": "‘", "â€“": "–", "â€”": "—",
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    return text

def save_pdf(articles, filename: str):
    """Generate a styled PDF with Unicode-safe DejaVu font and cleaned text."""
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()

    # Styles
    normal_style = ParagraphStyle(
        "Normal",
        parent=styles["Normal"],
        fontName="DejaVu",
        fontSize=11,
        leading=15,
    )
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        fontName="DejaVu-Bold",   
        fontSize=16,
        textColor=colors.HexColor("#163D64"),
        spaceAfter=12,
    )
    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Heading2"],
        fontName="DejaVu-Bold",   
        fontSize=13,
        textColor=colors.HexColor("#163D64"),
        spaceAfter=8,
    )

    story = []

    for idx, article in enumerate(articles, 1):
        
        article["title"] = clean_text(article.get("title", ""))
        article["summary"] = clean_text(article.get("summary", ""))
        article["key_points"] = [clean_text(pt) for pt in article.get("key_points", [])]

        # Article Heading
        story.append(Paragraph(f"Article {idx}", title_style))
        story.append(Spacer(1, 6))

        # Metadata
        meta = (
            f"<b>URL:</b> <a href='{article['url']}' color='blue'>{article['url']}</a><br/>"
            f"<b>Title:</b> {article['title']}<br/>"
            f"<b>Authors:</b> {', '.join(article['authors']) if article['authors'] else 'N/A'}<br/>"
            f"<b>Published on:</b> {article['publish_date'] if article['publish_date'] else 'N/A'}<br/>"
            f"<b>Sentiment:</b> {article['sentiment']}"
        )
        story.append(Paragraph(meta, normal_style))
        story.append(Spacer(1, 10))

        # Summary
        story.append(Paragraph("Summary", subtitle_style))
        story.append(Paragraph(article["summary"], normal_style))
        story.append(Spacer(1, 10))

        # Key Points
        story.append(Paragraph("Key Points", subtitle_style))
        if article["key_points"]:
            bullet_items = [
                ListItem(Paragraph(pt, normal_style), bulletColor=colors.HexColor("#2980B9"))
                for pt in article["key_points"]
            ]
            story.append(ListFlowable(bullet_items, bulletType="bullet", start="circle"))
        story.append(Spacer(1, 20))

        # Divider
        story.append(Paragraph(
            "<font color='#BDC3C7'>──────────────────────────────────────────────</font>",
            normal_style
        ))
        story.append(Spacer(1, 20))
        # Every  article will start from new page
        if idx < len(articles):
            story.append(PageBreak())

    doc.build(story)
