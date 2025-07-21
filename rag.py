import os
from dotenv import load_dotenv
from embedchain import App
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

load_dotenv()

class VideoBot:
    def __init__(self):
        self.bot = App()
    
    def _get_video_id(self, url):
        """Extract video ID from YouTube URL."""
        parsed_url = urlparse(url)
        if parsed_url.hostname in ('youtu.be',):
            return parsed_url.path[1:]
        if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
            if parsed_url.path == '/watch':
                return parse_qs(parsed_url.query)['v'][0]
            if parsed_url.path[:7] == '/embed/':
                return parsed_url.path.split('/')[2]
            if parsed_url.path[:3] == '/v/':
                return parsed_url.path.split('/')[2]
        return None

    def _get_transcript(self, video_id):
        """Get transcript for a YouTube video."""
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            return ' '.join([entry['text'] for entry in transcript_list])
        except Exception as e:
            raise Exception(f"Could not fetch transcript: {str(e)}")

    def add_youtube_video(self, url):
        """Add YouTube video content to the knowledge base."""
        try:
            # Extract video ID
            video_id = self._get_video_id(url)
            if not video_id:
                return "Error: Invalid YouTube URL"
            
            # Get transcript
            transcript = self._get_transcript(video_id)
            if not transcript:
                return "Error: Could not fetch transcript"
            
            # Add transcript to embedchain as text
            self.bot.add(transcript, data_type="text")
            return "Video transcript successfully added to knowledge base"
        except Exception as e:
            return f"Error adding video: {str(e)}"

    def query(self, question):
        """Query the knowledge base."""
        try:
            response = self.bot.query(question)
            return response
        except Exception as e:
            return f"Error generating response: {str(e)}"
