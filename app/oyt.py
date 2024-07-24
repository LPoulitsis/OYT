# Author: Lefteris Poulitsis
# Last Updated: 24/07/2024

"""
This program is a chatbot that generates responses based on a video transcript from YouTube.
The user provides a video ID and the program fetches the transcript from YouTube.
The chatbot then generates a context based on the transcript and the user can start questioning the chatbot.
"""

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import ollama
from termcolor import colored
from typing import List, Tuple, Dict, Optional

def generate_response(conversation_history: List[Dict[str, str]]) -> None:
    while True:
        question = input(colored("Question: ", "green"))
        print()
        if question.lower() == 'bye':
            break
        conversation_history.append({"role": "user", "content": question})
        try:
            response = ollama.chat(model="mistral", messages=conversation_history)
            response_text = response['message']['content']
        except Exception as e:
            response_text = f"Error in response: {e}"
        conversation_history.append({"role": "assistant", "content": response_text})
        print(f"{colored('Response:', 'blue')} {response_text}\n")

def generate_context(text_formatted: str) -> Tuple[str, List[Dict[str, str]]]:
    messages = [
        {
            "role": "system",
            "content": f"""You will be provided with a video 
                        transcript from YouTube which you will 
                        have to answer certain questions to 
                        the user based on the transcript contents.
                        Act as an expert in any given field related
                        to the video transcript's topics. 
                        Here's the transcript: {text_formatted}"""
        }
    ]
    try:
        response = ollama.chat(model="mistral", messages=messages)
        context_response = response['choices'][0]['message']['content']
    except Exception as e:
        context_response = f"Error in context generation: {e}"
    return context_response, messages

def format_video_transcript(video_id: str) -> Optional[str]:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = TextFormatter()
        return formatter.format_transcript(transcript)
    except Exception as e:
        print(colored(f"Error fetching transcript: {e}", "red"))
        return None

if __name__ == "__main__":
    logo = f"""
  {colored("___", "white")}{colored("__   __", "red")}{colored("_____", "yellow")}
 {colored("/ _ \\", "white")} {colored("\\ / /", "red")}{colored("_   _|", "yellow")}
{colored("| | | \\", "white")}{colored("V /", "red")}  {colored("| |", "yellow")}
{colored("| |_| |", "white")}{colored("| |", "red")}   {colored("| |", "yellow")}
{colored(" \\___/", "white")}{colored("|_|", "red")}   {colored("|_|", "yellow")}  
    """    
    
    print(colored(logo, "red"))
    
    print(f"""{colored("Welcome", "green")} to the {colored("Ollama", "white")} {colored("YouTube", "red")} {colored("Transcript", "yellow")} chatbot!
This chatbot generates responses based on a video transcript from YouTube.\n""")
    
    while True:
        video_id = input("Enter a video ID (or press 'x' to exit): ")
        
        if video_id.lower() == 'x':
            break
        
        # Check if video_id is a valid YouTube video ID
        if len(video_id) != 11:
            print(colored("Invalid video ID. Please try again.", "red"))
            continue
        
        text_formatted = format_video_transcript(video_id)
        
        if text_formatted:
            print(colored("Transcript has been saved successfully!", "green"))
            print(colored("Please wait while we prepare the model...", "yellow"))
            context_response, conversation_history = generate_context(text_formatted)
            print(colored("Context generated successfully!", "green"))
            conversation_history.append({"role": "assistant", "content": context_response})
            print("You can now start questioning the model. You can exit any time by typing 'bye'.\n")
            generate_response(conversation_history)
        else:
            print(colored("Failed to process the transcript. Please try with a different video ID.", "red"))
