import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.normpath(os.path.join(abs_working_directory, file_path))
    
    if os.path.commonpath([abs_working_directory, abs_file_path]) != abs_working_directory:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.abspath(abs_file_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    
    if not os.path.exists(abs_file_path):
        return f'Error: "{file_path}" does not exist'
    try:
        command = ["python3", abs_file_path]
        if args:
            command.extend(args)
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return f"Process exited with code {result.returncode}"
        if not result.stdout and not result.stderr:
            return f"No output produced"
        output = ""
        if result.stdout:
            output += f"STDOUT:\n{result.stdout}"
        if result.stderr:
            output += f"STDERR:\n{result.stderr}"
        return output

    except Exception as e:
        return f'Error: Failed to execute "{file_path}" - {str(e)}'
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in the specified directory and returns its output. Only files within the working directory can be executed for security reasons.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
    
)
