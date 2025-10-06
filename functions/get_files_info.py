import os
from google import genai 
from google.genai import types

def get_files_info(working_directory, directory="."):

    try:
        abs_path = os.path.abspath(working_directory)
        absolute_path = os.path.abspath(os.path.join(working_directory, directory))
    except Exception as e:
        return("Error: Something is wrong with the given paths")
    
    if not absolute_path.startswith(abs_path):
        return(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    
    if not os.path.isdir(absolute_path):
        return(f'Error: "{directory}" is not a directory')

    dir_content = get_dir_content(absolute_path)
    return dir_content

def get_dir_content(path):
    try:
        dir_content = os.listdir(path)
    except Exception as e:
        return(f"Error: {path} is not a real path")
    lines =[]
    for item in dir_content:
        if item.startswith("__"):
            continue
        item_path = os.path.join(path,item)
        try:
            lines.append(f" - {item}: file_size={os.path.getsize(item_path)} byts, is_dir={os.path.isdir(item_path)}")
        except Exception as e:
            return f"Error: {e}"
    return "\n".join(lines)


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


