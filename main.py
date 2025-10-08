import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from config import *
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import schema_write_file, write_file


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

function_dictionary = {
    "get_files_info" : get_files_info,
    "get_file_content" : get_file_content,
    "run_python_file" : run_python_file,
    "write_file" : write_file
}

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

    for i in range(0,LOOP_ITERATIONS):
        response = generate_content(client, messages, verbose)
        try:
            done = (not response.function_calls) and bool(response.text)
            if done or i == LOOP_ITERATIONS - 1:
                if response.text:
                    print("Final response:")
                    print(response.text)
                break
            #for candidate in response.candidates:
                #messages.append(candidate.content)
                #messages.append(genai.types.Content(response, role="user"))
        except Exception as e:
            return (f"Error: {e}")
        
    #print("print this!:", messages)

    sys.exit(0)

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model=MODEL_NAME, 
        contents=messages,
        config = types.GenerateContentConfig(tools=[available_functions], system_instruction = SYSTEM_PROMPT)
        )
    
    #print ("type(response):", type(response) )
    #print ("dir(response)", dir(response))
    for cand in response.candidates:
        messages.append(cand.content)
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    if response.function_calls:
        for function_call_part in response.function_calls:
            #print(f"Calling function: {function_call_part.name}({function_call_part.args})")
            function_call_result = call_function(function_call_part,True)
            #messages.append(genai.types.Content(role="user", parts=[function_call_result]))
            messages.append(function_call_result)
            resp = function_call_result.parts[0].function_response.response
            if not isinstance(resp, dict) or "result" not in resp:
                raise RuntimeError("Tool response missing 'result'")
            if verbose:
                print(resp["result"])
            #return response
    
        #print("Response: ")
    return response


def call_function(function_call_part, verbose=False):
    function_to_call = function_dictionary.get(function_call_part.name)
    function_args = {}
    if function_call_part.args != None:
        function_args = dict(function_call_part.args)
    function_args["working_directory"] = "./calculator"
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    if not function_to_call:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    function_result = function_to_call(**function_args)

    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"result": function_result},
            )
        ],
    )



if __name__ == "__main__":
    main()


