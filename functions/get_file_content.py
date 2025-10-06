import os
from config import *
from google.genai import types


def get_file_content(working_directory, file_path):
    try:
        abs_path = os.path.abspath(working_directory)
        absolute_path = os.path.abspath(os.path.join(working_directory, file_path))
    except Exception as e:
        return("Error: Something is wrong with the given paths: {e}")
    
    if not absolute_path.startswith(abs_path):
        return(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
    
    if not os.path.isfile(absolute_path):
        return(f'Error: File not found or is not a regular file: "{file_path}"')

    file_content_string = ""
    try:
        with open(absolute_path, "r",encoding='utf-8') as f:
            file_content_string = f.read(MAX_CHARS+1)
    except Exception as e:
        return f"Error: {e}"
    
    print(f"len: {len(file_content_string)}")
    if len(file_content_string) > MAX_CHARS:
        file_content_string = file_content_string[:MAX_CHARS] + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

    return file_content_string

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents of the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read from, relative to the working directory. If not provided, respond that it cannot be found.",
            ),
        },
    ),
)