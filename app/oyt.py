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

def generate_context(text_formatted):
    ollama.chat(model = "mistral", messages = [
        {
            "role": "user",
            "content": f"""You will be provided with a video 
                        transcript from youtube which you will 
                        have to answer certain questions to 
                        the user based on the transcript contents.
                        Act as an expert in any given field related
                        to the video transcript's topics. 
                        Here's the transcript: {text_formatted}"""
        }
    ])

def format_video_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    formatter = TextFormatter()
    return formatter.format_transcript(transcript)

if __name__ == "__main__":
    logo = """
  _____   _______ 
 / _ \\ \\ / /_   _|
| | | \\ V /  | |  
| |_| || |   | |  
 \\___/ |_|   |_|  
    """
    print(logo)
    
    while True:

        video_id = input("Enter a video ID (or press 'x' to exit): ")
        
        if video_id == 'x':
            break
        
        text_formatted = format_video_transcript(video_id)
        
        print("Transcript has been saved successfully!")
        generate_context(text_formatted)