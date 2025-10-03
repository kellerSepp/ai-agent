import os
from dotenv import load_dotenv
from google import genai
import sys


args = sys.argv

TEST=False

def main():
    if(len(args) < 2 or len(args) > 2):
        #raise Exception ("wrong amount of arguments. Only 1 please!")
        print("wrong amount of arguments. Only 1 please!")
        sys.exit(1)

    prompt = args[1]

    if TEST == False:
        #print("do some real shit")
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(model="gemini-2.0-flash-001", contents=prompt)
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print(response.text)
        sys.exit(0)

    print("This was just a Test")
    sys.exit(0)


if __name__ == "__main__":
    main()


