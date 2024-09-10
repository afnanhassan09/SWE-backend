import textwrap
import google.generativeai as genai
from IPython.display import Markdown
from article import extract_main_content
from caption import get_caption
import re

GOOGLE_API_KEY = "AIzaSyBWH-MAIj9PeMiWTEgDTJgI-FNVrzrPt9E"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")


def to_markdown(text):
    text = text.replace("•", "")
    return Markdown(textwrap.indent(text, "> ", predicate=lambda _: True))


def clean_text(text):

    text = re.sub(r"[>*•]", "", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    text = text.strip()

    lines = text.split("\n")
    seen = set()
    cleaned_lines = []
    for line in lines:
        if line not in seen:
            cleaned_lines.append(line)
            seen.add(line)

    return "\n".join(cleaned_lines)


def is_youtube_video_link(url):
    youtube_pattern = r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/(watch\?v=|v/|.+/|.*[?&]v=)?([^"&?/ ]{11})'
    return bool(re.match(youtube_pattern, url))


def extract_info_and_store(response_text):
    topic_pattern = r"Topic:\s*([^\n]+)"
    summary_pattern = r"Summary:\s*([^\n]+)"
    website_name_pattern = r"Website Name:\s*([^\n]+)"
    purpose_pattern = r"Purpose:\s*([^\n]+)"

    topic_match = re.search(topic_pattern, response_text, re.IGNORECASE)
    summary_match = re.search(summary_pattern, response_text, re.IGNORECASE)
    website_name_match = re.search(website_name_pattern, response_text, re.IGNORECASE)
    purpose_match = re.search(purpose_pattern, response_text, re.IGNORECASE)

    topic = topic_match.group(1).strip() if topic_match else None
    summary = summary_match.group(1).strip() if summary_match else None
    website_name = website_name_match.group(1).strip() if website_name_match else None
    purpose = purpose_match.group(1).strip() if purpose_match else None
    if topic != None and summary != None:
        topic = topic.replace(summary, "")
        topic = topic.replace(" Summary: ", "")
    if website_name != None and purpose != None:
        website_name = website_name.replace(purpose, "")
        website_name = website_name.replace(" Purpose: ", "")

    extracted_data = {
        "Topic": topic,
        "Summary": summary,
        "Website": website_name,
        "Purpose": purpose,
    }

    print("Extracted data = ", extracted_data)


def generate_summary(url):
    if is_youtube_video_link(url):
        print("Getting the captions from the video")
        content = get_caption(url)
    else:
        print("Scrapping the article")
        content = extract_main_content(url)
    print("Generating response...")

    prompt = f"""
    Analyze the following text and URL:
    URL: {url}
    Text: {content}

    Instructions:
    1. If the content is a web article or YouTube video caption, provide a summary in the following format:
        - **Topic**: 
        - **Summary**: 

    2. If the content is neither a web article nor a YouTube video caption, provide the following information only:
        - **Website Name**: 
        - **Purpose**: 
    """

    response = model.generate_content(prompt)
    summarized_text = clean_text(to_markdown(response.text).data)

    return extract_info_and_store(summarized_text)
