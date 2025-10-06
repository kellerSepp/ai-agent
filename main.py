import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from config import *

args = sys.argv

TEST=False

def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}")


    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    if TEST == False:
        #print("do some real shit")
        generate_content(client, messages, verbose)
        
        


        
        
        sys.exit(0)

    print("This was just a Test")
    sys.exit(0)

def  generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model=MODEL_NAME, 
        contents=messages,
        config = types.GenerateContentConfig(system_instruction = SYSTEM_PROMPT)
        )
    if len(args) > 2 and args[2] == "--verbose":
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print("Response: ")
    print(response.text)
    

if __name__ == "__main__":
    main()


