import os
from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        abs_path = os.path.abspath(working_directory)
        absolute_path = os.path.abspath(os.path.join(working_directory, file_path))
    except Exception as e:
        return(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
    
    absolute_path_as_list = os.path.split(absolute_path)
    print (absolute_path_as_list)

    try:
        if not os.path.exists(os.path.split(absolute_path)[0]):
            os.makedirs(os.path.split(absolute_path)[0])
    except Exception as e:
        return (f"Error: {e}")

    try:
        with open(absolute_path, "w") as f:
            f.write(content)
    except Exception as e:
        return (f"Error: Couldn't write to file, because: \n {e}")

    

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'



schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Execute Python files with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to file to write in. If not provided, respond that it cannot be executed.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write into given file",
            ),
        },
    ),
)