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
from termcolor import colored

def generate_response():
    while True:
        question = input(colored("Question: ", "green"))
        print()
        if question == 'bye':
            break
        response = ollama.chat(model = "mistral", messages = [
            {
                "role": "user",
                "content": question
            }
        ])
        print(f"{colored("Response:", "blue")} {response['message']['content']}\n")

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
    logo = f"""
  {colored("___", "white")}{colored("__   __", "red")}{colored("_____", "yellow")}
 {colored("/ _ \\", "white")} {colored("\\ / /", "red")}{colored("_   _|", "yellow")}
{colored("| | | \\", "white")} {colored("V /", "red")}  {colored("| |", "yellow")}
{colored("| |_| |", "white")}{colored("| |", "red")}   {colored("| |", "yellow")}
{colored(" \\___/", "white")} {colored("|_|", "red")}   {colored("|_|", "yellow")}  
    """    
    
    print(colored(logo, "red"))
    
    print(f"""{colored("Welcome", "green")} to the {colored("Ollama", "white")} {colored("YouTube", "red")} {colored("Transcript", "yellow")} chatbot!
This chatbot generates responses based on a video transcript from YouTube.\n""")
    
    while True:

        video_id = input("Enter a video ID (or press 'x' to exit): ")
        
        if video_id == 'x':
            break
        
        # Check if video_id is a valid YouTube video ID
        if len(video_id) != 11:
            print("Invalid video ID. Please try again.")
            continue
        
        text_formatted = format_video_transcript(video_id)
        
        print(colored("Transcript has been saved successfully!", "green"))
        print(colored("Please wait while we prepare the model...", "yellow"))
        generate_context(text_formatted)
        print("You can now start questioning the model. You can exit any time by typing 'bye'.\n")
        generate_response()