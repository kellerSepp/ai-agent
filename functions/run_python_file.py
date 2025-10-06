import os
import subprocess
import sys
from config import *
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    try:
        abs_path = os.path.abspath(working_directory)
        absolute_path = os.path.abspath(os.path.join(working_directory, file_path))
        abs_real = os.path.realpath(abs_path)
        file_real = os.path.realpath(absolute_path)
        if not os.path.commonpath([abs_real, file_real]) == abs_real:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    except Exception as e:
        return(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
    
    if not os.path.lexists(absolute_path):
        return (f'Error: File "{file_path}" not found.')
    
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        result = subprocess.run([sys.executable, absolute_path] + args, capture_output=True, text=True, cwd=working_directory, timeout=TIMEOUT_TIME)
        
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        if stdout == "" and stderr == "":
            return ("No output produced.")

        lines = [f"STDOUT: {stdout}", f"STDERR: {stderr}"]
        if result.returncode != 0 :
            lines.append(f"Process exited with code {result.returncode}")
        return "\n".join(lines)
    
    except Exception as e:
        return (f"Error: executing Python file: {e}")
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python files with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python-file to execute, relative from working directory.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Optional Arguments for the script. They are not mandatory, only optional",
            ),
        },
    ),
)

