import os


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