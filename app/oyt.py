# Author: Lefteris Poulitsis
# Last Updated: 19/09/2024 - DD/MM/YYYY

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

"""
_summary_ : This function generates responses based on the user's questions and the conversation history.
_conversation_history_ : A list of dictionaries containing the conversation history.
_return_ : None
"""
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

"""
_summary_ : This function generates a context based on the formatted transcript.
_text_formatted_ : A formatted string containing the video transcript.
_return_ : A tuple containing the context response and the conversation history.
"""
def generate_context(text_formatted: str) -> Tuple[str, List[Dict[str, str]]]:
    messages = [
        {
            "role": "system",
            "content": f"""You will be provided with a transcript from a YouTube video. Your task is to assist users by answering their questions based on this transcript. The following guidelines will help you provide accurate and informative responses:

            1. **Contextual Understanding**:
            - Thoroughly understand the contents of the transcript provided. Pay attention to the details, key points, and main topics discussed in the video.
            - Consider any technical terms, specific references, or unique content presented in the video transcript.

            2. **User Assumptions**:
            - Assume that the user asking questions has no prior knowledge of the video's content. They are seeking information and clarity on the topics covered.
            - The user is not the creator of the video, so provide explanations as if the user is hearing about the content for the first time.

            3. **Response Quality**:
            - Aim to provide clear, concise, and accurate answers to the user's questions.
            - Ensure your responses are informative and relevant to the content of the transcript. Avoid including unrelated information.

            4. **Expert Role**:
            - Act as an expert in any field related to the topics covered in the video transcript. Your responses should reflect a high level of knowledge and authority on the subject matter.
            - If the video covers multiple topics, be prepared to switch between subjects seamlessly and provide expert insights on each.

            5. **Engagement**:
            - Engage with the user's questions thoughtfully, providing detailed explanations where necessary.
            - Encourage further inquiry by offering additional context or suggesting related topics that might interest the user.

            Here's the transcript for your reference:
            {text_formatted}"""
        }
    ]
    try:
        response = ollama.chat(model="mistral", messages=messages)
        context_response = response['choices'][0]['message']['content']
    except Exception as e:
        context_response = f"Error in context generation: {e}"
    return context_response, messages

"""
_summary_ : This function fetches the transcript of a YouTube video and formats it.
_video_id_ : The ID of the YouTube video.
_return_ : The formatted transcript as a string or None if an error occurs.    
"""
def format_video_transcript(video_id: str) -> Optional[str]:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = TextFormatter()
        return formatter.format_transcript(transcript)
    except Exception as e:
        print(colored(f"Error fetching transcript: {e}", "red"))
        return None

"""
_summary_ : The main function of the program.
"""
def main():
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
        
        if video_id.lower() == 'x':
            break
        
        # Check if video_id is a valid YouTube video ID
        if len(video_id) != 11:
            print(colored("Invalid video ID. Please try again.", "red"))
            continue
        
        text_formatted = format_video_transcript(video_id)
        
        # Write the transcript to a file
        with open("transcript.txt", "w") as file:
            file.write(text_formatted)
        
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

if __name__ == "__main__":
    main()