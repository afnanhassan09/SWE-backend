from youtube_transcript_api import YouTubeTranscriptApi
import re


def extract_video_id(youtube_url):
    pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:[^/]+/.+/|(?:v|e(?:mbed)?)|.*[?&]v=)|youtu\.be/)([^"&?/ ]{11})'
    match = re.search(pattern, youtube_url)
    if match:
        return match.group(1)
    else:
        return None


def get_caption(youtube_link):
    video_id = extract_video_id(youtube_link)
    if video_id is None:
        raise ValueError("Invalid YouTube URL")

    try:
        # Fetch transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        caption = ""
        # Concatenate transcript entries
        for entry in transcript:
            caption += entry["text"] + " "
        return caption
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None
