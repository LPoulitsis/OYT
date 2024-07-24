# Author: Lefteris Poulitsis
# Last Updated: 24/07/2024

"""
This program is a chatbot that generates responses based on a video transcript, from YouTube.
The user provides a video ID and the program fetches the transcript from YouTube.
The chatbot then generates a context based on the transcript and the user can start questioning the chatbot.
"""

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import ollama